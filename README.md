# auctionhouse

Tools, data and notes for making gold in **WoW: Forever** (US, patch 1.60.1), built on the
auction house API at <https://wow-api.skyl3lazer.com/docs>. Python 3 standard library only.

The README has three parts:
1. [Price checking from any chat](#1-price-checking-from-any-chat): the main reason this repo exists.
2. [Gold farming](#2-gold-farming): the research and the current farming plan.
3. [General](#3-general): setup, the API, data quirks, security and conventions.

---

## 1. Price checking from any chat

**Goal:** any Claude chat that has this repo can answer "is X worth anything?" or "AH or
vendor?" in one step, using live data instead of guesses.

### Getting a chat ready
- **Cloud sessions:** attach `brilliance-git/auctionhouse`. The API key is saved as a network
  secret on the cloud environment, and the proxy adds it to each request. Scripts still need
  the variable set, so prefix commands with `WOW_API_KEY=proxy-injected`.
- **Local:** copy `.env.example` to `.env` and paste the key into it.
- Quick check: `python3 -c "import wowapi; print(wowapi.status())"`.

### How to price check
```sh
python3 scripts/item_report.py "Flask of Mojo" "Powerful Mojo"   # any items, by name
python3 scripts/dungeon_drops.py Krol                             # every researched drop for one instance
```
`item_report.py` matches exact names first and falls back to a partial match. It prints:
- the vendor price;
- the median AH price, the latest price, and the trend from the first third of the history
  to the last third;
- what the AH pays after the 5% cut;
- how many are usually listed, and how many are posted, leave the AH or sell per day
  (estimated sales = `sold_qty + taken_qty`);
- what is listed right now, and the cheapest listing.

**Horde AH only.** Every price check uses the home (Horde) auction house. Never check the
neutral house (`/v1/neutral/...`, Booty Bay etc.); `wowapi` deliberately has no functions
for it.

### How to read the answer (rules of thumb)
- **Compare the AH price after the 5% cut with the vendor price**, not the listed price.
  If it's within a few percent, vendor it: the deposit and waiting aren't worth it.
- **Liquidity matters as much as price.** A 30g item with ~9 listed (Expert Campfire
  blueprint) sells one at a time. A 4s item with thousands listed sells right away, but at
  the floor.
- **Check the trend.** "Posted per day" far above "leave the AH per day" means the market is
  oversupplied, and the price is probably falling (as with Righteous Orbs in Nov 2026).
- **Never listed on the AH (dungeon gear)** almost certainly means bind-on-pickup: vendor it.
  This held for every boss item checked on Wowhead. Since 2026-11-23 the catalog also holds
  recipe items, so an item can be in the catalog with no listings: `item_report.py` then says
  "no listings in history".
- **Items with a vendor price floor** (Righteous Orb has a 2g vendor price) are low-risk to
  hold or list: the worst case is the vendor.
- Prices are in **copper** (1g = 100s = 10,000c). `wowapi.gold(c)` formats them.

### Answering in chat
Give the verdict first ("vendor it" or "list it at about X"), then a small table: vendor
price, lowest AH price, AH after the cut, and how many are listed. Mention a trend only if
it changes the advice. If the item comes from a farm, add it to the farming docs (part 2).

### Things the API can't tell you
- Bind type, drop rates and boss loot tables. Wowhead has these, but it blocks automated
  requests, so ask the user for a screenshot of the tooltip or the "Dropped by" tab.
- Prices for items that have never been listed on this server. The catalog holds items
  seen on the AH plus items that appear in recipes, but only listed items have prices.

---

## 2. Gold farming

This repo is the home of the **gold farming analysis**. One chat owns that thread and
updates the docs below; other chats should read them rather than redo the research.

### Character
- **Protection Warrior.** The plan below is split into levelling (pre-60) and level 60.
- Passive income on the side: fishing (sell Spotted Yellowtail on the AH, vendor Rockscale Cod).

### Current plan
| Level | Farm | Why | Status |
|---|---|---|---|
| **Levelling (42–59)** | **Krol'dok Stronghold** | ~50 g/hr modelled: **41.6 g/hr from 6 bosses at real prices** (~8.3g/run in vendored BoP blues plus the Expert Campfire blueprint, 4.54%, ~27g) **+ ~8 g/hr trash coin (estimate)**; also the Krol'dok Warplate tank set. Nothing else in the levelling band models above ~21 g/hr conservatively (~30 optimistically). See `docs/kroldok-model-2026-11-23.md` and `docs/dungeon-farms-prot-warrior-2026-11-23.md` | estimated; solo viability **"maybe"** while levelling (elites 42–45, casters, fear), so **test one pack first** |
| Levelling (backups) | Zul'Farrak graveyard, The Drowned City, Razorfen Downs | ~18–30 g/hr modelled; ZF graveyard is a big near-level pull | not tested on a warrior |
| 60 | **Krol'dok at 60 (~50 g/hr, reliable solo)**; test the Sunken Temple troll loop and the DME loop (~40–41 g/hr, "maybe"; `docs/dungeon-loops-15min-2026-11-25.md`) | Ranked by solo viability first (`docs/dungeon-farms-viability-2026-11-23.md`): Krol'dok at 60 is the best farm a pre-raid prot warrior can count on. Then Maraudon ~30, ZF ~29 and SM Cathedral ~21. Sunken Temple's balcony-troll loop (~41–69), the DME loop (~40–66) and Alcaz Prison (~29–48) are "maybe". Strat Living, Shaper's Terrace, Scholomance and Blackmaw Hold model higher but are **unlikely solo** (level 58–60 elite casters, no documented prot solo): try them only after a test pack passes, or with raid gear after 9 Dec | tiers use Classic-era mechanics; Forever's prot rework may differ |

Rules: use normal pull-and-kill only. No pathing, leash or ledge tricks; Blizzard confiscated
gold and suspended players for the Blackmaw Hold farm (Nov 16–17, 2026). Instances are capped
at 5 per hour, so any run under 12 minutes uses the full cap.

### Docs
| File | What it holds |
|---|---|
| `docs/dungeon-loops-15min-2026-11-25.md` | Named ~15-minute loops (and 12-minute trims) for every long dungeon, ranked by solo tier then g/h against Krol'dok. Best: Sunken Temple trolls and DME at 60 (~40 g/h, "maybe"); Strat Living orb loop ~71 but "unlikely" solo |
| `docs/sunken-temple-2026-11-25.md` | Sunken Temple: the Spawn of Hakkar farm (~5–9 g/h, not worth a slot) and the six balcony trolls (~40–68 g/h; unlikely solo while levelling, "maybe" at 60, the best "maybe" to test after Krol'dok) |
| `docs/dungeon-farms-viability-2026-11-23.md` | Which of those farms a solo prot warrior in pre-raid gear can actually clear: reliable / maybe / unlikely tiers, re-ranked tables for levelling and 60, a one-pack test checklist, what improves the odds (`dungeon_farm_model.py --reasons`) |
| `docs/dungeon-farms-prot-warrior-2026-11-23.md` | Every Forever instance re-evaluated for a solo prot warrior while levelling and at 60 (model: `scripts/dungeon_farm_model.py`) |
| `docs/kroldok-model-2026-11-23.md` | Krol'dok boss-by-boss expected value, route rules, open questions |
| `docs/instance-loot-values-2026-11-23.md` | The analysis: BoP check, AH and vendor value per instance, g/hr estimates, ranking, and data still needed |
| `docs/research-prot-warrior-solo-farms-2026-11-23.md` | The original web-research brief (routes, loot tables, sources, exploit warnings) |
| `docs/farm-leaderboard-2026-11-23.md` | Demand-capped leaderboard of the whole Horde AH: market gold per day, level-60 materials, markets to avoid, what it changes in the plan. Re-run with `scripts/farm_leaderboard.py` (`--rate "Item=units/h"` for demand-capped g/h) |
| `docs/farm-log.md` | Measured runs: fill this in after every test session |
| `docs/findings-2026-11-22.md` | Fishing comparison and market-cornering scan (Waylaid Crates etc.) |

### Next steps
1. Do 1–2 timed Krol'dok runs and record them in `docs/farm-log.md`.
2. Collect the Wowhead "Drops" tab for each Krol'dok boss; see the list in section 5 of the
   analysis doc.
3. Replace the estimates with measured g/hr.
4. At 60, test Strat with melee-only packs, then decide.

### Open ideas
- A price watcher: alert when Waylaid Crates or Greater Shadow Protection Potions drop below
  their usual price (to buy), or when Righteous Orbs go above ~10g (to sell).

---

## 3. General

### Repo layout
```
wowapi.py                 API client, one function per endpoint
scripts/item_report.py    price check any item(s)
scripts/dungeon_drops.py  price the researched drops for each instance
scripts/fetch_snapshots.py download every snapshot, the catalog, vendor goods and recipes to data/ (~50 MB, git-ignored)
scripts/farm_leaderboard.py rank farmable commodities by market gold per day, offline from data/
scripts/dungeon_farm_model.py rough g/h model for every dungeon farm (levelling band and 60), ranked by solo viability tier (--reasons)
docs/                     dated analyses and research, plus the farm log
```

### API reference
All requests are GET with the key in the `X-API-Key` header. The schema is at
`/openapi.json` (no key needed); check it when something looks off. Updated 2026-11-23.

| Endpoint | `wowapi` function | Returns |
|---|---|---|
| `/v1/status` | `status()` | namespace, house ids (`house` = home/Horde 114), snapshot count, first and latest epoch |
| `/v1/snapshots?since&until` | `snapshots()` | `[{epoch, modified, diffed}]`, oldest first, about hourly |
| `/v1/snapshots/{epoch\|latest}/items` | `snapshot_items()` | `{epoch, columns, rows}`, one row per item |
| `/v1/snapshots/{epoch\|latest}/archive` | `snapshot_archive()` | the raw auction files, as zip bytes (kept 30 days; counts as 20 requests) |
| `/v1/items` | `items()` | `{id: {name, sell_price, purchase_price, quality, level, is_stackable, item_class, …}}`: items seen on the AH or in a recipe |
| `/v1/items/{id}` | `item()` | one item |
| `/v1/items/{id}/history?since&until` | `item_history()` | `{item_id, columns, rows}`: the item's row in every snapshot |
| `/v1/items/{id}/listings` | `item_listings()` | `{item_id, epoch, listings: [[unit_price, qty]…]}`, cheapest first; bid-only listings left out |
| `/v1/tooltips` | `tooltips()` | tooltip lines (binding, stats…), only for items the server has looked up |
| `/v1/vendor-goods` | `vendor_goods()` | ids of items vendors sell without limit |
| `/v1/recipes` | `recipes()` | crafting recipes and their reagents |
| `/v1/buyouts` | `buyouts()` | the service's study of past buyouts and price jumps |

**Deprecated upstream, will be removed:** `/v1/snapshots/{s}/prices`, `/v1/items/{id}/prices`
and `/v1/items/{id}/book`. The old function names `snapshot_prices()`, `item_prices()` and
`item_book()` still work: they call the new routes (`item_book()` returns Horde listings only).

**Not used:** the `/v1/neutral/...` routes (neutral house). Price checks are Horde only.

**Limits and errors:** 300 requests at once, refilled at 1 a second. HTTP 429 (rate limit) and
503 (snapshot being replaced) carry a wait time; `wowapi` retries both up to 3 times.

Row columns: `epoch` (or `item_id`), `min_price`, `qty`, `lots`, `fill_price`,
`sold_qty`, `gone_qty`, `gone_value`, `new_qty`, `taken_qty`.
- `fill_price` is the unit price paid when spending 2 gold on the cheapest listings.
- `gone_qty` counts listings that vanished with hours left: bought or cancelled, the data
  can't tell which.
- `sold_qty` counts certain sales out of listings still up; `taken_qty` estimates whole
  listings bought. **Estimated sales = `sold_qty + taken_qty`** (`wowapi.est_sold(row)`).
  Both are commodity-only, so gear shows sales only through `gone_qty`.
- The sales columns are null when the previous snapshot is more than 75 minutes older.

### Data quirks
- `sell_price` in `/v1/items` is the **vendor** price. `purchase_price` is what a vendor
  charges, when a vendor sells it.
- AH cut is 5%, and listing also costs a deposit. All prices here are the Horde AH; the
  neutral AH (Booty Bay etc.) is a separate, thinner market that this repo ignores.
- History starts 17 Nov 2026. Forever launched on 4 Nov, so prices are still settling: re-check
  before acting on any number in `docs/`.

### Security and privacy
- The API key lives only in `.env` (git-ignored) or the cloud environment's network secrets.
  **Never commit it or paste it into chat.**
- Commit as `brilliance-git <brilliance-git@users.noreply.github.com>`. Keep personal email
  addresses and names out of commits and docs.

### Conventions
- Analyses are dated docs (`docs/<topic>-YYYY-MM-DD.md`). Write a new dated file rather than
  silently rewriting old conclusions, and update the tables in this README when the plan
  changes.
- Label every number with where it came from: AH data (with date), Wowhead, a guide, or
  measured in-game.

### Known gaps
- The first commit made on the owner's computer (with `score_markets.py`, `buyout_history.py`
  and the full 2026-11-22 findings) was never pushed. Push it to a separate branch with
  `git push origin main:original-local`, then merge in what's missing.
