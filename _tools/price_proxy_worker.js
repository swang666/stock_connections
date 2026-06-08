/**
 * Cloudflare Worker — CORS-safe quote proxy for the AI Supply-Chain Graph.
 *
 * WHY: the graph page is static (GitHub Pages). A browser fetch straight to Yahoo Finance is
 * CORS-blocked, so the page can't get live quotes on its own. This ~free Worker fetches Yahoo
 * server-side and re-serves JSON with an Access-Control-Allow-Origin header. Stock quotes are
 * public data — NO API KEY is involved.
 *
 * NOTE: Yahoo locked down the old /v7/finance/quote endpoint (it now returns
 * {"finance":{"error":{"code":"Unauthorized"...}}} without an authenticated crumb). This worker
 * uses the still-open /v8/finance/chart endpoint instead, one request per symbol, and returns a
 * compact map the page can read directly:
 *     { "NVDA": {"price":205.1,"prev":211.2,"chgPct":-2.89}, ... }
 *
 * DEPLOY (one time, ~5 min): see _tools/PRICE_PROXY_SETUP.md. After deploying, put the Worker URL
 * into _tools/price_config.json (PROXY_URL) and rebuild the graph.
 *
 * Endpoint:
 *   /quote?symbols=NVDA,AMD,TSM     -> { SYM: {price, prev, chgPct} }  (batched server-side)
 */
const ALLOW = "*"; // tighten to "https://<you>.github.io" once you know your Pages origin
const MAXSYMBOLS = 60;
const CONCURRENCY = 6; // be gentle to Yahoo

export default {
  async fetch(req) {
    const url = new URL(req.url);
    const cors = {
      "Access-Control-Allow-Origin": ALLOW,
      "Access-Control-Allow-Methods": "GET, OPTIONS",
      "Cache-Control": "public, max-age=60", // 60s edge cache → fresh but kind to Yahoo
    };
    if (req.method === "OPTIONS") return new Response(null, { headers: cors });
    if (req.method !== "GET") return json({ error: "GET only" }, 405, cors);
    if (!url.pathname.endsWith("/quote")) {
      return json({ ok: true, usage: "/quote?symbols=NVDA,AMD,TSM" }, 200, cors);
    }

    const symbols = (url.searchParams.get("symbols") || "")
      .split(",").map(s => s.trim()).filter(Boolean).slice(0, MAXSYMBOLS);
    if (!symbols.length) return json({ error: "no symbols" }, 400, cors);

    const out = {};
    // simple concurrency-limited fan-out to the still-open v8 chart endpoint
    for (let i = 0; i < symbols.length; i += CONCURRENCY) {
      const batch = symbols.slice(i, i + CONCURRENCY);
      await Promise.all(batch.map(async sym => {
        try {
          const r = await fetch(
            "https://query1.finance.yahoo.com/v8/finance/chart/" +
              encodeURIComponent(sym) + "?range=1d&interval=1d",
            { headers: { "User-Agent": "Mozilla/5.0 (graph price proxy)" } }
          );
          const j = await r.json();
          const m = j && j.chart && j.chart.result && j.chart.result[0] && j.chart.result[0].meta;
          if (m && m.regularMarketPrice != null) {
            const price = m.regularMarketPrice;
            const prev = (m.chartPreviousClose != null ? m.chartPreviousClose : m.previousClose);
            const chgPct = (prev ? ((price - prev) / prev) * 100 : null);
            out[sym] = { price, prev: prev ?? null, chgPct };
          }
        } catch (_) { /* skip this symbol; the page handles missing quotes gracefully */ }
      }));
    }
    return json(out, 200, cors);
  },
};
function json(obj, status, cors) {
  return new Response(JSON.stringify(obj), {
    status, headers: { ...cors, "Content-Type": "application/json" },
  });
}
