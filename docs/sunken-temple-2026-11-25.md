# Sunken Temple (Temple of Atal'Hakkar): the "Sons of Hakkar" farm (2026-11-25)

**Question:** you used to farm the "Sons of Hakkar" in Sunken Temple. Is that, or a normal
Sunken Temple boss route, a good solo farm for a Protection Warrior in WoW: Forever, and how
does it compare with Krol'dok?

**Short answer**
- **Spawn of Hakkar alone is not a gold farm:** ~5–9 g/h. It's a single level 50–51 elite
  worth ~0.73 blues (~1–2g at a vendor) plus a ~22% chance of a BoE green (~1g on the AH) per
  kill, and you can only reset 5 times an hour. It's
  "maybe" solo while levelling and "reliable" at 60.
- **The balcony-troll chunk is the real Sunken Temple farm:** six troll minibosses, each with a
  guaranteed blue in Forever. It models at **~40 g/h** conservatively, ~68 optimistically.
  - **While levelling it's "unlikely" solo:** elite trolls 49–55 with caster priests and witch
    doctors.
  - **At 60 it's "maybe"**, and it's the best of the "maybe" farms on conservative numbers
    (41 vs DME 40, with the 15-minute loop model).
- **Against Krol'dok:** Krol'dok (~49–50 g/h, real prices, "maybe" while levelling and
  "reliable" at 60) stays ahead in both bands. Sunken Temple's troll chunk is the best farm to
  **test** at 60 after Krol'dok, on a par with Dire Maul East.

Reproduce with `python3 scripts/dungeon_farm_model.py --reasons`. Every g/h is a model, and
nothing is timed yet (`docs/farm-log.md`).

---

## 1. The farm: Spawn of Hakkar (confirmed)
- You confirmed the farm was **Spawn of Hakkar**
  ([Wowhead Forever NPC 5708](https://www.wowhead.com/forever/npc=5708)). "Son of Hakkar" is a
  separate Zul'Gurub mob, and that raid isn't open in Forever.
- **Your experience counts as evidence it can be soloed,** but the class you used isn't
  confirmed. A mage or hunter solo doesn't prove a prot warrior can do it.

## 2. Spawn of Hakkar
Wowhead Forever NPC page, read 2026-11-25; drop counts are out of 1,265 kills.

| | |
|---|---|
| Where | Basement of the Temple of Atal'Hakkar (Swamp of Sorrows); optional |
| Mob | **Level 50–51 elite beast.** Its Acid of Hakkar debuff needs extra healing in groups |
| Blues | **Slitherscale Boots 48%**, **Wingveil Cloak 25%**, ilvl 52, BoP. About **0.73 blues per kill**. Neither has ever been listed on the Horde AH |
| BoE greens | The world-drop green table: 122 items at ~0.2–1% each (Duskwoven, Righteous, Revenant, Crusader's, Heavy Lamellar and so on, ilvl 45–54). About **20–25% chance of a green per kill** |
| Other | Rugged Leather 3% and Thick Leather 3% (1–2 each), ignored. Deathblow, Slimescale Bracers and Stinging Bow at 0.08% each, ignored |
| Health | The page lists **88,600 HP ("Seasonal 20 Player")**. That's probably the raid-season version, not Forever's 5-player one. If it does apply, a prot warrior's ~150–250 DPS means 6–10 minutes for the kill alone |
| Respawn | Only on an instance reset (5 per hour) |
| Without a full clear? | Yes: enter, go down to the basement, kill it, leave, reset |

**Pricing the greens (Horde AH, 17–23 Nov 2026):**
- 163 level 45–54 BoE greens from the same name families have all been listed.
- Their median lowest price is **1.09g** (lower quartile 0.95g); the median vendor price is
  0.74g.
- At ~22% per kill × ~1.04g after the AH cut, a green adds **~0.23g per kill**.

**Model:**
- 0.73 × a blue at ilvl 52 (~1.1g conservative, ~1.9g anchored) + ~0.23g of greens + a few
  trash kills.
- ~7-minute runs, 5 an hour. That's **~5–9 g/h** (5–8 while levelling, 6–9 at 60).
- **If the 88,600 HP applies,** a run takes ~12 minutes. That's still 5 an hour, so the same
  g/h, with no slack.
- **Levelling:** "maybe" (one elite above a mid-40s character, no packs).
- **At 60:** "reliable", but still **not worth a lockout slot**. Krol'dok earns ~8× more per
  run.
- **If the old farm paid well,** the money was probably from skinning or the trash, not the
  Spawn. Classic guides and Forever posts point to Sunken Temple's **dragonkin and scales**:
  - That needs **Skinning**, which you don't have.
  - Green and Worn Dragonscale sell for ~5s on the Horde AH, the same as the vendor price
    (2026-11-25).

## 3. A normal Sunken Temple boss route: the six balcony trolls
- **Forever's loot rework:** "every boss has had their loot table modified and now drops a
  guaranteed Rare (Blue) item" (Warcraft Tavern, Forever dungeon guide). So one blue per boss
  is the stated rule here, not an assumption.
- **The chunk:** the six Atal'ai troll minibosses on the upper balconies, plus the trash
  between them, in ~12 minutes. Jammal'an, Ogom, the dragons and Eranikus need a longer
  clear, so they're left out.
- **Model** (6 blues at ilvl ~53, ~25 elite kills at ~52):

  | | Conservative | Anchored |
  |---|---|---|
  | Boss blues | 35.4 g/h | |
  | Trash coin | 5.8 g/h | |
  | **Total** | **~40 g/h** levelling (~39 at 60, after consumables) | ~67–68 g/h |
- **Solo viability:**
  - **Levelling: "unlikely".** Elite trolls 49–55 at or above your level, with Atal'ai
    priests and witch doctors (casters give no rage), plus Nightmare dragonkin elites that
    guides call hard to solo.
  - **At 60: "maybe".** The mobs are 5–11 levels below you, but the casters remain. Test one
    balcony first (checklist in `dungeon-farms-viability-2026-11-23.md`).
- **Not modelled:** the Avatar of Hakkar event. It needs blood from Hakkari Bloodkeepers and
  killing Nightmare Suppressors, which is too long for a 12-minute slot.

## 4. Known mage farm: rules apply
- A WoW: Forever forum thread reports a **solo mage Sunken Temple farm at 100+ g/h**. Another
  poster disputes this, putting the realistic figure at ~40–50 g/h without Skinning and ~70
  with it.
- Another thread describes it as relying on **ledge or pathing abuse**, with players arguing
  about whether it will be patched.
- Under this repo's rules (normal pull-and-kill only, after the Blackmaw Hold confiscations),
  **that method is off-limits.** It's also mage-specific.

## 5. Where it ranks

Updated with the named loops in `dungeon-loops-15min-2026-11-25.md` (the troll chunk now also counts Mageweave).


| Band | Farm | g/h (conservative / anchored) | Tier |
|---|---|---|---|
| Levelling | Krol'dok Stronghold | 49 / 49 | maybe |
| Levelling | **Sunken Temple: 6 balcony trolls** (12 min) | 42 / 70 | **unlikely** |
| Levelling | **Sunken Temple: Spawn of Hakkar only** | 5 / 8 | maybe |
| 60 | Krol'dok Stronghold at 60 | 50 / 50 | reliable |
| 60 | **Sunken Temple at 60: 6 balcony trolls** (12 min) | **41** / 69 | **maybe** (best "maybe" conservatively) |
| 60 | Dire Maul East (Pusillin + lashers + Alzzin) | 40 / 66 | maybe |
| 60 | Alcaz Prison (full) | 29 / 48 | maybe |
| 60 | Sunken Temple at 60: Spawn of Hakkar only | 6 / 9 | reliable |

**Verdict:**
- **Krol'dok stays the main farm in both bands.**
- **At 60,** add the Sunken Temple troll chunk to the "test one pack" list next to Dire Maul
  East. If it clears solo in ~12 minutes, it's the best 60 farm after Krol'dok.
- **The Spawn of Hakkar farm isn't worth a lockout slot** for gold.

## 6. Open questions
1. **What class did you farm Spawn of Hakkar on?** (The mob is confirmed.)
2. **Forever loot for Spawn of Hakkar and the balcony trolls:** item names, item levels, and
   whether any are BoE.
3. **A timed troll-chunk test at 60.**

## 7. Sources (read 2026-11-25)
- [Warcraft Tavern: Sunken Temple (Forever)](https://www.warcrafttavern.com/forever/guides/sunken-temple/), [Forever dungeons overview, loot rework](https://www.warcrafttavern.com/forever/guides/dungeons/), [Forever ST quests](https://www.warcrafttavern.com/forever/guides/sunken-temple-quests/), [Classic ST guide](https://www.warcrafttavern.com/wow-classic/guides/temple-of-atalhakkar/)
- [Wowhead: Temple of Atal'Hakkar (Forever overview)](https://www.wowhead.com/forever/guide/the-temple-of-atalhakkar-dungeon-overview-location-rewards); [Wowhead Classic ST strategy](https://www.wowhead.com/classic/guide/temple-of-atalhakkar-sunken-temple-dungeon-strategy-wow-classic)
- Spawn of Hakkar: [Wowhead Forever NPC 5708](https://www.wowhead.com/forever/npc=5708) (numbers relayed by the user's planning session, 2026-11-25), [wowclassicdb (TBC) NPC 5708](https://wowclassicdb.com/tbc/npc/5708), [wowclassicdb (WotLK)](https://wowclassicdb.com/wotlk/npc/5708), [Wingveil Cloak](https://warcraft.wiki.gg/wiki/Wingveil_Cloak), [Slitherscale Boots](https://warcraft.wiki.gg/wiki/Slitherscale_Boots)
- Forever loot tables and levels: [wowtbc.gg ST loot (Forever)](https://wowtbc.gg/warcraftforever/loot-tables/dungeons/the-temple-of-atal-hakkar/), [Mobalytics ST guide](https://mobalytics.gg/wow-forever/dungeons/sunken-temple-dungeon-guide), [kami-labs](https://kami-labs.fr/en/le-temple-englouti-wow-forever/), [Blazing Boost](https://blazingboost.com/wow-forever-classic/wow-forever-sunken-temple-guide)
- Solo mage farm: [Blizzard forums: 100g+/h claim](https://us.forums.blizzard.com/en/wow/t/solo-mage-sunken-temple-farm-100g-per-hour/2422599), [Blizzard forums: exploit discussion](https://us.forums.blizzard.com/en/wow/t/sunken-temple-solo-mage-farm/2421434?page=2), [YouTube 60–70 g/h mage](https://www.youtube.com/watch?v=eJXMrhi2GWI) (read via search snippets only; the forum pages couldn't be fetched)
- Dragonkin and scales: [Wowhead Classic leather and scales routes](https://www.wowhead.com/classic/guide/classic-leather-farming-specialty-scales), [PixelNitro solo instance guide](https://pixelnitro.com/wow-forever-best-solo-instance-gold-farming-guide-2026-classic-plus-solo-dungeon-methods/)
- Horde AH prices: `scripts/item_report.py`, 2026-11-25
