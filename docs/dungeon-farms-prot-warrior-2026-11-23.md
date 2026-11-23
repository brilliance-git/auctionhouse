# Dungeon farms for a solo Protection Warrior: every instance, re-evaluated (2026-11-23)

**Question:** of every instance in WoW: Forever today, which is the best solo gold farm for a
Protection Warrior, now (level 47) and at 60 in reasonable pre-raid gear?

**Short answer**
- **At 47: Krol'dok Stronghold, by a wide margin.** It makes ~50 g/h: **41.6 g/h from boss
  blues** (real sell prices and drop rates) plus **~8 g/h of trash coin** (an estimate from a
  guide video). Everything else at 47 models at 10–21 g/h on conservative numbers (up to ~30 on
  optimistic ones).
- **At 60: Krol'dok likely stays competitive; test Strat, Shaper's and DME to beat it.**
  - On conservative numbers only **Stratholme Living, Scarlet side (~62 g/h)** beats Krol'dok
    at 60 (~50 g/h), and only at low confidence. Most of Strat's value is Righteous Orbs at the
    2g vendor price.
  - Shaper's Terrace, Scholomance and Blackmaw Hold model at 47–50 g/h conservatively and
    77–85 g/h optimistically. Their order depends on how much level-60 BoP blues sell for,
    which is unknown.

Reproduce with `python3 scripts/dungeon_farm_model.py`. It prints both blue-value columns,
conservative first, plus the boss, trash and AH split. AH values are computed live from the
cached Horde AH snapshots (`data/`, 152 snapshots, 17–23 Nov 2026) with
`farm_leaderboard.py`'s demand cap at a 10% share.

> **Nothing here is measured in-game yet.** `docs/farm-log.md` is still empty. "Medium"
> confidence means the loot side uses real prices and drop rates; "low" means boss values come
> from the item-level curve below.

---

## 1. Rules carried over
- **Normal pull-and-kill only.** No pathing, leash, ledge or reset tricks. Blizzard
  confiscated gold and suspended players over the Blackmaw Hold Devotee farm (Nov 16–17).
- **5 new instances per hour** (hotfix ~Nov 21; Wowhead). Any run up to 12 minutes, including
  the exit and reset, earns the same per hour as a faster one.
- **Horde AH only.** No Skinning. **Mining unknown** (it matters for Shaper's Terrace).

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

**Not modelled; worth a look later:**
- **Dire Maul North tribute runs** (level 60).
  - **The route:** you skip or kill the guards, then kill only King Gordok. The tribute chest
    holds several items, possibly BoE (not checked).
  - **Solo prot fit: poor to uncertain.** The classic tribute run relies on stealth, Freezing
    Trap or invisibility to get past the guards (Guard Fengus, Slip'kik and Mol'dar). It also
    needs a Gordok Courtyard Key and an Ogre Tannin Basket. A prot warrior has to kill the
    guards instead, which is slower and makes the tribute smaller. Kill-everything tribute runs
    are possible but long.
  - Check Forever-specific changes before trying.
- **DM West.**
- **Sunken Temple:** long and caster-heavy.
- **Dungeons under level 30:** their blues sell for under ~40s.

**Raids:** Barrow Deeps (10-player), Hyjal Summit (20) and Onyxia's Lair (40) open on
**9 Dec 2026**. Molten Core, Zul'Gurub, BWL, AQ and Naxx have no date. None can be soloed by
a pre-raid prot warrior, so **all are excluded.** UBRS is also left out: it's a 10-player raid
instance.

## 3. Method

```
g/h = min(5, 60 / minutes per run) x (boss blues + trash coin + other vendor loot)
      + AH drops (demand-capped)
```

### Boss blues
- **The assumption: one BoP blue per boss kill.**
  - **Verified** (BoP from Wowhead tooltips, and Wowhead drop tables summing to ~90–100% per
    boss) only for Krol'dok, and BoP-only for Razorfen Kraul, Ruins of Lordaeron and SM.
  - **Assumed** for every other dungeon; see the `blues` column in the tables.
- **The error can go either way:**
  - **Down:** some classic bosses drop a green, or nothing, on part of their kills. That
    lowers the row.
  - **Up:** some classic dungeon blues are **BoE**, so they can sell on the Horde AH for more
    than a vendor pays. That raises the row.
- **Cheap BoP check (2026-11-23):** I looked up 32 known classic boss drops in the AH
  catalog, which lists every item ever seen on the Horde AH. Examples:
  - ZF: Jang'thraze, Sang'thraze, Zum'rah's Vexing Cane;
  - Razorfen Downs: Glutton's Cleaver, Coldrage Dagger;
  - Uldaman: The Rockpounder, Ironaya's Bracers;
  - Strat: Willey's Portable Howitzer, Hammer of the Grand Crusader;
  - Scholomance: Bone Ring Helm, Headmaster's Charge;
  - DME: Ring of Demonic Guile, Rod of the Ogre Magi;
  - Maraudon: Blackstone Ring, Gemshard Heart;
  - BRD: Ironfoe, Hand of Justice.

  **None has ever been listed.** That fits BoP, but it's weak evidence: Forever re-itemized
  some loot, so a name may have changed, or the item may simply not have dropped yet. No Forever
  boss loot names were checked for the Drowned City, Alcaz Prison, Blackmaw Hold or Shaper's
  Terrace.
- **Krol'dok: real data.** 19 sell prices and drop rates, worth 8.31g per run. Never scaled.
- **Every other dungeon: `blue(ilvl) = scale × 1.24g × e^(0.071 × (ilvl − 45.5))`.**
  - It's anchored on the mean real Krol'dok blue (1.24g at ilvl ~45.5).
  - The slope (+7% per item level) is the trend of the median vendor price of rare armor and
    weapons in `/v1/items`.
  - **Caveat:** `/v1/items` only holds items seen on the AH or used in recipes, so **the slope
    was fit on BoE blues, not on the BoP boss blues being modelled.**
  - **Two scales:**
    - **Conservative (default, shown first):** scale 0.56, which matches the catalog median at
      ilvl 60 (1.94g instead of 3.47g).
    - **Krol'dok-anchored:** scale 1.0.

  | ilvl | 31 | 40 | 47 | 53 | 56 | 58 | 60 | 62 |
  |---|---|---|---|---|---|---|---|---|
  | conservative (g) | 0.25 | 0.47 | 0.77 | 1.18 | 1.46 | 1.68 | **1.94** | 2.24 |
  | Krol'dok-anchored (g) | 0.44 | 0.84 | 1.38 | 2.11 | 2.61 | 3.01 | 3.47 | 4.00 |

  - **Checks against real prices:** ilvl 24 Mirror of Rath'mael (real 18s; conservative 15s,
    anchored 27s). ilvl 32 Thornspike (real 65s; conservative 27s, anchored 48s). So the
    conservative curve undershoots at low levels.
  - **Loot ilvl assumption:** Forever dungeons drop blues ~2 levels above the dungeon's top
    level, as Krol'dok does (ilvl 44–47 for a 40–45 dungeon).

### Trash coin
- **0.09s × mob level per elite kill** (~4s at 45). This comes from the loot shares in the
  Krol'dok guide video, so it's an estimate.
- **Non-elite mobs get 0.4× that** (roughly a third to a half). This applies to Dire Maul
  East's lashers.

### AH drops
- Each farm lists `Item=units/h`.
- `dungeon_farm_model.py` values them with `farm_leaderboard.capped_gph` on the cached `data/`
  at a 10% share. Only the units the Horde AH absorbs count at AH price; the rest count at
  vendor price.
- **If `data/` is missing,** dated fallback values from 2026-11-23 are used. They're in the
  script, with the command that produced them.

| Drop | Units/h assumed | Demand-capped g/h |
|---|---|---|
| Righteous Orb | 16 | 33.7, of which **only ~0.2 orbs/h sell on the AH**; the rest is the 2g vendor price |
| Runecloth | 40 | 2.1 |
| Mageweave Cloth | 40 | 1.7 |
| Silk Cloth | 60 | 1.1 |
| Essence of Earth | 5 | 2.3 |
| Living Essence + Heart of the Wild | 10 + 20 | 1.7 |
| Krol'dok wolf drops (Thick and Heavy Leather, Red Wolf Meat) | 5 each | 0.5 |
| Thorium Ore (Mining only, not in the totals) | 40 | 5.8 |

### Not counted anywhere
Grey vendor items and BoE greens from trash are **not** counted in any row. This understates
trash-heavy farms (SM mass pulls, ZF graveyard, Strat) more than boss-heavy ones.

### Run time
12 minutes (the cap) unless noted. Big dungeons are planned as chunks that fit the cap, so they
only count the bosses one chunk can reach.

## 4. Level 47 (now)

| # | Farm | Conservative g/h | Anchored g/h | Split (boss + trash + AH) | Blues | Soloability and risks | Confidence |
|---|---|---|---|---|---|---|---|
| 1 | **Krol'dok Stronghold** (full, Ogre Key shortcut) | **50** | 50 | **41.6 boss (real prices) + ~7.9 trash (estimate)** + 0.5 | verified | Mobs 42–45. Risks: Terrorhowl's 60-yard fear (Ashka), Twilight Peons that run for help, caster cultists, Mortal Strike Centurions, Mugg's Mauls phase | **Medium** |
| 2 | Zul'Farrak (graveyard + 2 bosses) | 21 | 27 | 7.7 + 11.9 + 1.7 | assumed | **Risky at 47:** the graveyard event pulls dozens of level 43–44 elites | Low |
| 3 | The Drowned City (full) | 19 | 30 | 14.1 + 5.1 | assumed | Trivial mobs (35–40); loot ilvl unconfirmed | Low |
| 4 | Razorfen Downs (full) | 18 | 27 | 11.7 + 6.0 | assumed | Easy level; some quilboar casters | Low |
| 5 | SM Cathedral | 16 | 22 | 8.1 + 6.8 + 1.1 | verified | Easy; Whitemane heals | Low |
| 6 | Uldaman (3-boss chunk) | 15 | 23 | 9.3 + 5.9 | assumed | Mostly melee; long, spread out | Low |
| 7 | Maraudon (Orange or Purple wing) | 15 | 22 | 8.9 + 6.3 | assumed | Mobs at your level, satyr casters | Low |
| 8 | City of Dalaran | 13 | 21 | 9.2 + 4.2 | assumed | Quest-locked; boss list unconfirmed | Low |
| 9 | Razorfen Kraul | 11 | 16 | 6.2 + 4.5 | verified | Trivial | Medium |
| 10 | Ruins of Lordaeron | 10 | 14 | 5.3 + 2.4 + 2.0 (Fermenter) | verified | Trivial; Stone Watchers turn immune | Medium |
| 11 | SM Armory | 9 | 11 | 2.3 + 6.8 | verified | Trivial | Low |

**Verdict at 47:** stay on **Krol'dok**. Its boss income alone (41.6 g/h from real prices) is
about twice the best alternative's total. If runs come in at 15 minutes (4 an hour), it still
makes ~40 g/h.

## 5. Level 60 (pre-raid gear)

| # | Farm | Conservative g/h | Anchored g/h | Split (conservative: boss + trash + AH) | Blues | Soloability and risks | Confidence |
|---|---|---|---|---|---|---|---|
| 1 | **Stratholme Living, Scarlet side** (12-min chunks + Galford) | **62** | 77 | 19.4 + 6.5 + **35.7 (orbs, mostly at vendor price; Runecloth)** | assumed | Many casters (Sorcerers, Battle Mages, Priests) give no rage. No documented prot-warrior solo | Low |
| 2 | Shaper's Terrace (4 bosses per run, teleport exit) | 50 | 85 | 44.7 + 5.3 (+5.8 with Mining) | assumed | Mount inside and teleport out save time; boss count disputed (4–11); no solo boss data | Low |
| 3 | **Krol'dok Stronghold at 60** | **50** | 50 | **41.6 (real) + ~7.9 (estimate)** + 0.5 | verified | **Trivial at 60, very safe.** The benchmark | **Medium** |
| 4 | Scholomance (4-boss chunk) | 49 | 79 | 38.8 + 8.0 + 2.1 | assumed | Caster-heavy (necromancers, Ras Frostwhisper), long | Low |
| 5 | Blackmaw Hold (4-boss chunk) | 47 | 77 | 38.8 + 7.8 | assumed | 55–60 elites; Devotees drop nothing now. **Normal boss clears only** | Low |
| 6 | Dire Maul East (lashers + 4 bosses) | 39 | 66 | 33.7 + 3.9 (non-elite) + 1.7 | assumed | **Best mob mix for prot:** non-elite, melee-only lashers. Alzzin and Lethtendris cast | Low |
| 7 | Stratholme Undead (3-boss chunk) | 39 | 62 | 29.1 + 7.8 + 2.1 | assumed | Mostly melee undead; Maleki casts | Low |
| 8 | Alcaz Prison (full) | 39 | 62 | 29.5 + 9.2 | assumed | Easy level at 60; Zarla Ober's dragon phase and Tidemistress (a caster) unknown solo | Low |
| 9 | Blackrock Depths (4-boss chunk) | 37 | 60 | 29.2 + 7.3 | assumed | Huge; pick one wing | Low |
| 10 | LBRS (3-boss chunk) | 33 | 53 | 25.3 + 7.7 | assumed | Orc packs, mostly melee | Low |
| 11 | Maraudon (Princess run) | 30 | 47 | 22.0 + 5.6 + 2.3 | assumed | Easy at 60 | Low |
| 12 | Zul'Farrak at 60 | 29 | 41 | 15.4 + 11.9 + 1.7 | assumed | Trivial | Medium |
| 13 | Uldaman at 60 | 25 | 39 | 18.7 + 5.9 | assumed | Long | Low |
| 14 | SM Cathedral at 60 (mass pull, 3 bosses) | 21 | 28 | 8.1 + 10.3 + 2.9 (Silk, Mageweave) | verified | Whole-wing pulls of level 34–40 humanoid elites; looting ~60 corpses is the time limit | Low |
| 15 | SM Armory at 60 (full clear + Herod) | 16 | 18 | 2.3 + 11.1 + 2.9 | verified | Same; only one boss | Low |
| 16 | SM Library at 60 | 12 | 16 | 4.1 + 6.5 + 1.9 | verified | Fewer mobs | Low |
| 17 | SM Graveyard at 60 | 8 | 9 | 1.4 + 5.6 + 1.0 (Wool) | verified | Low-level undead, little coin | Low |

### Scarlet Monastery at 60: mass pulls
- **The style:** gather a whole wing's humanoid packs, tank them together and kill them with
  AoE. This is normal pull-and-kill; no leash, reset or pathing tricks. In the Cathedral,
  aggroing Scarlet Commander Mograine reportedly pulls everything in the chapel
  ([almarsguides](https://almarsguides.com/wow/farming/60below/silk/SMCathedral.cfm)).
- **Kills per run (estimates; no source gives counts):**
  - Cathedral: ~60 elites (courtyard ~25 + chapel ~35) + Fairbanks, Mograine and Whitemane.
  - Armory: ~65 elites + Herod.
- **Coin:** the elite rate at mob level ~38 (~3.4s per kill).
- **Cloth:** Silk drops on about 1 in 2–3 kills (~125 an hour) and Mageweave ~5% (~15 an
  hour). The Horde AH absorbs all of it at a 10% share, but it's worth only ~2.3 + 0.6 g/h.
- **Using the cap:** a full Armory clear including all trash fits in ~12 minutes, so it uses a
  slot properly. Herod alone (~8 minutes) would waste a third of the slot. **Cathedral is the
  better use of a slot**: it has 3 bosses instead of 1 and a similar trash count.
- **Graveyard and Library are clearly worse:**
  - Graveyard (~8 g/h): low-level undead and Wool.
  - Library (~12 g/h): fewer mobs, and its 2 bosses are low ilvl.
- **Verdict: SM at 60 does not beat Krol'dok at 60.** On modelled income, the Cathedral makes
  ~21–28 g/h against Krol'dok's ~50. Its boss blues are ilvl ~40 (~0.5–0.8g each), and trash
  coin from level-38 mobs can't make up the gap.
- **The unmodelled part:** this model counts no grey items and no BoE greens from trash, for
  any farm. That matters most for trash-heavy farms like SM.
  - Classic-era mage guides report 60–80 g/h for level-60 Cathedral farming
    ([Icy Veins mage guide](https://www.icy-veins.com/wow-classic/classic-mage-goldmaking-guide-the-best-ways-to-make-gold)).
    That's a different economy and class, and it includes greens and greys.
  - One timed Cathedral run, gold before and after with greys sold, would settle it. If
    greens and greys add ~30 g/h, the Cathedral would rival Krol'dok, but nothing here shows
    that yet.

**Verdict at 60: Krol'dok likely stays competitive; test Strat, Shaper's and DME to beat it.**
- **Conservative numbers:** only Strat Living (~62) beats Krol'dok (~50), at low confidence.
  Its edge is Righteous Orbs at the 2g vendor price; at a 10% share the AH takes only ~0.2
  orbs an hour.
- **Optimistic numbers** (Krol'dok-anchored blues): Shaper's Terrace, Scholomance and Blackmaw
  Hold reach 77–85 g/h.
- **The plan:** at 60, time one run each of Strat Living, Shaper's Terrace and DME, log them in
  `farm-log.md`, and switch only if one beats Krol'dok's measured g/h.

## 6. Top 5 (conservative g/h first)

| Band | # | Farm | Est. g/h (conservative / anchored) | Main income | Confidence |
|---|---|---|---|---|---|
| 47 | 1 | Krol'dok Stronghold | **50** (41.6 boss, real + ~8 trash, estimate) | BoP boss blues | Medium |
| 47 | 2 | Zul'Farrak (GY + 2 bosses) | 21 / 27 | trash coin, Mageweave | Low |
| 47 | 3 | The Drowned City | 19 / 30 | BoP boss blues | Low |
| 47 | 4 | Razorfen Downs | 18 / 27 | BoP boss blues | Low |
| 47 | 5 | SM Cathedral | 16 / 22 | boss blues, coin, Silk | Low |
| 60 | 1 | Stratholme Living, Scarlet side | 62 / 77 | Righteous Orbs at vendor price, boss blues | Low |
| 60 | 2 | Shaper's Terrace | 50 / 85 | boss blues (+Thorium with Mining) | Low |
| 60 | 3 | Krol'dok Stronghold | **50** (41.6 real + ~8 estimate) | BoP boss blues | Medium |
| 60 | 4 | Scholomance (chunk) | 49 / 79 | boss blues, Runecloth | Low |
| 60 | 5 | Blackmaw Hold (chunk) | 47 / 77 | boss blues | Low |

## 7. Open questions (what would move these numbers most)
1. **Timed Krol'dok runs** (`farm-log.md`). They turn the only medium-confidence row into a
   measured one, including the ~8 g/h trash estimate.
2. **Vendor prices of two or three level-60 BoP blues** from Strat, Shaper's Terrace or DME.
   They settle the 0.56–1.0 scale that drives the whole level-60 table.
3. **Will the character take Mining?** It decides Shaper's Terrace's upside: ~5.8 g/h of
   Thorium on top (demand-capped), and the reason that farm exists for most players.
4. **Bind type and blue rate of boss loot** in the Drowned City, Alcaz Prison, Blackmaw Hold
   and Shaper's Terrace, plus their loot item levels.

## 8. Sources (all read 2026-11-23)
- Blizzard: [Explore the New Dungeons of WoW: Forever](https://news.blizzard.com/en-us/article/24301455/explore-the-new-dungeons-of-world-of-warcraft-forever)
- Wowhead: [Dungeons Overview (Forever)](https://www.wowhead.com/forever/guide/dungeons-overview-locations-details); [Maximum dungeons per hour reduced](https://www.wowhead.com/forever/news/maximum-dungeons-per-hour-reduced-in-wow-forever-hotfix-solo-gold-farming-nerf-383950)
- New dungeon lists and levels: [ConquestCapped](https://conquestcapped.com/guides/wow-forever/wow-forever-dungeons-overview/), [Mobalytics](https://mobalytics.gg/wow-forever/guides/wow-forever-dungeons-raids), [allthings.how](https://allthings.how/wow-forever-new-dungeons/), [space4games](https://space4games.com/en/games-en/wow-forever-dungeons/), [eloboost24](https://eloboost24.eu/blog/all-wow-forever-dungeons-by-level-every-dungeon-from-13-to-60-including-the-9-new-ones), [foreverchanges.pro](https://foreverchanges.pro/dungeons)
- Bosses: [Daybreak Forever: launch-day bosses](https://daybreakforever.com/blog/launch-day-dungeon-bosses), [lfcarry Alcaz Prison](https://lfcarry.com/guides/wow-forever-alcaz-prison), [wowforeverguides Shaper's Terrace](https://wowforeverguides.com/dungeons/the-shapers-terrace), [ConquestCapped Drowned City](https://conquestcapped.com/guides/wow-forever/wow-forever-the-drowned-city-guide/), [ConquestCapped Shaper's Terrace](https://conquestcapped.com/guides/wow-forever/wow-forever-shapers-terrace-guide/)
- Shaper's Terrace mining run: [Mobalytics rogue gold guide](https://mobalytics.gg/wow-forever/guides/rogue-gold-farming-guide)
- Raids: [Icy Veins raid preview](https://www.icy-veins.com/wow-forever/news/weekly-reset-attunement-locations-raid-sizes-official-wow-forever-raid-preview/), [Method](https://www.method.gg/wow-forever/wow-forever-raids-a-look-at-barrow-deeps-hyjal-summit-and-onyxias-lair)
- Level-60 farms: [Timesaver: best dungeons for gold at 60](https://timesaver.gg/blog/wow-forever-best-dungeons-for-gold), [ConquestCapped solo farming](https://conquestcapped.com/guides/wow-forever/wow-forever-solo-farming/)
- DM North tribute (classic mechanics, not checked for Forever): general Classic knowledge; verify before trying.
- Earlier repo research: `research-prot-warrior-solo-farms-2026-11-23.md`, `kroldok-model-2026-11-23.md`, `farm-leaderboard-2026-11-23.md`
