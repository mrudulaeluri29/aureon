#!/usr/bin/env python3
"""Find upcoming SunDevilCentral events that mention food, with their SunDevilCentral links.

SunDevilCentral (ASU's club and event platform) publishes every event in a public calendar feed. The feed has
no "free food" tag, so this script reads each event's title and description for food words and prints a short
list Cubbie can text.

  sundevil_food.py --now 2026-10-24T14:00 [--hours 48] [--campus Tempe] [--max 10]
  sundevil_food.py --sample

Times are Arizona time (UTC-7, no daylight saving). Exit codes: 0 ok (the list may be empty), 2 bad input,
3 feed unreachable.
"""
from __future__ import annotations

import argparse
import json
import quopri
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

FEED = "https://sundevilcentral.eoss.asu.edu/ical/arizonau/ical_arizonau.ics"
SAMPLE = Path(__file__).resolve().parent.parent / "assets" / "sample_sundevil.ics"
ARIZONA = timezone(timedelta(hours=-7))
CAMPUSES = {"tempe": "Tempe Campus", "downtown": "Downtown Phoenix Campus", "poly": "Polytechnic Campus",
            "polytechnic": "Polytechnic Campus", "west": "West Valley Campus", "west valley": "West Valley Campus"}

# Words that mean food is actually served. "Dinner series" or "lunch and learn" alone are too vague,
# so plain meal words only count next to "free", "provided" or "served".
FOOD = re.compile(
    r"free (food|pizza|lunch|dinner|breakfast|snacks?|boba|drinks|tacos|donuts|cookies|ice cream)"
    r"|(food|pizza|lunch|dinner|breakfast|snacks?|refreshments|drinks)( and \w+)? (will be |is |are )?(provided|served)"
    r"|\bpizza\b|\bsnacks\b|\brefreshments\b|\bboba\b|\bdonuts\b|\bcatered\b",
    re.IGNORECASE,
)
PAID = re.compile(r"\$\s?\d+|tickets? (are|cost)|admission fee|cost to attend", re.IGNORECASE)


def fail(message: str, code: int = 2) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(code)


def fetch(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "freebie-radar/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return response.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, TimeoutError) as exc:
        fail(f"SunDevilCentral feed unreachable: {exc}", 3)


def unescape(value: str) -> str:
    return (value.replace("\\n", " ").replace("\\N", " ").replace("\\,", ",")
            .replace("\\;", ";").replace("\\\\", "\\").strip())


def parse_events(text: str) -> list[dict]:
    text = re.sub(r"\r?\n[ \t]", "", text)  # unfold continuation lines
    events = []
    for block in text.split("BEGIN:VEVENT")[1:]:
        fields = {}
        for line in block.splitlines():
            if ":" not in line:
                continue
            head, value = line.split(":", 1)
            name, *params = head.split(";")
            if name == "SUMMARY" and "ENCODING=QUOTED-PRINTABLE" in params:
                value = quopri.decodestring(value.encode()).decode("utf-8", errors="replace")
            if name == "CATEGORIES" and "X-CG-CATEGORY=event_tags" in params:
                name = "TAGS"
                value = value.split(":", 1)[-1] if value.startswith("event_tags") else value
            if name == "ORGANIZER":
                value = next((p[4:].strip('"') for p in params if p.startswith("CN=")), "")
            fields.setdefault(name, value)
        events.append(fields)
    return events


def start_time(value: str) -> datetime | None:
    try:
        if value.endswith("Z"):
            return datetime.strptime(value, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc).astimezone(ARIZONA)
        return datetime.strptime(value[:15], "%Y%m%dT%H%M%S").replace(tzinfo=ARIZONA)
    except ValueError:
        return None


def snippet(text: str, match: re.Match) -> str:
    start = max(0, match.start() - 60)
    return ("..." if start else "") + text[start:match.end() + 60].strip() + "..."


def find_food(events: list[dict], now: datetime, hours: int, campus: str | None, limit: int) -> list[dict]:
    until = now + timedelta(hours=hours)
    found = []
    for event in events:
        starts = start_time(event.get("DTSTART", ""))
        if not starts or not (now - timedelta(hours=1) <= starts <= until):
            continue
        if campus and campus not in event.get("TAGS", ""):
            continue
        title = unescape(event.get("SUMMARY", ""))
        text = f"{title}. {unescape(event.get('DESCRIPTION', ''))}"
        match = FOOD.search(text)
        if not match:
            continue
        location = unescape(event.get("LOCATION", ""))
        found.append({
            "title": title,
            "host": event.get("ORGANIZER", ""),
            "starts": starts.strftime("%a %b %d, %I:%M %p").replace(" 0", " "),
            "when": starts.strftime("%Y-%m-%dT%H:%M"),
            "where": "" if "Sign in" in location else location,
            "food": snippet(text, match),
            "may_cost": bool(PAID.search(text)),
            "link": event.get("URL", ""),
        })
    found.sort(key=lambda e: e["when"])
    return found[:limit]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--now", help="student's local time now, e.g. 2026-10-24T14:00 (Arizona time)")
    parser.add_argument("--hours", type=int, default=48, help="how far ahead to look (default 48)")
    parser.add_argument("--campus", help="Tempe, Downtown, Poly or West Valley (default: all)")
    parser.add_argument("--max", type=int, default=10, help="most events to print (default 10)")
    parser.add_argument("--sample", action="store_true", help="use the bundled sample feed, no network")
    args = parser.parse_args()

    campus = None
    if args.campus:
        campus = CAMPUSES.get(args.campus.lower().replace(" campus", "").strip())
        if not campus:
            fail(f"--campus must be one of Tempe, Downtown, Poly, West Valley (got {args.campus!r})")
    if args.sample:
        text, default_now = SAMPLE.read_text(encoding="utf-8"), "2026-10-24T09:00"
    else:
        if not args.now:
            fail("give --now in the student's local time (or --sample)")
        text, default_now = fetch(FEED), args.now
    try:
        now = datetime.fromisoformat(args.now or default_now).replace(tzinfo=ARIZONA)
    except ValueError:
        fail(f"--now must look like 2026-10-24T14:00 (got {args.now!r})")
    if args.hours < 1 or args.max < 1:
        fail("--hours and --max must be at least 1")

    events = find_food(parse_events(text), now, args.hours, campus, args.max)
    print(json.dumps({"source": "SunDevilCentral", "count": len(events), "events": events},
                     indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
