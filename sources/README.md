# sources/ — immutable intake layer

Karpathy's pattern: this folder is **ground truth**. Drop raw documents here and never edit them:

- SEC filings (10-K, 10-Q, 8-K) — get them free from SEC EDGAR
- Earnings call transcripts
- News articles, analyst notes, press releases
- Product / supplier announcements

The LLM **reads** from here and **writes** to the `Companies/` and `Themes/` pages. It never modifies the originals, so you can always re-derive the wiki from scratch.

Tip: name files like `NVDA_10K_FY2025.pdf` or `2026-05_news_CEG-MSFT-nuclear.md` so provenance is obvious.
