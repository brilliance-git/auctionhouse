# Krol'dok Stronghold: farm model (2026-11-23)

Theorycraft for a solo Protection Warrior at level 47. Drop rates come from Wowhead "Drops" tabs
(screenshots supplied by hand, 1,453–2,069 kills sampled per boss). Every boss blue is
bind-on-pickup, so it's vendor income.

## Vendor prices
Real sell prices for every boss except Nar'gurk were read from Wowhead tooltips (a screen
recording supplied by the user, 2026-11-23). Nar'gurk's items are still estimates: the median
vendor price of Classic blues in the AH catalog with the same slot and type, at a similar
item level. That method was within ~15% on the items checked.

## Expected value per boss kill
| Boss | Drops: sell price (drop %) | EV per kill |
|---|---|---|
| **Slavecrusher Grox** | Slavecrusher Scepter 1g 72s 54c (35.17%), Resistance Breaker Spaulder 78s 29c (31.04%), Chain of Binding 52s 16c (33.04%), **Blueprint: Expert Campfire ~27g on the AH (4.54%)** | **2g 19s** (1g 16s of it from the blueprint) |
| **Overlord Mugg** | Mugg's Jabber 2g 33s 36c (24.99%), Mugg's Crosser 2g 34s 20c (21.89%), Emblem of Slamming 94s 01c (20.98%), Strongly Scented Hood 70s 75c (24.31%); Eye of Mugg (quest item) 44%; **Krol'dok Ogre Key 14%** | **1g 47s** |
| War Handler Ashka | Bloodied Gutslicer 2g 38s 30c (36.44%), Worgbinder's Treads 1g 00s 64c (29.20%), War Handler's Gaze 71s 94c (34.37%) | 1g 41s |
| Bossman Toof | Toofbreaker 2g 03s 18c (36.21%), Band of Bossman 80s 70c (31.58%), Big-Belly Belt 40s 49c (32.21%) | 1g 12s |
| Twilight Commander Zarmok | Shadowlight Athame 1g 88s 48c (32.38%), Zarmok's Plated Signet 75s 97c (34.30%), Shadecaster's Leggings 75s 68c (31.69%) | 1g 11s |
| Nar'gurk | Krol'dok Warplate Chest ~1g 09s est. (26%), Warplate Helmet ~80s est. (28%), Chain of the Corruptor ~53s est. (36%); Tome of Twilight (quest item) 42% | ~70s (estimate) |
| Kroog (rare) | Black Horn Necklace, Kroog's Backscratcher | not counted: spawn rate unknown |
| **All 6 bosses** | | **~8g 00s per run** |

Zone-wide quest drops: Cultist Ear 4%, Twilight Bangle 2%. Very rare: Sturdy Junkbox and
Aquamarine (0.06% each).

## Per hour
- Bosses only: 5 runs × ~8.0g ≈ **~40 g/hr** (the blueprint is ~5.8 g/hr of that, and comes in
  ~25g lumps about every 4.4 hours).
- Plus elite trash coin and greys: **not yet measured.**
- Over half the expected value comes from 6 weapons worth 1g 72s–2g 38s each (Scepter,
  Gutslicer, Athame, Toofbreaker, Jabber, Crosser), so single hours will vary widely.

## Route rules
1. **The cap sets the target.** 5 instances an hour means a run can take up to 12 minutes,
   leaving ~10 minutes of killing after ~2 for exit and reset. Finishing faster than that
   earns nothing extra in the dungeon. Use leftover minutes for fishing instead.
2. **Kill all 6 bosses if the route fits in about 12 minutes.** Even the lowest-value bosses
   (Nar'gurk, ~0.7g) are worth killing when the time would otherwise go unused.
3. **If a full route runs over 12 minutes, cut the low-value parts.** Drop the lowest gold per
   minute first. That's Nar'gurk, unless his quest item (Tome of Twilight, 42%) or the
   Warplate tank pieces change his value. Mugg is now the second-best boss, so keep him. Never cut Grox.
4. **Trash:** clear what's in the way. Take extra melee packs only if they fit in the 12
   minutes. Avoid caster packs (Twilight cultists), because you get no rage from blocking.
   Measured coin per pull will decide whether optional packs are worth it.
5. The average run earns ~0.8g per minute. Any optional section that pays less than that per
   minute, and pushes the run over 12 minutes, should be cut.

## Still needed
1. **A timed test run:** the time at each boss kill, the time to exit and reset, gold before
   and after (greys vendored, blues kept), and the repair bill. Log it in `docs/farm-log.md`.
2. **Boss order and layout:** which bosses are on the main path and which need a detour, and
   which trash you can skip.
3. **Nar'gurk's sell prices:** Chain of the Corruptor, Krol'dok Warplate Helmet and
   Krol'dok Warplate Chest. These are the last estimated prices.
4. **Quest items:** what Tome of Twilight, Eye of Mugg, Cultist Ear and Twilight Bangle start
   or turn in for (gold, XP, rep), and whether any can be repeated.
5. **Krol'dok Ogre Key (14% from Mugg):** what it opens.
6. **Kroog:** how often he spawns, and his sell prices.
7. **Professions:** Skinning, for the wolves and worgs.
