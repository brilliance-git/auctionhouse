# Dire Maul and Maraudon re-modelled with real Wowhead Forever drop tables (2026-11-25)

**Input:** `docs/wowhead-drops-classic-2-2026-11-25.md`, from wowhead.com/forever NPC "Drops"
tabs; same format and method as `classic-dungeons-real-drops-2026-11-25.md`.
- All 84 item IDs were checked on the **Horde AH**: ever listed means BoE (AH fill price after
  the 5% cut), never listed means BoP (item-level curve).
- Boss greens are valued at the median vendor price: 0.85g at ilvl 48–55, 1.37g at ilvl 56–63.
- Reproduce with `python3 scripts/dungeon_farm_model.py`; loops using this data show
  `real-rate`.

## Short answer
- **The Dire Maul East loop now beats Krol'dok on conservative numbers:** **~56 g/h**
  (12 minutes; 86 optimistic) against Krol'dok's ~50.
  - **Why:** Alzzin drops 1.94 blues per kill, and Pusillin 1.35 greens per kill.
  - **But it's still "maybe" solo:** non-elite melee lashers are ideal for rage, but Alzzin and
    Lethtendris cast. Krol'dok's ~50 uses real sell prices and is "reliable" at 60; DME's
    blues are valued with the item-level curve.
  - **So DME is now the first farm to test at 60.** If one run clears solo in ~12 minutes, it
    edges out Krol'dok.
- **The Maraudon Princess loop rises from ~32 to ~41 g/h** (12 minutes; 64 optimistic).
  Princess Theradras drops 1.89 blues per kill. It's still the best **"reliable"** loop after
  Krol'dok, about 9 g/h behind.
- **DM North changes shape:**
  - The guards (Mol'dar, Fengus, Slip'kik) **drop no blues**; they aren't in the list.
  - The value is at the end: King Gordok 2.19, Cho'Rush 3.32 blues per kill plus 1.64 greens
    and potions, and Captain Kromcrush 1.0.
  - A ~20-minute run to Gordok models at **~63 g/h** (100 optimistic), at 3 runs an hour. It's
    "unlikely" solo (ogre packs 56–60 with ogre mages).
  - The 12-minute version (guards + Kreeg only) is worth ~14.
- **DM West's Warpwood loop:** 33 / 52 (15 min). "Unlikely" (Highborne casters).
  - Immol'thar (1.94) and Tortheldrin (2.12) are deep inside and not on the loop.

## 1. BoE check (Horde AH, 17–25 Nov 2026)
7 of 84 IDs have ever been listed. **Every boss blue in Dire Maul and Maraudon is BoP,**
including Princess Theradras's Blackstone Ring, Bracers and Gemshard Heart. The BoE items are
all trash drops:

| Item | Fill price | ~Listed | Source and rate | Counted as |
|---|---|---|---|---|
| **Pattern: Warbear Helm** | 173.5g | 2 | Eldreth Seether 9% | not counted (trash; 2 listed, no sales seen) |
| **Pattern: Living Crown** | 42g | 9 | Warpwood Treant 6% | not counted (trash) |
| Pristine Black Diamond | 18.3g | 51 | Eldreth Seether 1% | not counted |
| Stonebark Gauntlets | 10g | 4 | Ironbark Protector 2% | not counted |
| Barbed Thorn Necklace | 4.5g | 10 | Warpwood Treant 2% | not counted |
| Phasing Boots | 3.0g | 4 | Phase Lasher 4% | not counted |

- **Plans: Martyr's Legplates** (Gordok Brute 5%) has never been listed, so it's BoP or not yet
  seen.
- **Savage Frond** (Treants and Ironbark Protectors ~92%, Phase Lashers 35%, Razorlash 33%) has
  never been listed either: no AH value.
- **Other extras counted on boss kills:**
  - Cho'Rush: Major Healing Potion 42% (~21s) and Major Mana Potion 42% (~76s).
  - Landslide: Lifeless Stone and Smooth Stone Chip.
  - Rotgrip: Pointy Crocolisk Tooth.

## 2. Boss data used
| Dungeon | Boss | Blues per kill | ilvl | Greens per kill |
|---|---|---|---|---|
| Maraudon | **Princess Theradras** | **1.89** | 54 | 3% |
| Maraudon | Noxxion / Razorlash / Landslide / Rotgrip | 1.01 / 1.07 / 1.07 / 1.04 | 51–53 | 2–10% |
| Maraudon | Lord Vyletongue / Celebras / Gizlock | 0.99 / 1.07 / 1.03 | 50–53 | 2–3% |
| DME | **Alzzin the Wildshaper** | **1.94** | 59 | 10% |
| DME | **Pusillin** | 0.42 | 58 | **135%** |
| DME | Zevrim / Hydrospawn / Lethtendris | 0.99 / 1.02 / 0.98 | 58 | 13% / 24% / 6% |
| DMW | Tendris / Illyanna / Kalendris | 0.99 / 0.90 / 0.99 | 61 | 18% / 7% / 29% |
| DMW | Immol'thar / Prince Tortheldrin | 1.94 / 2.12 | 62 | 10% / 8% |
| DMN | **Cho'Rush the Observer** | **3.32** | 61 | **164%** |
| DMN | King Gordok / Captain Kromcrush / Stomper Kreeg | 2.19 / 1.00 / 0.72 | 60–63 | 5% / 19% / 16% |

## 3. Updated loops (conservative / anchored g/h)
| Loop | Before | Now | Tier |
|---|---|---|---|
| Krol'dok at 60 | 50 | **50** (real sell prices) | reliable |
| **Maraudon: Princess loop (12 min)**: Noxxion > Landslide > Rotgrip > Princess | 32 / 50 | **41 / 64** | reliable |
| **Dire Maul East (12 min)**: Pusillin > Zevrim > Hydrospawn > lashers > Alzzin | 40 / 66 | **56 / 86** | maybe |
| Dire Maul East (15 min, + Lethtendris) | 40 / 66 | 53 / 82 | maybe |
| **Dire Maul North: to King Gordok (~20 min)**: guards > Kreeg > Kromcrush > Gordok + Cho'Rush | 33 / 54 (old guard route) | **63 / 100** | unlikely |
| Dire Maul West: Warpwood loop (15 min) | 26 / 42 | 33 / 52 | unlikely |

The 12-minute DME loop wins over 15 minutes: Lethtendris adds less than the extra slot costs.

## 4. Not counted (upside)
- **Trash greens.** Phase Lashers drop 59% greens per kill, Warpwood Treants 48%, Ironbark
  Protectors 53%, Gordok Brutes 38%. If the DME route's lashers are Phase Lashers (the
  Conservatory's Whip Lashers aren't in the list), ~20 a run at the 1.37g vendor floor would
  add **~20–30 g/h** to DME.
  - Trash greens stay excluded everywhere, so dungeons are compared the same way.
- **Trash patterns:** Warbear Helm (~174g), Living Crown (~42g). Thin markets.
- **Boss greens sold on the AH** instead of to a vendor (lower quartile ~2.00g vs 1.37g).

## 5. Verdict: which gets closer to Krol'dok?
- **Dire Maul East.** It passes Krol'dok on conservative numbers (56 vs 50) and has upside from
  trash greens. It's the one "maybe" to test first at 60.
- **Maraudon's Princess loop** (41) is the best **reliable** alternative, still ~9 g/h short.
- **Krol'dok stays the plan until a DME test run says otherwise.** Its number is the most solid
  (real prices), and DME's lead depends on the blue curve and on soloing Alzzin and
  Lethtendris.

## 6. Real vs estimated
| Part | Status |
|---|---|
| Blues and greens per kill, ilvls, drop rates (DM, Maraudon) | **real** (Wowhead Forever, 2026-11-25) |
| BoE vs BoP | **real** (Horde AH) |
| Vendor value of BoP blues | **estimated** (item-level curve) |
| Green value | **real** vendor median floor |
| Routes, minutes, trash counts | **estimated** |
| Solo viability | **judgement** (Classic-era mechanics) |
| Uldaman, ZF, RFD, SM, RFK, City of Dalaran, Ruins of Lordaeron | **real since**: see `uldaman-zf-sm-real-drops-2026-11-25.md`, except City of Dalaran (no Wowhead data) |
