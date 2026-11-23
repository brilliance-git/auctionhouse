# Demand-capped farm leaderboard — 2026-11-23

**Question:** which farmable commodities are worth the time, given how much gold the Horde AH
actually **absorbs per day**? Price alone misleads. A 9g item that sells 50 a day can't
absorb much farming.

**Source for every number below, unless marked otherwise:** Horde AH (house 114), 151 hourly
snapshots from **17 Nov 2026 13:17 UTC to 23 Nov 2026 20:25 UTC** (6.3 days), computed by
`scripts/farm_leaderboard.py` from the `snapshot_items` tables cached in `data/`.
Catalog, vendor goods and recipes are from `/v1/items`, `/v1/vendor-goods` and `/v1/recipes`,
pulled 2026-11-23.

> **Prices are still settling.** WoW: Forever launched on 4 Nov 2026 and the history only
> starts on 17 Nov. Many level-60 materials are still moving 20–60% a week. Re-run the script
> before acting on any number here:
> ```sh
> python3 scripts/fetch_snapshots.py      # only downloads the new snapshots
> python3 scripts/farm_leaderboard.py --top 40
> ```

This builds on `findings-2026-11-22.md` (fishing, market cornering) and
`instance-loot-values-2026-11-23.md` / `kroldok-model-2026-11-23.md` (dungeon farms). It does
not redo them.

---

## 1. Method

### Item set (784 items with price history, 619 sell at least 1 a day)
I checked the actual `item_class` / `item_subclass` values in `/v1/items` before choosing the
filter. Trade goods are `item_class = "Trade Goods"`, with subclasses Herb, Metal & Stone, Cloth,
Leather, Cooking (meat and fish), Elemental, Enchanting, Other (gems, venom sacs, mojo, orbs),
Parts and Trade Goods. The filter:

- **Kept:** every `is_stackable` item, with all classes and subclasses considered.
- **Removed:**
  - classes Projectile, Key, Quiver, Container and Recipe;
  - every item in `/v1/vendor-goods` (thread, dyes, flux, vials, spices and so on);
  - **crafted-only goods**: any output of a recipe in `/v1/recipes` (bolts, cured hides,
    grinding stones, potions, Arcanite Bar, Enchanted Thorium and so on). These are kept,
    because they are also farmed directly:
    - smelted bars (Mining recipes), flagged `smelt`;
    - base leathers (Light, Medium, Heavy, Thick and Rugged), which come from Skinning even
      though Leatherworking can also make them;
    - Elemental Fire and the elemental essences, which drop even though Alchemy can transmute
      them;
  - Refined Deeprock Salt, which a Salt Shaker makes (not a recipe, so the filter missed it).
- Quest-class items that do trade on the AH (Vulture Gizzard, Pristine Black Diamond) stay in,
  flagged `quest`.
- `--include-crafted` shows the crafted goods too.

### Per item
| Column | Definition |
|---|---|
| **net** | median `fill_price` × 0.95 (5% AH cut). `fill_price` is what you'd get selling volume. Falls back to median `min_price` when there's never a `fill_price`. |
| **sold/d** | estimated units sold per day = `sold_qty + taken_qty` (`wowapi.est_sold`), averaged over the hours in which the item's sales columns are **not null** (null = missing, not zero), × 24 |
| **sure/d** | `sold_qty` only: certain sales out of listings still up. A **floor** for sold/d. |
| **g/day** | market gold per day = net × sold/d |
| **sure g/d** | net × sure/d: the floor version |
| qty / lots | median units listed / median number of listings (liquidity and competition) |
| new/gone | units posted per day vs units leaving with time left per day |
| trend | median value in the last third of the history vs the first third |

**Flags:**
- **oversupplied:** new/gone is ≥ 1.5× the market-wide median, or above the median while
  listed qty grew 50% or more. The market-wide median new/gone is **2.09**, not 1, because
  `new_qty` counts every repost while `gone_qty` never counts expired listings. Comparing an
  item with 1 would flag everything.
- **falling:** trend −15% or worse. **rising:** +15% or better.
- **vendor:** net is within 5% of the vendor price.

### How far to trust sold/d
`taken_qty` (whole listings bought) is an estimate, and it dominates: across the board,
sold/d is ~8× sure/d. The whole filtered market comes to **~60,000 g/day estimated vs ~7,200 g/day
certain**. The truth lies between the two, and cancel-and-repost churn by undercutters probably
inflates `taken_qty`. So:
- use **g/day to rank** (as asked: it is consistent across items);
- use **sure g/d as the pessimistic case** (both columns are below);
- be most wary of items where sure/d is near 0 (Righteous Orb 2/day, Dark Rune 8, Powerful
  Mojo 6): their sales are almost all inferred.

### The demand cap (`--rate`) and the market-share assumption
`--rate "Item=units_per_hour"` adds:
```
AH units/h = min(rate, sold/d ÷ 24 × share)
gold/h     = AH units/h × max(net, vendor) + (rate − AH units/h) × vendor
```
Units the market can't absorb are vendored rather than left piling up on the AH.

**Share defaults to 10%** (`--share`). Why: the top markets have 50–300 listings (the `lots`
column) from many sellers, and you only sell while you hold the cheapest listings. One extra
seller who posts often and undercuts can realistically take a 5–25% share. Taking much more
needs constant undercutting, which drives the price down for everyone, so the price would no
longer be the median used here. Use `--share 0.25` for an optimistic case.

**Consequence:** at a 10% share, an item adds at most **g/day ÷ 240 gold per hour**. Even the
#1 market (Rugged Leather, ~2,000 g/day) caps at **~8 g/h** from the AH, and at sure-sales
rates it's under 1 g/h. **No single commodity outpaces a vendor-loot dungeon farm** (Krol'dok
~41.5 g/h estimated) unless your share is large or you farm several items at once.

### Item level as a zone proxy
`level` in the catalog is the item level. Reliability:
- **Good** for gathered and dropped materials. Herbs, ore, cloth and leather follow the
  gathering or mob tier (Mageweave 40, Thick Leather 40, Runecloth 50, Rugged Leather 50,
  Black Lotus 60). The source zone is usually around that level or up to ~10 above it.
- **Rough** for enchanting mats, which follow the level of the gear disenchanted, not a zone.
  Also rough for Arcane Crystal (60, but mined from Thorium veins in 45+ zones) and Heavy Stone
  (25, from Iron veins in 30s zones).
- **Useless** for items at level 1: Mote of Unstable Magic, quest items, whelp scales, venom
  sacs and feathers. Filter by name for those.

So `--min-level` / `--max-level` is a decent first cut for materials, not a zone guarantee.
**No level filter by default.**

---

## 2. Top 20 overall (whole Horde AH, ranked by market g/day)

| # | Item | ilvl | Subclass | Net (after 5% cut) | Vendor | Sold/d (est.) | Sure/d | **Market g/day** | Sure g/d | Qty / lots | Trend | Flags |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Rugged Leather | 50 | Leather | 18s 53c | 5s 00c | 10,856 | 562 | **2,012** | 104 | 3,284 / 191 | +4% | |
| 2 | Arcane Crystal | 60 | Other | 14g 56s | 20s 00c | 113 | 24 | **1,644** | 350 | 118 / 49 | +41% | rising |
| 3 | Runecloth | 50 | Cloth | 5s 22c | 4s 00c | 25,917 | 755 | **1,354** | 39 | 12,048 / 295 | −12% | |
| 4 | Thorium Ore | 40 | Metal & Stone | 23s 79c | 2s 50c | 5,455 | 677 | **1,298** | 161 | 3,208 / 136 | +3% | |
| 5 | Thorium Bar | 50 | Metal & Stone | 27s 03c | 6s 00c | 4,530 | 895 | **1,224** | 242 | 2,338 / 54 | +2% | smelt |
| 6 | Essence of Water | 55 | Elemental | 3g 90s | 4s 00c | 306 | 61 | **1,193** | 237 | 180 / 50 | +12% | |
| 7 | Mithril Ore | 40 | Metal & Stone | 9s 52c | 2s 50c | 12,355 | 833 | **1,176** | 79 | 3,867 / 188 | +5% | |
| 8 | Mote of Unstable Magic | 1 | Other | 10s 45c | 2s 00c | 10,714 | 2,271 | **1,120** | 237 | 3,447 / 69 | −15% | falling |
| 9 | Black Dragonscale | 55 | Leather | 1g 64s | 10s 00c | 676 | 91 | **1,114** | 149 | 411 / 83 | −46% | oversupplied, falling |
| 10 | Mithril Bar | 40 | Metal & Stone | 10s 81c | 4s 00c | 9,303 | 1,200 | **1,005** | 130 | 4,648 / 114 | +5% | oversupplied, smelt |
| 11 | Black Lotus | 60 | Herb | 7g 71s | 10s 00c | 130 | 19 | **1,003** | 144 | 209 / 79 | −13% | |
| 12 | Mageweave Cloth | 40 | Cloth | 4s 15c | 2s 50c | 23,224 | 833 | **963** | 35 | 6,018 / 244 | −1% | |
| 13 | Thick Leather | 40 | Leather | 5s 80c | 3s 00c | 16,546 | 760 | **960** | 44 | 4,748 / 215 | 0% | |
| 14 | Greater Eternal Essence | 55 | Enchanting | 2g 50s | 1c | 365 | 82 | **915** | 206 | 282 / 47 | +32% | rising |
| 15 | Large Brilliant Shard | 55 | Enchanting | 2g 71s | 1c | 324 | 52 | **879** | 142 | 222 / 61 | +8% | |
| 16 | Devilsaur Leather | 50 | Leather | 66s 46c | 5s 00c | 1,183 | 215 | **786** | 143 | 860 / 69 | −23% | falling |
| 17 | Dream Dust | 45 | Enchanting | 23s 51c | 1c | 3,100 | 470 | **729** | 110 | 1,425 / 101 | −16% | falling |
| 18 | Heavy Stone | 25 | Metal & Stone | 3s 20c | 60c | 21,322 | 627 | **683** | 20 | 3,921 / 176 | −1% | |
| 19 | Ironweb Spider Silk | 50 | Cloth | 54s 15c | 25s 00c | 1,182 | 76 | **640** | 41 | 565 / 131 | +42% | rising |
| 20 | Vulture Gizzard | 1 | Quest | 2g 38s | 0c | 260 | 75 | **619** | 179 | 189 / 36 | +7% | quest |

**Reading it:**
- **Volume beats price.** Cheap, deep markets (Rugged Leather 18s, Runecloth 5s, Mithril and
  Thorium Ore) absorb as much gold as the 5–15g items (Arcane Crystal, Black Lotus), and they
  take any quantity you can farm.
- **On the certain-sales floor, the expensive items rank higher.** Arcane Crystal leads, then
  Dark Iron Bar, Thorium Bar, Mote of Unstable Magic, Essence of Water and Greater Eternal
  Essence. The cheap deep markets are the ones most reliant on the `taken_qty` estimate.
- **Most of the top 20 need a profession:**
  - Skinning (Rugged, Thick and Devilsaur Leather, Black Dragonscale), which the character
    doesn't have;
  - Mining (ores, bars, Arcane Crystal, Heavy Stone);
  - Herbalism (Black Lotus);
  - Enchanting (essences, shards, dust).
- **No profession needed (kill drops):** Runecloth, Mageweave, Essence of Water (and the other
  elemental essences), Ironweb Spider Silk and Vulture Gizzard.
- **Mote of Unstable Magic** (ilvl 1, Miscellaneous/Other) is listed in only 36% of hours,
  but trades in big volume. The AH data doesn't show its source. Check Wowhead before planning
  around it.

---

## 3. Level-60 materials (item level 50+; herbs, ore, cloth, leather, elementals, enchanting, other)

For when the character hits 60. Same columns, filtered to `--min-level 50` and the material
subclasses.

| # | Item | ilvl | Subclass | Net | Vendor | Sold/d | Sure/d | **g/day** | Sure g/d | Qty / lots | Trend | Flags | Needs |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Rugged Leather | 50 | Leather | 18s 53c | 5s | 10,856 | 562 | **2,012** | 104 | 3,284 / 191 | +4% | | Skinning |
| 2 | Arcane Crystal | 60 | Other | 14g 56s | 20s | 113 | 24 | **1,644** | 350 | 118 / 49 | +41% | rising | Mining |
| 3 | Runecloth | 50 | Cloth | 5s 22c | 4s | 25,917 | 755 | **1,354** | 39 | 12,048 / 295 | −12% | | drop |
| 4 | Thorium Bar | 50 | Metal & Stone | 27s 03c | 6s | 4,530 | 895 | **1,224** | 242 | 2,338 / 54 | +2% | smelt | Mining |
| 5 | Essence of Water | 55 | Elemental | 3g 90s | 4s | 306 | 61 | **1,193** | 237 | 180 / 50 | +12% | | drop |
| 6 | Black Dragonscale | 55 | Leather | 1g 64s | 10s | 676 | 91 | **1,114** | 149 | 411 / 83 | −46% | oversupplied, falling | Skinning |
| 7 | Black Lotus | 60 | Herb | 7g 71s | 10s | 130 | 19 | **1,003** | 144 | 209 / 79 | −13% | | Herbalism |
| 8 | Greater Eternal Essence | 55 | Enchanting | 2g 50s | 1c | 365 | 82 | **915** | 206 | 282 / 47 | +32% | rising | Enchanting |
| 9 | Large Brilliant Shard | 55 | Enchanting | 2g 71s | 1c | 324 | 52 | **879** | 142 | 222 / 61 | +8% | | Enchanting |
| 10 | Devilsaur Leather | 50 | Leather | 66s 46c | 5s | 1,183 | 215 | **786** | 143 | 860 / 69 | −23% | falling | Skinning |
| 11 | Ironweb Spider Silk | 50 | Cloth | 54s 15c | 25s | 1,182 | 76 | **640** | 41 | 565 / 131 | +42% | rising | drop |
| 12 | Dreamfoil | 54 | Herb | 13s 70c | 1s | 4,440 | 219 | **608** | 30 | 2,659 / 228 | −6% | | Herbalism |
| 13 | Lesser Eternal Essence | 50 | Enchanting | 89s 54c | 1c | 619 | 85 | **554** | 76 | 490 / 76 | +19% | rising | Enchanting |
| 14 | Essence of Earth | 55 | Elemental | 4g 35s | 4s | 119 | 19 | **516** | 83 | 96 / 49 | 0% | | drop |
| 15 | Righteous Orb | 60 | Other | 9g 47s | 2g | 53 | 2 | **504** | 21 | 102 / 73 | −25% | oversupplied, falling | drop (Strat) |
| 16 | Gromsblood | 50 | Herb | 22s 78c | 2s 50c | 2,171 | 252 | **495** | 57 | 1,162 / 133 | +13% | | Herbalism |
| 17 | Essence of Air | 55 | Elemental | 3g 21s | 4s | 143 | 57 | **459** | 184 | 129 / 29 | −25% | oversupplied, falling | drop |
| 18 | Plaguebloom | 57 | Herb | 18s 05c | 2s 50c | 2,277 | 236 | **411** | 43 | 1,226 / 93 | −20% | falling | Herbalism |
| 19 | Dark Iron Bar | 50 | Metal & Stone | 2g 14s | 6s | 187 | 119 | **402** | 256 | 255 / 12 | −35% | falling, smelt | Mining |
| 20 | Dark Rune | 55 | Other | 1g 71s | 20s | 224 | 8 | **384** | 14 | 195 / 98 | −20% | oversupplied, falling | drop (Scholo/Strat) |
| 21 | Illusion Dust | 55 | Enchanting | 27s 53c | 1c | 1,392 | 271 | **383** | 75 | 1,415 / 107 | −8% | | Enchanting |
| 22 | Felcloth | 50 | Cloth | 56s 48c | 20s | 671 | 83 | **379** | 47 | 552 / 126 | −14% | oversupplied | drop |
| 23 | Stranglevine | 60 | Herb | 34s 14c | 2s 50c | 1,035 | 42 | **354** | 14 | 617 / 172 | −17% | falling | Herbalism |
| 24 | Dark Iron Ore | 50 | Metal & Stone | 13s 30c | 5s | 2,548 | 88 | **339** | 12 | 1,603 / 127 | −1% | oversupplied | Mining |
| 25 | Mountain Silversage | 56 | Herb | 11s 39c | 1s 50c | 2,933 | 367 | **334** | 42 | 2,087 / 151 | −3% | | Herbalism |

The "Needs" column is general game knowledge, not AH data; confirm drop sources on Wowhead.

**For a level-60 prot warrior with no gathering profession**, the realistic AH targets are:
- **Runecloth:** deep market, any quantity, but only ~1.2s over vendor.
- **Elemental essences:** Water, Earth and Air at 3–4g each, but only 100–300 sold a day.
- **Ironweb Spider Silk:** rising.
- **Felcloth:** oversupplied.
- **Righteous Orb / Dark Rune:** falling, and almost no certain sales.

Picking up **Mining** would open the strongest stable group: Thorium Ore and Bar, plus Arcane
Crystal as a bonus.

---

## 4. Avoid: oversupplied or falling (by g/day at stake)

| Item | ilvl | Net | Sold/d | Sure/d | g/day | Trend | Flags |
|---|---|---|---|---|---|---|---|
| Mote of Unstable Magic | 1 | 10s 45c | 10,714 | 2,271 | 1,120 | −15% | falling |
| Black Dragonscale | 55 | 1g 64s | 676 | 91 | 1,114 | **−46%** | oversupplied, falling |
| Mithril Bar | 40 | 10s 81c | 9,303 | 1,200 | 1,005 | +5% | oversupplied (sell the ore instead: 9s 52c with no smelting) |
| Devilsaur Leather | 50 | 66s 46c | 1,183 | 215 | 786 | −23% | falling |
| Dream Dust | 45 | 23s 51c | 3,100 | 470 | 729 | −16% | falling |
| **Righteous Orb** | 60 | 9g 47s | 53 | **2** | 504 | **−25%** | oversupplied, falling |
| Essence of Air | 55 | 3g 21s | 143 | 57 | 459 | −25% | oversupplied, falling |
| Plaguebloom | 57 | 18s 05c | 2,277 | 236 | 411 | −20% | falling |
| Dark Iron Bar | 50 | 2g 14s | 187 | 119 | 402 | −35% | falling |
| Dark Rune | 55 | 1g 71s | 224 | 8 | 384 | −20% | oversupplied, falling |
| Felcloth | 50 | 56s 48c | 671 | 83 | 379 | −14% | oversupplied |
| Stranglevine | 60 | 34s 14c | 1,035 | 42 | 354 | −17% | falling |
| **Powerful Mojo** | 55 | 1g 35s | 227 | 6 | 309 | **−27%** | falling |
| Golden Pearl | 40 | 1g 19s | 250 | 12 | 299 | +1% | oversupplied, and only 20s over vendor |
| Death Lotus | 60 | 8g 45s | 33 | 8 | 275 | **−49%** | oversupplied, falling |
| Giant Egg | 45 | 7s 25c | 3,620 | 135 | 262 | −34% | falling |
| Undeath Engine | 60 | 4g 00s | 64 | 4 | 255 | **−61%** | oversupplied, falling (vendor 2g 50s is the floor) |
| Heavy Thorium Ore | 60 | 24s 54c | 989 | 152 | 243 | +66% | oversupplied: qty is growing faster than the price |

Run `python3 scripts/farm_leaderboard.py --avoid --top 40` for the full list.

---

## 5. What this changes in the farming plan (README part 2)

Loot from the current farms, as it shows up on this board (same data, same date):

| Farm | Item | Net | Vendor | Sold/d | Sure/d | g/day | Trend | Verdict |
|---|---|---|---|---|---|---|---|---|
| Krol'dok (Ashka's wolves) | Thick Leather | 5s 80c | 3s 00c | 16,546 | 760 | 960 | 0% | AH. The market takes any quantity. |
| Krol'dok (wolves) | Heavy Leather | 1s 89c | 1s 50c | 26,157 | 771 | 495 | +2% | Marginal: 39c over vendor |
| Krol'dok (wolves) | Red Wolf Meat | 2s 58c | 87c | 8,394 | 105 | 217 | −4% | AH |
| Krol'dok, ZF | Mageweave Cloth | 4s 15c | 2s 50c | 23,224 | 833 | 963 | −1% | AH. Deep market. |
| Krol'dok | Flask of Mojo | 2s 50c | 2s 50c | 1,125 | 58 | 28 | 0% | **vendor** |
| Krol'dok | Flask of Big Mojo | 5s 56c | 5s 00c | 826 | 55 | 46 | 0% | vendor (11% over, not worth the deposit) |
| Krol'dok (rare) | Aquamarine | 11s 67c | 10s 00c | 535 | 12 | 62 | −1% | vendor-ish |
| Krol'dok (wolves) | Thick Furry Mane (grey) | 7s 97c | 8s 12c | 1 | 0 | 0 | — | **vendor** |
| Strat Living | **Righteous Orb** | 9g 47s | 2g 00s | 53 | **2** | 504 | **−25%** | oversupplied, falling: see below |
| Strat | Runecloth | 5s 22c | 4s 00c | 25,917 | 755 | 1,354 | −12% | AH. Takes any quantity. |
| Strat / L55 trolls | Powerful Mojo | 1g 35s | 20s | 227 | 6 | 309 | **−27%** | list a few, falling |
| Strat | Dark Rune | 1g 71s | 20s | 224 | 8 | 384 | −20% | list a few, falling |
| DME | Living Essence | 22s 80c | 5s | 551 | 68 | 126 | −23% | oversupplied, falling |
| Fishing | Raw Spotted Yellowtail | 35c | 4c | 7,495 | 738 | 26 | +26% | AH (confirms `findings-2026-11-22.md`) |

**Krol'dok Stronghold (now): no change.** The plan's ~41.5 g/h comes from bind-on-pickup blues
that you vendor, and vendor income has no demand cap. The trash loot all sells into very deep
markets (Thick Leather, Mageweave and Red Wolf Meat each sell thousands a day), so list
everything that isn't flagged "vendor". But a run yields only a handful of units at 2–6s, so
it adds pennies an hour. The Expert Campfire blueprint is a recipe, so it isn't on this board.
`kroldok-model-2026-11-23.md` still covers it: ~9 listed, sell one at a time.

**Zul'Farrak (backup): no change.** Mageweave nets 4s 15c against a 2s 50c vendor price, and
the market absorbs any amount. ZF's value is still coin and greys.

**Stratholme at 60: lower the Righteous Orb upside.** At 15 orbs an hour (the doc's ~3 orbs
per run × 5 runs), the demand cap at a 10% share lets **~0.2 orbs/h onto the AH**. Script
output for `--rate "Righteous Orb=15"`:
```
Righteous Orb   rate 15/h   AH 0.2/h   vendored 14.8/h   31.66 g/h   (uncapped: 142 g/h)
```
So plan on the **vendor-floor ~38 g/h** from `instance-loot-values-2026-11-23.md`, not on
AH orbs. On top of that:
- the orb market is falling (−25% over 6 days);
- it's oversupplied (posting outpaces sales);
- only ~2 a day are certain sales.

Sell a few orbs a day when the price is above ~9g; vendor the rest. Runecloth from the same
farm is a solid side income because its market takes any quantity.

**New idea at 60: elemental-essence farms with no profession.** Essence of Water (3g 90s,
~300/day, +12%) and Essence of Earth (4g 35s, ~120/day, steady) are the best kill-drop
markets at level 60. A 10% share caps them at about **5 g/h and 2 g/h** from the AH, so they
only pay as a bonus on a farm that already makes vendor gold, not as the main reason to farm.
Essence of Air is falling; avoid it.

**Profession question.** Mining would give the strongest stable markets: Thorium Ore and Bar
(~1,200–1,300 g/day each, flat) plus Arcane Crystal (14g 56s, rising). A Krol'dok run can't
compete with that, but gathering competes with dungeon time. Decide once there are measured
gathering rates.

---

## 6. Farm rates still needed (from in-game testing)

The demand cap only becomes a g/h number once you plug in a measured rate. Record these in
`docs/farm-log.md`, then run `--rate`:

| Item | Where | Why it matters |
|---|---|---|
| Thick Leather, Heavy Leather, Red Wolf Meat, Mageweave Cloth per Krol'dok run | Krol'dok trash | Small, but the only AH-sellable trash loot |
| Mageweave Cloth per hour | ZF graveyard | Second income stream there |
| Runecloth per hour and Righteous Orbs per run | Strat Living (at 60) | Confirms whether Strat beats Krol'dok |
| Essence of Water / Earth per hour | Level-55+ elemental camps (sources to be confirmed on Wowhead) | Best profession-free level-60 markets |
| Thorium Ore and Arcane Crystal per hour | Only if Mining is picked up | Strongest stable markets on the board |

Example once rates exist:
```sh
python3 scripts/farm_leaderboard.py --top 0 --rate "Runecloth=120" --rate "Righteous Orb=15" --rate "Essence of Water=6"
```
(`--top 0` skips the leaderboard and prints only the rate table. Add `--share 0.25` for an
optimistic case.)
