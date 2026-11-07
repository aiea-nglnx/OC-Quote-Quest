# OC Quote Quest: how to run

1. Put `oc-quote-quest.html` and `server.py` in the same folder.
2. In that folder run `python3 server.py` (Windows: `py server.py`).
3. Open **http://localhost:8000**

## Before any demo
Open **Data connections** (bottom of *Scout a site*) and click **Test connections**.
Every source should show ✓. For any ✕, note the message; most can be fixed by switching that
layer to a backup source.

## The four tabs
| Tab | Who it's for | What it does |
|---|---|---|
| **Scout a site** | Congregations, anyone with one site | Address search or map click → parcel outline, lot size, zoning, land use, 12 hazard/context layers, law-by-law answers, next steps. "What you know" boxes let an owner confirm faith/college ownership (SB 4) and city-confirmed non-historic status (SB 9). |
| **Find sites** | Acquisitions leads | Pick a city and land-use types (vacant, parking…) → every matching parcel from SCAG's land-use layer, on the map and ranked by size → screen the top N against the laws → CSV. |
| **Check a list** | City housing staff, surplus-land lists | Upload any CSV with lat/lon, APN or address columns (e.g. HCD's surplus-land file) → every row located and screened → ranked, mapped, CSV export, draft outreach email. |
| **Rules** | The team | Enter statute numbers (SB 684/1123 max lot size, SB 9 minimum new-lot size) with the section and date checked. Until all three are filled, that test stays UNKNOWN. |

## What's verified and what isn't
- Data layers come from the repo's `DATA-SOURCES.md` (verified 2026-11-06), plus CAL FIRE's 2025/2023
  fire zones and the USFWS National Wetlands Inventory.
- The earthquake fault-zone layer is **found by name on the state's server each run**, since no stable
  public URL was confirmed. If it can't be found, fault checks show UNKNOWN.
- Statute numbers are **not built in**: your team enters them in Rules from the official text.
- Zoning tests (single-family, commercial) are keyword matches on SCAG's zoning record, so check the code.
- Not legal advice.

The server caches answers in `.cache/` for a day (add it to `.gitignore`) and only relays to an
allowlist of public government/OSM hosts. No API keys.
