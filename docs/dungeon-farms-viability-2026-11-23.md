# Dungeon farms: can a solo Protection Warrior actually clear them? (2026-11-23)

**Question:** `dungeon-farms-prot-warrior-2026-11-23.md` ranks farms by modelled gold per hour,
as if every one could be cleared solo. Which of them can a solo prot warrior in pre-raid gear
actually do?

**Short answer**
- **At 60:** the farms at the top of the old ranking are the least likely to work solo:
  Stratholme, Scholomance, Shaper's Terrace, Blackmaw Hold and LBRS. That's level 58–60 elite
  packs with casters, and there's no documented prot-warrior solo of any of them.
  **Ranked by viability first, Krol'dok at 60 (~50 g/h) is the best farm you can count on.**
  Next come the Maraudon Princess loop (~41), the ZF loop (~39) and the SM Cathedral (~26). Of
  the "maybe" farms, Dire Maul East (~56) is the one to test, and the only one that beats Krol'dok.
- **So the next step hasn't changed:** a timed solo Krol'dok run. If it works, nothing at 60
  needs to replace it unless a test beats it.

Reproduce with `python3 scripts/dungeon_farm_model.py --reasons`. Every g/h is a model, and
`docs/farm-log.md` is still empty.

> **This uses Classic-era mechanics; Forever may differ.** In Classic, a warrior has no
> self-heal, prot does little damage, casters starve rage (no melee hits to block), and big
> pulls need sustain warriors lack. Forever reworked Protection: rage now comes from blocks,
> dodges and parries, and guides report holding 10–15 mobs rage-capped
> (`research-prot-warrior-solo-farms-2026-11-23.md`). That may move melee-heavy farms up a
> tier. It does little for caster packs. Treat the tiers as a starting point until a test says
> otherwise.

---

## 1. Tiers

| Tier | Rule of thumb | What it means |
|---|---|---|
| **reliable** | mobs ~10+ levels below you | They barely hurt; safe to farm on autopilot |
| **maybe** | mobs 3–9 levels below, **or** non-elite / melee-only packs | Doable with care and consumables; test one pack first |
| **unlikely** | elites within ~2 levels, packs with casters or healers, or huge near-level pulls | Expect deaths and repair bills; don't plan income on it |

- The script applies this rule (`auto_tier`) from the level gap and elite status. An explicit
  per-farm tier with a reason overrides it where research says otherwise (`TIERS` in the
  script).
- **Consumables** are subtracted from "maybe" and "unlikely" farms. This is an estimate:
  ~10 healing potions, ~10 bandages and one elixir an hour.
  - **Prices (Horde AH, 2026-11-23):** Greater or Superior Healing Potion ~4s, Heavy
    Mageweave Bandage ~6s, Heavy Runecloth Bandage ~14s, Elixir of Fortitude ~30s.
  - **That's ~2.5 g/h at 60.** Small next to the deaths and repairs a farm
    that's too hard would cost.

## 2. Level 60 (pre-raid gear), ranked by viability, then g/h
Regenerated from `python3 scripts/dungeon_farm_model.py` on 2026-11-25. These are the named loops
with real Wowhead Forever drop tables for every dungeon except City of Dalaran. Where a loop has
a 12- and a 15-minute variant, the better one is shown.

| Tier | Farm | g/h (conservative / anchored) | Why this tier |
|---|---|---|---|
| reliable | **Krol'dok Stronghold at 60** | **50** / 50 | Elites 42–45 (gap 15+); real boss sell prices |
| reliable | **Maraudon: Princess loop (12 min)** | **41** / 64 | Elites 44–52; Princess Theradras (1.89 blues per kill) hits hard but is a known solo kill at 60 in Classic |
| reliable | Zul'Farrak: graveyard + pyramid loop (15 min) | 39 / 55 | Elites 43–48 (gap 12+) |
| reliable | SM Cathedral: mass pull (12 min) | 26 / 33 | Humanoids 34–40 (gap 20+) |
| reliable | Razorfen Downs: full clear (12 min) | 24 / 37 | Elites 37–46 (gap 14+) |
| reliable | Uldaman: back-door loop (15 min) | 23 / 37 | Elites 41–47 |
| reliable | The Drowned City: full clear (10 min) | 21 / 32 | Elites 35–40 (gap 20+) |
| reliable | SM Armory / Library / Graveyard | 17 / 14 / 11 | Low-level mobs |
| reliable | Razorfen Kraul / City of Dalaran (estimated) / Ruins of Lordaeron | 14 / 13 / 8 | Low-level mobs |
| reliable | Sunken Temple: Spawn of Hakkar only | 6 / 8 | One level 50–51 elite |
| maybe | **Dire Maul East: Pusillin + lashers + Alzzin (12 min)** | **56** / 86 | Non-elite, melee-only level-54 lashers: the best mob type for rage. Alzzin and Lethtendris cast |
| maybe | Blackrock Depths: entrance loop (12 min) | 34 / 54 | Only the lower-level front wings (mobs ~50–54); caster packs elsewhere |
| maybe | Alcaz Prison: full clear (15 min) | 29 / 48 | Elites 48–53 (gap 7–12); Tidemistress is a caster; Zarla Ober's dragon phase is unknown |
| maybe | Sunken Temple: trolls > Jammal'an + Ogom (15 min) | 20 / 30 | Elite trolls 49–55 with casters; the balcony trolls drop no blues |
| unlikely | **Stratholme Undead: ziggurats + Ramstein (15 min)** | **105** / 135 | Elites 57–60; Maleki and acolytes cast; Ramstein hits very hard |
| unlikely | **Stratholme Living: Willey + Galford orb loop (15 min)** | **103** / 130 | Elites 57–60 with Sorcerers, Battle Mages and Priests; no documented prot solo |
| unlikely | LBRS: front loop (12 min) | 77 / 96 | Elites 55–60 orc packs with casters |
| unlikely | Stratholme Undead: side-gate loop (15 min) | 75 / 105 | Elites 57–60 |
| unlikely | Shaper's Terrace: Titanosaur + Nanaya loop (15 min) | 70 / 111 | Elites 58–60; no solo data; Nanaya's route position unconfirmed |
| unlikely | Dire Maul North: to King Gordok (20 min) | 63 / 100 | Ogre packs 56–60 with ogre mages |
| unlikely | Scholomance: Rattlegore + Jandice + Ras (15 min) | 58 / 83 | Elites 58–60, caster-heavy |
| unlikely | Blackmaw Hold: first bosses (15 min) | 33 / 55 | Elites 55–60; no solo reports |
| unlikely | Dire Maul West: Warpwood loop (15 min) | 33 / 52 | Highborne casters and arcane aberrations 56–60 |

**At 60:**
- **Krol'dok is the plan.** It's the reliable baseline (~50 g/h, real sell prices).
- **Test Dire Maul East first.** It's the best "maybe" and the only farm a solo prot warrior
  might handle that beats Krol'dok on conservative numbers (56).
- **Maraudon's Princess loop (41) is the reliable backup,** then the ZF loop (39).
- **Stratholme (~100+), LBRS (77) and Shaper's Terrace (70)** pay the most but are "unlikely"
  solo. They only count once a test pack shows they can be done, or with raid gear after 9 Dec.
- **What moves farms up:** the Forever prot rework, and the gear and items in section 4.

## 3. How to test one pack (before committing to a farm)
1. **Prepare:** full health and rage-ready. Have healing potions, bandages, a Free Action
   Potion, and your fear break (Berserker Rage; Will of the Forsaken if Undead) off cooldown.
2. **Pick a representative pack:** one with the mob types the route needs (casters included),
   not the easiest one.
3. **Pull with Charge or a ranged pull,** then Shield Block, Revenge and Thunder Clap. Watch:
   - **Rage:** do you stay above ~30? Casters standing back mean the answer is "no".
   - **Health:** how much does the pack take off you, and does anything stun-lock or fear you?
   - **Casters:** can you interrupt or line-of-sight them into melee?
4. **Write down** the time to kill the pack, health lost, and consumables used. Estimate the
   whole route: packs × time per pack + bosses + exit.
5. **Pass:** the route fits about 12 minutes and costs under ~1 potion per pack.
   **Fail:** a death or a near-death. Drop the farm a tier, or fix the cause (section 4).
6. **Log it** in `docs/farm-log.md`, including failed attempts and repair costs.

## 4. What improves the odds
- **Engineering explosives:** AoE damage prot lacks, and a stun from some (Thorium Grenade).
  Dense Dynamite ~20–25s, Thorium Grenade ~40–60s on the Horde AH (2026-11-23).
- **A lifesteal weapon enchant:** self-healing on every hit. Formula: Enchant Weapon -
  Lifestealing lists at ~36–70g; you'd need an enchanter to apply it.
- **Free Action Potions** (~4–5s): stop roots and stuns (Knockdown, Force Compliance adds,
  Crushing Slam setups).
- **Krol'dok Battlegear:** the 4-piece heal on block is doubled in Strongholds, which helps at
  Krol'dok.
- **Health-regen gear and race:** Troll's Blood potions, and Undead or Troll racials (see the
  research brief).
- **Raid gear:** Barrow Deeps, Hyjal Summit and Onyxia's Lair open on **9 Dec 2026**.
  Better armor and weapons could move Strat, Scholomance and Shaper's Terrace from "unlikely"
  towards "maybe".
- **Your own rules still apply:** normal pull-and-kill only. No pathing, leash, ledge or reset
  tricks.

## 5. Earlier dungeons farmed at 60 (added 2026-11-25)
All are out-levelled at 60, so they're "reliable" and clear faster (~8–12 min, still capped at
5 runs an hour). From `python3 scripts/dungeon_farm_model.py` (conservative / anchored g/h):

| Farm | g/h | Note |
|---|---|---|
| Maraudon: Princess loop (12 min) | 41 / 64 | real drop tables; best reliable after Krol'dok |
| Zul'Farrak: graveyard + pyramid loop (15 min) | 39 / 55 | real drop tables (`uldaman-zf-sm-real-drops-2026-11-25.md`) |
| SM Cathedral (mass pull) | 26 / 33 | real drop tables |
| Razorfen Downs (full) | 24 / 37 | real drop tables |
| Uldaman: back-door loop with Archaedas (15 min) | 23 / 37 | real drop tables |
| The Drowned City: full clear (10 min) | 21 / 32 | real drop tables |
| SM Armory / Library / Graveyard | 17 / 14 / 11 | real drop tables |
| Razorfen Kraul (full) | 14 / 21 | real drop tables |
| City of Dalaran (full) | 13 / 21 | estimated: Wowhead has no data |
| Ruins of Lordaeron (full) | 8 / 11 | real drop tables |
| Sunken Temple: Spawn of Hakkar only | 6 / 8 | |

None beats Krol'dok (~50). Anything under ~15 g/h (SM Library and Graveyard, Razorfen Kraul,
City of Dalaran, Ruins of Lordaeron, Spawn of Hakkar) isn't worth a lockout slot while Krol'dok
is available. They're kept in the ranking for comparison. Maraudon is covered by the Princess
loop and Alcaz Prison by its full clear.

## 6. Changes to the plan
- **Level 60:** Krol'dok at 60 is the plan. **Test Dire Maul East first** (~56, "maybe"); the
  Maraudon Princess loop (~41) is the reliable backup. Stratholme, LBRS, Shaper's Terrace,
  Scholomance and Blackmaw Hold come only after a test pack passes, or with raid gear after 9 Dec.

Builds on `dungeon-farms-prot-warrior-2026-11-23.md` (instance list, loot model, sources),
which this doc does not rewrite.
