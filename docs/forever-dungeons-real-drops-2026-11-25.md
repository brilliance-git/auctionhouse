# Forever-only dungeons re-modelled with real Wowhead drop tables (2026-11-25)

**Input:** `docs/wowhead-drops-forever-2026-11-25.md`, collected the same day from wowhead.com/forever
NPC "Drops" tabs. It covers Krol'dok, The Drowned City, Alcaz Prison, Shaper's Terrace,
Blackmaw Hold and Spawn of Hakkar, with 23 to 14,670 kills sampled per mob.

**Method:**
- I looked up every item ID in that file (125) and every named extra on the **Horde AH**.
- **Ever listed means BoE:** valued at the AH price after the 5% cut, demand-capped at a 10%
  share.
- **Never listed means BoP:** vendor only.

Reproduce with `python3 scripts/dungeon_farm_model.py --reasons`. Loops using these boss
tables show `real-rate` in the `blues` column.

## Short answer
- **Every boss and trash blue in the file is bind-on-pickup.** None of the 121 blue or epic
  gear IDs has ever been listed on the Horde AH. That includes the **Krol'dok Warplate
  Pauldrons, Legplates and Gauntlets** and **Outrider's Gloves** from Twilight Outrider trash.
  So **Krol'dok gains nothing from its trash blues** beyond their vendor price.
- **The blue value itself is still estimated.** The API only knows AH-seen items, so it has no
  vendor price for these BoP blues; they still use the item-level curve. Now **real:** blues
  per kill, item levels, and every sellable extra.
- **Does the ranking change?**
  - **At the top, no.** Krol'dok (~50 g/h, real sell prices) is still the best farm a solo prot
    warrior can count on.
  - **Shaper's Terrace moves up.** A loop that includes **Nanaya** reaches **~67–72 g/h**
    conservatively and ~100–113 optimistically. Nanaya drops a Maker's Spark 94% of the time,
    a level-60 green 99% and a blueprint 5.5%. That's now the highest-value loop in the model,
    ahead of Strat Living (59–71). But it's still **"unlikely" solo** (elites 58–60, no solo
    data), and Nanaya's position on the route isn't confirmed.
  - **Blackmaw Hold drops slightly** (35 → 33 conservative): Elder Shaman Bloodmane averages
    only 0.80 blues per kill.
  - **Alcaz Prison** (~29) and **The Drowned City** (~16) are essentially unchanged.

## 1. Checks
| Claim | Result |
|---|---|
| Forever bosses drop ~1 blue per kill | **Confirmed.** Main bosses range 0.89–1.02 (Nar'gurk 0.89, Deathless Marrow 0.90, Mugg 0.92, Withermaw 0.92). **Lowest: Elder Shaman Bloodmane 0.80** |
| Titanosaur drops ~1.5 blues | **Confirmed: 1.52 per kill** (241 kills) |
| Nanaya: green ~99%, Maker's Spark ~94% | **Confirmed** (546 kills). Also Blueprint: Arcane Forge 5.5% and Freya's Sigil 1.1% |
| Krol'dok Warplate trash pieces and Outrider's Gloves | **All BoP** (never listed). Outrider's Gloves 4.8%; Pauldrons 1.0%, Legplates 0.9%, Gauntlets 0.8% per Twilight Outrider kill. Gear for you, no gold |
| Expert Campfire blueprint (Grox) | **4.3%** on 2,047 kills (was 4.54% on 1,453). Krol'dok boss value 8.31 → **8.25g per run** |

## 2. Sellable extras (Horde AH, 17–25 Nov 2026)
| Item | Source and rate | AH price | Vendor | Est. sold per day | Counted as |
|---|---|---|---|---|---|
| **Maker's Spark** | Nanaya 94% | ~2.70g | **2.50g** | ~29 | The AH takes ~0.1 an hour at a 10% share, so almost all go to the vendor: **~2.35g per Nanaya kill** |
| BoE green (ilvl 56–63) | Nanaya 99% | median 3.00g, lower quartile 2.00g (467 items) | median 1.36g | many items | lower quartile after the cut: **~1.88g per kill** |
| Blueprint: Arcane Forge | Nanaya 5.5% | ~90g (≈4 listed) | 12g | no sales seen | vendor price: **0.66g per kill** (AH upside ~4.7g if one sells) |
| **Blackmaw Pouch** | each Blackmaw boss 8–13%, trash 4% | ~85s | 2s | ~330 | AH: **~0.08g per boss kill** |
| Mote of Unstable Magic | bosses ~6%, Legashi 26%, Druid 39% | ~11s | 2s | ~10,300 | not counted (~0.01g per boss kill) |
| **Pattern: Timbermaw Tunic** | Blackmaw Druid (trash) 6.3% | ~155–180g (≈5 listed) | 75s | no sales seen | **not counted.** A real upside of ~10g per Druid kill if the market takes one now and then |
| Plans: Breastplate of Salvation | Legashi Summoner 4.6% | never listed | ? | — | BoP or not yet seen; no value |
| Ancient Gurubashi Idol | Deathless Marrow 51% | never listed | ? | — | no value |
| Sealed Expert's / Artisan's Writ | trash ~0.7% | ~31s / ~40s | 0 | 360–560 | negligible |
| Codex: Prayer of Fortitude | Strashaz Enchantress 0.6% | ~85s | 77s | — | negligible |
| Fel-Tainted Flesh | Legashi 5% | ~9s | 2s | ~400 | negligible |

**Trash greens (not counted in the totals):** the main trash mob in each dungeon drops a BoE
green on **18–38% of kills**: Risen Sentry 38%, Legashi 23%, Twilight Outrider 22%, Blackmaw
Druid 21%, Strashaz Enchantress 18%. The model counts no trash greens for any dungeon, because
the Classic dungeons have no equivalent data and adding them only here would skew the
comparison.
- **For Krol'dok** that's a possible **+5–8 g/h** upside: ~40 trash kills a run × ~20% ×
  ~0.7–1g per green, if the market absorbs them.

## 3. Updated loops (conservative / anchored g/h)
| Band | Loop | Before | Now | Tier |
|---|---|---|---|---|
| Levelling | Krol'dok Stronghold | 49 | 49 (boss 41.2 real + trash 7.9 estimate) | maybe |
| Levelling | The Drowned City (6 bosses, now with Primeval Elemental instead of the rare Gill) | 16 / 25 | 16 / 25 | maybe |
| Levelling | Alcaz Prison: first four bosses (15 min) | 24 / 39 | 23 / 38 | unlikely |
| 60 | **Krol'dok at 60** | 50 | **50** | **reliable** |
| 60 | Alcaz Prison: full clear (15 min) | 29 / 48 | 29 / 48 | maybe |
| 60 | **Shaper's Terrace: Titanosaur + Nanaya loop (15 min)**, new | — | **72 / 113** | unlikely |
| 60 | Shaper's Terrace: Titanosaur + Nanaya loop (12 min), new | — | 67 / 100 | unlikely |
| 60 | Shaper's Terrace: dinosaur loop (12 min) | 46 / 82 | 54 / 95 | unlikely |
| 60 | Blackmaw Hold: first bosses (15 min) | 35 / 59 | 33 / 55 | unlikely |

- **The Shaper's Terrace Nanaya loop:** Mount in > Titanosaur > Venomridge > Thunderhoof >
  Direhorn Matriarch > **Nanaya** > teleport out.
  - About **20 g/h of its value is sellable extras** from Nanaya: Maker's Spark, green and
    blueprint.
  - The rest is boss blues at ilvl 63, with Titanosaur alone giving 1.52 per kill.
- **Blackmaw's 12-minute variant** now skips Bloodmane, since he has the lowest blue rate.

## 4. Verdict
- **Krol'dok stays the plan**, both while levelling and at 60.
- **At 60, the Shaper's Terrace Nanaya loop is the highest-value target in the model.**
  - It overtakes Strat Living as the "best if it's soloable" farm, and its income doesn't
    depend on the Righteous Orb market.
  - **Test one dinosaur pull and Nanaya** before planning on it, or come back with raid gear
    after 9 Dec.
  - Mining adds ~5.8 g/h of Thorium on top.
- **Blackmaw Hold and Alcaz Prison stay below Krol'dok** on every curve.

## 5. Real vs estimated
| Part | Status |
|---|---|
| Blues per kill, item levels, extra drop rates (6 Forever dungeons) | **real** (Wowhead Forever, 2026-11-25) |
| BoP vs BoE | **real** (Horde AH: never listed means BoP) |
| Vendor value of BoP blues | **estimated** (item-level curve). Krol'dok excepted: real tooltip sell prices |
| Maker's Spark, Blackmaw Pouch, greens, blueprint | **real** Horde AH prices; demand caps estimated from sales per day |
| Routes, boss order (Nanaya's position especially), minutes, trash counts | **estimated** |
| Solo viability | **judgement** (Classic-era mechanics) |
