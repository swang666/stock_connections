
## 2026-05-27 — manual run
- Files ingested: 7 (Citi, JPM China, UBS Micron, Nomura SerDes, Furukawa, 2× TMT Breakout)
- New companies: 13 + 2 demand-driver themes (CPO, China Indigenous AI)
- New relationships: 35
- Tags: analyst opinions marked (VIEW, firm); stated facts (FACT, firm). Verify before acting.

2026-05-27: no new files

2026-05-28: no new files

## 2026-05-29 — scheduled run
- Files ingested: 6 — ASML HQ visit (GS), Dell F1Q27 first take (GS), Marvell LT outlook (Morgan Stanley), TMTB EOD Wrap, Trump 2026Q1 holdings (xlsx), 玻璃基板行业交流 (glass-substrate expert call, docx).
- New companies: 7 — BOE, Corning (GLW), Innolux, AUO, Huawei, Teradyne (TER), XLight. New theme: 1 — Glass Core Substrate (T_GLASS).
- New relationships: 15 (after de-dup). Graph rebuilt: 70 nodes, 161 edges.
- Tagging: analyst forecasts marked (VIEW, firm date); stated facts (FACT, firm/source date). Uncertain links flagged (?).
- Notes / flagged for review:
  • Glass-substrate call (untrusted expert-call transcript) is the richest source: BOE→Huawei, Innolux→NVIDIA (~7-layer, end-2027), Corning preferred glass for 11-layer; domestic glass (Kaisheng/Caihong) only 3-4 layers (low substitution → Corning is a choke point). AUO↔NVIDIA CPO marked (?).
  • Trump 2026Q1 holdings xlsx is primarily a portfolio/political tracker, NOT supply-chain research. Only one supply-chain-relevant item extracted: XLight (US govt-backed EUV startup) competes with ASML — speculative, strength 1 (?). Remainder (memecoins, family/drone investments, equity-stake tracker) intentionally NOT ingested as graph edges.
  • Marvell & CPO-undersupply items mostly CONFIRM existing edges (MRVL→T_NET); no duplicate rows added — evidence noted in wiki only.
  • No instruction-like / prompt-injection content detected in any file; all treated as untrusted data.
  • Spreadsheet was NOT open — written directly, no pending CSV.
2026-05-29: no new files
2026-05-30: no new files

## 2026-05-31 — engine fixes + evidence backfill (manual, from chat)
- Bug fixes:
  • bottleneck_analysis.py bucket(): "manufactures chips" now classified BEFORE the EDA/IP rule;
    the loose substring "ip" was matching inside "chips" and mis-bucketing every foundry edge as
    EDA/IP. Effect: TSMC now reads near-sole-source (Alts 5->2, rank #6->#2); ASML Alts 3->4.
  • Path resolution standardized: both engines resolve the xlsx via __file__ (env STOCKKB_XLSX
    override), replacing bottleneck's sandbox-only /sessions/* glob.
  • VIEW down-weighting added: edges supported only by analyst (VIEW) evidence count ~0.6x in
    catalyst; bottleneck applies a 0.7–1.0 confidence factor from FACT/VIEW share. ASML (VIEW-heavy)
    correctly discounted.
- Evidence backfill: 36 high-value edges (foundry, EUV, equipment, HBM, OSAT, optical, custom
  silicon, networking, GPU sales, power, EDA). 31 sourced to primary/credible refs (SEC filings,
  NVIDIA/Amkor newsrooms, Arista 10-K, trade press) and FACT-tagged; source_doc URLs added.
  Coverage: evidence 84->120, FACT/VIEW tagged 64->95, source_doc 54->87.
- Flagged for follow-up (NEEDS-SOURCE / NEEDS-REVIEW, not fabricated):
  • Samsung -> NVIDIA HBM/DRAM: Samsung repeatedly FAILED NVIDIA HBM3E qual; DRAM die qualified but
    not HBM package — edge may be DRAM-only/aspirational. REVIEW.
  • Micron -> AMD HBM: plausible, unverified this pass (reports cite Samsung 12-Hi for MI350).
  • Lam -> Micron / Lam -> SK Hynix (memory etch/dep): structural, needs primary cite.
  • Amkor -> AMD (OSAT): plausible, needs cite (Amkor publicly tied to NVIDIA/Apple).
- New tool: _tools/validate.py — checks dangling edges, dup ids, bad strength, broken wiki-links,
  node<->page parity, orphans, and evidence/source/tag coverage. Current: 0 errors, 196 warnings
  (gaps to backfill). Recommend running as the final step of the daily job.
- Graph rebuilt: 82 nodes, 189 edges; bottleneck scores re-baked.
2026-05-31: no new files

## 2026-05-31 — drift fixes + automation (manual, from chat)
- update_graph.py now regenerates THREE artifacts every run (kills manual-maintenance drift):
  1. AI Supply Chain Graph.html (as before)
  2. 00 - START HERE.md layer index — rebuilt from the Nodes sheet. Was stale (47/82 nodes); now 82/82,
     all 14 layers + 10 themes.
  3. Degree (analytics) sheet — out/in/total degree per node, sorted. Was empty (0/62 populated); now 82 rows.
- bottleneck_analysis.py bucket(): added a "glass_substrate" category so glass-core-substrate makers
  serving the same customer are treated as mutual alternatives (future-proofing; current glass edges
  form a vertical Corning->Innolux->NVIDIA chain so rankings unchanged).
- validate.py wired into the daily job (update-stock-kb SKILL.md, STEP 5): runs after update_graph.py;
  ERRORs must be driven to zero before a run is considered clean; validator summary recorded in the log.
- Removed dead _tools/graph_template_v2.html (v3 is the live template).
- Rebuilt + validated: 82 nodes, 189 edges, errors=0, warnings=196 (evidence/source gaps to backfill).
