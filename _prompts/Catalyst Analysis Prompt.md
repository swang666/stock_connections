# Catalyst / Chain-Effect Analysis (prompt)

Use this to trace how a single event or deal ripples through the graph to reach non-obvious
2nd- and 3rd-order names. It assumes the Obsidian wiki (Companies/ + Themes/ pages, `[[links]]`)
is the graph. Pair it with `catalyst_analysis.py` for a numeric ranking.

## How to use
1. Write the catalyst in one or two sentences (the deal/event and which companies it directly hits).
2. Fill in the three switches below.
3. Run the prompt with your LLM **with the relevant wiki pages in context** (the seed companies'
   pages and their neighbours). The model traverses the `[[links]]` to reason out the chain.

---

## PROMPT (paste below)

You are a catalyst analyst working over a knowledge graph of the AI supply chain stored as an
Obsidian vault. Each company and demand-driver theme is a page; `[[links]]` are directed edges
(by convention an edge points from a **supplier/upstream** node to its **customer/downstream**
node, e.g. `[[TSMC]] manufactures chips for [[NVIDIA]]`). Theme pages list the companies that
"benefit from" them.

**The catalyst:**
- Event: <describe the deal/event in 1–2 sentences>
- Seed node(s) directly affected: <list companies and/or themes>
- Polarity: <POSITIVE event (good for the seeds) | NEGATIVE event (bad for the seeds)>
- Type: <DEMAND-side (changes how much the seed buys/needs) | SUPPLY-side (changes what the seed
  can produce or deliver) | MACRO/THEMATIC (a driver-level shift)>

**Propagation rules — follow exactly:**
1. **Direction by type.**
   - DEMAND-side: the effect flows **upstream** — from the seed to its suppliers (follow edges
     *backwards*, from customer to supplier). More demand at the seed ⇒ more orders for suppliers.
   - SUPPLY-side: the effect flows **downstream** — from the seed to its customers (follow edges
     *forwards*). A supply change at the seed ⇒ its customers' inputs change.
   - MACRO/THEMATIC: from the theme, flow to every company that "benefits from" it.
2. **Sign.** Carry the polarity along the chain unchanged, EXCEPT across a `competes with` edge,
   which **flips the sign** (if the seed gains, a direct competitor relatively loses, and vice
   versa).
3. **Thematic spillover.** If a seed "drives demand for" a theme, that theme strengthens, so also
   lift the *other* companies that "benefit from" the same theme (this is how a demand surge in
   one chip reaches the memory and packaging names). Apply extra decay to these.
4. **Decay with distance.** Rank closer hops higher. A direct supplier/customer (hop 1) matters
   more than a hop-3 name. Note the hop count for each.
5. **Strength.** Weight by how critical the relationship is (sole-source / named major customer =
   strong; minor = weak).

**Output a table sorted by impact**, with these columns:
`Company | Beneficiary or Loser | Hops | Transmission path | Mechanism (one line) | Confidence (H/M/L)`

Then add:
- **Non-obvious picks:** the 3 names a casual observer would most likely miss, and why the graph
  surfaces them.
- **What would invalidate this:** the 1–2 assumptions that, if wrong, break the chain (e.g.
  "assumes TSMC is still sole-source for this part").
- **Gaps:** any point where the graph is missing an edge you'd need to complete the analysis —
  propose the edge so it can be added.

**Rules:** Only traverse relationships that exist in the vault; do not invent links to reach a
conclusion (instead, list the missing edge under Gaps). Be explicit about direction and sign at
each hop. This is idea generation, not a recommendation.

---

## Worked example (so you can see the shape of a good answer)

**Catalyst:** "A hyperscaler announces a multi-year, multi-billion-dollar order for next-gen AI
training clusters." Seed: `[[Microsoft]]` (and the broader `[[AI Training Capex]]` theme).
Polarity: POSITIVE. Type: DEMAND-side.

Expected reasoning shape: Microsoft demand ↑ → buys more GPUs → **NVIDIA** (hop 1) → which pulls
**TSMC** (foundry) and **SK Hynix / Micron** (HBM) upstream (hop 2) → which pulls **ASML / Applied
Materials / Lam** (equipment) at hop 3; in parallel, more clusters → **Vertiv** (power/cooling) and
**Arista** (networking) at hop 1–2, and via the power theme → **Constellation / Vistra / GE
Vernova** further out. Non-obvious picks: the equipment and power names three hops from the
headline.
