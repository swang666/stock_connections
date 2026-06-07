# AI Supply-Chain Knowledge Graph

A living map of who supplies, sells to, and benefits from whom across the AI value chain —
built as an [Obsidian](https://obsidian.md) vault where every company and demand-driver theme is
a Markdown page and the `[[links]]` between pages are the edges of a directed supplier→customer
graph. The same relationships live in a spreadsheet that powers two analysis engines and an
interactive graph.

> **Idea generation only — not investment advice.** Every relationship and chokepoint is a
> starting point for research, not a recommendation. Verify against primary sources before acting.

## Quick start

```bash
pip install -r requirements.txt          # just openpyxl

# What benefits if a hyperscaler places a giant training-cluster order?
python3 catalyst_analysis.py --seeds NVDA --polarity pos --kind demand

# Where are the chokepoints / pricing power?
python3 bottleneck_analysis.py --top 20

# Rebuild the interactive graph + START HERE index + analytics after editing the data
python3 _tools/update_graph.py

# Check graph integrity
python3 _tools/validate.py
```

**Just want to look?** Two ways:

- **Live (no download):** https://swang666.github.io/stock_connections/ — runs in the browser, nothing to install.
- **Local:** open **`AI Supply Chain Graph.html`** in any browser — fully self-contained (data baked in, no server or internet needed).

Both have Catalyst, Bottleneck, and **Path-trace** modes in the side panel, show the **evidence and
source citation** behind every relationship when you click a node, and distinguish stated-fact edges
from analyst-opinion edges (FACT vs VIEW). A **"FACT only"** toggle hides opinion-based edges so
you can see just the confirmed structure.

**Path trace** lets you pick any two companies (Set = A, Set = B) and highlights the shortest
supply-chain path between them — e.g. *ASML → TSMC → Microsoft* — with the relationship verb on each
hop. It prefers the directed supplier→customer route, falling back to the reverse or an undirected
path if needed.

> **Maintainers:** the live page is `index.html` at the repo root, regenerated automatically by
> `_tools/update_graph.py` (a byte-identical copy of the graph). To publish it, enable **GitHub
> Pages**: repo **Settings → Pages → Source: Deploy from a branch → Branch: `main` / root → Save**.
> The site goes live at the link above in ~1 minute and refreshes on every push.

## What's here

| Path | What it is |
|---|---|
| `AI-Supply-Chain-Network.xlsx` | Source of truth — **Nodes** and **Edges** sheets |
| `Companies/`, `Themes/` | The wiki: one page per company / demand-driver theme |
| `AI Supply Chain Graph.html` | Interactive, static graph (open directly) |
| `catalyst_analysis.py` | Chain-effect engine — propagates a shock through the graph |
| `bottleneck_analysis.py` | Chokepoint engine — scores criticality × uniqueness × constraint |
| `_tools/` | `update_graph.py` (regenerator), `validate.py` (integrity checks), template, logs |
| `_prompts/` | Extraction + analysis prompt methodology |
| `00 - START HERE.md` | The in-Obsidian index (auto-generated from the spreadsheet) |

## Data model

- **Nodes**: `node_id, name, type (Company/Theme), ticker, layer (1–14, themes=0), layer_name, segment, country, key_products, role_in_ai_chain`.
- **Edges**: `source_id, source_name, relationship, target_id, target_name, strength (1–3), evidence, as_of, source_doc`.
- **14 value-chain layers**: 1 EDA/IP · 2 Equipment · 3 Foundry · 4 Chip designers · 5 Memory ·
  6 Advanced packaging · 7 Optical/interconnect · 8 Networking · 9 Servers/ODM · 10 Hyperscalers ·
  11 AI labs · 12 Datacenter REITs · 13 Power & cooling · 14 Power gen / utilities.
- Edge evidence is **tagged** `(FACT, firm date)` for stated facts vs `(VIEW, firm date)` for
  analyst opinions, so an opinion never reads as a confirmed relationship.

## Editing / extending

Drop research into `sources/inbox/`, run the extraction prompt in `_prompts/`, append rows to the
spreadsheet + wiki, then `python3 _tools/update_graph.py` to rebuild. `validate.py` should report
`errors=0` afterward.

## A note on sources

The raw third-party research that seeded this graph (sell-side reports, expert-call transcripts,
etc.) is **intentionally excluded** from this repo for licensing reasons — see `.gitignore`. What's
published is the *extracted* knowledge: relationships, short evidence notes, and citations. To
reproduce or extend, add your own sources to `sources/inbox/`.
