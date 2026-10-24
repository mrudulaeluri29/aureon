#!/usr/bin/env python3
"""Keep Freebie Radar from texting the same find twice, and sort finds by date.

Cubbie collects finds (from email, Canvas and web pages), writes them to a JSON list and runs:

  seen.py new  --finds FILE --today YYYY-MM-DD   print finds not sent yet, past dates dropped, soonest first
  seen.py mark --finds FILE                      record those finds as sent

Each find is an object with at least "type" and "title"; "when" (YYYY-MM-DD or YYYY-MM-DDTHH:MM, local time)
and "link" are used when present. State lives in ~/.config/freebie-radar/seen.json.
--sample uses assets/sample_finds.json and never reads or writes the student's state.

Exit codes: 0 ok, 2 bad input.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

SAMPLE = Path(__file__).resolve().parent.parent / "assets" / "sample_finds.json"
STATE = Path.home() / ".config" / "freebie-radar" / "seen.json"
KEEP_DAYS = 180
TYPES = {"food", "study", "scholarship", "opportunity"}


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(2)


def parse_day(value: str, label: str) -> date:
    try:
        return date.fromisoformat(value.strip())
    except (ValueError, AttributeError):
        fail(f"{label} must look like 2026-10-27 (got {value!r})")


def parse_when(value) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).strip()).replace(tzinfo=None)
    except ValueError:
        fail(f"'when' must look like 2026-10-27 or 2026-10-27T17:00 (got {value!r})")


def key(find: dict) -> str:
    # Same event or deadline from two sources (an email and a web page) should count once,
    # so the key is the type plus the title with punctuation and case stripped.
    title = re.sub(r"[^a-z0-9]+", " ", find["title"].lower()).strip()
    return f"{find['type']}|{title}"


def load_finds(path: Path) -> list[dict]:
    try:
        finds = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"can't read {path}: {exc}")
    if not isinstance(finds, list):
        fail("the finds file must be a JSON list of objects")
    for i, find in enumerate(finds):
        if not isinstance(find, dict) or not find.get("title") or find.get("type") not in TYPES:
            fail(f"find {i} needs a 'title' and a 'type' of {', '.join(sorted(TYPES))}")
        parse_when(find.get("when"))
    return finds


def load_state(path: Path | None) -> dict[str, str]:
    if path is None or not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}  # a damaged state file only means a find may repeat once


def cmd_new(finds: list[dict], state: dict[str, str], today: date) -> dict:
    fresh, already, past, duplicate, batch = [], 0, 0, 0, set()
    for find in finds:
        when = parse_when(find.get("when"))
        if key(find) in state:
            already += 1
        elif when and when.date() < today:
            past += 1
        elif key(find) in batch:
            duplicate += 1
        else:
            batch.add(key(find))
            fresh.append(find)
    # Dated finds first, soonest first; undated ones after, in the order Cubbie found them.
    fresh.sort(key=lambda f: (parse_when(f.get("when")) is None, parse_when(f.get("when")) or datetime.max))
    return {"new": fresh, "already_sent": already, "past": past, "duplicates": duplicate}


def cmd_mark(finds: list[dict], state: dict[str, str], today: date) -> dict[str, str]:
    cutoff = (today - timedelta(days=KEEP_DAYS)).isoformat()
    state = {k: v for k, v in state.items() if v >= cutoff}
    for find in finds:
        state.setdefault(key(find), today.isoformat())
    return state


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("command", choices=["new", "mark"])
    parser.add_argument("--finds", help="JSON list of finds")
    parser.add_argument("--today", help="student's local date, YYYY-MM-DD (default: this computer's date)")
    parser.add_argument("--sample", action="store_true", help="use the bundled sample; leaves saved state alone")
    args = parser.parse_args()

    if args.sample:
        path, state_path = SAMPLE, None
        today = parse_day(args.today or "2026-10-25", "--today")
    else:
        if not args.finds:
            fail("give --finds FILE (or --sample)")
        path, state_path = Path(args.finds).expanduser(), STATE
        today = parse_day(args.today, "--today") if args.today else date.today()

    finds = load_finds(path)
    state = load_state(state_path)

    if args.command == "new":
        print(json.dumps(cmd_new(finds, state, today), indent=1, ensure_ascii=False))
        return 0

    state = cmd_mark(finds, state, today)
    if state_path is not None:
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(json.dumps(state, indent=1), encoding="utf-8")
    print(f"marked {len(finds)} finds as sent" + (" (sample, nothing saved)" if state_path is None else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
