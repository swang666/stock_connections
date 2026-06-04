#!/usr/bin/env python3
"""
X-scan state + helpers (stdlib only).  Used by the twice-daily X scan.

Commands:
  slot-now
      Print current local time, slot (morning/afternoon), suggested filename
      stamp (YYYY-MM-DD-HHMM), and the 'since' cutoff (last successful scan).
  state-show
      Print the saved manifest (last scan + per-handle markers).
  state-set --slot morning|afternoon [--at ISO8601Z] --json '{"handle":{"last_post_url":..,"last_post_iso":..}, ...}'
      Record this run as the latest scan and store per-handle last-seen markers.
  trend-add --slot morning|afternoon [--at ISO8601Z] --json '{"NVDA":{"mentions":3,"sentiment":"pos"}, ...}'
      Append this scan's per-ticker tally to trends.json.
  trend-report [--last N]
      Show per-ticker mention counts across the last N scans, newest first, with delta.
  price-queries --tickers NVDA,MRVL,...
      Print the exact WebSearch queries to run to confirm each ticker's move
      (the agent runs WebSearch itself; this script never hits the network).

Timezone is read from watchlist.json (default America/Los_Angeles), with a
self-contained US-Pacific DST fallback so it works without the tzdata package.
"""
import argparse, datetime as dt, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
WATCHLIST = os.path.join(HERE, "watchlist.json")
STATE = os.path.join(HERE, "x_scan_state.json")
TRENDS = os.path.join(HERE, "trends.json")

def _load(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return default

def _save(path, obj):
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)
        f.write("\n")

def _second_sunday(year, month):
    d = dt.date(year, month, 1)
    # weekday(): Mon=0..Sun=6  -> first Sunday
    first_sun = 1 + (6 - d.weekday()) % 7
    return first_sun + 7  # second Sunday

def _first_sunday(year, month):
    d = dt.date(year, month, 1)
    return 1 + (6 - d.weekday()) % 7

def _us_pacific_offset(utc):
    """Return UTC offset hours for America/Los_Angeles (no tzdata needed)."""
    y = utc.year
    dst_start = dt.datetime(y, 3, _second_sunday(y, 3), 10)   # 2am PST = 10:00 UTC
    dst_end = dt.datetime(y, 11, _first_sunday(y, 11), 9)     # 2am PDT = 09:00 UTC
    return -7 if dst_start <= utc < dst_end else -8

def _now_local():
    cfg = _load(WATCHLIST, {})
    tz = cfg.get("timezone", "America/Los_Angeles")
    utc = dt.datetime.utcnow()
    try:
        from zoneinfo import ZoneInfo
        loc = dt.datetime.now(ZoneInfo(tz))
        return loc.replace(tzinfo=None), tz, loc.utcoffset().total_seconds()/3600, utc
    except Exception:
        off = _us_pacific_offset(utc)
        return utc + dt.timedelta(hours=off), tz, off, utc

def _slot_for(local, cfg):
    boundary = cfg.get("slots", {}).get("afternoon_starts_at_local_hour", 12)
    return "afternoon" if local.hour >= boundary else "morning"

def cmd_slot_now(_a):
    cfg = _load(WATCHLIST, {})
    local, tz, off, utc = _now_local()
    slot = _slot_for(local, cfg)
    st = _load(STATE, {})
    print(f"timezone          : {tz} (UTC{off:+.0f})")
    print(f"now_local         : {local.strftime('%Y-%m-%d %H:%M')} ({slot} slot)")
    print(f"now_utc           : {utc.strftime('%Y-%m-%dT%H:%MZ')}")
    print(f"filename_stamp    : {local.strftime('%Y-%m-%d-%H%M')}")
    print(f"report_path       : X-Reports/{local.strftime('%Y-%m-%d-%H%M')}-x-scan.md")
    print(f"since_cutoff_utc  : {st.get('last_scan_utc','(none - first run; use ~12h window)')}")
    print(f"since_cutoff_local: {st.get('last_scan_local','(none)')} [{st.get('last_slot','')}]")

def cmd_state_show(_a):
    print(json.dumps(_load(STATE, {"note": "no state yet"}), indent=2))

def cmd_state_set(a):
    cfg = _load(WATCHLIST, {})
    local, tz, off, utc = _now_local()
    at = a.at or utc.strftime('%Y-%m-%dT%H:%MZ')
    markers = json.loads(a.json) if a.json else {}
    st = _load(STATE, {})
    st["last_scan_utc"] = at
    st["last_scan_local"] = local.strftime('%Y-%m-%d %H:%M')
    st["last_slot"] = a.slot
    st.setdefault("handles", {})
    for h, m in markers.items():
        st["handles"][h] = m
    _save(STATE, st)
    print(f"state updated: last_scan_utc={at} slot={a.slot}; {len(markers)} handle markers")

def cmd_trend_add(a):
    local, tz, off, utc = _now_local()
    at = a.at or utc.strftime('%Y-%m-%dT%H:%MZ')
    tally = json.loads(a.json)
    rows = _load(TRENDS, {"scans": []})
    rows["scans"].append({"utc": at, "local": local.strftime('%Y-%m-%d %H:%M'),
                          "slot": a.slot, "tickers": tally})
    rows["scans"] = rows["scans"][-60:]  # keep last ~30 days
    _save(TRENDS, rows)
    print(f"trend row added: {at} slot={a.slot}; {len(tally)} tickers")

def cmd_trend_report(a):
    rows = _load(TRENDS, {"scans": []})["scans"]
    if not rows:
        print("no trend history yet"); return
    last = rows[-a.last:]
    agg = {}
    for i, s in enumerate(last):
        for tk, v in s["tickers"].items():
            m = v.get("mentions", 1) if isinstance(v, dict) else v
            agg.setdefault(tk, {"total": 0, "recent": 0, "sent": []})
            agg[tk]["total"] += m
            if i >= len(last) - 2:  # last 2 scans
                agg[tk]["recent"] += m
            if isinstance(v, dict) and v.get("sentiment"):
                agg[tk]["sent"].append(v["sentiment"])
    print(f"Trend over last {len(last)} scans ({last[0]['local']} -> {last[-1]['local']}):")
    print(f"{'Ticker':<8}{'Total':>6}{'Last2':>7}  Sentiment trail")
    for tk, v in sorted(agg.items(), key=lambda kv: (-kv[1]['recent'], -kv[1]['total'])):
        trail = ",".join(v["sent"][-5:])
        print(f"{tk:<8}{v['total']:>6}{v['recent']:>7}  {trail}")

def cmd_price_queries(a):
    tickers = [t.strip().upper() for t in a.tickers.split(",") if t.strip()]
    print("# Run each as a WebSearch (do NOT fetch a quote API from a script):")
    for t in tickers:
        print(f'WebSearch: "{t} stock price today close percent move {dt.date.today().year}"')

def main():
    p = argparse.ArgumentParser(description="X-scan state + helpers")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("slot-now").set_defaults(fn=cmd_slot_now)
    sub.add_parser("state-show").set_defaults(fn=cmd_state_show)
    s = sub.add_parser("state-set"); s.add_argument("--slot", required=True); s.add_argument("--at"); s.add_argument("--json", required=True); s.set_defaults(fn=cmd_state_set)
    s = sub.add_parser("trend-add"); s.add_argument("--slot", required=True); s.add_argument("--at"); s.add_argument("--json", required=True); s.set_defaults(fn=cmd_trend_add)
    s = sub.add_parser("trend-report"); s.add_argument("--last", type=int, default=10); s.set_defaults(fn=cmd_trend_report)
    s = sub.add_parser("price-queries"); s.add_argument("--tickers", required=True); s.set_defaults(fn=cmd_price_queries)
    a = p.parse_args()
    a.fn(a)

if __name__ == "__main__":
    main()
