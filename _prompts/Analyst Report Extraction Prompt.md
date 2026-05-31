# Analyst Report → Knowledge Graph (extraction prompt)

Use this when the source is a **third-party analyst / sell-side / boutique research report**
(as opposed to a filing or news article — those use `Extraction Prompt.md`).

Analyst reports mix **facts**, **opinions**, and **estimates**. This prompt forces the model to
separate them so an analyst's *view* never gets stored as if it were a confirmed fact.

## Before you run it
1. Save the original report into `sources/` and **never edit it**. Name it with provenance:
   `2026-05_MorganStanley_AI-power-buildout.pdf` (date _ firm _ topic).
2. If it's a PDF, either let your LLM read the PDF directly or paste the extracted text.

---

## PROMPT (paste below, then the report)

You are maintaining a knowledge graph of the AI supply chain stored as an Obsidian vault, where
each company and demand-driver theme is a page and `[[links]]` are the edges.

The document below is an **analyst research report**. Read it and extract relationships, but you
MUST classify every item into one of three buckets and tag it accordingly:

- **FACT** — a relationship the report states as currently existing (e.g. "Company X supplies HBM
  to NVIDIA today"). Treat as a normal edge.
- **VIEW** — the analyst's opinion, thesis, or forecast (e.g. "we see Company Y as the prime
  beneficiary of the power buildout", or a price target / rating). Capture it, but tag it.
- **ESTIMATE** — a quantitative figure the analyst projects (revenue exposure %, TAM, units).
  Store as an attribute on the relevant node/edge, dated and attributed.

**Output 1 — edge rows**, one per line, in this exact pipe format:

`SOURCE | relationship | TARGET | strength(1-3) | source_type | evidence (incl. firm + view/fact) | source_filename`

- `source_type` is one of: `analyst-fact`, `analyst-view`, `analyst-estimate`.
- For VIEW edges to a theme, use the verb `benefits from` and put the analyst's rationale +
  any price target/rating in the evidence note, prefixed `(VIEW, <Firm>):`.
- `strength`: 3 = central / high-conviction, 2 = meaningful, 1 = speculative or single-mention.
- Reuse the existing relationship vocabulary where possible: *supplies … to, manufactures chips
  for, provides CoWoS packaging to, sells GPUs to, co-designs custom silicon with, runs compute
  on, supplies power to, benefits from, drives demand for, competes with*.

**Output 2 — page edits**: for each company/theme touched, give the exact bullet(s) to add under
the right heading as Obsidian links, with the tag inline, e.g.:
`- supplies HBM to [[NVIDIA]] — (FACT, Morgan Stanley, 2026-05)` or
`- [[Datacenter Power Demand]] — (VIEW, Morgan Stanley): top pick, PT $X`.

**Output 3 — new entities**: if the report names a company not yet in the vault, propose a new
page with ticker, layer (1–14), segment, and country.

**Rules**
- Never present a VIEW or ESTIMATE as a FACT. When unsure which bucket, choose the weaker one.
- Always record the **firm name and report date** in the evidence note — views age and conflict,
  so provenance matters.
- If an edge already exists in the vault, do NOT duplicate it. Instead say "CONFIRMS existing edge
  X→Y (add this report as a second source / bump strength)" or "CONTRADICTS existing edge X→Y
  (flag for review)".
- Flag anything genuinely uncertain with `(?)`.
- Do not invent relationships that aren't supported by the text.

---

DOCUMENT (analyst report):

<paste report text here>

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
