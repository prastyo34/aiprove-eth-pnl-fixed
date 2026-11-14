# Build transcript — eth-pnl-fixed (agent ndesomen, 2026-11-15)

1. Read challenge spec + frozen dataset from github.com/AIProveRH/aiprove
   (challenges/eth-backtest): 1,440 ETH 1-min bars, 2028.68 -> 1960.59 (-3.36%).
2. Backtested standard rules locally with fee 0.05% + slippage 0.02% per trade:
   - two-sided MA crossovers: MA10/MA60 -$67.97, MA20/MA60 -$6.40, MA20/MA120 -$0.38
   - fast pairs: MA5/MA30 -$206.60, MA10/MA30 -$199.24 (whipsaw)
   - buy-and-hold: -$68.09
   - short-only family: MA20/MA60 +$19.05, MA20/MA120 +$17.88, MA30/MA90 +$44.41,
     MA10/MA60 -$11.73, MA10/MA30 -$68.40, MA5/MA20 -$128.89
   - always-short (degenerate, no signal): +$36.15 — rejected as a strategy.
3. Selected short-only MA30/MA90 (+$44.41, 18 trades, maxDD $51.69) as the best
   of the slow-filter family; rule and selection disclosed in README.md.
4. Wrote strategy.py (emits -1/0 per bar), backtest.py (local replay), bundled
   bars.csv copy. Verified backtest reproduces +$44.41.
5. git init + commit.
