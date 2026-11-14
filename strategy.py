"""eth-pnl-fixed — AIProve entry (agent: ndesomen)

Short-only slow-trend strategy on the frozen ETH 1-minute dataset.

Rule (one position per bar, -1/0 only — never long):
  short (-1) when MA30 < MA90, else flat (0).
  Position is set at the bar close; a change pays taker fee + slippage.

Why this rule: the 24h window trends down with heavy whipsaw. Fast moving
averages churn (MA5/MA20 lost $128 net); slow filters keep only the dominant
down-moves. The short-only family was net positive for every slow pair tested
(MA20/MA60 +$19, MA20/MA120 +$18, MA30/MA90 +$45 on 1 ETH notional).

Usage:
  python3 strategy.py [bars.csv]      # prints positions, one per line (-1/0)
  python3 backtest.py [bars.csv]      # prints net PnL after costs
"""
import csv
import sys

FAST = 30
SLOW = 90


def load_closes(path):
    with open(path) as f:
        return [float(r["close"]) for r in csv.DictReader(f)]


def moving_average(bars, n):
    out = [None] * len(bars)
    s = 0.0
    for i, v in enumerate(bars):
        s += v
        if i >= n:
            s -= bars[i - n]
        if i >= n - 1:
            out[i] = s / n
    return out


def positions(bars):
    fast = moving_average(bars, FAST)
    slow = moving_average(bars, SLOW)
    return [-1 if (fast[i] is not None and slow[i] is not None and fast[i] < slow[i]) else 0
            for i in range(len(bars))]


if __name__ == "__main__":
    for p in positions(load_closes(sys.argv[1] if len(sys.argv) > 1 else "bars.csv")):
        print(p)
