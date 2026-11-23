# Krol'dok Stronghold: farm model (2026-11-23)

Theorycraft for a solo Protection Warrior at level 47. Drop rates come from Wowhead "Drops" tabs
(screenshots supplied by hand, 1,453–2,069 kills sampled per boss). Every boss blue is
bind-on-pickup, so it's vendor income.

## How the vendor prices were estimated
Only three real sell prices are known: Zarmok's Plated Signet 75s 97c, Thornspike 65s 22c,
Mirror of Rath'mael 17s 68c. For every other blue, the estimate is the **median vendor price of
Classic blues in the AH catalog with the same slot and type, within ±1–4 item levels**.
Checked against the known prices: rings at ilvl 45 estimate ~87s (real 76s), daggers at ilvl 32
~58–67s (real 65s). Weapons, two-handers above all, sell for the most. Where no comparable
item existed, 80s is a placeholder.

## Expected value per boss kill
| Boss | Drops (rate) | EV per kill |
|---|---|---|
| **Slavecrusher Grox** | Scepter 1H mace 35% (~1g 96s), Chain of Binding 33% (~80s?), Spaulder 31% (~1g 03s), **Expert Campfire blueprint 4.54% (~27g on the AH)** | **~2g 43s** (1g 16s of it from the blueprint) |
| War Handler Ashka | Bloodied Gutslicer 2H 36% (~2g 61s), Gaze 34% (~85s), Treads 29% (~50s) | ~1g 37s |
| Twilight Commander Zarmok | Signet 34% (75s 97c real), Leggings 32% (~80s?), Athame 32% (~2g 27s) | ~1g 24s |
| Bossman Toof | Toofbreaker 36% (~2g 07s), Band 32% (~1g 08s), Belt 32% (~20s) | ~1g 16s |
| Nar'gurk | Chain of the Corruptor 36% (~53s), Warplate Helmet 28% (~80s?), Warplate Chest 26% (~1g 09s); Tome of Twilight (quest item) 42% | ~70s |
| Overlord Mugg | Jabber 25%, Hood 24%, Crosser 22%, Emblem of Slamming 21% (~53–80s each); Eye of Mugg (quest item) 44%; **Krol'dok Ogre Key 14%** | ~66s |
| Kroog (rare) | Black Horn Necklace, Kroog's Backscratcher | not counted: spawn rate unknown |
| **All 6 bosses** | | **~7g 57s per run** |

Zone-wide quest drops: Cultist Ear 4%, Twilight Bangle 2%. Very rare: Sturdy Junkbox and
Aquamarine (0.06% each).

## Per hour
- Bosses only: 5 runs × ~7.6g ≈ **~38 g/hr** (the blueprint is ~5.8 g/hr of that, and comes in
  ~25g lumps about every 4.4 hours).
- Plus elite trash coin and greys: **not yet measured.**
- About half the expected value comes from 4 weapon drops (Scepter, Gutslicer, Athame,
  Toofbreaker), so single hours will vary widely.

## Route rules
1. **The cap sets the target.** 5 instances an hour means a run can take up to 12 minutes,
   leaving ~10 minutes of killing after ~2 for exit and reset. Finishing faster than that
   earns nothing extra in the dungeon. Use leftover minutes for fishing instead.
2. **Kill all 6 bosses if the route fits in about 12 minutes.** Even the lowest-value bosses
   (Nar'gurk, Mugg, ~0.7g each) are worth killing when the time would otherwise go unused.
3. **If a full route runs over 12 minutes, cut the low-value parts.** Drop the lowest gold per
   minute first. That's probably Mugg or Nar'gurk, unless the quest items or the Ogre Key
   change their value. Never cut Grox.
4. **Trash:** clear what's in the way. Take extra melee packs only if they fit in the 12
   minutes. Avoid caster packs (Twilight cultists), because you get no rage from blocking.
   Measured coin per pull will decide whether optional packs are worth it.
5. The average run earns ~0.75g per minute. Any optional section that pays less than that per
   minute, and pushes the run over 12 minutes, should be cut.

## Still needed
1. **A timed test run:** the time at each boss kill, the time to exit and reset, gold before
   and after (greys vendored, blues kept), and the repair bill. Log it in `docs/farm-log.md`.
2. **Boss order and layout:** which bosses are on the main path and which need a detour, and
   which trash you can skip.
3. **Real sell prices** for the weapons, since they carry the estimate: Slavecrusher Scepter,
   Bloodied Gutslicer, Shadowlight Athame, Toofbreaker, Mugg's Jabber and Mugg's Crosser.
4. **Quest items:** what Tome of Twilight, Eye of Mugg, Cultist Ear and Twilight Bangle start
   or turn in for (gold, XP, rep), and whether any can be repeated.
5. **Krol'dok Ogre Key (14% from Mugg):** what it opens.
6. **Kroog:** how often he spawns, and his sell prices.
7. **Professions:** Skinning, for the wolves and worgs.
