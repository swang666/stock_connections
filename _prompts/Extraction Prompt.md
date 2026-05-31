# Extraction Prompt (the LLM 'compiler')

Paste a source document (or point your LLM at a file in `sources/`) and run this prompt.

---

You are maintaining a knowledge graph of the AI supply chain stored as an Obsidian vault.

**Task:** Read the document below. Extract every concrete business relationship between two companies, and every link between a company and a demand driver. Use ONLY facts stated or strongly implied in the text.

**Output two things:**

1. **Edge rows** in this exact pipe format (one per line):
   `SOURCE | relationship | TARGET | strength(1-3) | one-line evidence | source_filename`
   - Use existing relationship verbs where possible: *supplies … to, manufactures chips for, provides CoWoS packaging to, sells GPUs to, co-designs custom silicon with, runs compute on, supplies power to, benefits from, drives demand for, competes with*.
   - strength: 3 = major/named dependency, 2 = meaningful, 1 = minor/speculative.

2. **Page edits**: for each company or theme touched, give the new bullet(s) to add under the right heading, written as Obsidian links, e.g. `- supplies HBM to [[NVIDIA]] — 2026 supply agreement`.

**Rules:** Do not invent relationships. If a company isn't in the vault yet, propose a new page with ticker, layer (1–14), segment, and country. Flag anything uncertain with `(?)`.

---

DOCUMENT:

<paste source here>

---

## ADD-ON: capture bottleneck / constraint signals (for the bottleneck engine)

When a source describes how *tight* or *hard-to-substitute* a supply relationship is, encode that
in the edge's **evidence note** using these signal words where they genuinely apply — the
bottleneck scorer (`bottleneck_analysis.py`) reads this text, so consistent wording makes a node
score correctly:

- **Strong choke** → use: `sole-source`, `sole`, `monopoly`, `bottleneck`, `constrained`,
  `shortage`, `undersupplied`, `scarce`, `gatekeeper`, `tight supply`.
- **Pricing power / capacity** → use: `capacity`, `lead time`, `allocation`, `LTA`, `locked`,
  `premium`, `ASP`, `pricing`, `tight`.
- **Substitution** → if the report names alternative suppliers or a credible second source / 
  in-housing / China-localization threat, add an edge for each alternative and note it (this lowers
  the node's uniqueness, correctly).

Examples of good evidence notes:
- `(FACT, ASML) sole-source for EUV lithography; gatekeeper of leading-edge nodes`
- `(FACT, UBS) HBM tight / undersupplied; ASP +50% y/y; hyperscalers locked under LTA`
- `(VIEW, JPM) capacity allocation tight at OSAT; lead times extending`

Keep notes short. Only use a signal word if the source supports it — do not inflate constraint.
