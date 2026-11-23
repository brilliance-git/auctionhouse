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
- how many are usually listed, and how many are posted, leave the AH or sell per day.

### How to read the answer (rules of thumb)
- **Compare the AH price after the 5% cut with the vendor price**, not the listed price.
  If it's within a few percent, vendor it: the deposit and waiting aren't worth it.
- **Liquidity matters as much as price.** A 30g item with ~9 listed (Expert Campfire
  blueprint) sells one at a time. A 4s item with thousands listed sells right away, but at
  the floor.
- **Check the trend.** "Posted per day" far above "leave the AH per day" means the market is
  oversupplied, and the price is probably falling (as with Righteous Orbs in Nov 2026).
- **Never seen on the AH (dungeon gear)** almost certainly means bind-on-pickup: vendor it.
  This held for every boss item checked on Wowhead.
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
- Items that have never been listed on this server: the item catalog only holds items seen
  on the AH.

---

## 2. Gold farming

This repo is the home of the **gold farming analysis**. One chat owns that thread and
updates the docs below; other chats should read them rather than redo the research.

### Character
- **Protection Warrior, level 47** (as of 2026-11-23). Update this when it changes; it
  decides which farm is best.
- Passive income on the side: fishing (sell Spotted Yellowtail on the AH, vendor Rockscale Cod).

### Current plan
| Level | Farm | Why | Status |
|---|---|---|---|
| **42–59 (now)** | **Krol'dok Stronghold** | ~30 g/hr from vendored BoP blues and the Expert Campfire blueprint (4.54%, ~27g), plus coin and the Krol'dok Warplate tank set | estimated; **needs test runs** |
| 44+ (backup) | Zul'Farrak graveyard | coin and greys, plus XP; 40–50 g/hr reported for mages | not tested on a warrior |
| 60 | Stratholme Living, Scarlet side | Righteous Orbs (84% from Galford, 7–11% from trash, ~9g on the AH, 2g vendor floor); ~38 g/hr vendoring everything | **no documented prot warrior solo**, so test it |

Rules: use normal pull-and-kill only. No pathing, leash or ledge tricks; Blizzard confiscated
gold and suspended players for the Blackmaw Hold farm (Nov 16–17, 2026). Instances are capped
at 5 per hour, so any run under 12 minutes uses the full cap.

### Docs
| File | What it holds |
|---|---|
| `docs/instance-loot-values-2026-11-23.md` | The analysis: BoP check, AH and vendor value per instance, g/hr estimates, ranking, and data still needed |
| `docs/research-prot-warrior-solo-farms-2026-11-23.md` | The original web-research brief (routes, loot tables, sources, exploit warnings) |
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
scripts/fetch_snapshots.py download every snapshot to data/ (~45 MB, git-ignored)
docs/                     dated analyses and research, plus the farm log
```

### API reference
All requests are GET with the key in the `X-API-Key` header.

| Endpoint | `wowapi` function | Returns |
|---|---|---|
| `/v1/status` | `status()` | namespace, house ids (home 114, neutral 117), snapshot count, first and latest epoch |
| `/v1/snapshots?since&until` | `snapshots()` | `[{epoch, modified, diffed}]`, oldest first, about hourly |
| `/v1/snapshots/{epoch\|latest}/prices` | `snapshot_prices()` | `{columns, rows}`, one row per item |
| `/v1/snapshots/{epoch\|latest}/archive` | `snapshot_archive()` | the raw auction files, as zip bytes |
| `/v1/items` | `items()` | `{id: {name, sell_price, purchase_price, quality, level, is_stackable, item_class, …}}`, only items seen on the AH |
| `/v1/items/{id}` | `item()` | one item |
| `/v1/items/{id}/prices?since&until` | `item_prices()` | the item's row in every snapshot |
| `/v1/items/{id}/book` | `item_book()` | current listings: `{home: [[unit_price, qty]…], neutral: […]}` |
| `/v1/tooltips` | `tooltips()` | tooltip lines, only for items the dashboard has looked up |
| `/v1/vendor-goods` | `vendor_goods()` | ids of items vendors sell without limit |
| `/v1/recipes` | `recipes()` | crafting recipes and their reagents |
| `/v1/buyouts` | `buyouts()` | the service's study of past buyouts and price jumps |

Price row columns: `epoch` (or `item_id`), `min_price`, `qty`, `lots`, `fill_price`,
`sold_qty`, `gone_qty`, `gone_value`, `new_qty`, `taken_qty`.
- `gone_qty` counts everything that left the AH: sales, expiries and cancellations.
- `sold_qty` is the service's estimate of actual sales, and is mostly 0 for non-stackable
  items.

### Data quirks
- `sell_price` in `/v1/items` is the **vendor** price. `purchase_price` is what a vendor
  charges, when a vendor sells it.
- AH cut is 5%, and listing also costs a deposit. Neutral AH (Booty Bay etc.) is a separate,
  thinner market.
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
