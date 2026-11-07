# OC-Quote-Quest (Angelina MAIN w/ Harshal)
Claude Impact Lab: UCI × SoCal Affordable Housing (Nov 7, 2026) Participant repo

# OC Quote Quest - LANE 1

> For a small housing nonprofit, a congregation with an underused lot, or city housing staff: OC Quote Quest checks Orange County parcels against California's new housing laws and public hazard maps, then shows which laws might open each site, what rules it out, and what is still unknown.

**Team:** Handoff
**Members:** Angelina A. Pao, Harshal
**Lane:** 1 Find it
**Built at:** Claude Impact Lab: UCI × SoCal Affordable Housing, November 7, 2026

## The real user

We designed for three made-up users from the lane's `scenarios.json`. The first is a one-person acquisitions team at a small housing nonprofit, with no GIS staff. The second is the facilities chair of a congregation whose parking lot sits half-empty during the week. The third is city housing staff checking lists of candidate sites. Laws like SB 9, SB 4, AB 2011 and SB 684 / SB 1123 have opened up land, and the parcel and hazard data is public. But no one has connected the two, so answering "could homes go here?" still takes a consultant or luck.

**Before:** Someone opens a dozen separate maps (zoning, FEMA flood, CAL FIRE, fault zones, wetlands), reads each law's exclusions by hand, and pieces it together one parcel at a time. For many teams, the only sites they find are the ones that happen to come to them: a city calls about surplus land, or a church offers its lot.

**After:** There are three ways in:
- **Scout a site:** search an address or click the map. The tool outlines the parcel, estimates lot size, queries the public layers live, and gives each law a verdict (POSSIBLE / RULED OUT / UNKNOWN) with the reason for each test.
- **Find sites:** pick a city and land-use types such as vacant or parking. The tool lists every matching parcel, ranks them by size, and screens the top ones.
- **Check a list:** upload a CSV, such as HCD's surplus-land file. Every row is located, screened, ranked and mapped.

## What we built

A single-page web app (`oc-quote-quest.html`) and a small Python server (`server.py`).

- **Scout a site:**
  - address search (OpenStreetMap), or click the map
  - county parcel outline, APN, and lot size estimated from the outline
  - 12 public layers queried live: zoning, existing land use, housing-element sites, FEMA flood, CAL FIRE fire hazard zones, earthquake fault zones, NWI wetlands, landslide, liquefaction, high-quality transit areas, CalEnviroScreen, and the parcel itself
  - a law-by-law screen with passed / failed / unknown tests and a link to each official rule
  - a next-steps checklist
- **"What you know about this site":** the owner can confirm faith or nonprofit-college ownership (SB 4), and that the city says the site isn't historic (SB 9). Answers that rely on these are labelled "you confirmed".
- **Find sites:** a city-wide search of SCAG's existing land-use layer, filtered by land-use type and minimum lot size, mapped and ranked, with screening of the top N and CSV export.
- **Check a list:** batch screening of any CSV, locating each row by lat/lon, then APN, then address. Includes ranking, map markers, CSV export, and a **draft** outreach email that is never sent.
- **Rules:** statute numbers (SB 684 / SB 1123 maximum lot size, SB 9 minimum new-lot size) are entered by the team with the section and the date checked. Until all three are filled in, those tests stay UNKNOWN.
- **Data connections:** a button that tests every source and reports why any failed.
- **Demo tour:** an 8-step guided walkthrough with presenter notes (open `/?tour`). The full demo script is in `DEMO.md`.

Screenshot: [add after first live run]


<img width="1310" height="962" alt="image" src="https://github.com/user-attachments/assets/ecb0eb7c-a178-48a0-8eec-d0bd7d752ce6" />
<img width="1312" height="952" alt="image" src="https://github.com/user-attachments/assets/40946b6b-487f-4339-994d-c6b7194144f6" />
<img width="1315" height="957" alt="image" src="https://github.com/user-attachments/assets/19f3a73a-757e-4734-bd20-5c73a727fdd6" />

**Demo video:** UPLOADED HERE
**Live demo:** [link, optional]

## How Claude is used

- **How we built it with Claude:**
  - Claude helped frame the problem from the Lane 1 brief.
  - It wrote and revised the app, the relay server and the docs.
  - It found additional public endpoints (CAL FIRE 2025/2023 fire zones, the USFWS National Wetlands Inventory) by web search.
  - It wrote a Node test harness with simulated ArcGIS responses (19 checks: engine logic, backup sources, rules, CSV parsing, APN and address lookup, CSV export safety).
  - Claude worked in a sandbox with no internet. It never reached the live services, and it did not hard-code statute numbers it couldn't verify.
- **Inside the tool when it runs:** Claude is **not called at runtime**. Every answer comes from public map services and transparent rule logic in the page, so there are no API keys and no model output to trust.
- **What a person checks:**
  - ownership and willingness to sell
  - historic status, with the city
  - statute numbers entered in Rules
  - the raw zoning code (the zoning tests are keyword matches)
  - that the site hasn't been built on since the data was published
  - water/sewer capacity and contamination
  - every draft email, before anyone sends it

## Try it

```bash
# Python 3.8+ only, standard library. No installs, no API keys.
git clone <this repo>
cd OC-Quote-Quest
python3 server.py            # Windows: py server.py
# open http://localhost:8000          (guided tour: http://localhost:8000/?tour)

# Before a demo: open "Data connections" (bottom of Scout a site) → Test connections.

# Shaky Wi-Fi: rehearse once online (answers are cached in .cache/ for a day), then
OFFLINE=1 python3 server.py  # answers only from the cache; map tiles still need internet
```

- **Needs:** Python 3 and a modern browser.
- **Why the server:** it fetches Leaflet if a CDN is blocked, relays requests to public map services to avoid CORS errors, and caches answers. It only relays to an allowlist of public hosts.
- **Environment variables:** `PORT` (default 8000) and `OFFLINE=1` (optional).
- **Repo hygiene:** add `.cache/` to `.gitignore`.

## Sources and assumptions

| Item | Source or assumption | Date checked |
|---|---|---|
| Law pathways (SB 9, SB 4, AB 2011, SB 684 / SB 1123) and links to official sources | Lane 1 `data/pathways.json` (HCD fact sheets, Gov. Code §65912.101) | 2026-11-06 (per repo) |
| Exclusions checked for each law | Lane 1 brief and HCD fact sheets, simplified. ASSUMPTION that this is enough for a screen; verify against the statute | 2026-11-06 (per repo) |
| SB 684 / SB 1123 max lot size; SB 9 minimum new-lot size | **Not built in.** Entered by the team in Rules, with section and date | set when entered |
| OC parcels (APN, address, outline) | OC Public Works Parcels FeatureServer | 2026-11-06 (per repo) |
| Zoning, existing land use, housing-element sites | SCAG LDX `Zoning_poly_OR`, `Existinglanduse_poly_OR`, `HousingElementSite_poly_scag` | 2026-11-06 (per repo) |
| Flood | FEMA NFHL layer 28 (counts only SFHA = T); backup: OC Floodplains (zones A/V) | 2026-11-06 (per repo) |
| Fire | CAL FIRE FHSZ LRA 2025 and SRA 2023 FeatureServers; backups: older CAL FIRE maps and OC LRA | Found 2026-11-07; not yet tested live |
| Wetlands | USFWS National Wetlands Inventory MapServer (small-box query) | Found 2026-11-07; not yet tested live |
| Earthquake fault zones | CGS Alquist-Priolo layer, **looked up by name** on the state's server each run (no stable URL confirmed) | Each run; UNKNOWN if not found |
| Landslide, liquefaction, transit areas, CalEnviroScreen | CGS Landslide Zones, OC Liquefaction, Caltrans HQTA, CalEnviroScreen 5.0 | 2026-11-06 (per repo) |
| Surplus land | HCD Surplus Land Act Notices CSV (data.ca.gov) | 2026-11-06 (per repo) |
| Lot size | Calculated from the parcel outline (spherical approximation). ASSUMPTION: close enough for screening, not a survey | – |
| "Single-family" / "commercial" zone | Keyword match on SCAG's zoning record. ASSUMPTION; verify the code | – |
| Ranking score weights (+3 per POSSIBLE law, +3 active surplus notice, +2 lot ≥ 10,000 sq ft, +2 vacant/parking, −3 per mapped hazard, −1 per unknown hazard, −2 archived) | ASSUMPTION, labelled in the tool | – |
| Sample points in "Check a list" | Made-up demo rows, labelled "not a real listing" | – |

## What is real and what is mocked

| Part | Status |
|---|---|
| Live queries to public map services | Working in code. Tested only against simulated responses; **run the connection test before relying on it** |
| Parcel outline, APN, lot-size estimate | Working (simulated test) |
| Law screen with passed / failed / unknown | Partly working: a simplified screen; AB 2011 and SB 684 / SB 1123 conditions are mostly not modelled |
| Owner and historic confirmation boxes | Working |
| Rules tab (statute numbers) | Working; empty until the team fills it in |
| Find sites (city-wide search) | Partly working: depends on detecting SCAG field names automatically; shows the fields it found if detection fails |
| Check a list (batch) | Working (simulated test); address lookup is limited to about 1 per second |
| Backup sources (flood, fire) | Working (simulated test) |
| Earthquake fault zones | Partly working: depends on the name lookup succeeding |
| Draft outreach email | Mocked by design: a draft, never sent |
| Sample points | Mocked (labelled as not real listings) |

## Where it gets things wrong

- **Ownership:** free public data doesn't show owner type. SB 4 is UNKNOWN unless the owner confirms it.
- **Zoning:** single-family and commercial are keyword matches, not a reading of each city's code. It can be wrong in both directions.
- **Historic status:** UNKNOWN until the city confirms it. There's no single public layer of local historic designations.
- **Lot-size limits:** UNKNOWN until the statute numbers are entered in Rules.
- **AB 2011 and SB 684 / SB 1123:** corridor width, frontage, prior use, density and other conditions aren't modelled, so these never reach POSSIBLE on map data alone.
- **Stale data:** SCAG land use and housing-element lists can lag reality, so a "vacant" parcel may already be built on.
- **Point checks:** most hazard checks use one point inside the parcel. A large parcel can partly overlap a hazard zone and still show "not inside".
- **Not covered:** contamination, water and sewer capacity, and city objective standards (parking, setbacks, height).
- **Don't trust it with:** a final eligibility decision, an offer price, or anything filed with a city. Use it as a screen to decide which sites to look at closely. Not legal advice.

## Next steps

**For a nonprofit or city to use it next month:**
1. Run the connection test and fix any source that fails.
2. Fill in Rules from the statute text with a lawyer or planner, and have them review the exclusion lists for each law.
3. Pick one city and check the zoning matches against its actual code.
4. Host it, for example on a small cloud server running `server.py`, so staff don't need Python.

**With one more week:**
- Check hazards against the whole parcel outline instead of one point.
- Add state cleanup-site (contamination) and utility service-area layers.
- Add owner-type leads from the IRS exempt-organizations file and worship-site maps, clearly labelled as leads, not facts.
- Model AB 2011 corridor conditions for one city.
- Compare housing-element sites with building footprints to flag stale sites.
- Optionally, add a Claude assistant that explains a site's results in plain language, with the API key kept on the server.

## Data and privacy

This project uses only public or provided data. It contains no personal information about real
tenants, buyers or residents. It does not file applications or contact any city or person.

It doesn't show owner names. Address search sends the typed text to OpenStreetMap's Nominatim service. Settings and counters are stored only in your browser.

## License

MIT, see the LICENSE file in this repo (or tell us what you chose).
