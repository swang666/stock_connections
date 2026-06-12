
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

## 2026-06-01 — daily ingest (Cowork scheduled job)
- MANIFEST REPAIR: _tools/ingested.json was truncated mid-write (unterminated string in the "edgar"
  array). Backed up to ingested.json.corrupt.bak and rebuilt as valid JSON, preserving all 13
  ingested filenames and the 3 recorded accessions (NVDA/AMD/MRVL). fetch_edgar.py had been crashing
  on json.load before this fix.
- EDGAR (STEP 1): live fetch_edgar.py run repaired-and-launched, but SEC filer-discovery did not
  complete within the sandbox network/time budget (no new "pulling/wrote" output beyond filer
  enumeration; 10 foreign-listed filers correctly skipped). No NEW filings pulled by this run.
  However, 11 EDGAR extracts from a prior (crashed) run were sitting unprocessed in sources/inbox —
  these were processed this run as STEP 2 new files.
- Inbox files processed (11, all EDGAR extracts):
  AMD 10-K (0000002488-26-000018), NVDA 10-K (0001045810-26-000021),
  MRVL 10-K (0001835632-26-000011), AMZN 10-K (0001018724-26-000004),
  BE 10-K (0001628280-26-006516), ANET 10-K (0001596532-26-000013),
  AMKR 10-K (0001047127-26-000014), ASML 20-F (0001628280-26-011378),
  AAOI 10-K (0001437749-26-005875), BX 10-K (0001193125-26-082531),
  ARM 20-F (0001973239-26-000097).
- New companies added: 0 (all 11 issuers already nodes).
- New edges added: 1
  • AAOI -> Microsoft "supplies optical transceivers to" (s3) — AAOI 10-K names Microsoft as
    largest internet-data-center customer at 28.8% of FY2025 revenue (top-10 = 96.6%). FACT,
    source_doc = AAOI 10-K index URL.
- Existing edges strengthened (evidence upgraded to primary EDGAR FACT + source_doc; no dup rows): 6
  • AVGO->ANET: added sole-source/predominant merchant-silicon signal (ANET 10-K) — bottleneck cue.
  • AMD->MSFT, AMD->META, AMD->ORCL: filled empty evidence with AMD 10-K (Instinct MI300 deployed
    at scale by Microsoft/Meta/Oracle).
  • MRVL->MSFT (Maia) and MRVL->AMZN (Trainium/XPU): upgraded secondary sources to MRVL 10-K FACT.
- Wiki: additive bullets on Applied Optoelectronics.md (->Microsoft), Microsoft.md (<-AAOI), and a
  sole-source note on Arista Networks.md.
- Skipped / no new edges (boilerplate risk-factor sections, no named AI counterparty): AMZN, ASML,
  ARM, AMKR, BE, BX. BE named SK ecoplant/SK eternix (S.Korea distribution) — out of AI-supply-chain
  scope, not added. NVDA 10-K confirms customer concentration (top customer 22%, second 14%) but
  does NOT name customers, so existing named NVDA edges left unchanged.
- Regenerate: graph rebuilt 82 nodes / 190 edges; START HERE + Degree sheet re-synced.
- Validate: errors=0, warnings=190 (was 196; evidence/source backfill from this run). PASS.
- NOTE: Excel lock file (.~lock.AI-Supply-Chain-Network.xlsx#) present — openpyxl write still
  succeeded on disk. User should close Excel WITHOUT saving and reopen, or a stale copy may
  overwrite these changes.

2026-06-01: no new files (manual re-run). EDGAR fetch_edgar.py blocked by SEC 403 Forbidden on filer discovery (sandbox fair-access throttling); 0 filings pulled. No new inbox files. Graph unchanged at 82 nodes / 190 edges.

2026-06-02: no new files. EDGAR fetch_edgar.py unreachable from sandbox (DNS name-resolution failure / proxy 403 Forbidden on sec.gov — network not allowlisted); 0 filings pulled. All 24 inbox files already in ingested.json — 0 new inbox files. ingested.json unchanged; graph unchanged at 82 nodes / 190 edges. No spreadsheet write attempted.

2026-06-02 (manual, X-report ingest): One-off fold of X-Reports FACT-tagged findings into the graph (X reports live in X-Reports/, not sources/inbox/, so they had never been ingested).
- New companies (4): SIVE Sivers Semiconductor (L7), GFS GlobalFoundries (L3), QCOM Qualcomm (L4), CIFR Cipher Mining (L12).
- New edges (7), all (FACT, X-scan 2026-06-02): SIVE-partners with->GFS; SIVE-benefits from->T_CPO; GFS-benefits from->T_CPO; ARM-licenses CPU IP to->QCOM; QCOM-benefits from->T_INFER; NVDA-partners with->MRVL ($2B investment); CIFR-benefits from->T_INFER.
- Held back (per conservative policy): all VIEW/unverified items — Serenity's "$XFAB next $TSEM" framing, Xintech COUPE idea, the $36B Anthropic-TPU debt package, TSMC +15% 3nm-hike rumor, Leopold/Situational Awareness holding claims, Trump/quantum clickbait, Sunny Optical CPO entry. Candidates CIEN/JBL/GLXY left out (lower priority).
- Wiki: created 4 company pages; additive bullets on Marvell, Arm Holdings, Co-Packaged Optics (CPO), AI Inference Demand.
- Regenerate: 86 nodes / 197 edges. Validate: errors=0, warnings=190. PASS. Excel was closed.

## 2026-06-03 — scheduled ingest
- **Inbox files processed (7):** Bernstein "5 CEOs at SDC" (260602); Morgan Stanley "Taiwan meetings" (260601); ZeroHedge "Nobody Wanted Software"; TMTB EOD Wrap (CRDO/HPE first takes); TMTB Morning Wrap(17); tmtb632026; GS Korea strategy "KOSPI→12000".
- **Edges added: 8.** New companies added: 3 — xAI (L11), MediaTek (L4), Entegris (L2).
  - CRDO → supplies AECs to → Amazon / Microsoft / xAI (FACT, TMTB 2026-06-02: top 10%+ FQ4 customers).
  - MediaTek → co-designs custom silicon with → Google (FACT, MS 06-01: lower-cost TPU, ramp ~2027); MediaTek → competes with → Broadcom (VIEW, MS: 15-20% vs 80%+ share).
  - NVIDIA → competes with → Intel (FACT, MS: ~$20bn Grace/Vera Arm CPU vs x86); TSMC → manufactures chips for → Intel (VIEW, MS: roadmap parts moving to TSMC, EMIB-T plan B).
  - Entegris → supplies materials to → TSMC (FACT, Bernstein: yield-critical specialty/purity materials).
- **Evidence strengthened (no dup):** SK Hynix & Samsung → benefits from → HBM Demand had EMPTY evidence; filled with (VIEW, GS/MS 2026-06): HBM/DRAM undersupplied through 2028, ASP +20%+, LTAs.
- **Validator:** errors=0, warnings=188 (pre-existing source_doc/evidence-coverage on legacy rows). PASS. Graph: 89 nodes, 205 edges.
- **Flagged / skipped:**
  - "UBS-Tencent Holdings 2026 AIC" — **image-only PDF (no text layer, no embedded fonts)**; pdftotext yields no usable text. NOT ingested — re-drop a text-based copy to process.
  - ZeroHedge / TMTB EOD / tmtb632026 / GS Korea are market-flow / strategy commentary; processed but yielded few/no new concrete supply-chain edges (used only for theme VIEW evidence). Treated VIEWs as tagged, not facts.
  - Excel was CLOSED (no lock file) — xlsx written directly.

## 2026-06-03 — inbox ingest (APPLY)
**Files processed (33):** 3 x-scan extracts (0734/1634/2229), TMTB_dell_nvda, 22 TMTB daily morning/wrap notes (0515–0603), and PDFs (ASML, LITE 纪要, 博通/Broadcom GS, semianalysis space DC, UBS-Tencent, 'Worries Are Gone' ZeroHedge).

**New companies added (5):** AYAR (Ayar Labs, L7), STM (STMicroelectronics, L7), NANYA (Nanya Technology, L5), ALAB (Astera Labs, L7), SMTC (Semtech, L7).

**New edges added (20):**
- AYAR→NVDA (supplies optical components), AYAR→T_CPO.
- STM→T_CPO, STM→T_INFER, STM→T_POWER.
- NANYA→T_HBM, NANYA→CSCO (supplies memory).
- AVGO→ANTHROPIC + AVGO→OPENAI (co-designs custom silicon; Broadcom now 6 custom-silicon engagements per GS 6/3).
- LITE→NVDA (supplies optical components; NVIDIA locked considerable InP laser capacity).
- ALAB→AMZN (supplies interconnect, Trainium/UALink), ALAB→T_NET, ALAB→T_INFER.
- OPENAI→AMZN (runs compute on; Trainium capacity).
- INTC→GOOGL (co-designs custom silicon; Intel IPU deployed at Google).
- MRVL→GOOGL (co-designs custom silicon; networking chip in Google/Intel IPU — flagged (?)).
- BE→NBIS (supplies on-site fuel-cell power).
- SMTC→T_NET, SMTC→T_CPO.
- ASML→T_HBM.

**Dedup:** 0 duplicate edges added. Several restated relationships from x-scan/TMTB (AVGO↔GOOGL/MTK, TSM→AVGO, ANTHROPIC→GOOGL, MU→T_HBM, AMAT→INTC, FOXCONN→NVDA) already existed and were skipped.

**FACT vs VIEW:** FACT edges from filings-grade/CEO statements/x-scan FACT extracts; tagged VIEW for analyst forecasts (STM→T_POWER Mizuho, ALAB→T_INFER ISI, MRVL→GOOGL Funda-AI(?), SMTC→T_CPO, ASML→T_HBM GS).

**Skipped / not extracted:** The 22 TMTB daily wraps are dominated by analyst price-target/rating commentary (VIEWs) and already-known relationships; only genuinely new, concrete supply/demand links were folded in to avoid graph bloat. ZeroHedge (macro sentiment), semianalysis space-datacenter (niche orbital compute), and UBS-Tencent (China domestic AI, Tencent not a vault node) yielded no net-new on-theme edges. No instruction-like/unsafe file content encountered.

**Validator:** errors=0  warnings=188 (all pre-existing legacy-edge gaps: source_doc/evidence missing on older rows) — PASS. Graph regenerated: 94 nodes, 225 edges, bottleneck baked; START HERE + Degree sheet re-synced.

**Note:** Excel was NOT open (no lock file); xlsx written directly, no pending CSV.
2026-06-04: no new files

## 2026-06-04
- Inbox files processed: 2026-06-04-0404-x-scan-extract.md (1 new file; all other inbox files already ingested).
- Edges added: 1 — FOXCONN —partners with→ INTC (strength 2, FACT X-scan 2026-06-04: Hon Hai/Intel strategic collaboration on next-gen AI infrastructure, Edge AI, Physical AI).
- Skipped (de-dup, restated existing edges): SIVE —partners with→ GFS; LITE —benefits from→ T_CPO.
- New companies added: 0 (all referenced nodes already in Nodes sheet).
- Wiki: added "partners with" bullets to Companies/Foxconn (Hon Hai).md and Companies/Intel.md (additive sections).
- Validator: errors=0, warnings=188 (pre-existing: source_doc/evidence coverage). PASS.
- Excel: no lock file found; xlsx written directly. Graph regenerated (94 nodes, 226 edges).

## 2026-06-05 (Cowork daily ingest)
Inbox files processed (3, all FACT-only X-scan extracts):
- 2026-06-04-1204-x-scan-extract.md
- 2026-06-04-2004-x-scan-extract.md
- 2026-06-05-0404-x-scan-extract.md

Edges added: 2
- SAMBANOVA --partners with--> INTC (strength 1) — Intel Xeon rack-scale pairing, Computex 2026
- TSM --benefits from--> T_INFER (strength 3) — C.C. Wei 6/4 AGM, 2026 rev >30%, agentic-AI demand

New companies added: 1
- SambaNova Systems (SAMBANOVA), layer 4 Chip Designers (Accelerators/Networking), USA — private

Skipped as duplicates of existing edges (7 candidate edges in extracts, 5 already present):
- FOXCONN--partners with-->INTC (exists, X-scan 2026-06-04 prior ingest)
- AVGO--co-designs custom silicon with-->ANTHROPIC / OPENAI / META (all exist)
- AVGO--benefits from-->T_TRAIN (exists; Q2 FY26 $10.8B confirmation noted but not duplicated)

Wiki: created Companies/SambaNova Systems.md; appended additive bullets to Companies/Intel.md, Companies/TSMC.md, Themes/AI Inference Demand.md.

Validator: errors=0, warnings=188 (all pre-existing missing-evidence/source_doc on older rows; new rows fully tagged). Graph regenerated: 95 nodes, 228 edges.
Spreadsheet was NOT open (no lock file); xlsx written directly, no pending CSV needed.

## 2026-06-06 — daily ingest
- Inbox files processed (2): 2026-06-05-1204-x-scan-extract.md, 2026-06-05-2004-x-scan-extract.md (both FACT-grade X-scan extracts).
- New companies added (2): ByteDance (BYTEDANCE, layer 10), SpaceX (Colossus compute) (SPCX, layer 10).
- New edges added (9): MU→NVDA & SAMSUNG→NVDA (supplies HBM, Vera Rubin HBM4); ARM→META/OPENAI/ORCL/BYTEDANCE (licenses CPU IP, Arm AGI-CPU); GOOGL→SPCX & ANTHROPIC→SPCX (runs compute on); NVDA→SPCX (sells GPUs to).
- Strengthened 2 existing edges (untagged→FACT + source_doc): SKHYNIX→NVDA (HBM4 cert), AVGO→GOOGL (TPU commitment). No duplicate rows added.
- Deduped out (2): SKHYNIX→NVDA and AVGO→GOOGL already existed (strengthened instead).
- Validator: errors=0, warnings=184 (PASS). The 5 "flagged" warnings are intentional (?) markers.
- FLAGGED FOR USER REVIEW: the 20:04 extract attributes the "Colossus" compute facilities (Memphis) to SpaceX, but Colossus is commonly associated with xAI. The 3 SPCX edges and the SPCX node carry a "(?)" flag and a warning callout on the page. Verify the SpaceX-vs-xAI attribution and the ~$30B Google / ~$45B Anthropic deal figures against primary sources before relying on them.
- Spreadsheet was NOT open (no lock file); xlsx written directly, no pending CSV.

## 2026-06-07
- Inbox files processed: 2026-06-06-2256-x-scan-extract.md, 2026-06-07-0404-x-scan-extract.md (both pre-extracted FACT-grade x-scan extracts).
- Edges added: 0. All 7 unique candidate edges (AVGO co-designs w/ GOOGL/META/OPENAI/ANTHROPIC; MU/SAMSUNG/SKHYNIX supplies HBM to NVDA) already exist as FACT-grade rows — restatements of the 2026-06-05 x-scan, deduplicated.
- New companies added: 0 (all 9 referenced nodes already present).
- Strengthened 1 existing edge: AVGO|co-designs custom silicon with|META — added source_doc (X-Reports/2026-06-06-2256-x-scan.md) and dated FACT provenance to a previously unsourced "MTIA"-only evidence note. No duplicate row created.
- Validator: errors=0, warnings=182 (PASS). Graph rebuilt: 97 nodes / 237 edges.
- Excel: no lock file found (spreadsheet not open); xlsx write succeeded.
- Flagged for review: existing SAMSUNG|supplies HBM/DRAM to|NVDA edge still carries a NEEDS-REVIEW(?) note (prior Samsung HBM3E qual failures) — unchanged this run; the new x-scan asserts FACT-grade Samsung HBM4 cert, which the separate "supplies HBM to" edge already reflects.

## 2026-06-07 (ingest)
**Inbox files processed:** 15 new files.
**Edges added:** 20 (de-duplicated; ~10 candidate edges skipped as already present). **New companies:** 6.

**New nodes:** SMIC (L3 China foundry), Cambricon (L4 China AI accel), Largan Precision (L7 TW optical), Zhen Ding Technology (L6 TW PCB/substrate), Wiwynn (L9 TW ODM), Camtek (L2 IL inspection).

**Files that yielded new relationships:**
- *Bernstein — Huawei LogicFolding (2026-06-04):* SMIC benefits-from China buildout + manufactures-for Huawei/Cambricon; Cambricon/SMIC as China-AI beneficiaries. (Mostly VIEW — beneficiary calls, tagged accordingly.)
- *Citi — COMPUTEX CPO Ready to Go (2026-06-05):* Foxconn/MediaTek/TSMC/Wiwynn/Largan → CPO; MediaTek co-designs with Ayar Labs.
- *Citi — Zhen Ding (4958.TW) (2026-06-05):* ZDT optical-module PCB → Optical buildout; ABF-substrate supply to MediaTek (FACT-ish) and NVDA/AVGO/QCOM ("in the queue" → VIEW, flagged "(?)").
- *Jefferies — Blayne's Bytes (2026-06-05):* Broadcom drives HBM demand (TPUv8 content); Google → AI Training Capex ($85bn raise); Camtek HBM-inspection orders.
- *Morgan Stanley — Build for Future AI Infrastructure:* MediaTek co-designs Grace CPU with NVIDIA (N1X AI PC); SMIC→Cambricon foundry (VIEW, "(?)"); Cambricon competes with NVIDIA.
- *BofA — NVIDIA CFO Keynote (2026-06-04):* confirms existing NVDA→CPO (Feynman optical scale-up) — no new edge.

**Processed, no new edges (macro / positioning / consumer / narrative, or image-only PDFs):** Asia Technology Outlook (HBM tightness restates existing), Barclays US Economics (jobs), Goldman Sachs US Daily (no Fed cuts), J.P. Morgan Positioning Intelligence, Morgan Stanley Global Macro (payrolls), Bernstein Apple WWDC preview (consumer), 利率问题解读 (rates), 期权解读周五暴跌 (options), Anthropic-vs-OpenAI IPO race (The Information, narrative).

**Notes / flags:**
- Several PDFs were image-only (no text layer); supply-chain-relevant ones OCR'd via tesseract (BofA NVDA, both Citi notes, Jefferies). Macro/consumer image-only PDFs were not OCR'd (no graph value).
- VIEW vs FACT: China-semis beneficiary calls and "ABF clients in queue" stored as VIEW; speculative/pipeline items flagged "(?)".
- NOT in vault but repeatedly named (held back as conservative, no clean single edge): GUC, Alchip, Hua Hong, Piotech, Hygon, Onto, Cohu, Unimicron.
- Spreadsheet was NOT open (no lock file); xlsx written directly.

**Validator:** errors=0, warnings=182 (pre-existing categories: source_doc/evidence missing on legacy rows). Graph: 103 nodes, 257 edges. PASS.

## 2026-06-08 — scheduled ingest
Inbox files processed (3): 2026-06-07-1204-x-scan-extract.md, 2026-06-07-2003-x-scan-extract.md, 2026-06-08-0404-x-scan-extract.md.
Edges added: 3 — SKHYNIX→partners with→NVDA (3); NVDA→sells GPUs to→NAVER (2); NVDA→partners with→DOOSAN (1). All FACT-tagged.
New companies added: 2 — NAVER (Naver, layer 10 Hyperscalers/Cloud, 035420.KS, South Korea); DOOSAN (Doosan, layer 13 Power & Cooling, 000150.KS, South Korea).
Skipped as duplicates: SKHYNIX supplies HBM/memory→NVDA (3 verb-variants of existing 'supplies HBM to' edge); SKHYNIX benefits from T_HBM; MU benefits from T_HBM; TSM manufactures chips for NVDA; TSM manufactures chips for MRVL (existing strength-2 edge; new FACT restated multi-year foundry-capacity but not re-added).
Validator: errors=0, warnings=182 (all pre-existing: missing source_doc/evidence/untagged on legacy rows; none introduced by this run).
Graph regenerated: 105 nodes, 260 edges. Spreadsheet was NOT open (no lock file); xlsx written directly.

## 2026-06-08 (ingest)
- **Inbox files processed:** 19 new files.
  - x-scan extracts: 2026-06-08-1204, 2026-06-08-2004 (FACT-grade, pre-formatted).
  - Analyst reports w/ edges: MS Cerebras initiation, MS Kioxia group call, MS "Weekly: NVDA memory cuts", CITI SoCAMM2 reduction (OCR), Nomura structural memory shortage (OCR), Bernstein Vera Rubin GW cost, GS Micron 3Q preview, TMTB EOD Wrap + Morning Wrap(19), citi morning.
  - No-edge / macro / educational (reviewed, no relationships extracted): JPM "Investing in Tech 101", JPM "Macro Week Ahead", GS "CTA", "美股盘面", MS "Software Snippets: Token Budgeting", "特朗普计划会见 AI 公司" (political), "Rubin深度+AI+PCB报告" (low-quality Chinese retail infographic — see flag below).
- **New companies added (4):** HITACHI (Hitachi, 6501.T, L2), AAPL (Apple, L10), CBRS (Cerebras Systems, L4), KIOXIA (Kioxia Holdings, 285A.T, L5).
- **New edges added (10):**
  - HITACHI partners with INTC (FACT, x-scan).
  - NVDA sells GPUs to AAPL; AAPL runs compute on GOOGL; AAPL partners with GOOGL (FACT, x-scan — Apple PCC on Google Cloud Nvidia GPUs; Gemini-based Foundation Models).
  - CBRS benefits from T_INFER (VIEW, MS, PT $250 OW); CBRS competes with NVDA (VIEW, MS).
  - KIOXIA benefits from T_INFER (VIEW, MS — NAND/SSD, tight supply, LTA).
  - GLW supplies optical fiber to AMZN (FACT, TMTB); GLW benefits from T_NET (VIEW, TMTB).
  - SMCI builds AI servers for XAI (VIEW, TMTB/Bluefin via X — reported ~1,500-rack/$5B+ award; flagged "(?)").
- **De-dup:** x-scan rows "NVDA sells GPUs to GOOGL" and "TXN benefits from T_POWER" already existed → skipped.
- **Validator:** errors=0, warnings=182 (all pre-existing: source_doc/evidence missing on legacy rows). PASS. Graph = 109 nodes / 270 edges.
- **Flagged for user review:**
  - SMCI→xAI award is sourced from "Bluefin via X" (social/secondary) — tagged VIEW + "(?)", verify against a primary source.
  - Memory-shortage cluster (MS/CITI/Nomura) all corroborate NVIDIA cutting Vera Rubin SoCAMM2/LPDDR5X from 192GB→96GB modules (55TB→28TB per rack) due to DRAM shortage; suppliers reportedly filling only ~60% of SoCAMM2 demand; CMX/NAND demand rising. No new edges added (reinforces existing MU/Samsung/SK Hynix → NVDA memory + T_HBM); consider strengthening those evidence notes manually.
  - "Rubin深度+AI+PCB报告" names Chinese PCB/CCL beneficiaries (沪电/胜宏/生益 Shengyi, copper foil 隆扬+三井/Mitsui, Q-Glass) as Rubin NVL144 winners — NOT ingested as nodes/edges due to low source quality (garbled retail infographic). Recommend a primary-sourced pass if you want these added.
- Excel was CLOSED (no lock file); xlsx written directly.

## 2026-06-09 (scheduled ingest)
- Inbox files processed: 1 — `2026-06-09-0404-x-scan-extract.md` (FACT-only X-scan extract).
- Edges added: 1 — SIVE → supplies beamforming ICs to → ALL.SPACE (strength 2; FACT, X-scan 2026-06-09, $8.2M Ka-band BFIC order for 2027).
- Edges skipped (dedup): 1 — NVDA → sells GPUs to → SPCX already exists (restated SpaceX "AI1" GB300/Rubin reference design; no duplicate row added).
- New companies added: 1 — ALL.SPACE (ALLSPACE), private UK SATCOM terminal maker, layer 8 Networking Systems. (Extract proposed layer_name "Networking" → corrected to canonical "Networking Systems".)
- Wiki: appended downstream bullet to Companies/Sivers Semiconductor.md; created Companies/ALL.SPACE.md.
- Validator: errors=0, warnings=182 (pre-existing: source_doc/evidence coverage; PASS).
- EDGAR pull remains DISABLED (sec.gov unreachable). No instruction-like files encountered. Excel was not open (no lock file).

## 2026-06-10 — daily ingest

Inbox files processed (3):
- 2026-06-09-1204-x-scan-extract.md
- 2026-06-09-2004-x-scan-extract.md
- Semianalysis 原文- Powered Down, Lights Off. 800VDC Pushout and CPO Delays.pdf (image-only PDF; OCR'd via tesseract)

Changes:
- New companies (3): HANMI (Hanmi Semiconductor, equip/TC bonders), APH (Amphenol, copper interconnect), FORM (FormFactor, test/probe).
- New edges (7): HUAWEI→T_CHINA (FACT, $295B China DC buildout); HANMI→SKHYNIX supplies HBM bonding equipment (FACT, ₩44.2B HBM4 TC-bonder order); AAPL runs compute on NVDA (FACT, PCC on NVDA GPUs via Google Cloud); SMCI→T_INFER (FACT, ~$39B order book); APH→T_NET (VIEW, SemiAnalysis); FORM→T_CPO (VIEW, SemiAnalysis); TER→T_CPO (VIEW, SemiAnalysis).
- Evidence strengthened (2): LITE→T_CPO (added FACT CPO order + SemiAnalysis timing caution); VRT→T_POWER (was empty; SemiAnalysis 800VDC-pushout view).
- Skipped as duplicates: AAPL→GOOGL runs compute on, NVDA→GOOGL sells GPUs to, MU/SKHYNIX/SAMSUNG→NVDA supplies HBM to, LITE→NVDA optical, SKHYNIX→T_HBM, LITE→T_CPO (strengthened instead).
- Wiki: 3 new pages (Hanmi Semiconductor, Amphenol, FormFactor); additive bullets on Huawei, SK Hynix, Apple, Supermicro, Teradyne, Lumentum, Vertiv + Themes (China Indigenous AI Buildout, AI Inference Demand, CPO, Optical & Networking Buildout, HBM Demand, Datacenter Power Demand).
- Notable VIEWs not graphed (logged only): SemiAnalysis negative on LITE/COHR/HIMX/AAOI (CPO timing), WOLF/NVTS (800VDC pushout removes near-term WBG catalyst) — negative sentiment has no edge type; captured in theme/company notes.
- Validator: nodes=113 edges=278 errors=0 warnings=181 (pre-existing coverage gaps: source_doc/evidence missing on older rows). Graph regenerated.
- Excel not open; xlsx written directly. (Note: this run completed a 2026-06-09 ingest that was interrupted before regenerate/record; no double-writes — dedupe guard verified.)

## 2026-06-10 — Narrative Atlas added as source (user request)

New source: https://narrative-graph.onrender.com/feed (Narrative Atlas — daily per-ticker analyst-narrative digests).
Dedupe mechanism: _tools/narrative_atlas_state.json — every feed event gets key sha1(date|ticker|stance|summary[:120])[:16]; only events whose key is absent from "seen" are processed; the feed has no working server-side date filter (?from/?to ignored), so dedupe is client-side. State initialized with all 252 currently-visible events; events ≤2026-06-09 marked seen WITHOUT ingestion (historical backfill deliberately skipped to avoid stale/duplicate narratives).

From today's 31 events (2026-06-10):
- New companies (3): CIEN (Ciena, optical L7), IFX (Infineon, power semis L13 — judgment call, no analog/power-semi layer exists), FLEX (Flex, EMS/DC power L9).
- New edges (7, all VIEW): STM→T_NET (BofA upgrade, AI optical); AMAT/LRCX/KLAC→T_TRAIN (Barclays semicap capex); IFX→T_POWER (Jefferies, 800V pushout neutral/positive — corroborates SemiAnalysis); FLEX→T_POWER (JPM); CIEN→T_NET (JPM).
- Skipped as duplicates/restatements: SMCI $39B orders (already FACT from x-scan), TSM May rev, ANET→T_NET, NBIS→T_INFER, BE→T_POWER.
- Skipped as out-of-scope/uncertain: software-sentiment items (SNOW/TWLO/MDB/FROG/DDOG/NET/ZS/RDDT/NFLX/HOOD/CHWY/APP/DASH), META layoffs, AMZN freight, SKHYNIX supplier-pricing (vague), OPENAI 10GW Ohio DC w/ possible NVDA backing (negotiation-stage, not graphed), PSTG (single sentiment, node sprawl).
- Validator: nodes=116 edges=285 errors=0 warnings=181. Graph regenerated.

## 2026-06-10 (evening run)
- Inbox files processed: 18 (3 x-scan extracts 06-10, MS Siemens Energy, MS 800V, MS CPO, MS chipflation, MS memory "Healthy Reset", JPM MLCC/Sinocera fireside, Citi ORCL F4Q26 results, DB ORCL preview (OCR), Jefferies ORCL (OCR), DB SIA digest (OCR), TMTB morning(20)+EOD(1), BofA flows, 2x ZeroHedge ETF pieces)
- Narrative Atlas: 252 events visible, 0 new (all previously seen); state last_run updated.
- Nodes added: 5 — ENR (Siemens Energy, L14), DELTA (Delta Electronics, L13), SINOCERA (Sinocera 300285.SZ, L2 materials), ASE (ASE Technology, L6), FOCI (3363.TWO, L7).
- Edges added: 8 — ENR→T_POWER (VIEW MS); DELTA→T_POWER (VIEW MS, 800VDC racks 4Q26); SINOCERA→T_TRAIN (FACT JPM); SINOCERA supplies MLCC powder to SAMSUNG (FACT JPM, flagged (?) — actual customer likely Samsung Electro-Mechanics, not Electronics); ASE→T_CPO (VIEW MS); FOCI→T_CPO (VIEW MS); ORCL→T_INFER (FACT Citi, RPO $638B); BE supplies fuel-cell power to ORCL (FACT Jefferies).
- Evidence strengthened: TSM→T_CPO (+ PIC capacity 10kwpm 1Q27, MS 2026-06-10).
- Restatements skipped (already in graph): x-scan 06-10 edges (SKHYNIX/SAMSUNG/MU HBM→NVDA, NVDA→T_CPO, AVGO↔GOOGL, TSM→GOOGL/T_TRAIN); SMCI $39B orders; STM optical/CPO.
- Skipped, no supply-chain mechanism: BofA flow trends, 2x ZeroHedge ETF/positioning pieces, MS chipflation + memory decks (macro/cycle context, no new company relationships), DB SIA digest (industry stats), DB ORCL preview (restates OCI story), TMTB wraps (sentiment).
- Validator: errors=0, warnings=181 (legacy evidence/source gaps). Graph regenerated: 121 nodes / 293 edges.
- Excel was NOT open (no lock file); xlsx written directly.

## 2026-06-11 (scheduled run)

**Inbox files processed (10):** TMTB EOD Wrap/ADBE First Take; x-scan extracts 06-11 0404 & 2004; CPU.pdf (BofA agentic-CPU TAM $170bn); Intel double upgrade.pdf (BofA); Oppenheimer-SpaceX.pdf (IPO initiation); TACO Thursday ZeroHedge (macro only — no edges); TMTB Morning Wrap (21); 旭创.pdf (BofA Zhongji Innolight); 英特尔应筹集资金 (SemiAnalysis Intel capital raise).

**Narrative Atlas:** 240 events visible, 45 new. 6 graphed (WDC, STX, INTC, ARM, WOLF, NVTS). ~14 were restatements of existing edges (MU, SNDK, LITE, COHR, CRWV, BE, ORCL, STM, IFX, SMCI, SPCX, AMD — no duplicate rows added). ~25 skipped as off-topic: software/app sentiment (PANW, CRWD, DDOG, DASH, EPAM, ACN), consumer/e-commerce (NFLX, MELI, ETSY, EBAY, CVNA, DUOL, SPOT, HOOD, META ads, AMZN freight), price-move chatter without mechanism (ASML/AMAT, GOOGL, AVGO, TSEM, VRSN, NVDA generic, TSLA SpaceX-IPO sentiment).

**Added:** 7 nodes (WDC Western Digital, STX Seagate, WOLF Wolfspeed, NVTS Navitas, TSLA Tesla, INNOLIGHT Zhongji Innolight, TSEM Tower Semiconductor) and 16 edges. Evidence upgraded on 2 existing edges: MU→T_HBM (FACT: 2026 HBM capacity sold out, binding contracts), LITE→T_NET (FACT: capacity fully booked through 2028).

**Notable FACT edges:** SPCX acquired XAI ($250B, early 2026); Terafab chip-manufacturing JV SpaceX/Tesla/Intel (1TW/yr goal); AVGO+Apollo+Blackstone 20GW datacenter platform; CDNS 14A IP for INTC; NVDA strategic investment in INTC; Innolight deep Google relationship (>40% 1.6T share); Tower Semi $1.3bn SiPho 2027 contracts.

**Flagged / skipped with reasons:**
- GOOGL→Samsung TPU-v10 capacity + MediaTek design (The Information via TMTB): rumored & disputed in TMTB Slack — NOT graphed.
- SpaceX agreement to acquire Cursor: pending deal, app-layer — not graphed (noted only).
- WOLF/NVTS edges are strength-1 VIEW with (?) — 800VDC timing dispute (SemiAnalysis pushout vs JPM/Jefferies pushback).
- TACO Thursday ZeroHedge: macro-only, no supply-chain content.
- Oracle "four AI infra contracts" in TMTB(21): counterparties not legible in PDF extraction — no edge.

**Validator:** nodes=128 edges=309 errors=0 warnings=179 (legacy source_doc/evidence gaps) — PASS. Graph regenerated (update_graph.py).

**Excel:** no lock file detected; xlsx write succeeded directly.
