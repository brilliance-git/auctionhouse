# Dungeon farms for a solo Protection Warrior: every instance, re-evaluated (2026-11-23)

**Question:** of every instance in WoW: Forever today, which is the best solo gold farm for a
Protection Warrior, now (level 47) and at 60 in reasonable pre-raid gear?

**Short answer**
- **At 47: Krol'dok Stronghold, by a wide margin** (~52 g/h). It's the only farm here with real
  boss prices and drop rates. Everything else at 47 models at roughly 10–30 g/h.
- **At 60: no clear winner until something is timed in-game.** Stratholme Living (Scarlet
  side), Shaper's Terrace, Scholomance, Blackmaw Hold and Dire Maul East all model at
  ~45–85 g/h, and their order depends on how much level-60 BoP blues sell to a vendor for
  (unknown). **Krol'dok at 60 (~52 g/h) is the safe benchmark:** proven prices, trivial mobs.
  A level-60 farm is only worth switching to if a timed run beats it.

Reproduce with `python3 scripts/dungeon_farm_model.py` (add `--blue-scale 0.55` for the
conservative case). AH caps come from `python3 scripts/farm_leaderboard.py --rate ...`
(Horde AH, 152 snapshots, 17–23 Nov 2026, 10% market share).

> **Nothing here is measured in-game yet.** `docs/farm-log.md` is still empty. Every g/h is a
> model. "Medium" confidence means the loot side uses real prices and drop rates; "low" means
> boss values come from the item-level curve below.

---

## 1. Rules carried over
- **Normal pull-and-kill only.** No pathing, leash, ledge or reset tricks. Blizzard
  confiscated gold and suspended players over the Blackmaw Hold Devotee farm (Nov 16–17).
- **5 new instances per hour** (hotfix ~Nov 21; Wowhead). Any run up to 12 minutes, including
  the exit and reset, earns the same per hour as a faster one.
- **Horde AH only.** No Skinning. Mining unknown (it matters only for Shaper's Terrace).
- **All boss blues in these dungeons are bind-on-pickup**, so they're vendor income. That's
  confirmed for Krol'dok, Razorfen Kraul, Ruins of Lordaeron and SM; assumed for the rest.

## 2. Every instance in WoW: Forever (as of 2026-11-23)

**9 Forever dungeons** (Blizzard's level ranges; sources disagree on some):

| Dungeon | Levels | Where | Bosses | Notes |
|---|---|---|---|---|
| Hall of Thanes | 13–18 | under Ironforge | ? | Alliance-designed; Horde has no quests and must get through Ironforge. **Excluded.** |
| Ruins of Lordaeron | 15–20 | above Undercity | 6–7 | Horde counterpart; trash loop ~10 min |
| Excavation Site: Wetlands | 24–29 (or 26–31) | Wetlands | ? | Low-level loot, not modelled |
| City of Dalaran | 28–33 | Alterac Mountains | ? | Unlocked by a quest chain (Tarren Mill for Horde) |
| The Drowned City | 35–40 | off Stranglethorn coast | 6 | Zul'Alai, Var'Taka, Captain Dreadrise, Deathless Marrow, Gill, Min'loth |
| **Krol'dok Stronghold** | 40–45 | Riverglades | 6 (+ rare Kroog) | Detailed in `kroldok-model-2026-11-23.md` |
| Alcaz Prison | 48–53 | Dustwallow Marsh | 5 | Overseer Wrex, The Questioner, Tidemistress Ca'zass, Katerina the Cleaner, Zarla Ober (becomes the dragon Blazeroar) |
| Blackmaw Hold | 55–60 | Azshara | 7 (one source) | Devotee loot removed Nov 16 |
| Shaper's Terrace | 58–60 | Un'Goro Crater | 4–11 (sources differ) | Mount inside, teleport exit, 2 Rich Thorium Veins per reset |

Unreleased: Half-Pint Tavern and Manor Mistmantle exist in beta client files, with no release
date.

**Classic dungeons** (about 26 including wings; ~35 dungeons and wings in total): Ragefire
Chasm, Wailing Caverns, Deadmines, Shadowfang Keep, Blackfathom Deeps, Stockade (inside
Stormwind, so **excluded for Horde**), Gnomeregan, Razorfen Kraul, Scarlet Monastery
(Graveyard, Library, Armory, Cathedral), Razorfen Downs, Uldaman, Zul'Farrak, Maraudon, Sunken
Temple, Blackrock Depths, Lower and Upper Blackrock Spire, Dire Maul (East, West, North),
Scholomance, and Stratholme (Living and Undead).

- **Not modelled:** dungeons under level 30 (their blues sell for under ~40s), Sunken Temple
  (long and caster-heavy), and DM West and North (Tribute runs need special keys and routes;
  worth a separate look at 60).

**Raids:** Barrow Deeps (10-player), Hyjal Summit (20) and Onyxia's Lair (40) open on
**9 Dec 2026**. Molten Core, Zul'Gurub, BWL, AQ and Naxx have no date. None can be soloed by
a pre-raid prot warrior, so **all are excluded.** UBRS is also left out: it's a 10-player raid
instance.

## 3. Method

```
g/h = min(5, 60 / minutes per run) x (boss blues + trash coin + other vendor loot) + AH bonus
```

- **Boss blues: one BoP blue per boss kill.** Krol'dok's tables sum to 90–100% per boss.
  - **Krol'dok uses real numbers:** 8.31g per run from 19 real sell prices and drop rates.
  - **Every other dungeon uses a curve:** `blue(ilvl) = 1.24g × e^(0.071 × (ilvl − 45.5))`.
    - It's anchored on the mean real Krol'dok blue (1.24g at ilvl ~45.5).
    - The slope (+7% per item level) comes from the median vendor price of rare armor and
      weapons in `/v1/items`.
    - Checks against real prices: ilvl 24 gives 27s (Mirror of Rath'mael: real 18s); ilvl 32
      gives 48s (Thornspike: real 65s).

  | ilvl | 31 | 40 | 47 | 53 | 56 | 58 | 60 | 62 |
  |---|---|---|---|---|---|---|---|---|
  | blue (g) | 0.44 | 0.84 | 1.38 | 2.11 | 2.61 | 3.01 | **3.47** | 4.00 |

  - **The level-60 end is the weak point.** The catalog median at ilvl 60 is only **1.94g**.
    So every level-60 table below is shown twice: Krol'dok-anchored, and conservative
    (`--blue-scale 0.55`).
  - **Loot ilvl assumption:** Forever dungeons drop blues ~2 levels above the dungeon's top
    level, as Krol'dok does (ilvl 44–47 for a 40–45 dungeon).
- **Trash coin:** 0.09s × mob level per elite (~4s at 45, from the Krol'dok guide video's loot
  shares).
- **AH bonus:** `farm_leaderboard.py --rate "Item=units/h"` at a 10% share. Only the units the
  Horde AH absorbs count at AH price; the rest count at vendor price. This is why AH goods add
  little:

  | Drop | Units/h assumed | Demand-capped g/h |
  |---|---|---|
  | Righteous Orb | 15 | 31.7, of which **only ~0.2 orbs/h sell on the AH**; the rest is the 2g vendor price |
  | Runecloth | 40 | 2.1 |
  | Mageweave Cloth | 40 | 1.7 |
  | Silk Cloth | 60 | 1.1 |
  | Essence of Water | 5 | 5.2 |
  | Essence of Earth | 5 | 2.3 |
  | Thorium Ore (Mining only) | 40 | 5.8 |
  | Living Essence + Heart of the Wild | 30 | 1.7 |
  | Thick Leather (looted) | 15 | 0.9 |

- **Run time:** 12 minutes (the cap) unless noted. Runs are planned as chunks that fit the
  cap, so big dungeons count only the bosses one chunk can reach.

## 4. Level 47 (now)

| # | Farm | g/h (model) | Conservative | Main income | Soloability and risks | Confidence |
|---|---|---|---|---|---|---|
| 1 | **Krol'dok Stronghold** (full, Ogre Key shortcut) | **52** | 52 | 6 boss blues (8.31g/run, real) | Mobs 42–45. Risks: Terrorhowl's 60-yard fear (Ashka), Twilight Peons that run for help, caster cultists, Mortal Strike Centurions, Mugg's Mauls phase | **Medium** |
| 2 | The Drowned City (full) | 30 | 19 | 6 boss blues (ilvl ~40, assumed) | Trivial mobs (35–40); loot ilvl unconfirmed | Low |
| 3 | Zul'Farrak (graveyard + 2 bosses) | 27 | 21 | coin from ~60 zombies, Mageweave | **Risky at 47:** the graveyard event pulls dozens of level 43–44 elites | Low |
| 4 | Razorfen Downs (full) | 27 | 18 | 5 boss blues | Easy level; some quilboar casters | Low |
| 5 | Uldaman (3-boss chunk) | 23 | 15 | boss blues | Mostly melee troggs and dwarves; long, spread out | Low |
| 6 | SM Cathedral | 22 | 16 | 3 bosses, humanoid trash coin, Silk | Easy; Whitemane heals | Low |
| 7 | Maraudon (Orange or Purple wing) | 22 | 15 | 2 bosses | Mobs at your level, satyr casters | Low |
| 8 | City of Dalaran | 21 | 13 | boss blues (ilvl ~34) | Quest-locked; boss list unconfirmed | Low |
| 9 | Razorfen Kraul | 16 | 11 | 5 bosses (Thornspike 65s real) | Trivial | Medium |
| 10 | Ruins of Lordaeron | 14 | 10 | 7 low-ilvl blues, Fermenter blueprint | Trivial; Stone Watchers turn immune | Medium |
| 11 | SM Armory | 11 | 9 | Herod + trash | Trivial | Low |

**Verdict at 47:** stay on **Krol'dok**. Even if its run time comes in at 15 minutes (4 runs an
hour), it's still ~41 g/h, ahead of anything else in this band under either curve.

## 5. Level 60 (pre-raid gear)

| # | Farm | g/h (Krol'dok curve) | g/h (conservative) | Main income | Soloability and risks | Confidence |
|---|---|---|---|---|---|---|
| 1 | **Stratholme Living, Scarlet side** (12-min chunks + Galford) | 77 | **61** | **Righteous Orbs at the 2g vendor price** (~3.2/run), 2 boss blues, Runecloth | Many casters (Sorcerers, Battle Mages, Priests) give no rage. No documented prot-warrior solo | Low |
| 2 | Shaper's Terrace (4 bosses per run, teleport exit) | 85 | 49 | 4 boss blues (ilvl ~62); +5.8 g/h Thorium **only with Mining** | Mount inside and teleport out save time; boss count disputed (4–11); no solo boss data | Low |
| 3 | **Krol'dok Stronghold at 60** | 52 | **52** | 6 boss blues (real prices) | **Trivial at 60, very safe.** The benchmark | **Medium** |
| 4 | Scholomance (4-boss chunk) | 79 | 48 | boss blues, Runecloth | Caster-heavy (necromancers, Ras Frostwhisper), long | Low |
| 5 | Blackmaw Hold (4-boss chunk) | 77 | 46 | boss blues | 55–60 elites; Devotees drop nothing now. **Normal boss clears only** | Low |
| 6 | Dire Maul East (lashers + 4 bosses) | 72 | 45 | boss blues, Living Essence | **Best mob mix for prot:** non-elite, melee-only lashers. Alzzin and Lethtendris cast | Low |
| 7 | Stratholme Undead (3-boss chunk) | 62 | 39 | boss blues, Runecloth | Mostly melee undead; Maleki casts | Low |
| 8 | Alcaz Prison (full) | 62 | 38 | 5 boss blues (ilvl ~53) | Easy level at 60; Zarla Ober's dragon phase and Tidemistress (a caster) unknown solo | Low |
| 9 | Blackrock Depths (4-boss chunk) | 60 | 36 | boss blues | Huge; pick one wing | Low |
| 10 | LBRS (3-boss chunk) | 53 | 33 | boss blues | Orc packs, mostly melee | Low |
| 11 | Maraudon (Princess run) | 47 | 30 | boss blues, Essence of Earth | Easy at 60 | Low |
| 12 | Zul'Farrak at 60 | 41 | 29 | coin, Mageweave | Trivial | Medium |
| 13 | Uldaman at 60 | 39 | 24 | boss blues | Long | Low |

**Verdict at 60:**
- Under the conservative curve only **Strat Living** clearly beats Krol'dok, and only because
  orbs have a 2g vendor price. At a 10% share the AH takes only ~5 orbs a day (~0.2 an hour), so
  the **AH adds almost nothing.**
- Under the Krol'dok curve, five farms sit in the 72–85 g/h range.
- At 60, first measure **one timed run each** of Strat Living, Shaper's Terrace and DM East,
  and log them in `farm-log.md`. Until those come in, keep Krol'dok, which is safe and
  measurable.

## 6. Top 5

| Band | # | Farm | Est. g/h | Main income | Confidence |
|---|---|---|---|---|---|
| 47 | 1 | Krol'dok Stronghold | ~52 | BoP boss blues (vendor), real prices | Medium |
| 47 | 2 | The Drowned City | 19–30 | BoP boss blues | Low |
| 47 | 3 | Zul'Farrak (GY + 2 bosses) | 21–27 | trash coin, Mageweave | Low |
| 47 | 4 | Razorfen Downs | 18–27 | BoP boss blues | Low |
| 47 | 5 | Uldaman (chunk) | 15–23 | BoP boss blues | Low |
| 60 | 1 | Stratholme Living, Scarlet side | 61–77 | Righteous Orbs at vendor price, boss blues | Low |
| 60 | 2 | Shaper's Terrace | 49–85 | boss blues (+Thorium with Mining) | Low |
| 60 | 3 | Krol'dok Stronghold | ~52 | BoP boss blues, real prices | Medium |
| 60 | 4 | Scholomance (chunk) | 48–79 | boss blues, Runecloth | Low |
| 60 | 5 | Blackmaw Hold (chunk) | 46–77 | boss blues | Low |

DM East (45–72) sits just behind and has the best mob mix for a prot warrior.

## 7. What would move these numbers most
1. **Timed Krol'dok runs** (`farm-log.md`). They turn the only medium-confidence row into a
   measured one.
2. **Vendor prices of two or three level-60 BoP blues** from Strat, Shaper's Terrace or DME.
   They settle the 0.55–1.0 uncertainty that drives the whole level-60 table.
3. **Loot item levels for the Drowned City, Alcaz Prison and Shaper's Terrace.**
4. **Mining:** a yes adds ~5.8 g/h (demand-capped) to Shaper's Terrace.

## 8. Sources (all read 2026-11-23)
- Blizzard: [Explore the New Dungeons of WoW: Forever](https://news.blizzard.com/en-us/article/24301455/explore-the-new-dungeons-of-world-of-warcraft-forever)
- Wowhead: [Dungeons Overview (Forever)](https://www.wowhead.com/forever/guide/dungeons-overview-locations-details); [Maximum dungeons per hour reduced](https://www.wowhead.com/forever/news/maximum-dungeons-per-hour-reduced-in-wow-forever-hotfix-solo-gold-farming-nerf-383950)
- New dungeon lists and levels: [ConquestCapped](https://conquestcapped.com/guides/wow-forever/wow-forever-dungeons-overview/), [Mobalytics](https://mobalytics.gg/wow-forever/guides/wow-forever-dungeons-raids), [allthings.how](https://allthings.how/wow-forever-new-dungeons/), [space4games](https://space4games.com/en/games-en/wow-forever-dungeons/), [eloboost24](https://eloboost24.eu/blog/all-wow-forever-dungeons-by-level-every-dungeon-from-13-to-60-including-the-9-new-ones), [foreverchanges.pro](https://foreverchanges.pro/dungeons)
- Bosses: [Daybreak Forever: launch-day bosses](https://daybreakforever.com/blog/launch-day-dungeon-bosses), [lfcarry Alcaz Prison](https://lfcarry.com/guides/wow-forever-alcaz-prison), [wowforeverguides Shaper's Terrace](https://wowforeverguides.com/dungeons/the-shapers-terrace), [ConquestCapped Drowned City](https://conquestcapped.com/guides/wow-forever/wow-forever-the-drowned-city-guide/), [ConquestCapped Shaper's Terrace](https://conquestcapped.com/guides/wow-forever/wow-forever-shapers-terrace-guide/)
- Shaper's Terrace mining run: [Mobalytics rogue gold guide](https://mobalytics.gg/wow-forever/guides/rogue-gold-farming-guide)
- Raids: [Icy Veins raid preview](https://www.icy-veins.com/wow-forever/news/weekly-reset-attunement-locations-raid-sizes-official-wow-forever-raid-preview/), [Method](https://www.method.gg/wow-forever/wow-forever-raids-a-look-at-barrow-deeps-hyjal-summit-and-onyxias-lair)
- Level-60 farms: [Timesaver: best dungeons for gold at 60](https://timesaver.gg/blog/wow-forever-best-dungeons-for-gold), [ConquestCapped solo farming](https://conquestcapped.com/guides/wow-forever/wow-forever-solo-farming/)
- Earlier repo research: `research-prot-warrior-solo-farms-2026-11-23.md`, `kroldok-model-2026-11-23.md`, `farm-leaderboard-2026-11-23.md`
