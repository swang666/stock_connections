"""Refresh the earnings dates in _tools/event_calendar.json via yfinance.

Run by the close run (cheap; ~10 quote-page hits). Macro dates (FOMC/CPI) are static
for the year and never touched here. Failures per symbol are non-fatal; the previous
date is kept so a flaky fetch never blanks the calendar.
Usage: python _tools/update_event_calendar.py
"""
import datetime
import json
import sys
import time
from pathlib import Path

import yfinance as yf

PAUSE_S = 3  # politeness gap between symbols; Yahoo rate-limits bursts

path = Path(__file__).parent / "event_calendar.json"
cal = json.loads(path.read_text(encoding="utf-8"))
today = datetime.date.today()
earnings = dict(cal.get("earnings") or {})

def to_date(x):
    if isinstance(x, datetime.datetime):
        return x.date()
    if isinstance(x, datetime.date):
        return x
    try:
        return x.date()  # pandas Timestamp
    except AttributeError:
        return None

for i, sym in enumerate(cal.get("symbols", [])):
    if i:
        time.sleep(PAUSE_S)
    try:
        t = yf.Ticker(sym)
        dates = []
        try:
            c = t.calendar
            if isinstance(c, dict):
                dates = [to_date(d) for d in (c.get("Earnings Date") or [])]
        except Exception:
            pass
        if not any(dates):
            df = t.get_earnings_dates(limit=12)
            if df is not None and len(df):
                dates = [to_date(d) for d in df.index]
        future = sorted(d for d in dates if d and d >= today)
        if future:
            earnings[sym] = future[0].isoformat()
        elif sym in earnings and earnings[sym] < today.isoformat():
            # stale past date and nothing new found: drop it so runs see "unknown", not "safe"
            del earnings[sym]
    except Exception as e:  # noqa: BLE001 - per-symbol failures must not kill the refresh
        print(f"{sym}: refresh failed ({e})", file=sys.stderr)

cal["earnings"] = earnings
cal["earnings_updated"] = today.isoformat()
path.write_text(json.dumps(cal, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"earnings": earnings, "updated": cal["earnings_updated"]}, indent=2))
