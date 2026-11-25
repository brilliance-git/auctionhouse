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
- **Protection Warrior, farming at level 60** (pre-raid gear).
- Passive income on the side: fishing (sell Spotted Yellowtail on the AH, vendor Rockscale Cod).

### Current plan (level 60)
Ranked by solo viability first, then modelled g/hr (`python3 scripts/dungeon_farm_model.py`).
Conservative / optimistic figures.

| Role | Farm | Why | Status |
|---|---|---|---|
| **Baseline (reliable)** | **Krol'dok Stronghold** | ~50 g/hr: **41.2 g/hr from 6 bosses at real sell prices** (BoP blues plus the Expert Campfire blueprint, 4.3%, ~27g) **+ ~8 g/hr trash coin (estimate)**. Mobs 42–45, so trivial at 60. Ogre Key shortcut. See `docs/kroldok-model-2026-11-23.md` | modelled; **needs timed runs** |
| **Test first (maybe)** | **Dire Maul East: Pusillin > Zevrim > Hydrospawn > lashers > Alzzin (12 min)** | ~56 / 86 g/hr from real drop tables (Alzzin 1.94 blues, Pusillin 1.35 greens): above Krol'dok on conservative numbers. Non-elite melee lashers suit rage; Alzzin and Lethtendris cast. See `docs/dire-maul-maraudon-real-drops-2026-11-25.md` | not tested solo |
| **Reliable backup** | **Maraudon: Princess loop (12 min)** | ~41 / 64 g/hr (Princess Theradras 1.89 blues). Mobs 44–52. Next: **Zul'Farrak graveyard + pyramid (15 min) ~39 / 55** (real drop tables, `docs/uldaman-zf-sm-real-drops-2026-11-25.md`) | not tested |
| Other "maybe" | BRD entrance loop (~34 / 54), Alcaz Prison (~29 / 48), Sunken Temple Jammal'an + Ogom (~20 / 30; the balcony trolls drop no blues) | see `docs/dungeon-loops-15min-2026-11-25.md` | not tested |
| **Unlikely solo (highest value)** | **Stratholme** (Undead ziggurats + Ramstein ~105 / 135, Living Willey + Galford ~103 / 130), LBRS (~77), Shaper's Terrace Nanaya loop (~70), DM North to Gordok (~63), Scholomance (~58) | Boss greens and BoE set pieces from real drop tables. Level 57–62 elite casters, no documented prot-warrior solo. Try one pack first, or come back with raid gear after 9 Dec. See `docs/classic-dungeons-real-drops-2026-11-25.md` | test one pack |

Rules: use normal pull-and-kill only. No pathing, leash or ledge tricks; Blizzard confiscated
gold and suspended players for the Blackmaw Hold farm (Nov 16–17, 2026). Instances are capped
at 5 per hour, so any run under 12 minutes uses the full cap.

### Docs
| File | What it holds |
|---|---|
| `docs/farming-gear-2026-11-25.md` | Gear plan for farming at 60 as a solo prot warrior: heal-on-hit and damage-on-block/reflect items, Icy Veins' pre-raid lists adapted for solo farming, buying order, and Horde AH prices for the BoE items, plus a checklist by slot with sources and drop chances (Recovery enchant ~3g in materials, Shield Spike ~9.50g, Valor pieces ~35g for three, Skullflame Shield ~515g, Force Reactive Disk not in the game until Molten Core) |
| `docs/uldaman-zf-sm-real-drops-2026-11-25.md` | Uldaman, Zul'Farrak, all of SM, Razorfen Downs and Razorfen Kraul at 60 from real Wowhead Forever drop tables: ZF graveyard + pyramid ~39 g/hr (third reliable farm), SM Cathedral ~26, RFD ~24, Uldaman ~23, RFK ~14, Ruins of Lordaeron ~8; all boss blues BoP. Every farm is real-data except City of Dalaran (no Wowhead data) |
| `docs/wowhead-drops-classic-4-2026-11-25.md` | Raw Wowhead Forever drop tables for the rest of SM, Razorfen Downs and Razorfen Kraul |
| `docs/wowhead-drops-classic-5-2026-11-25.md` | Raw Wowhead Forever drop tables for Roogug (RFK) and Ruins of Lordaeron; notes that City of Dalaran has no Wowhead data |
| `docs/wowhead-drops-classic-3-2026-11-25.md` | Raw Wowhead Forever drop tables for Uldaman, Zul'Farrak and SM (Loksey, Vishas) |
| `docs/dire-maul-maraudon-real-drops-2026-11-25.md` | Dire Maul and Maraudon from real Wowhead Forever drop tables (`docs/wowhead-drops-classic-2-2026-11-25.md`): DME loop ~56 g/hr (passes Krol'dok conservatively, "maybe"), Maraudon Princess ~41 (best reliable after Krol'dok), DM North to Gordok ~63 ("unlikely") |
| `docs/wowhead-drops-classic-2-2026-11-25.md` | Raw Wowhead Forever drop tables for Dire Maul and Maraudon |
| `docs/classic-dungeons-real-drops-2026-11-25.md` | Sunken Temple, LBRS, BRD, Scholomance and Stratholme re-modelled from real Wowhead Forever drop tables (`docs/wowhead-drops-classic-2026-11-25.md`): BoE set pieces and boss greens push Strat to ~100+ g/hr ("unlikely" solo); Sunken Temple falls to ~20 |
| `docs/wowhead-drops-classic-2026-11-25.md` | Raw Wowhead Forever drop tables (blues with item IDs, ilvl, drop %, greens per kill) for five Classic dungeons |
| `docs/forever-dungeons-real-drops-2026-11-25.md` | The six Forever-only dungeons re-modelled from real Wowhead Forever drop tables (`docs/wowhead-drops-forever-2026-11-25.md`): every listed blue is BoP (Krol'dok Warplate trash pieces included); the Shaper's Terrace Titanosaur + Nanaya loop (~70 g/hr conservative; it was the highest-value loop until the Stratholme loops, ~100+, got real data) is "unlikely" solo |
| `docs/wowhead-drops-forever-2026-11-25.md` | Raw Wowhead Forever boss and trash drop tables (blues with item IDs, ilvl, drop %) for the six Forever-only dungeons |
| `docs/dungeon-loops-15min-2026-11-25.md` | Named ~15-minute loops (and 12-minute trims) for every long dungeon, ranked by solo tier then g/h against Krol'dok. First version, from estimates. Its numbers are superseded by the real-drop docs above (DME ~56, Sunken Temple ~20, Strat ~100+); the routes still apply |
| `docs/sunken-temple-2026-11-25.md` | Sunken Temple: the Spawn of Hakkar farm (~6 g/h, not worth a slot) and the trolls > Jammal'an + Ogom route (~20 g/h with real drop tables: the balcony trolls drop no blues) |
| `docs/dungeon-farms-viability-2026-11-23.md` | Which of those farms a solo prot warrior in pre-raid gear can actually clear: reliable / maybe / unlikely tiers, the re-ranked level-60 table, a one-pack test checklist, what improves the odds (`dungeon_farm_model.py --reasons`) |
| `docs/dungeon-farms-prot-warrior-2026-11-23.md` | Every Forever instance re-evaluated for a solo prot warrior at 60 (model: `scripts/dungeon_farm_model.py`) |
| `docs/kroldok-model-2026-11-23.md` | Krol'dok boss-by-boss expected value, route rules, open questions |
| `docs/instance-loot-values-2026-11-23.md` | The analysis: BoP check, AH and vendor value per instance, g/hr estimates, ranking, and data still needed |
| `docs/research-prot-warrior-solo-farms-2026-11-23.md` | The original web-research brief (routes, loot tables, sources, exploit warnings) |
| `docs/farm-leaderboard-2026-11-23.md` | Demand-capped leaderboard of the whole Horde AH: market gold per day, level-60 materials, markets to avoid, what it changes in the plan. Re-run with `scripts/farm_leaderboard.py` (`--rate "Item=units/h"` for demand-capped g/h) |
| `docs/farm-log.md` | Measured runs: fill this in after every test session |
| `docs/findings-2026-11-22.md` | Fishing comparison and market-cornering scan (Waylaid Crates etc.) |

### Next steps
1. **Gear:** weapon sustain enchant (Recovery, ~3g in materials) + Thorium Shield Spike (~9.50g)
   first; Skullflame Shield (~515g) later. See `docs/farming-gear-2026-11-25.md`.
2. Do 1–2 timed Krol'dok runs at 60 and record them in `docs/farm-log.md`.
3. Time one Dire Maul East loop. Switch if it beats Krol'dok's measured g/hr.
4. Try one Stratholme pack to see whether the "unlikely" tier is too pessimistic.
5. Replace the estimates with measured g/hr.

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
scripts/dungeon_farm_model.py rough level-60 g/h model for every dungeon farm, ranked by solo viability tier (--reasons)
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
- Commit as `Claude <noreply@anthropic.com>`, SSH-signed, so GitHub shows the commit as
  Verified. Keep personal email addresses and names out of commits and docs.

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
