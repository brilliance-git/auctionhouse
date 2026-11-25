# ~15-minute dungeon loops: gold per minute instead of full clears (2026-11-25)

> **Correction (2026-11-25, `classic-dungeons-real-drops-2026-11-25.md`):** Sunken Temple, LBRS, BRD, Scholomance and Stratholme now use real Wowhead Forever drop tables.
> - **Sunken Temple falls to ~20–22 g/h:** the balcony trolls drop no blues.
> - **BRD stays at ~34.**
> - **Strat Undead (ziggurats + Ramstein ~105), Strat Living (~103), LBRS (~77) and Scholomance (~58) jump:** boss greens and BoE set pieces. All are "unlikely" solo.
> - **Krol'dok (~50) is still the best reliable farm,** and DME (~40) is the best "maybe".
>
> Run `python3 scripts/dungeon_farm_model.py` for current numbers; the tables below are as first written.


**Question:** for every dungeon the model treated as too long (a generic "N-boss chunk",
"partial" or "long"), what's the best concrete loop of about 15 minutes, from zone-in to reset?
And does it beat Krol'dok?

**Short answer**
- **No loop beats Krol'dok among farms a solo prot warrior can count on.** Krol'dok makes
  ~50 g/h at 60, using real boss prices, and it's "reliable" (out-levelled).
- **Best loops:**

  | Loop | g/h (conservative / anchored) | Tier |
  |---|---|---|
  | **Sunken Temple: balcony trolls (12 min)** | **41** / 69 | maybe |
  | **Dire Maul East: Pusillin + lashers + Alzzin** | **40** / 66 | maybe |
  | Blackrock Depths: entrance loop | 34 / 57 | maybe |
  | **Maraudon: Princess loop** | 32 / 50 | **reliable** |
  | Stratholme Living: Willey + Galford (15 min) | **71** / 96 | unlikely |

  Strat Living is the highest-value loop overall, but it's "unlikely" solo: level 57–60
  elite casters, and no documented prot solo.
- **15 minutes vs 12 minutes:**
  - **12 wins** when the 15-minute loop only adds a low-value boss or a long walk: Sunken
    Temple (Spawn of Hakkar is worth ~1.3g), Uldaman and Maraudon at 60, BRD.
  - **15 wins** when the extra 3 minutes buy one or two full bosses near the route:
    Stratholme Living, Scholomance, DM West, LBRS, Blackmaw Hold, Alcaz Prison.
  - **DME and Shaper's Terrace tie.** In DME, 4 runs × 5 bosses and 5 runs × 4 bosses come to
    the same 20 boss kills an hour.

> **Updated 2026-11-25 with real Wowhead Forever boss tables** (`forever-dungeons-real-drops-2026-11-25.md`):
> the Drowned City, Alcaz Prison, Blackmaw Hold and Shaper's Terrace rows now use real blues per kill. The new Shaper's Terrace Nanaya loop (72 / 113, "unlikely") is the highest-value loop.

Reproduce with `python3 scripts/dungeon_farm_model.py --reasons`. Each loop appears twice, as
`(15 min)` and `(12 min)`.

> **How solid this is:**
> - **Estimated:** routes follow Classic-era layouts (the Forever-only dungeons use the boss
>   orders sources list), and every boss order, kill count and minute figure is an estimate.
>   Boss blues for anything but Krol'dok use the item-level curve.
> - **Real:** AH drops (Runecloth, Mageweave, Righteous Orb, Living Essence, Heart of the
>   Wild, Essence of Earth) are priced live on the **Horde AH only** (17–23 Nov 2026
>   snapshots), demand-capped at a 10% share. Nothing is timed in-game yet.
> - **Rules:** normal pull-and-kill only. Normal resets within the 5-per-hour cap are fine;
>   no pathing, leash, ledge or reset exploits.

---

## 1. How the loops are modelled
- **Each loop runs twice:**
  - **15 minutes:** 4 runs an hour.
  - **Trimmed to 12 minutes:** 5 runs an hour, the instance cap.
- **The rest is unchanged from the earlier PRs:**
  - **Boss blues:** one per boss (Forever: "every boss … drops a guaranteed Rare").
  - **Trash coin:** 0.09s × mob level per elite, 0.4× for non-elites.
  - **AH drops** per trash kill or per run.
  - **Consumables:** −2.5 g/h on "maybe" and "unlikely"
    farms.
- **These named loops replace the old generic entries** for the same dungeons ("… chunk",
  "… partial", "Alcaz Prison (full)", "Maraudon (Princess run)", "The Drowned City (full)",
  the Sunken Temple troll chunk). That's clearer than keeping both.
  - The Spawn of Hakkar-only farm and every non-chunk farm (Krol'dok, SM, ZF, RFK, RFD, City
    of Dalaran, Ruins of Lordaeron) are unchanged.
- **Typical 15-minute budget:**
  - ~1–2 min zone-in and walk to the first pull;
  - ~9–10 min of trash and bosses;
  - ~1–2 min of looting;
  - ~1–2 min exit and reset (Shaper's Terrace has a teleport exit).

## 2. Ranked: level 60

| Tier | Loop | 15 min | 12 min | Win | Route (15 min) | Why this tier |
|---|---|---|---|---|---|---|
| reliable | *Krol'dok at 60 (benchmark)* | — | **50** / 50 | — | same as above | Elites 42–45 (gap 15+) |
| reliable | **Maraudon: Princess loop** | 32 / 49 | 32 / 50 | 12 | Orange side > Noxxion > Razorlash > Landslide > Rotgrip > Princess Theradras (12 min skips Razorlash) | Elites 44–52; Princess hits hard. Essence of Earth + Runecloth on the AH |
| reliable | Uldaman: back-door loop | 20 / 32 | 21 / 33 | 12 | Back entrance > Ironaya > Obsidian Sentinel > Ancient Stone Keeper > Galgann > Grimlok > Revelosh (12 min skips Revelosh) | Elites 41–47 |
| maybe | **Sunken Temple: balcony trolls (+ Spawn)** | 38 / 63 | **41** / 69 | 12 | Six balcony trolls > Spawn of Hakkar > exit | Elite trolls 49–55 (gap 5–11) with casters |
| maybe | **Dire Maul East: Pusillin + lashers + Alzzin** | 40 / 66 | 40 / 66 | tie | Pusillin chase (key) > Zevrim Thornhoof > Hydrospawn > Lethtendris > Conservatory lashers > Alzzin (12 min skips Lethtendris) | Non-elite melee lashers suit rage; Alzzin and Lethtendris cast |
| maybe | Blackrock Depths: entrance loop | 33 / 56 | 34 / 57 | 12 | Lord Roccor > Houndmaster Grebmar > High Interrogator Gerstahn > Ring of Law > Pyromancer Loregrain (12 min skips Loregrain) | Front wings ~50–54; some Dark Iron casters |
| maybe | Alcaz Prison: full clear | 29 / 48 | 28 / 46 | 15 | Wrex > The Questioner > Tidemistress > Katerina > Zarla Ober (Blazeroar) | Elites 48–53; Tidemistress casts; dragon phase unknown |
| unlikely | **Stratholme Living: Willey + Galford orb loop** | **71** / 96 | 59 / 75 | 15 | Festival Lane > Malor the Zealous > Cannon Master Willey > Archivist Galford (orbs 84%) > The Unforgiven | Elites 57–60 with Sorcerers, Battle Mages, Priests |
| unlikely | **Shaper's Terrace: Titanosaur + Nanaya loop** (added by the real-drops update) | **72** / 113 | 67 / 100 | 15 | Mount in > Titanosaur > Venomridge > Thunderhoof > Direhorn Matriarch > Nanaya > teleport out | Elites 58–60; Nanaya's position unconfirmed |
| unlikely | Shaper's Terrace: dinosaur loop | 53 / 93 | 54 / 95 | 12 | Mount in > Titanosaur > Venomridge > Thunderhoof > Direhorn Matriarch > Izha'Rel and Tor'Rel > teleport out | Elites 58–60. Melee beasts suit rage better than casters, but no solo data. +~5.8 g/h Thorium only with Mining |
| unlikely | Stratholme Undead: side-gate loop | 38 / 63 | 37 / 60 | 15 | Magistrate Barthilas > Baroness Anastari > Nerub'enkan > Maleki the Pallid | Elites 57–60; Maleki and acolytes cast |
| unlikely | Blackmaw Hold: first bosses | 33 / 55 | 32 / 53 | 15 | Withermaw > Impaan the Imprisoner > Elder Shaman Bloodmane > Bonesnout (order unconfirmed) | Elites 55–60; no solo reports; not the old Devotee room |
| unlikely | LBRS: front loop | 34 / 55 | 33 / 53 | 15 | Highlord Omokk > Shadow Hunter Vosh'gajin > War Master Voone > Mother Smolderweb | Orc packs 55–60 with casters |
| unlikely | Dire Maul North: kill-everything | 33 / 54 | 31 / 51 | 15 | Guard Mol'dar > Stomper Kreeg > Guard Fengus > Guard Slip'kik (no King Gordok in 15 min) | Ogre packs 56–60 with ogre mages; killing the guards forfeits most of the tribute |
| unlikely | Scholomance: Rattlegore + Jandice | 29 / 48 | 26 / 41 | 15 | Viewing Room trash > Rattlegore > Jandice Barov > Ras Frostwhisper | Caster-heavy, 58–60 |
| unlikely | Dire Maul West: Warpwood loop | 26 / 42 | 23 / 36 | 15 | Tendris Warpwood > Illyanna Ravenoak > Magister Kalendris | Highborne casters and arcane aberrations, 56–60 |

**Level-60 verdict:**
- **Krol'dok (50) stays the plan.**
- **Worth one test each,** if Krol'dok ever runs dry or you want variety: Sunken Temple's
  troll loop (41) and the DME loop (40). Both are "maybe", with conservative values about
  10 g/h below Krol'dok and optimistic values about 15–20 g/h above it.
- **Maraudon's Princess loop (32)** is the best "reliable" alternative.
- **Strat Living's 15-minute orb loop (71–96)** is the biggest prize. It only counts once a
  test pack shows a prot warrior can handle its casters, or with raid gear after 9 Dec.

## 3. Route notes
- **Sunken Temple:**
  - The six balcony trolls are the core.
  - Spawn of Hakkar (the old farm, confirmed) only adds ~1.3g per kill: ~0.73 blues plus a
    ~22% BoE green. The 12-minute trolls-only loop wins.
  - Spawn of Hakkar's listed 88,600 HP (probably the raid-season version) would make the
    15-minute variant even worse.
  - See `sunken-temple-2026-11-25.md`.
- **Stratholme Living:**
  - Galford is the orb source (84%); trash orbs are ~9.5% per kill.
  - Even so, almost all orbs end up at the 2g vendor price: at a 10% share, the AH takes
    ~0.2 an hour.
  - The 15-minute loop wins because it adds Malor and The Unforgiven (two more blues).
- **DME:**
  - Pusillin's chase gives the Crescent Key.
  - The lashers are non-elite, so coin is 0.4×, but they're the best rage source in any
    level-60 dungeon.
  - Living Essence and Heart of the Wild add ~2–3 g/h.
- **DM North:** "kill-everything" gives up the tribute chest, so this models the boss blues
  only. A real tribute run needs the guards alive (stealth or traps), which a prot warrior
  can't do.
- **BRD:** the entrance loop stays in the lower-level front half. The Ring of Law boss is
  random.
- **Shaper's Terrace:** a mount works inside and there's a teleport exit, so the 15-minute
  loop fits 5 bosses. Rich Thorium Veins (2 per reset) need Mining.
- **Blackmaw Hold:** the boss order is unconfirmed (one source lists 7 bosses). The old
  Devotee room has had no loot since 16 Nov; stay out of it.

## 4. What's estimated, what's real
| Part | Status |
|---|---|
| Routes, boss order, kill counts, minutes | **estimated** (Classic layouts; Forever-only dungeons from guide boss lists) |
| Boss blue value (all but Krol'dok) | **estimated** (item-level curve; conservative = catalog median) |
| Krol'dok boss value | **real** (Wowhead sell prices and drop rates) |
| Trash coin | **estimated** (from a Krol'dok guide video) |
| Spawn of Hakkar drops | **real** drop rates (Wowhead Forever, 1,265 kills); greens priced from 163 Horde AH greens |
| Runecloth, Mageweave, Righteous Orb, Living Essence, Heart of the Wild, Essence of Earth | **real** Horde AH prices, demand-capped |
| Solo viability | **judgement** using Classic-era mechanics; Forever's prot rework may move melee-heavy loops up |

## 5. Next tests (log in `docs/farm-log.md`)
1. **A timed Krol'dok run:** still the most important number.
2. **At 60:** one test pack from Sunken Temple's balcony trolls and from DME. Pass if the loop
   fits about 12–15 minutes at under ~1 potion per pack.
3. **One Strat Living Scarlet pack:** if a prot warrior can handle Sorcerers and Battle Mages,
   the 15-minute orb loop is the best value in the game for this character.
