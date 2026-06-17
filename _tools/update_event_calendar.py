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

PAUSE_S = 3        # politeness gap between symbols; Yahoo rate-limits bursts
RETRIES = 4        # per-symbol attempts on a rate-limit before giving up
BACKOFF_S = 8      # base backoff; grows 8s, 16s, 32s... between retries


def with_retry(fn):
    """Call fn(); on a Yahoo rate-limit, back off and retry. Returns fn() or raises
    the last error. Decouples a transient 429 at the moment of the refresh from a
    blanked calendar entry — the close run's pocket guard depends on this data."""
    last = None
    for attempt in range(RETRIES):
        try:
            return fn()
        except Exception as e:  # noqa: BLE001
            last = e
            if "rate" in str(e).lower() or "too many" in str(e).lower():
                time.sleep(BACKOFF_S * (2 ** attempt))
                continue
            raise
    raise last

path = Path(__file__).parent / "event_calendar.json"
cal = json.loads(path.read_text(encoding="utf-8"))
today = datetime.date.today()
earnings = dict(cal.get("earnings") or {})
earnings_last = dict(cal.get("earnings_last") or {})

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
            c = with_retry(lambda: t.calendar)
            if isinstance(c, dict):
                dates = [to_date(d) for d in (c.get("Earnings Date") or [])]
        except Exception:
            pass
        if not any(dates):
            df = with_retry(lambda: t.get_earnings_dates(limit=12))
            if df is not None and len(df):
                dates = [to_date(d) for d in df.index]
        if not any(d and d < today for d in dates):
            # calendar API often returns only the next date; pull history for the past ones
            try:
                df = with_retry(lambda: t.get_earnings_dates(limit=12))
                if df is not None and len(df):
                    dates += [to_date(d) for d in df.index]
            except Exception:
                pass
        future = sorted(d for d in dates if d and d >= today)
        past = sorted(d for d in dates if d and d < today)
        if future:
            earnings[sym] = future[0].isoformat()
        elif sym in earnings and earnings[sym] < today.isoformat():
            # stale past date and nothing new found: drop it so runs see "unknown", not "safe"
            del earnings[sym]
        if past:
            # most recent PAST report: lets runs reason about earnings proximity offline
            # when no future date is scheduled (see pocket event guard c)
            earnings_last[sym] = past[-1].isoformat()
    except Exception as e:  # noqa: BLE001 - per-symbol failures must not kill the refresh
        print(f"{sym}: refresh failed ({e})", file=sys.stderr)

cal["earnings"] = earnings
cal["earnings_last"] = earnings_last
cal["earnings_updated"] = today.isoformat()
path.write_text(json.dumps(cal, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"earnings": earnings, "earnings_last": earnings_last,
                  "updated": cal["earnings_updated"]}, indent=2))
