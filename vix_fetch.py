#!/usr/bin/env python3
import sys
from datetime import datetime
import csv
import urllib.request

def fetch_vix_yahoo():
    import yfinance as yf

    vix = yf.Ticker("^VIX")
    hist = vix.history(period="1d")

    if hist.empty:
        raise RuntimeError("Yahoo: empty response")

    close = float(hist.iloc[-1]["Close"])
    return "VIX", close


def fetch_vix_stooq():
    url = "https://stooq.pl/q/d/l/?s=vi.f&i=d"

    with urllib.request.urlopen(url, timeout=15) as r:
        rows = list(csv.reader(r.read().decode("utf-8").splitlines()))

    if len(rows) < 2:
        raise RuntimeError("Stooq: no data")

    # CSV: Date,Open,High,Low,Close,Volume
    close = float(rows[-1][4])
    return "VI.F", close


def main():
    timestamp = datetime.utcnow().isoformat()

    try:
        symbol, value = fetch_vix_yahoo()
        source = "yahoo"
    except Exception as yahoo_err:
        try:
            symbol, value = fetch_vix_stooq()
            source = "stooq"
        except Exception as stooq_err:
            print(
                f"ERROR,yahoo={yahoo_err},stooq={stooq_err}",
                file=sys.stderr,
            )
            sys.exit(1)

    print(f"{timestamp},{symbol},{value:.2f},{source}")


if __name__ == "__main__":
    main()
