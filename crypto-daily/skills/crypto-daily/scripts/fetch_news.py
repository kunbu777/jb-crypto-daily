#!/usr/bin/env python3
"""
Fetch crypto & financial news from multiple RSS feeds.
Sources: The Block, ForexLive, WSJ Markets, CoinDesk
"""

import json
import sys
import argparse
from datetime import datetime, timezone, timedelta
from urllib.request import urlopen, Request, build_opener, HTTPRedirectHandler
from urllib.error import URLError
import xml.etree.ElementTree as ET


RSS_FEEDS = [
    {"name": "The Block", "url": "https://www.theblock.co/rss.xml"},
    {"name": "ForexLive", "url": "https://www.forexlive.com/feed"},
    {"name": "WSJ Markets", "url": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml"},
    {"name": "CoinDesk", "url": "https://www.coindesk.com/arc/outboundfeeds/rss"},
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; CryptoDailyBot/1.0)"
}


def parse_date(date_str):
    """Parse various RSS date formats to UTC datetime."""
    if not date_str:
        return None
    formats = [
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S GMT",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S%z",
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue
    return None


def fetch_feed(source):
    """Fetch and parse a single RSS feed."""
    articles = []
    try:
        opener = build_opener(HTTPRedirectHandler())
        req = Request(source["url"], headers=HEADERS)
        with opener.open(req, timeout=15) as resp:
            content = resp.read()

        root = ET.fromstring(content)
        ns = {}

        # Handle both RSS and Atom
        items = root.findall(".//item") or root.findall(".//{http://www.w3.org/2005/Atom}entry")

        for item in items:
            def get(tag, fallback=""):
                el = item.find(tag)
                return (el.text or "").strip() if el is not None else fallback

            title = get("title")
            link = get("link")
            pub_date = get("pubDate") or get("published") or get("{http://www.w3.org/2005/Atom}published")
            description = get("description") or get("{http://www.w3.org/2005/Atom}summary")

            parsed_dt = parse_date(pub_date)

            articles.append({
                "source": source["name"],
                "title": title,
                "link": link,
                "pubDate": pub_date,
                "parsedDate": parsed_dt.isoformat() if parsed_dt else None,
                "parsedDateObj": parsed_dt,
                "content": description[:500] if description else "",
            })

    except Exception as e:
        print(f"[WARNING] Failed to fetch {source['name']}: {e}", file=sys.stderr)

    return articles


def filter_by_date(articles, target_date_str):
    """Filter articles published on the target date (UTC+8)."""
    tz_taipei = timezone(timedelta(hours=8))
    try:
        target = datetime.strptime(target_date_str, "%Y-%m-%d").date()
    except ValueError:
        return articles

    filtered = []
    for a in articles:
        dt = a.get("parsedDateObj")
        if dt:
            local_dt = dt.astimezone(tz_taipei)
            if local_dt.date() == target:
                filtered.append(a)
    return filtered


def format_all_news(articles):
    """Format articles into a single string for AI analysis."""
    output = ""
    for a in articles:
        output += f"【來源】{a['source']}\n"
        output += f"【標題】{a['title']}\n"
        output += f"【日期】{a['pubDate']}\n"
        output += f"【連結】{a['link']}\n"
        output += f"【內容】{a['content']}\n"
        output += "\n---\n\n"
    return output


def main():
    parser = argparse.ArgumentParser(description="Fetch crypto/finance RSS news")
    parser.add_argument("--date", help="Target date in YYYY-MM-DD format")
    parser.add_argument("--relative", choices=["yesterday", "today", "day-before-yesterday"],
                        help="Relative date")
    parser.add_argument("--date-range", action="store_true", help="Show available date range")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    # Fetch all feeds
    all_articles = []
    for source in RSS_FEEDS:
        articles = fetch_feed(source)
        all_articles.extend(articles)

    # Sort by date descending
    all_articles.sort(key=lambda x: x.get("parsedDateObj") or datetime.min.replace(tzinfo=timezone.utc), reverse=True)

    if args.date_range:
        dates = set()
        tz_taipei = timezone(timedelta(hours=8))
        for a in all_articles:
            dt = a.get("parsedDateObj")
            if dt:
                dates.add(dt.astimezone(tz_taipei).date().isoformat())
        sorted_dates = sorted(dates)
        if sorted_dates:
            print(json.dumps({"min": sorted_dates[0], "max": sorted_dates[-1], "dates": sorted_dates}))
        else:
            print(json.dumps({"min": None, "max": None, "dates": []}))
        return

    # Determine target date
    tz_taipei = timezone(timedelta(hours=8))
    now_taipei = datetime.now(tz_taipei)

    if args.date:
        target_date = args.date
    elif args.relative == "yesterday":
        target_date = (now_taipei - timedelta(days=1)).strftime("%Y-%m-%d")
    elif args.relative == "day-before-yesterday":
        target_date = (now_taipei - timedelta(days=2)).strftime("%Y-%m-%d")
    else:
        target_date = now_taipei.strftime("%Y-%m-%d")

    filtered = filter_by_date(all_articles, target_date)

    # Remove parsedDateObj (not JSON serializable)
    for a in filtered:
        a.pop("parsedDateObj", None)

    if args.json:
        print(json.dumps({"date": target_date, "count": len(filtered), "articles": filtered}, ensure_ascii=False, indent=2))
    else:
        if not filtered:
            print(f"NO_CONTENT:{target_date}")
        else:
            print(f"DATE:{target_date}")
            print(f"COUNT:{len(filtered)}")
            print("---")
            print(format_all_news(filtered))


if __name__ == "__main__":
    main()
