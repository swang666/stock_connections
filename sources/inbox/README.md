# 📥 inbox — drop new research here

Put new research reports / filings / articles in **this folder** (`sources/inbox/`).
The scheduled update job reads everything here, extracts supply-chain relationships,
updates the spreadsheet + wiki + graph, and logs what it added to `_tools/update_log.md`.

Supported: .pdf, .docx, .txt, .md, .html  (PDFs are read automatically)

Naming tip (helps provenance): `2026-05_MorganStanley_AI-power.pdf` = date _ firm _ topic.

Files are NEVER deleted — once processed they're recorded in `_tools/ingested.json` so
they won't be re-processed. You can leave them here or move them to `sources/` afterwards.
