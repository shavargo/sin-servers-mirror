# sin-servers-mirror

Daily SiN dedicated-server address list for launchers and tools.

**Mirror (use this):** https://raw.githubusercontent.com/shavargo/sin-servers-mirror/main/servers.txt

## Why

SiN Gold clients are on Steam, but dedicated servers typically use classic Q2-engine networking (`hostport`, default **22450**) and do **not** reliably show up on Steam’s master. Launchers should not scrape ad-hoc lists on every refresh.

## Sources

| Source | How |
|--------|-----|
| `extras.txt` | Always-included community / pinned addresses |
| Optional public text lists (e.g. Qtracker) | HTTP scrape when the URL still returns plain `ip:port` lines |

Addresses are unioned and deduped. Empty optional sources are fine — extras carry the list.

## Update schedule

- Cron: daily at 12:23 UTC
- Manual: Actions → **Update servers.txt** → Run workflow

## Local

```bash
python3 scripts/fetch_servers.py
```

## Attribution

Unofficial community cache. Not affiliated with Nightdive, Ritual, or Valve.
