#!/usr/bin/env python3
"""Build the Bumkus Showcase gallery page from showcase.json.

Usage: python3 build.py
Reads showcase.json in this directory and writes index.html in this
directory. Python standard library only; no dependencies.

Rules enforced by this script:
- The intro (Bumkus Showcase description) renders as the page intro.
- Slots with "held": true are NOT rendered.
- Descriptions are copied verbatim from showcase.json; this script never
  edits wording, adds prices, or adds financing language.
"""

import html
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
JSON_PATH = HERE / "showcase.json"
HTML_PATH = HERE / "index.html"


def card(slot):
    name = html.escape(slot["name"])
    url = html.escape(slot["url"])
    desc = html.escape(slot["description"])
    return (
        "    <section class=\"card\">\n"
        f"      <h2>{name}</h2>\n"
        f"      <p>{desc}</p>\n"
        f"      <p><a href=\"{url}\">Visit {name}</a></p>\n"
        "    </section>\n"
    )


def main():
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    intro = data["intro"]
    rendered = [s for s in data["slots"] if not s.get("held")]
    if len(rendered) != 8:
        print(
            f"REFUSED: expected 8 rendered slots, found {len(rendered)}",
            file=sys.stderr,
        )
        return 1
    cards = "".join(card(s) for s in rendered)
    page = (
        "<!DOCTYPE html>\n"
        "<html lang=\"en\">\n"
        "<head>\n"
        "<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        "<title>Bumkus Showcase</title>\n"
        "<style>\n"
        "body { font-family: Georgia, serif; margin: 2em auto; "
        "max-width: 44em; padding: 0 1em; line-height: 1.5; }\n"
        ".card { border-top: 1px solid #ccc; padding: 1em 0; }\n"
        "h1 { font-size: 1.8em; }\n"
        "h2 { font-size: 1.2em; margin-bottom: 0.2em; }\n"
        "</style>\n"
        "</head>\n"
        "<body>\n"
        "  <header>\n"
        "    <h1>Bumkus Showcase</h1>\n"
        f"    <p>{html.escape(intro['description'])}</p>\n"
        "  </header>\n"
        "  <main>\n"
        f"{cards}"
        "  </main>\n"
        "</body>\n"
        "</html>\n"
    )
    HTML_PATH.write_text(page, encoding="utf-8")
    print(f"Wrote {HTML_PATH} ({len(rendered)} slots rendered)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
