# Live-price proxy setup (one time, ~5 minutes, free, no API key)

The graph page is static (GitHub Pages), so a browser can't fetch Yahoo Finance directly — it gets
CORS-blocked. A tiny **Cloudflare Worker** fetches Yahoo server-side and adds the CORS header, so the
page can read live quotes. Stock quotes are public data; **no API key is required**. Free tier is
100,000 requests/day — far more than this needs.

## Steps

1. **Create a free Cloudflare account** → https://dash.cloudflare.com/sign-up (skip if you have one).

2. **Create a Worker**: in the dashboard, go to **Workers & Pages → Create application → Create Worker**.
   Give it a name like `ai-graph-prices`. Click **Deploy** (it deploys a hello-world first).

3. **Paste the code**: click **Edit code**, delete the sample, and paste the entire contents of
   `_tools/price_proxy_worker.js` from this repo. Click **Deploy**.

4. **Copy the Worker URL** shown at the top, e.g. `https://ai-graph-prices.yourname.workers.dev`.
   Test it in a browser: visiting
   `https://ai-graph-prices.yourname.workers.dev/quote?symbols=NVDA,AMD`
   should return a compact JSON map like `{"NVDA":{"price":205.1,"prev":211.2,"chgPct":-2.89},...}`.
   (If you ever see `{"finance":{"error":{"code":"Unauthorized"...}}}`, that's Yahoo's old
   /v7/quote endpoint being blocked — make sure you pasted the current worker, which uses
   /v8/chart instead.)

5. **Wire it into the graph**: open `_tools/price_config.json`, paste the URL into `PROXY_URL`, save:
   ```json
   { "PROXY_URL": "https://ai-graph-prices.yourname.workers.dev", "REFRESH_SECONDS": 60 }
   ```

6. **Rebuild**: `python3 _tools/update_graph.py`, then commit & push. The graph's **Prices mode** now
   pulls live quotes through your proxy on each visit.

## Notes
- **Lock it down (optional):** once you know your Pages origin, change `ALLOW` in the worker from
  `"*"` to `"https://<you>.github.io"` so only your site can use the proxy, then redeploy.
- **No proxy?** Leave `PROXY_URL` empty — the graph works fully; the live-price layer just stays off.
- **Refresh cadence:** the page re-fetches every `REFRESH_SECONDS` (default 60) while open; the worker
  also edge-caches 60s, so quotes are ~1 min fresh without hammering Yahoo.
