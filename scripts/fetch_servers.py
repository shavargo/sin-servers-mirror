#!/usr/bin/env python3
"""Build a merged SiN address list from extras + optional public scrapes."""

from __future__ import annotations

import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTRAS = ROOT / "extras.txt"
OUT = ROOT / "servers.txt"

OPTIONAL_URLS = [
    "https://www.qtracker.com/server_lists/sin.txt",
    "http://www.qtracker.com/server_lists/sin.txt",
]

ADDR_RE = re.compile(r"^(\d{1,3}(?:\.\d{1,3}){3}):(\d{1,5})\b")
USER_AGENT = "sin-servers-mirror/0.1 (+https://github.com/shavargo/sin-servers-mirror)"


def parse_addrs(text: str) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = ADDR_RE.match(line)
        if not m:
            continue
        addr = f"{m.group(1)}:{int(m.group(2))}"
        if addr not in seen:
            seen.add(addr)
            out.append(addr)
    return out


def http_get(url: str, timeout: float = 20.0) -> str | None:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
        text = raw.decode("utf-8", "replace")
        if "<html" in text[:200].lower():
            return None
        return text
    except Exception as e:
        print(f"[warn] {url}: {e}", file=sys.stderr)
        return None


def main() -> int:
    addrs: list[str] = []
    seen: set[str] = set()

    extras = parse_addrs(EXTRAS.read_text(encoding="utf-8") if EXTRAS.is_file() else "")
    for a in extras:
        if a not in seen:
            seen.add(a)
            addrs.append(a)

    for url in OPTIONAL_URLS:
        body = http_get(url)
        if not body:
            continue
        for a in parse_addrs(body):
            if a not in seen:
                seen.add(a)
                addrs.append(a)

    addrs.sort(
        key=lambda s: tuple(
            int(x) if x.isdigit() else x for x in s.replace(":", ".").split(".")
        )
    )

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"# SiN dedicated server seeds — generated {now}",
        "# Sources: extras.txt + optional public lists (when available).",
        "# Format: one ip:port per line (game / connect port).",
        "",
    ]
    lines.extend(addrs)
    lines.append("")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {len(addrs)} address(es) to {OUT}")
    if not addrs:
        print("[error] server list is empty", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
