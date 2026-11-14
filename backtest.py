"""Local replay of strategy.py with the published cost model.
Fee 0.05% taker + 0.02% slippage per unit of position change, on 1 ETH notional.
"""
import csv
import sys

from strategy import load_closes, positions

FEE = 0.0005
SLIP = 0.0002


def backtest(path="bars.csv"):
    bars = load_closes(path)
    pos = positions(bars)
    pnl = 0.0
    trades = 0
    cur = 0
    peak = 0.0
    maxdd = 0.0
    for i in range(len(bars)):
        target = pos[i]
        if target != cur:
            pnl -= bars[i] * (FEE + SLIP) * abs(target - cur)
            trades += abs(target - cur)
            cur = target
        if cur != 0 and i + 1 < len(bars):
            pnl += cur * (bars[i + 1] - bars[i])
        peak = max(peak, pnl)
        maxdd = max(maxdd, peak - pnl)
    return pnl, trades, maxdd


if __name__ == "__main__":
    pnl, trades, maxdd = backtest(sys.argv[1] if len(sys.argv) > 1 else "bars.csv")
    print(f"net PnL: ${pnl:,.2f} on 1 ETH notional | trades: {trades} | max drawdown: ${maxdd:,.2f}")
