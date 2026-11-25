# Uldaman, Zul'Farrak and Scarlet Monastery at 60, with real Wowhead Forever drop tables (2026-11-25)

**Input:** `docs/wowhead-drops-classic-3-2026-11-25.md` (wowhead.com/forever NPC "Drops" tabs):
full tables for Uldaman (10 bosses) and Zul'Farrak (13), and partial data for Scarlet Monastery
(Houndmaster Loksey and Interrogator Vishas only).

**Method:** same as `dire-maul-maraudon-real-drops-2026-11-25.md`.
- All 75 item IDs were checked on the **Horde AH**: ever listed means BoE (AH price), otherwise
  BoP (vendor value from the item-level curve).
- Boss greens are counted at the median vendor price: ilvl 41–47 0.52g, ilvl 30–40 0.27g.
- All three dungeons are **out-levelled at 60, so every loop is "reliable"**. The 5-per-hour
  instance cap applies.
- Reproduce with `python3 scripts/dungeon_farm_model.py`.

## Short answer
| Farm (at 60) | g/h (conservative / anchored) | Before | Data |
|---|---|---|---|
| *Krol'dok Stronghold (baseline)* | *50 / 50* | | real sell prices |
| *Dire Maul East (12 min, "maybe")* | *56 / 86* | | real tables |
| *Maraudon: Princess loop (12 min)* | *41 / 64* | | real tables |
| **Zul'Farrak: graveyard + pyramid loop (15 min)** | **39 / 55** | 29 / 41 | **real tables** |
| Zul'Farrak: Antu'sul + Theka + graveyard (12 min) | 29 / 39 | | real tables |
| **Uldaman: back-door loop with Archaedas (15 min)** | **23 / 37** | 20 / 32 | **real tables** |
| Uldaman: back-door loop (12 min) | 21 / 33 | 21 / 33 | real tables |
| SM Library: Loksey + Doan (10 min) | 13 / 16 | 12 / 16 | **partial** (Loksey real, Doan estimated) |
| SM Graveyard: Vishas + Thalnos (8 min) | 10 / 13 | 8 / 9 | **partial** (Vishas real, Thalnos estimated) |
| SM Cathedral, SM Armory | 21 / 28, 16 / 18 | unchanged | **not yet backed by real drops** |

- **Zul'Farrak is now the second-best "reliable" farm,** a close third behind Krol'dok (50) and
  the Maraudon Princess loop (41). It's ~11 g/h short of Krol'dok.
  - **Why it's up:** the 15-minute loop now reaches six real ~1-blue bosses (Zum'rah, Nekrum,
    Sezz'ziz, Bly, Ruuzlu, Ukorz) plus ~80 trash kills of coin.
- **Uldaman edges up** once Archaedas is in the loop, but stays a ~20–23 g/h farm.
- **Scarlet Monastery stays low.** Its ilvl 34–36 blues are worth little even at a steady
  ~1–1.3 per kill.
- **Nothing here beats Krol'dok or the DME loop.**

## 1. BoE check (Horde AH, 17–25 Nov 2026)
5 of 75 IDs have ever been listed. **Every boss blue in Uldaman, ZF and SM (Loksey, Vishas) is
BoP.**

| Item | Fill price | ~Listed | Source and rate | Counted as |
|---|---|---|---|---|
| Pattern: Skulker's Leather Shoes | 0.99g | 13 | Zerillis (rare) ~1% | negligible |
| Pattern: Skycaller's Mail Boots | 0.36g | 21 | Eric "The Swift" ~1% | negligible |
| Pattern: Frothing Cord | 0.28g | 19 | Dustwraith (rare) ~1% | negligible |
| Pattern: Radiant Cord | 0.19g | 12 | Sandarr Dunereaver (rare) 2% | negligible |
| Unearthed Bands | 4.2g | 8 | Olaf ~0% | negligible |

- **Never listed:** Plans: Prefect's Boots (Baelog 1%) and the quest or zone items: Archaedic
  Stone (Archaedas 94%; removed from his blue count), Gahz'rilla's Electrified Scale, Divino-matic
  Rod, Shattered Necklace parts, Heart of Zeal, Zum'rah's Head.
- **Small sellables counted:** Mageweave (Baelog 10%, ZF trash), Silk and Wool (SM), Smooth Stone
  Chip and Solid Stone (Obsidian Sentinel), Swiftness Potion (Eric 18%).

## 2. Boss data used (blues per kill, ilvl)
- **Uldaman:**
  - Archaedas 1.03 (ilvl 49, after removing the Archaedic Stone).
  - Ironaya 1.08 and Revelosh 1.03 (ilvl 42).
  - Galgann 1.08, Grimlok 1.04 and Ancient Stone Keeper 1.05 (ilvl 46–47).
  - Obsidian Sentinel 0.99 (ilvl 44).
  - The Lost Dwarves (Baelog 0.99, Olaf 0.92, Eric 0.92) are not on the loop.
- **Zul'Farrak:**
  - Chief Ukorz Sandscalp 1.14 (ilvl 50); Ruuzlu, Sezz'ziz and Sergeant Bly 1.03–1.04.
  - Theka 1.01, Antu'sul 1.00, Nekrum 0.99, Witch Doctor Zum'rah 0.94, Hydromancer Velratha 0.87
    (ilvl 47–50).
  - Gahz'rilla 1.02 needs the Mallet of Zul'Farrak, so he's not on the loop.
  - Rares (Sandarr, Zerillis, Dustwraith) are not counted.
- **Scarlet Monastery:** Houndmaster Loksey 1.27 (ilvl 36), Interrogator Vishas 1.04 (ilvl 34).
  - **Not yet backed by real drops:** Bloodmage Thalnos, Ironspine, Fallen Champion, Azshir the
    Sleepless, Arcanist Doan, Herod, Whitemane, Mograine, Scarlet Champion, Scarlet Centurion and
    Fairbanks.
  - Doan and Thalnos are estimated at 1 blue per kill (Forever's stated rule).
  - The Cathedral and Armory rows are unchanged estimates.

## 3. Loops
- **Zul'Farrak, graveyard + pyramid (15 min, 4 an hour):**
  1. Graveyard: Witch Doctor Zum'rah plus ~50 zombies.
  2. Pyramid stairs event: Nekrum Gutchewer, Shadowpriest Sezz'ziz, Sergeant Bly's crew.
  3. Ruuzlu, then Chief Ukorz Sandscalp.
  - **Beats the 12-minute variant** (Antu'sul > Theka > graveyard: 29 / 39). The pyramid adds
    four bosses for three extra minutes.
- **Uldaman, back door (15 min):** Ironaya > Obsidian Sentinel > Ancient Stone Keeper > Galgann
  > Grimlok > Archaedas (the order is assumed).
  - The 12-minute variant skips Obsidian Sentinel and Grimlok.
- **SM Library (10 min):** Loksey > Doan, with Silk.
- **SM Graveyard (8 min):** Vishas > Thalnos, with Wool. Short runs waste part of a lockout slot.
  Neither is worth it while Krol'dok is available.

## 4. Real vs estimated
| Part | Status |
|---|---|
| Blues and greens per kill, ilvls (Uldaman, ZF, Loksey, Vishas) | **real** (Wowhead Forever, 2026-11-25) |
| BoE vs BoP | **real** (Horde AH) |
| Vendor value of BoP blues | **estimated** (item-level curve) |
| Doan, Thalnos, SM Cathedral and Armory, RFD, RFK, City of Dalaran, Ruins of Lordaeron | **estimated, not yet backed by real drops** |
| Routes, minutes, trash counts | **estimated** |
