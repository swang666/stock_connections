# Quant model - LLM-integrated, backtest-gated

A two-layer system on top of the knowledge graph:

- **Quant layer (deterministic Python):** `quant_model.py` + `_tools/fetch_history.py`. Factor
  scoring, signals, rule-derived levels, and a walk-forward backtest. Every number traces to a
  formula; no price predictions.
- **LLM layer (the morning brief, optional next step):** reads the quant signals, overlays catalyst
  /filing context, judges news-vs-noise, and writes the plan in plain language. The LLM interprets;
  it never invents prices.

> **Not a profit promise, not investment advice.** A backtest that looks good usually still fails
> live (overfitting, regime change, costs). Use it as a sanity gate, not a guarantee. You decide and
> place every order.

## The three factors

| Factor | Source | What it captures |
|---|---|---|
| **Structural** | `bottleneck_analysis.py` score | Who the chain depends on, few substitutes; your graph's edge |
| **Momentum / trend** | trailing return (`--mom-days`, default 63d) | Is the name already working |
| **Relative strength** | multi-window cross-sectional return rank | Whether strength persists across 1/3/6 month windows |

Combined into a composite score with weights you control (`--w-struct --w-mom --w-rs`).

## Workflow

```bash
# 1. Pull history. Includes graph tickers plus NVDA/SOXX/SMH/QQQ/SPY benchmarks.
python3 _tools/fetch_history.py --years 5

# 2. BACKTEST FIRST. Does the rule beat a benchmark after cash, slippage, and exposure caps?
python3 quant_model.py --backtest --top 5 --rebal 21 --benchmark NVDA \
  --cash-reserve 0.10 --max-layer-weight 0.35 --slippage-bps 10 \
  --backtest-stop 0.25 --portfolio-stop 0.20

# 3. Robustness check. Prefer broad consistency over one tuned result.
python3 quant_model.py --sweep --benchmark NVDA --backtest-stop 0.25 --portfolio-stop 0.20

# 4. Today's signals + YOUR-rule levels, only after the backtest gives confidence.
python3 quant_model.py --signals --top 6 --stop 0.08 --target 0.16

# 5. Sanity unit tests anytime.
python3 quant_model.py --selftest
```

## What the levels mean

`Entry<= / Stop / Target` are your stop/target fractions applied to the latest close: arithmetic,
not a forecast. `--stop 0.08 --target 0.16` means stop = price x 0.92 and target = price x 1.16
(a 2R setup). They tell you where your own rule puts the exits, so you trade a system instead of a
hunch.

## Backtest controls

- `--cash-reserve`: leaves part of the portfolio in cash, matching the experiment plan's dry powder.
- `--max-layer-weight`: caps exposure to a graph layer, so five tickers do not secretly become one
  CoWoS/advanced-packaging bet.
- `--slippage-bps`: subtracts a simple turnover cost on rebalances and simulated stop exits.
- `--backtest-stop`: optional close-based per-name stop-loss simulation. Daily bars cannot see
  intraday stop behavior, so treat this as approximate.
- `--portfolio-stop`: optional portfolio drawdown circuit breaker.
- `--exclude`: removes symbols from the strategy universe while still allowing them in history for
  benchmarks. Defaults exclude known ticker-identity/data-problem symbols (`BOE,XFAB,SPCX`).
- `--sweep`: runs a small parameter grid across top-N, rebalance cadence, momentum window, and
  factor weights.

## Honest limitations

- **In-sample risk.** The backtest tunes on the same history it reports on. Use `--sweep` and prefer
  rules that work across a range of parameters.
- **Structural lookahead.** The historical test applies today's graph-derived bottleneck scores to
  past prices. That is useful as a current-thesis overlay, but it is not a pure historical proof
  unless you later add dated graph snapshots.
- **Survivorship & costs.** Stooq history is split/adjusted and the model now applies configurable
  slippage, but small-caps and volatile names can still trade worse than the toy assumption.
- **The structural factor is slow.** Bottleneck scores barely change day to day. Most signal
  variation still comes from price factors. The graph is the why, not the when.
- **It still cannot predict prices.** Nothing here does. It systematizes a rule and measures it.

## Journal

Use `trading_log.csv` for any paper or real experiment entries: thesis, invalidation condition,
rule parameters, benchmark, fill, review date, and outcome. The log is part of the system; without
it, the experiment cannot teach you much.

*Idea-generation only. Not investment advice. Verify against primary sources.*
