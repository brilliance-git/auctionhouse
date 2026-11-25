# Five Classic dungeons re-modelled with real Wowhead Forever drop tables (2026-11-25)

> **Update (2026-11-25):** later docs replaced this one's estimates for the other dungeons. Dire Maul East is ~56 / 86 g/h from real drop tables (`dire-maul-maraudon-real-drops-2026-11-25.md`), and Maraudon, Uldaman, ZF, SM, RFD, RFK and Ruins of Lordaeron are real too (`uldaman-zf-sm-real-drops-2026-11-25.md`). Only City of Dalaran is still estimated, because Wowhead has no data for it. The DME figures below (~40) are as first written.

**Input:** `docs/wowhead-drops-classic-2026-11-25.md`, collected from wowhead.com/forever NPC
"Drops" tabs. It covers Sunken Temple, LBRS, BRD, Scholomance and Stratholme (21 of 22 mobs).
Dire Maul, Maraudon, Uldaman, ZF, RFD, SM, RFK, City of Dalaran and Ruins of Lordaeron aren't
in it, so they're still estimates.

**Method (as in `forever-dungeons-real-drops-2026-11-25.md`):**
- I looked up all 269 item IDs on the **Horde AH**.
- **Ever listed means BoE:** valued at the AH fill price after the 5% cut.
- **Never listed means BoP:** vendor value from the item-level curve, since the API has no
  vendor price for never-listed items.
- Real blues per kill and item levels replace the estimates in the loops for these five
  dungeons (`real-rate` in `python3 scripts/dungeon_farm_model.py`).

## Short answer
- **Does anything now beat Krol'dok (~50 g/h)? Yes, on paper, but only farms rated
  "unlikely" solo:**

  | Loop | g/h (conservative / anchored) |
  |---|---|
  | **Stratholme Undead: ziggurats + Ramstein (15 min)** | **105** / 135 |
  | **Stratholme Living: Willey + Galford (15 min)** | **103** / 130 |
  | Lower Blackrock Spire: front loop (12 min) | 77 / 96 |
  | Stratholme Undead: side gate (15 min) | 75 / 105 |
  | Scholomance: Rattlegore + Jandice + Ras (15 min) | 58 / 83 |

  The jump comes from **boss greens** (many Strat and Scholomance bosses drop 0.9–2.4 greens
  per kill, valued here at the vendor floor) and **BoE dungeon-set pieces** (Gauntlets of
  Valor ~45g, Shadowcraft Gloves ~27g, Devout Gloves ~26g). All are level 57–62 elite caster
  content with no documented prot-warrior solo.
- **Krol'dok (~50, real sell prices) is still the best farm you can count on** at 60. **Strat is now clearly the prize to test** at 60, or with raid gear after 9 Dec.
- **"Reliable" and "maybe" loops that changed:**
  - **Sunken Temple falls from ~41 to ~20 g/h.** The six balcony troll minibosses are **not in
    Wowhead's list of mobs that drop a blue**, so they drop none. The loop's real value is
    Jammal'an and Ogom (~1 blue each) plus Spawn of Hakkar. It's no longer the best "maybe";
    **Dire Maul East (~40, still estimated) is.**
  - **Blackrock Depths' entrance loop stays at ~34 g/h** with real data (Roccor's 1.86 "blues"
    are mostly Rockshard Pellets ammo).
  - Every other reliable or maybe loop is in dungeons without data, so unchanged.

## 1. Checks
| Claim | Result |
|---|---|
| Final bosses drop 2–3 blues | **Confirmed:** Drakkisath 2.96, Willey 2.65, Rivendare 2.62, The Beast 2.04, Thaurissan 2.01, Dathrohan 1.97, Gandling 1.91, Shade of Hakkar 1.91, Kirtonos 1.90, Grizzle 1.93, Ras 1.86, Roccor 1.86, Shade of Eranikus 1.74 |
| …but some of those "blues" are ammo or recipes | **Willey:** 0.86 is Miniature Cannon Balls. **Roccor:** 0.87 is Rockshard Pellets. **Vosh'gajin:** 0.86 is Doomshot. **Grizzle:** 0.96 is Plans: Dark Iron Pulverizer. Removed from the gear-blue count (ammo is worth ~0) |
| Many Strat and Scholomance bosses drop lots of greens | **Confirmed:** Ramstein 244%, Ras 184%, Anastari 181%, Jandice 176%, Ezra Grimm 178%, Barthilas 175%; most others 85–97% |
| Sunken Temple balcony trolls | **Not in the list, so no blues.** The earlier "6 guaranteed blues" troll loop is corrected |

## 2. BoE items found (ever listed on the Horde AH, 17–25 Nov 2026)
25 of the 269 IDs have been listed. Fill price, about how many are listed at a time, and the
source:

| Item | Fill price | ~Listed | Source and rate | Counted as |
|---|---|---|---|---|
| **Gauntlets of Valor** | 45.0g | 12 | Ramstein 15% | AH ×0.95: **6.4g per kill** |
| **Shadowcraft Gloves** | 27.0g | 16 | Vosh'gajin 17% | AH: **4.4g per kill** |
| **Devout Gloves** | 25.6g | 14 | Galford 19% | AH: **4.6g per kill** |
| Bindings of Elements | 35.0g | 17 | Crypt Beast (trash) 5% | not counted (trash) |
| Cord of Elements / Magister's Bindings | 13.5g / 6.4g | 21 / 28 | Firebrand trash 2–3% | in the LBRS Pyromancer value |
| Piccolo of the Flaming Fire | 5.0g | 8 | Forresten 19% | not on a modelled route |
| Dreadmist Bracers | 4.9g | 28 | Zigris 11% | in Zigris's value |
| Shadowcraft Belt, Wildheart Belt, Magister's Belt | 3.3–6.4g | 22–50 | trash 3–8% | not counted |
| **Pattern: Robe of the Archmage** | 26.0g | 15 | **Firebrand Pyromancer 19%** | vendor price 1.50g (~1 an hour is more than the market takes); AH sale is upside |
| **Formula: Enchant Weapon - Lifestealing** | 50.0g | 6 | Spectral Researcher 1.6% | not counted (trash, thin market) |
| Pattern: Pristine Scorpid Leggings | 101g | 5 | Spectral Researcher 4% | not counted (trash, thin market) |
| Pattern: Black Dragonscale Helm / Shoulders / Leggings | 75.5g / 5.0g / 4.5g | 7–17 | trash 5–10% | not counted |
| Pattern: Ironfeather Leggings, Red Dragonscale Leggings | 29g / 12g | 8–9 | trash 5% | not counted |
| Plans: Dark Iron Pulverizer / Dark Iron Plate | 0.50g / 0.70g | 23–24 | Grizzle 96% / Ribbly 23% | vendor 0.30g |
| Bottom Half of Advanced Armorsmithing | 0.85g | 18 | Goraluk 22% | negligible |
| Rockshard Pellets (ammo) | 50c each | huge | Roccor 87% | ~0 |
| Sealed Artisan's Writ | 0.40g | 228 | trash ~1–2% | negligible |

**Never listed (no AH value):** Doomshot, Miniature Cannon Balls, Core of Elements, Essence of
Hakkar, Dark Iron Scraps, Bone Fragments, Crypt Fiend Parts, Atal'ai Haze, Fragment of the
Firelands, Ironfel and Invader's Scourgestone.

**Small sellable extras:** Ironweb Spider Silk ~60s (Smolderweb 12%), Major Healing Potion ~22s
(Zigris 13%), Unadorned Seal of Ascension ~3s.

**Hidden upside:** Wowhead's list shows up to three blues per mob. Bosses with more ("…")
probably hide more BoE dungeon-set pieces, so BoE value is under-counted.

## 3. How greens are valued
- **Boss greens are counted at the median vendor price for their item-level range:** ilvl 48–55 →
  0.85g, ilvl 56–63 → 1.37g (511 / 487 greens in the catalog).
  - Selling on the AH pays more: lower quartile ~1.00g / ~2.00g, so ~0.95g / ~1.90g after
    the cut.
  - But Strat's loops yield ~20 greens an hour, more than the random-green market will
    absorb. The vendor price is the floor; AH sales are upside.
- **Nanaya's 99% green** (Shaper's Terrace) is re-valued the same way: 1.88 → 1.36g. The Nanaya
  loop goes from 72 to 70.
- **Trash greens are still not counted**, so all dungeons are compared the same way.

## 4. Updated loops (conservative / anchored g/h)
| Loop | Before | Now | Tier |
|---|---|---|---|
| Krol'dok at 60 | 50 | **50** | reliable |
| Dire Maul East (estimated) | 40 / 66 | 40 / 66 | maybe |
| Blackrock Depths: entrance loop (12 min) | 34 / 57 | 34 / 54 | maybe |
| Sunken Temple at 60: trolls > Jammal'an + Ogom (12 min) | 41 / 69 | **20 / 30** | maybe |
| **Stratholme Undead: ziggurats + Ramstein (15 min)**, new | — | **105 / 135** | unlikely |
| **Stratholme Living: Willey + Galford (15 min)** | 71 / 96 | **103 / 130** | unlikely |
| LBRS: front loop (12 min) | 33 / 53 | **77 / 96** | unlikely |
| Stratholme Undead: side gate (15 min) | 38 / 63 | 75 / 105 | unlikely |
| Shaper's Terrace: Titanosaur + Nanaya (15 min) | 72 / 113 | 70 / 111 | unlikely |
| Scholomance: Rattlegore + Jandice + Ras (15 min) | 29 / 48 | 58 / 83 | unlikely |

**Routes:**
- **Strat Undead, ziggurats + Ramstein:** side gate > Baroness Anastari > Nerub'enkan > Maleki
  the Pallid > Slaughterhouse > Ramstein the Gorger.
  - Ramstein alone is worth ~10g per kill in extras: Gauntlets of Valor 15%, 2.44 greens.
  - The route is tight for 15 minutes.
- **Strat Living:** Malor > Willey > Galford > The Unforgiven. Value: Galford's Devout Gloves
  and greens, plus the orbs at the 2g vendor price.
- **LBRS front loop:** Omokk > Vosh'gajin (Shadowcraft Gloves 17%) > Voone > Smolderweb, plus
  ~5–6 Firebrand Pyromancers.
  - A Pyromancer kill is worth ~0.73g: the Robe of the Archmage pattern at its vendor price,
    plus Cord of Elements and Magister's Bindings.
  - The 12-minute variant (without Smolderweb) wins.

## 5. Verdict
- **Plan unchanged: Krol'dok** at 60.
- **At 60, the test order changes:**
  1. **Stratholme** (Undead ziggurats + Ramstein, or Living Willey + Galford): ~100 g/h if a
     prot warrior can handle it, so test one pack first.
  2. **LBRS front loop** (~77).
  3. **Shaper's Terrace Nanaya loop** (~70).
  4. **Dire Maul East** (~40, the only "maybe" above BRD).

  **Sunken Temple drops off the list** (~20).
- **What would help:** a timed Strat test and the Dire Maul tables (DME is still estimated).

## 6. Real vs estimated
| Part | Status |
|---|---|
| Blues per kill, ilvls, greens per kill, extra drop rates (5 Classic dungeons) | **real** (Wowhead Forever, 2026-11-25) |
| BoE vs BoP | **real** (Horde AH: ever listed means BoE) |
| BoE values | **real** Horde AH fill prices; thin markets noted |
| Vendor value of BoP blues | **estimated** (item-level curve) |
| Green value | **real** vendor median as the floor; AH upside not counted |
| Routes, minutes, trash counts, Pyromancers per loop | **estimated** |
| Solo viability | **judgement** (Classic-era mechanics) |
| Dire Maul, Maraudon, Uldaman, ZF, RFD, SM, RFK, Dalaran, RoL | **real since**: see `dire-maul-maraudon-real-drops-2026-11-25.md` and `uldaman-zf-sm-real-drops-2026-11-25.md`. City of Dalaran is still estimated (no Wowhead data) |
