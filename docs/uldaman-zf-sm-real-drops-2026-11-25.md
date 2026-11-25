# Uldaman, Zul'Farrak, Scarlet Monastery, Razorfen Downs and Razorfen Kraul at 60, with real Wowhead Forever drop tables (2026-11-25)

> **Update (same day):** `wowhead-drops-classic-4-2026-11-25.md` completes Scarlet Monastery and adds Razorfen Downs and 7 of 8 Razorfen Kraul bosses. See section 5; the SM rows in the table below are superseded there.

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
| SM Library: Loksey + Doan (10 min) | 14 / 17 | 12 / 16 | real tables (see section 5) |
| SM Graveyard: Vishas + Thalnos (8 min) | 11 / 13 | 8 / 9 | real tables (see section 5) |
| SM Cathedral mass pull, SM Armory full clear (12 min) | 26 / 33, 17 / 19 | 21 / 28, 16 / 18 | real tables (see section 5) |

- **Zul'Farrak is now the third-best "reliable" farm,** just behind Krol'dok (50) and the
  Maraudon Princess loop (41). It's ~11 g/h short of Krol'dok.
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
| City of Dalaran | **estimated: Wowhead has no data for it** (everything else in this doc is real, see sections 5 and 6) |
| Routes, minutes, trash counts | **estimated** |

## 5. Update: all of Scarlet Monastery, Razorfen Downs and Razorfen Kraul
Source: `docs/wowhead-drops-classic-4-2026-11-25.md`. It has the other 11 SM mobs, all 6 RFD
bosses, and 7 of 8 RFK bosses (Roogug missing). All are out-levelled at 60, so every loop is
"reliable".

**BoE check:** 6 of 71 IDs have ever been listed on the Horde AH, all from Cathedral trash.
**Every boss blue in SM, RFD and RFK is BoP.**

| Item | Fill price | ~Listed | Source and rate | Counted as |
|---|---|---|---|---|
| **Scarlet Chestpiece** | ~35g | 6 | Scarlet Champion 1% | vendor 0.70g (thin market; ~1 every 1.5 h on the Cathedral loop is upside) |
| Scarlet Gauntlets | ~5.8g | 18 | Scarlet Centurion 4% | vendor 0.27g (upside ~5.5g each) |
| Mark of Kern / Cobalt Crusher | ~10g / ~5.6g | 4–7 | Centurion / Champion ~0% | negligible |
| Sealed Expert's Writ | ~31s | ~490 | Centurion / Champion 1% | counted |
| Pattern: Filigreed Pristine Circlet | ~0.3g | 21 | Earthcaller Halmgar (rare) 1% | negligible |

Quest items aren't in any blue count: Skull of the Coldbringer (Amnennar 33%), Razorflank's
Heart (Charlga 40%), Small Scroll. None has ever been listed.

**Boss data (blues per kill, ilvl):**
- **SM:**
  - Herod 1.19 (42); Fairbanks 1.09 (42); Mograine 1.08 (44); Whitemane 1.07 (44).
  - Doan 0.99 (39, with 98% greens); Thalnos 1.07 (36).
  - Graveyard rares: Ironspine 1.10, Fallen Champion 1.08, Azshir 1.06 (35). Not counted; they
    don't spawn every run.
- **RFD:** **Amnennar 1.81** (43); Mordresh 1.09, Plaguemaw 1.08, Glutton 1.08, Tuten'kash 1.07
  (41–42); Ragglesnout (rare) 1.06.
- **RFK:**
  - Aggem 1.07; Jargba 1.06; Ramtusk 1.06; Agathelos 1.05; Charlga 1.01 (ilvl 31–35).
  - Blind Hunter 1.03 and Earthcaller Halmgar 1.02 are rares, not counted.
  - Roogug: 1.04 blues per kill (ilvl 30), added in section 6.

**Results at 60 (conservative / anchored g/h):**

| Farm | Now | Before | Data |
|---|---|---|---|
| *Krol'dok Stronghold (baseline)* | *50 / 50* | | real sell prices |
| *Dire Maul East (12 min, "maybe")* | *56 / 86* | | real tables |
| *Maraudon: Princess loop (12 min)* | *41 / 64* | | real tables |
| *Zul'Farrak: graveyard + pyramid (15 min)* | *39 / 55* | | real tables |
| **SM Cathedral: mass pull (12 min)** | **26 / 33** | 21 / 28 | real tables |
| **Razorfen Downs: full clear (12 min)** | **24 / 37** | 18 / 27 | real tables |
| SM Armory: full clear + Herod (12 min) | 17 / 19 | 16 / 18 | real tables |
| Razorfen Kraul: full clear (10 min) | 14 / 21 | 11 / 16 | real tables (Roogug added, section 6) |
| SM Library: Loksey + Doan (10 min) | 14 / 17 | 13 / 16 (partial) | real tables |
| SM Graveyard: Vishas + Thalnos (8 min) | 11 / 13 | 10 / 13 (partial) | real tables |

**Routes:**
- **SM Cathedral:** courtyard pull, then the chapel pull (aggroing Mograine pulls the chapel),
  then Mograine > Whitemane > Fairbanks.
- **RFD:** Tuten'kash (gong) > Mordresh Fire Eye > Glutton > Plaguemaw > Amnennar.
- **RFK:** Roogug > Aggem > Jargba > Ramtusk > Agathelos > Charlga.

**Verdict:**
- **Nothing here comes close to Krol'dok (~50), DME (~56), Maraudon Princess (~41) or the ZF
  loop (~39).**
- The best of this group are the **SM Cathedral mass pull (~26)** and **RFD's full clear
  (~24)**.
- The Cathedral has the one real upside: its Scarlet Chestpiece and Scarlet Gauntlets drops are
  BoE and sell for ~35g and ~5.8g on the AH, if those thin markets take them.
- RFK, SM Library and SM Graveyard (11–14) aren't worth a lockout slot while Krol'dok is
  available.
- **Still not backed by real drops:** City of Dalaran only (see section 6).

## 6. Update: Roogug and Ruins of Lordaeron
Source: `docs/wowhead-drops-classic-5-2026-11-25.md`.
- **Razorfen Kraul is now fully real-data.** Roogug drops 1.04 blues per kill (ilvl 30).
- **Ruins of Lordaeron has all 6 bosses:** 0.92–1.00 blues per kill at ilvl 20–24, with
  6,000–7,700 kills sampled each.

**BoE check:** none of the 21 IDs (Roogug's 2741xx items and the Ruins' 2712xx items) has ever
been listed on the Horde AH, so **all are BoP**, at vendor value.
- **Not counted (quest items, never listed):** Highly Toxic Strain (Witherfang 26%), Abominable
  Head (The Baron 36%), Head of the Baron (18%).
- **Counted:** Rath'mael's Blueprint: Fermenter (7%) sells for ~6.6g on the AH, ~0.44g per kill.

**City of Dalaran has no data on Wowhead.** Its zone page (16560) has no NPC list and no drops
list, only quests and guides, so it can't be backed by real drops. It stays on estimates.

**Results at 60 (conservative / anchored g/h, all "reliable"):**

| Farm | Now | Before | Data |
|---|---|---|---|
| *Krol'dok Stronghold (baseline)* | *50 / 50* | | real sell prices |
| *Dire Maul East (12 min, "maybe")* | *56 / 86* | | real tables |
| *Maraudon: Princess loop (12 min)* | *41 / 64* | | real tables |
| *Zul'Farrak: graveyard + pyramid (15 min)* | *39 / 55* | | real tables |
| *SM Cathedral: mass pull (12 min)* | *26 / 33* | | real tables |
| *Razorfen Downs: full clear (12 min)* | *24 / 37* | | real tables |
| **Razorfen Kraul: full clear (10 min)** | **14 / 21** | 14 / 22 (Roogug estimated) | **real tables** |
| City of Dalaran: full clear (10 min) | 13 / 21 | unchanged | **estimated (no Wowhead data)** |
| **Ruins of Lordaeron: full clear (8 min)** | **8 / 11** | 10 / 14 (7 bosses estimated) | **real tables** |

- **Ruins route:** Witherfang > The Baron > The Abandoned > Bjork > Viktor the Vile >
  Rath'mael (order assumed). It's 6 bosses, not the 7 the estimate assumed, and their ilvl 20–24
  blues sell for a few silver.
- **Verdict:** neither comes close to the farms above, and neither is worth a lockout slot while
  Krol'dok is available. Every farm in the model is now backed by real drop data **except City of
  Dalaran**.

