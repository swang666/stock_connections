# AI Supply-Chain Bottleneck — Trading Experiment

**Public version.** This document describes the experiment's design and the live operating
rulebook an AI agent follows to run it. Operational records (account identifiers, briefs,
trade logs, the live policy file) are kept private; this copy is sanitized for sharing.

**Setup:** a dedicated Robinhood *cash* account (no margin, no day-trade leverage), seeded with
**$1,000**, fractional shares enabled. The agent trades it autonomously on a schedule, within the
hard limits below, and reports to the owner by email digest after every close run.

> **This is not investment advice.** It is a structured protocol for an experiment. The graph
> generates *hypotheses about structural importance*, which is **not** the same as a prediction
> that a stock will rise. Verify everything against primary sources before acting.

---

## Part I — The experiment design

### 0. What the graph can and cannot tell you

The bottleneck engine ranks companies by **how much of the chain depends on them × how few
substitutes exist × how much shortage/pricing-power language appears in the evidence.** That is a
useful lens for *where margin and pricing power concentrate.* It is **silent on three things that
decide whether a trade makes money:**

1. **Valuation / what's already priced in.** A real chokepoint trading at 50× sales can fall 40%
   and still be a chokepoint.
2. **Timing.** The graph has no view on whether today is a good entry.
3. **Confidence of the edges.** Some relationships are FACT (filings), some are VIEW (analyst
   opinion). The score treats them similarly even after down-weighting.

The discipline below exists to compensate for what the graph doesn't model: **sizing to survive
being wrong, and pre-defining what would invalidate each idea.**

### 1. The hypothesis being tested

> *"A basket of the highest structural-bottleneck names in the AI supply chain, sized for
> survival and held through their catalysts, outperforms simply buying NVDA — over a defined
> window, after costs."*

Writing the hypothesis down gives a **benchmark (NVDA, and SOXX)** and an end date, so the
experiment can actually succeed or fail rather than drifting.

### 2. Candidate universe — graph rank × live price × the one risk that matters

From `bottleneck_analysis.py --top 15`, filtered to US-listed, liquid, fractionable names
(prices as of 2026-06-08):

| # | Score | Ticker | Layer / role | The single risk to check before buying |
|---|------|--------|--------------|------------------------------------------|
| 1 | 64.3 | **GLW** | Glass substrate — sole-source for high-layer glass core | Glass-core is a *2027-28* story; is the timeline priced too early? |
| 2 | 47.5 | **ENTG** | Materials/filtration — reach 23, sole-source | Tied to wafer starts, not just AI |
| 3 | 46.8 | **TSM** | Foundry — the master chokepoint | Taiwan/China tail; CoWoS is the real bottleneck |
| 4 | 34.6 | **MU** | HBM/DRAM — shortage language | Memory is *cyclical*; sold-out today ≠ sold-out in 2027 |
| 5 | 36.4 | **ASML** | EUV monopoly | China export exposure + lumpy orders |
| 6 | 30.7 | **LITE** | Optical/CPO — capacity-constrained | CPO is a thesis, not yet volume |
| 7 | 29.6 | **CRDO** | Retimers — allocation, sole-source sockets | Small, single-thesis, very high multiple |
| 8 | 29.3 | **AMKR** | OSAT advanced packaging | Real but commoditizing at the low end |
| 9 | 25.8 | **SNPS** | EDA — duopoly, every chip needs it | Least tight, but most *durable* moat |
| 10 | 25.4 | **LRCX** | Etch/deposition equipment | WFE-cyclical, moves with capex |

The *purest* structural chokepoints (GLW, ENTG, TSM, ASML, SNPS) and the *highest-beta thesis
bets* (CRDO, LITE, MU) are not the same risk profile and aren't sized the same.

### 3. Position-sizing framework (survival first)

- **Max single position: 15% ($150).** No name can sink the experiment.
- **Target 6–8 positions** — enough to test the *basket* hypothesis.
- **Tier by conviction:** core chokepoints get larger slices; thesis bets get half-size.
- **Keep ~10–15% cash** as dry powder for catalyst pullbacks.

### 4. Entry discipline — don't chase

Staggered entry: **1/3 now, 1/3 in ~1 week, 1/3 on any 5%+ pullback in the name.** No buying a
name more than 3% above its prior session's close (the "no-chase" rule).

### 5. Catalyst calendar — dates to act around

- **Nov 27, 2026 — China Ga/Ge/Sb export-control expiry.** Biggest swing for substrate/optical.
- **Jan 2027 — NVDA Rubin Ultra + HBM4 ramp.** Pulls MU, TSM, packaging.
- **Mid-2027 — HBM4E / advanced-packaging inflection.** MU, AMKR, TSM.
- **2028 — Glass-core substrate mass production.** The GLW thesis checkpoint.

### 6. Risk rules — exits pre-defined while calm

- Per-name invalidation sentence, written at entry, logged with the trade.
- Per-name stop: −25% from cost → exit at the next run.
- Portfolio circuit-breaker: basket −20% → stop buying, review the hypothesis, never average
  down on autopilot.
- No options, no leverage, no shorting.
- **Concentration honesty:** GLW, TSM, ASML, AMKR, MU all route through CoWoS/advanced
  packaging — the basket is less diversified than 7 tickers looks.

### 7. Measurement

Every entry logs: date, ticker, $, fill price, benchmark snapshot (NVDA + SOXX), one-line thesis,
invalidation condition, rule parameters, review date. The research question: **did the
high-bottleneck names beat the demand-driver anchors (NVDA/AMD/AVGO)?**

Performance is reported two ways: the **headline is total portfolio return** (positions + cash vs
the $1,000 inception baseline, same denominator as the fully-invested NVDA/SOXX benchmarks), and
**positions-only return** as secondary detail — the honest measure of the picks themselves,
without the cash cushion flattering down days.

---

## Part II — The live operating rulebook (what the agent actually obeys)

An AI agent (Claude) executes this experiment via scheduled runs on the owner's machine, with
Robinhood API access scoped to the dedicated experiment account only. Every run reads the private
policy file first and obeys it exactly. **Anything not expressly permitted → do nothing, write
the proposal in the brief, notify the owner, and wait.** The owner's replies always override.

### Schedule (the only times trading is allowed)

- **Open run:** 6:35am PT (9:35 ET), Mon–Fri. **Close run:** 12:45pm PT (3:45 ET), Mon–Fri.
- **Dip-watch:** a free quote poller runs every 15 minutes between the two runs and launches an
  extra agent run only when something actionable fires — an unfilled name crossing into the buy
  band, a stop breach, or a ≥5% pullback that unlocks a tranche-3 add. Event-driven runs act
  only on the condition that fired; the two fixed runs keep the thinking duties (discovery,
  reflection).
- Market closed → report-only. Run starting >60 min late → manage risk only, no new buys.
- No trading outside these runs unless the owner explicitly instructs in a live conversation.

### Universe (core basket + discovered names)

- **Core basket:** ENTG, TSM, GLW, ASML, SNPS, MU, CRDO, AMKR.
- **Discovered names** (added by the daily discovery duty, max 1 per day): must be US-listed,
  liquid, fractionable, with FACT-tagged graph evidence of a structural role in the AI chain.
  Starter buy ≤ $40; all caps and guards apply; every addition is announced in the digest and
  the owner can veto by email (position exited at the next run).
- SOXX — benchmark/control position only. NVDA — measurement benchmark ONLY, never tradeable.

### Hard limits (violating any of these = do not place the order)

1. Max **$150 cost basis per name** (15% of the experiment).
2. Max **$300 new money deployed per run**.
3. **Limit orders only** — with one carve-out: opening tranche buys may use fractional **market**
   orders (dollar-based sizing), regular hours only, while the live price is ≤ 3% above the
   prior session's close. (Robinhood mechanics force this: fractional sizing exists only on
   market orders; limit orders are whole-share only.)
4. **No chasing:** no opening buy more than 3% above the prior session's close.
5. **Cash reserve:** never let cash fall below **$150**.
6. No options, no leverage, no shorting.
7. Cash-account discipline: never risk a good-faith violation; when in doubt, wait for
   settlement.

### Buy plan (staggered tranches)

Full targets: ENTG $130 · TSM $130 · GLW $120 · ASML $110 · SNPS $100 · MU $90 · CRDO $80 ·
AMKR $80. Tranche 1 = ~1/3 of each target; tranche 2 = ~1/3 on/after one week, only for names
whose tranche 1 filled; tranche 3 only on a ≥5% pullback from the tranche-1 fill. Unfilled GTC
limits older than 3 sessions are cancelled. (GLW is held at tranche-1 size pending an
investigation into a large drop in its bottleneck score.)

### Sell / risk rules

- Per-name stop: close ≤ −25% from average cost → exit at the next run (limit near the bid,
  walked down if unfilled).
- Portfolio circuit-breaker at −20% total: stop all buying, do not auto-liquidate, notify the
  owner, write a review brief.
- Thesis invalidation (qualitative): never auto-sell on news alone; flag and propose.

### Daily duties (added 2026-06-10)

1. **Trade every market day (≥1 executed order).** Preference ladder: (a) guard-compliant
   tranche buys; (b) tranche-3 dip adds; (c) a discovered-name starter; (d) forced-min fallback
   at the close run — a $10 fractional buy of the universe name least extended vs prior close.
   Only the forced-min trade may exceed the no-chase guard; it is tagged `forced-min` in the log
   so the cost of the mandatory-trade rule itself is measurable. If caps/cash floor make any buy
   impossible, a documented attempt satisfies the duty — never sell just to trade.
2. **Discover daily.** Each close run re-runs the bottleneck engine, checks the catalyst
   calendar and X/Twitter scan trends, and compares candidates against the universe.
   Considered-but-rejected candidates are listed in the brief with reasons.
3. **Reflect daily.** Each close run reviews the day's trades and cumulative performance vs
   NVDA & SOXX, writes a Reflection section in the brief, and appends dated lessons + behavior
   changes to a learning log. When a lesson implies a rule change, the agent edits the policy
   itself — allowed scope: buy plan, universe, guard tuning within hard limits, run procedure.
   Not allowed without owner approval: the hard limits, the schedule, the cash reserve, or the
   daily-duties section. Every self-modification is dated and logged.

### Overnight pocket (side experiment)

A capped $100 "gamble pocket" tests the close-to-open overnight effect: at the close run, if a
universe name is down ≥3% intraday, buy $100 of the deepest dipper (settled cash only, one
position at a time, combined per-name cap still enforced); at the next open run, sell it —
**always, profit or loss**. The thesis is the overnight gap; once the open prints it has resolved,
and holding losers would turn bounded one-night risk into open-ended bag-holding while poisoning
the statistics. Every trade is tagged separately and the strategy is judged on its own win rate
and average net P/L after ~20 trades.

### Event awareness

An event calendar (FOMC decisions, CPI releases, universe earnings dates — the macro dates
verified against the Fed and BLS schedules, earnings auto-refreshed daily) feeds two rules:
the overnight pocket never holds across a CPI morning or a candidate's own earnings report
(those gaps are event bets, not the overnight effect), and every brief lists events within the
next five trading days so basket adds into events are conscious decisions, not accidents.
Macro data is deliberately used as a **risk filter, not a signal** — context like VIX/sentiment
may be logged and evaluated, but only promoted to a trading rule with evidence from the
experiment's own trades.

### Each run, in order

1. Read the policy file (obey its status flag), then the directives log — newest first.
2. Check the market is open; pull portfolio, positions, open orders, live quotes. Robinhood
   tools unavailable → report-only brief.
3. Manage existing state first (stops, stale orders), then tranche buys within the limits.
   Close run only: run the three daily duties.
4. Log every order and fill (thesis, invalidation, parameters, benchmark snapshot, review date).
5. Write a brief: positions & P/L vs NVDA/SOXX, actions taken with reasons, anything
   proposed-but-not-done, what the next run should watch.
6. Anything ambiguous → default to inaction + proposal in the brief.

### How the owner steers it (asynchronously)

- **Digest out:** after every close run (and after an open run only on ALERT), the brief + the
  day's log rows are emailed to the owner.
- **Directives in:** the owner replies to any digest; every run reads recent replies (verified
  to be authored by the owner's own address) as directives. Directives may tighten or pause
  activity freely; they may only EXCEED a hard limit if they explicitly and unambiguously say
  so. A standing auto-execution authorization lets rulebook-compliant trades execute without
  per-order confirmation; anything outside the rulebook still requires explicit approval.
- **Pause:** reply "pause", set the policy status flag to `paused`, or disable the scheduled
  tasks.

---

*Experimental research account. Idea-generation framework, not investment advice. The levels
above are arithmetic rules set by the owner, not price predictions.*
