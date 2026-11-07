# OC Quote Quest: demo guide

## The story in one line
> "California opened up land for homes and the parcel data is public, but nobody connected them.
> Now a congregation, a one-person nonprofit or city staff can check a site, a city or a whole
> list in minutes, and the tool is honest about what public data can't answer."

## Before demo day
1. **Pick your sites.** Choose one parcel per user story that you've checked yourself:
   - a church or other faith parking lot (for SB 4)
   - a city with useful vacant or parking land (for Find sites)
   - a small CSV of candidate sites, or a filtered HCD surplus file (for Check a list)

   Put your Scout point in `DEMO_PT` near the bottom of `oc-quote-quest.html`.
2. **Fill in the Rules tab** from the official statute text (number, section, date checked). If you
   haven't, leave it empty. Showing an UNKNOWN is fine and honest.
3. **Run the connection test** ("Data connections" at the bottom of Scout a site). Everything should be ✓.
4. **Rehearse online with the server running** (`python3 server.py`). Every answer you load is
   cached in `.cache/`.

## On the day
- **Wi-Fi works:** `python3 server.py` → open `http://localhost:8000/?tour`
- **Wi-Fi is shaky:** `OFFLINE=1 python3 server.py`. The data answers come from your rehearsal
  cache. (Map tiles still need internet; the journal works without them.)
- Make the browser full screen and zoom to 110–125% so the room can read it.
- `?tour` opens the **guided tour**. Each card shows a **"Say it"** line for you, plus a
  **▶ button** that performs that step. Use the arrow keys to move and Esc to close.

## Running order (follows the tour)
| # | Show | Say | Click |
|---|---|---|---|
| 0 | Title card | The problem: laws public, data public, sites still found by luck. | Next |
| 1 | **Scout**: search box | "Meet a made-up facilities chair with a half-empty church lot." | ▶ Drop the sample pin |
| 2 | "What you know" box | "No free data says who owns a parcel. We let the owner confirm it, and label it." | ▶ Tick "we own it" and explore |
| 3 | Clues → laws | "Twelve public maps answer live. Look at the UNKNOWNs: we never round up to yes." | Tap the SB 4 card to open its reasons |
| 4 | **Find sites** | "Our acquisitions lead wanted ten sites to call. Here's every vacant or parking parcel, biggest first." | ▶ Load types → Find parcels → Screen top 10 |
| 5 | **Check a list** | "City staff: half your list is on a slope or in a fire zone. Now you see it up front." | ▶ Use sample points (or upload your CSV) |
| 6 | **Rules** | "Legal numbers come from the statute with a section and a date. We don't hard-code what we can't verify." | – |
| 7 | Data connections | Limits and next steps (below). | Test connections |

## Say the limits out loud (judges reward this)
- Owner type isn't in free public data. SB 4 depends on the owner confirming it.
- The single-family and commercial zoning tests are keyword matches on SCAG's zoning record.
- SCAG land use can lag reality, so the tool flags "check it hasn't been built on".
- Historic status needs the city. Lot-size limits need the statute numbers entered in Rules.
- Not legal advice. Nothing is sent or filed: the outreach email is only a draft.
- **Next:** contamination (state cleanup sites), water/sewer capacity, city objective standards.

## Backup plan
- If a layer shows ✕ live, say so and move on: "That's why answers say unknown instead of yes."
- If the map won't load, the journal still works with search or typed coordinates.
- Keep screenshots of each tour step in case the projector or laptop fails.

## Likely judge questions
- **"How do you know it's right?"** Every answer links its source layer and official rule, with
  the time checked. Unknowns stay unknown.
- **"Who would use this tomorrow?"** A congregation's facilities chair, a one-person acquisitions
  team, city housing staff: the three users in the brief.
- **"What would it take to go further?"** Owner data from the Assessor roll, contamination and
  utility layers, and one city's objective standards, done well.
