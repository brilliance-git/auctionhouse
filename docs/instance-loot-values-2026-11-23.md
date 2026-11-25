# Instance loot values for a solo Protection Warrior — 2026-11-23

Inputs: `docs/research-prot-warrior-solo-farms-2026-11-23.md` (web research),
6 days of AH data (145–147 hourly snapshots, 17–23 Nov 2026), and Wowhead tooltips /
drop tables supplied by hand (Wowhead blocks automated requests).
Re-run prices with `python3 scripts/dungeon_drops.py`.

## Character
- Protection Warrior.
- Instance cap: 5 new instances/hour → any run under 12 min uses the full cap.

## 1. Boss gear is bind-on-pickup → vendor only
Confirmed on Wowhead (tooltip "Binds when picked up"):

| Item | Instance | Vendor | Drop % |
|---|---|---|---|
| Thornspike | RFK (Aggem Thorncurse) | 65s 22c | 32.13% |
| Zarmok's Plated Signet | Krol'dok (Twilight Commander Zarmok) | 75s 97c | 34.30% |
| Krol'dok Warplate Chest | Krol'dok (Nar'gurk) | ? | ? |
| Mirror of Rath'mael | Ruins of Lordaeron (Rath'mael) | 17s 68c | 34.22% |

None of the boss gear from RoL, RFK, SM or Krol'dok appeared on the AH in 6 days. As a
cross-check, gear known to be BoP in Classic (Thornspike, Corpsemaker, Herod's Shoulder,
Hand of Justice, Ironfoe…) is also absent, while known BoE items (Skullflame Shield,
Gutwrencher, Arcanite Reaper) are present.

## 2. What is actually sellable

| Instance | Item | AH median | Vendor | Drop | Note |
|---|---|---|---|---|---|
| Strat Living (Scarlet) | **Righteous Orb** | ~9–10g (fell from ~12g to ~9g over the 6 days) | **2g** | Galford **84%** (621/735), trash 7–11% | ~100 listed; 2.5× more posted than leaves the AH |
| Strat | Runecloth | 5–6s | 4s | ~1/3 kills | |
| Krol'dok | **Blueprint: Expert Campfire** | ~25–30g | 3g | **4.54%** (66/1,453) from Slavecrusher Grox | only ~9 listed — sell one at a time |
| RoL | Blueprint: Fermenter | ~6g | 4s | **7%** (439/6,206) from Rath'mael | |
| RoL | Blueprint: Arcane Salvager | ~3.4g | 4s | ? | |
| ZF | Mageweave Cloth | 4s | 3s | low | AH ≈ vendor |
| ZF | world-drop gear (Fiery War Axe, Blackskull Shield, Robes of Insight…) | 20–45g | 1–2g | very rare | bonus only |
| DME | Living Essence | 21–27s | 5s | ? | |
| DME | Heart of the Wild | 4s | 4s | 27% | no AH value |
| SM | Silk 2s, Fadeleaf 4s | | | | weak |
| any | Flask of Mojo | 2s 64c | 2s 50c | | vendor it |
| any | Flask of Big Mojo | ~5s 70c | 5s | | barely worth listing |
| any | Powerful Mojo (L55 trolls) | ~1g 15c–1g 40c (fell from ~2g) | 20s | | list it |

## 3. Estimates

### Krol'dok Stronghold (the level-60 baseline farm)
Bosses 42–45, nearly all elite, ~5 min run (Wowhead). 7 bosses incl. rare Kroog.
- Campfire blueprint: 5 runs/h × 4.54% × ~27g × 0.95 ≈ **~6 g/h** (avg; one every ~4.4 h, streaky).
- BoP blues: ~1 per boss at ~76s vendor (ilvl ~45) × 7 bosses ≈ ~5g/run ≈ **~25 g/h**.
- Plus elite coin + greys: **unmeasured**.
- **≈ 30 g/h + coin**, plus tank gear (Warplate set: 2pc +100 armor, 3pc +5 Def, 4pc heal on block,
  5pc stacking Stamina; Zarmok's Signet).
- Use normal pull-and-kill only. The mage ledge/pathing farm is exploit-adjacent (see the
  Blackmaw Hold bans, Nov 16–17).

### Stratholme Living, Scarlet side (unproven for warriors)
Assume ~25 kills per 12-min chunk → ~2.4 trash orbs + 0.84 Galford ≈ 3 orbs/run.
- Vendor-only: ~7.6g/run ≈ **~38 g/h**. With AH orbs: up to ~27g/run, but the market
  can't absorb 15 orbs/h — sell a few per day, vendor the rest.
- **No documented case of a prot warrior soloing Strat in Forever** (searched 2026-11-23).
  Many Scarlet mobs are casters (no melee → no rage from blocks). Test with melee-only packs
  (Guardsmen, Gallants, Defenders, Monks) and always kill Galford.
  One other database lists Galford's orb drop at 18%; Wowhead's sample of 735 kills says 84%.

### Others
- ZF graveyard: coin/grey farm, 40–50 g/h reported for mages; untested on warriors.
- RoL, RFK: ~1–3g/run in vendored blues. SM, DME lashers: weak.

## 4. Ranking
All at level 60 (see `dungeon-farms-viability-2026-11-23.md` and later docs for the current ranking):
1. **Krol'dok** — the reliable baseline (out-levelled).
2. Strat Living Scarlet side, if soloable.
3. ZF graveyard (gold only).

## 5. Data still needed to pin down Krol'dok g/h
1. **1–2 timed test runs:** gold before/after (greys vendored, blues kept), run time, full loot list.
2. Wowhead **Drops** tab for each boss: Slavecrusher Grox, Twilight Commander Zarmok,
   War Handler Ashka, Nar'gurk, Bossman Toof, Overlord Mugg, Kroog (+ spawn rate);
   sell prices for a few more blues (Warplate Chest, Emblem of Slamming, one each from Grox/Ashka/Mugg).
3. Trash: average money per kill, trash drop list, and whether the Warplate
   Pauldrons/Gauntlets/Legplates are BoP or BoE.
4. What the **Krol'dok Ogre Key** (Overlord Mugg) opens.
