# Gear for farming at 60: solo Protection Warrior (2026-11-25)

**Question:** what gear should a level-60 prot warrior pick up to farm the loops in this repo
(Krol'dok, Maraudon Princess, ZF, then testing Dire Maul East and harder)? Includes every
item in WoW: Forever that **damages attackers** (when struck or on block) or **heals you** (on
hit, when struck or on block).

**Sources:**
- Icy Veins, Forever Protection Warrior gear (updated 24 Nov 2026) and stat priority pages.
- Icy Veins news on Enchant Weapon – Recovery (19 Nov 2026).
- Wowhead Forever item database: "Effect text" and "Struck in combat effect" filters, and item
  tooltips (25 Nov 2026).
- This repo's real drop tables and Horde AH prices.

Horde AH prices for the BoE items are in section 6. They come from the live Horde AH, never
the neutral house.

## Short answer
1. **Sustain first.** Put a healing enchant on your weapon:
   - **Enchant Weapon – Recovery** is a new Forever enchant. You buy it with Merchant's Favor.
   - **Enchant Weapon – Lifestealing** is the formula that lists at ~50g on the Horde AH.
   - Either one cuts the downtime between pulls, which is where solo farming time goes.
2. **Damage on block.** Add a **Thorium Shield Spike** to your shield, and pick up the
   **Girdle of Extracted Answers**, a plate belt from Alcaz Prison that deals 20–30 damage
   every time you block. In big pulls you block a lot, and in Forever every block also gives
   5 rage.
3. **Skullflame Shield** is the one item that does both: it steals 270 life when struck (3%)
   and deals 90–140 Fire damage to everything around you (2%). It's BoE, so it's a purchase,
   but at ~515g on the Horde AH it's a later buy (section 6).
4. **Stamina and Armor next.** Icy Veins' defensive priority is Stamina > Armor > Agility >
   Avoidance > Defense. The hit, expertise and defense caps are set against level-63 bosses.
   Against our out-levelled farms (mobs 42–52) they don't matter, so don't pay for them yet.
5. **Pick up what drops on your own loops:**
   - Blackstone Ring from the Maraudon Princess (44%).
   - Razor Gauntlets from Alzzin and Satyr's Bow from Zevrim, both on the Dire Maul East loop.
   - Fist of the Damned from Ogom in Sunken Temple: a life-stealing weapon with +2 Defense.

## 1. Forever mechanics that decide what's worth having
- **Rage from defence:**
  - Shield Specialization 5/5 gives +5% block chance and **5 rage per block**.
  - Master of Defense 2/2 gives **5 rage per dodge or parry** while you have a shield equipped.
  - So in a 10–15 mob pull, block chance and avoidance are rage, not only mitigation.
- **Block Value** raises damage stopped and Shield Slam damage. Strength gives 1 Block Value
  per 20.
- **Thunder Clap and Revenge scale with Attack Power,** and Sunder Armor threat scales with AP
  in Forever. AP and Strength speed up AoE clears.
- **Caps are for bosses:**
  - 8% hit, 6.5% / 14% expertise and 440 defense are all set against level-63 bosses.
  - Shield Block already covers crits, which is why Icy Veins ranks Defense last.
- **Zone-doubled effects:** some Forever items double in Strongholds and Cities. **Krol'dok is
  a Stronghold**, so these are worth more there.
  - Krol'dok Battlegear's 4-piece heal on block.
  - The Lion Horn of Stormwind.
  - Defender's Grip Stabilizer.

## 2. Heal on hit, when struck, or on block
| Item | Effect (Wowhead Forever tooltip) | Req | Bind | Source | For farming |
|---|---|---|---|---|---|
| **Enchant Weapon – Recovery** | Heals 5% of max health when your melee attack is dodged or parried; 10 s internal cooldown | Enchanting 140 | – | Recipe: 45 Merchant's Favor from Beneris, Durotar Supply and Logistics (just west of the Crossroads). Mats: 6 Soul Dust, 4 Large Glimmering Shard, 6 Greater Astral Essence, 4 Pyrite, 4 Silver Ore | **Best sustain per gold.** Procs less against lower-level mobs (they dodge and parry less), so it's weaker at Krol'dok and Maraudon, better at DME and up |
| **Enchant Weapon – Lifestealing** | Chance on hit to steal life | Enchanting | – | Formula ~50g on the Horde AH (thin, ~6 listed) | Procs on your hits, so it works on any mob level |
| **Skullflame Shield** | When struck in melee: 3% chance to steal 270 life. When struck: 2% chance of 90–140 Fire damage to all targets around you. 2256 armor, 40 block | 54 | **BoE** | World drop | **Best farming shield.** Heal and AoE together, and big pulls mean many procs |
| Krol'dok Battlegear (4-piece) | Chance on block to heal; **doubled in Strongholds** | – | BoP | Krol'dok Stronghold | Built for the baseline farm (see `kroldok-model-2026-11-23.md`) |
| **Fist of the Damned** | Chance on hit: steals 56 life. +2 Defense | 49 | BoP | Ogom the Wretch, Sunken Temple | **On the Sunken Temple "maybe" loop** (Jammal'an + Ogom) |
| Wraith Scythe | Chance on hit: steals 49 life (×2 vs Undead) | 51 | BoP | Boss drop, Blackrock Depths | BRD isn't one of our loops |
| The Cruel Hand of Timmy | Chance on hit: steals 85 life | 55 | BoP | Timmy the Cruel, Stratholme | "Unlikely" tier dungeon |
| Eater of the Dead | Chance on hit: steals 21 life (×3 vs Undead), +16 AP | 49 | BoP | Ogom the Wretch, Sunken Temple | Weaker than Fist of the Damned |
| Demon Forged Breastplate | When struck: 3% chance to steal 240 life over 4 s | 52 | BoE | Crafted, Blacksmithing | A chest with a heal proc; weaker stats than the set chests |
| Julie's Dagger | Chance on hit: heals 78 over 12 s | 50 | BoE | World drop | Small |
| Truesilver Breastplate | When struck: 3% chance to heal 60–100 | 44 | BoE | Crafted, Blacksmithing | Too small at 60 |
| Maw of Min'loth | When struck in melee: 10% chance to steal 40 life (3 s cooldown) | 37 | BoP | Min'loth, The Drowned City | Too low-level |
| Lifegiving Gem | Use: heal 15% and +15% max health for 20 s (5 min cooldown) | 60 | BoP | Broodlord, Blackwing Lair | **Not in the game yet** (raid not released) |

## 3. Damage back to attackers (reflect and on-block)
| Item | Effect (Wowhead Forever tooltip) | Req | Bind | Source | For farming |
|---|---|---|---|---|---|
| **Girdle of Extracted Answers** | **20–30 Physical damage every time you block** (plate waist) | 48 | BoP | The Questioner, Alcaz Prison | **Strongest on-block item you can farm.** Alcaz is a "maybe" (~29 g/h) |
| **Thorium Shield Spike** | Attaches to your shield; deals damage every time you block | Blacksmithing 250 | BoE | Crafted | Cheap, and works on any shield |
| Force Reactive Disk | On block: an electrical charge damages **all nearby enemies** (1 s cooldown; can damage the shield) | 60 | BoE | Crafted, Engineering; the schematic comes from Molten Core | **Not in the game yet:** Molten Core isn't out. The only AoE-on-block shield once it is |
| **Razor Gauntlets** | When struck in combat: 7 Nature damage to the attacker | 54 | BoP | Alzzin the Wildshaper, Dire Maul East | **On the DME loop.** Hits every time you're struck |
| Crest of Retribution | +1.2% block chance; 6–39 Physical every block | 55 | BoP | Ramstein the Gorger, Stratholme | "Unlikely" tier dungeon |
| Aegis of the Scarlet Commander | 13–15 Holy every block | 39 | BoP | Scarlet Commander Mograine, SM Cathedral | From our filler farm, but low-level shield stats |
| Naglering | +5 Defense; 3 Arcane to the attacker when struck | 54 | BoP | Golem Lord Argelmach, Blackrock Depths | Small |
| Skullflame Shield | See section 2: 2% chance of 90–140 Fire to everything around you when struck | 54 | BoE | World drop | |
| Vile Protector | When struck: 5% chance of 105–175 Shadow to the attacker | ~28 | BoP | Quest (Compendium) | Too low-level |
| Freezing Band, Girdle of Reprisal, The Green Tower | 1% "when struck" procs | 36–47 | mixed | Various | Too rare to matter |
| Bramblebark Barrier, Bristlecone Cloak, Razorsteel Shoulders, Flame Seared Signet | 2–3 damage to the attacker when struck | 52–59 | mixed | Mount Hyjal quests (Bramblebark, Bristlecone), a quest reward (Razorsteel), Terrorspark in Burning Steppes (Signet) | Negligible |
| Fetish of Chitinous Spikes | Use: 25 Nature damage to attackers for 30 s (3 min cooldown) | 60 | BoP | Buru the Gorger, Ruins of Ahn'Qiraj | **Not in the game yet** (raid not released) |

**How much is it worth?** A rough estimate, not measured: holding 10–15 mobs that each swing
about every 2 s means ~5–7 hits a second.
- **Razor Gauntlets** at 7 damage per hit add roughly 35–50 damage per second to the whole pack.
- **On-block items** add per block: the Girdle's 25 average, plus the Shield Spike and any
  shield effect. With ~20–30% block chance and Shield Block up, that's roughly 1–2 blocks a
  second. Each block also gives 5 rage.
- These effects stack, and they're damage you don't spend rage or time on.

## 4. Core pre-raid gear (Icy Veins, Forever)
Icy Veins lists four pre-raid sets: Balanced, Threat, Survivability and Affordable. For solo
farming, use **Survivability** as the target and **Affordable** as the path.

| Slot | Survivability pick | Affordable pick | Source |
|---|---|---|---|
| Head | Faceguard of Heroism | Helm of the Executioner | Dungeon Set 2 / Baron Rivendare (Strat) |
| Neck | Horn of Ve'han | Horn of Ve'han | Quest "Work Well Done" |
| Shoulders | Pauldrons of Heroism | Spaulders of Valor | Dungeon Set 2 / Rend Blackhand (UBRS) |
| Cloak | Shifting Cloak | Stalwart Cloak | Leatherworking / Pix Xizzix vendor (75) |
| Chest | Breastplate of Heroism | Burnished Pridescales | Dungeon Set 2 / Unbound Spirit (Blackmaw Hold) |
| Bracers | Vigorsteel Vambraces | Bracers of Valor | Darkmaster Gandling (Scholo) / **BoE** |
| Hands | Handguards of Heroism | **Gauntlets of Valor** | Dungeon Set 2 / **BoE, ~45g on the Horde AH** |
| Waist | Waistguard of Heroism | Belt of Valor | Dungeon Set 2 / **BoE** |
| Legs | Warmaster Legguards | Handcrafted Mastersmith Leggings | Rend Blackhand / Goraluk Anvilcrack (UBRS) |
| Feet | Sabatons of Heroism | Shalehusk Boots | Dungeon Set 2 / Panzor the Invincible (BRD) |
| Rings | Cutthroat's Signet + Myrmidon's Signet | Cutthroat's Signet + **Blackstone Ring** | Pix Xizzix vendor (75) / **BoE** / **Princess Theradras, Maraudon (44%)** |
| Trinkets | Adaptive Combat Assistant + Royal Seal of Eldre'Thalas | Adaptive Combat Assistant + Cleansed Vilebranch Medallion | Pix Xizzix vendor (125) / Quest "Codex of Defense" (Dire Maul) / **Alliance-only quest: skip on Horde** |
| Main hand | Scaleguard Scimitar (12 Block Value) | Scaleguard Scimitar | Direhorn Matriarch, Shaper's Terrace |
| Shield | The Immovable Object (27 Block Value) | Draconian Deflector | Alterac Valley Exalted / General Drakkisath (UBRS) |
| Ranged | Carapace Spine Crossbow | Deep Jungle Rifle | Nerub'enkan (Strat) / Thunderhoof (Shaper's Terrace) |

**Notes for this character:**
- **Dungeon Set 2 (Heroism)** is a long questline. On Horde it starts with Mokvar in
  Orgrimmar and needs the Valor pieces, Argent Dawn Honored and UBRS access. It's the long-term
  goal; you don't need it for the reliable farms.
- **Pix Xizzix**, the vendor in Stranglethorn, sells several useful pieces:
  - Stalwart Cloak and Cutthroat's Signet (75 each), and Adaptive Combat Assistant (125).
  - Valiant's Waistguard (100).
  - **Defender's Grip Stabilizer:** +13 Defense, and on use +8% block chance for 15 s,
    **doubled in Strongholds**, so it's strong at Krol'dok.
  - Icy Veins shows the price without the currency. Check his currency in game.
- **The Lion Horn of Stormwind** (BoE trinket, req 58): +8 Defense. When struck, a chance to
  add 725 armor to the party for 30 s, **doubled in Strongholds and Cities**.
- **Horde substitutes:**
  - The Cleansed Vilebranch Medallion is Alliance-only. Use the Royal Seal of Eldre'Thalas, the
    Lion Horn or Defender's Grip Stabilizer instead.
  - Blackhand's Breadth comes from "For The Horde!" on Horde.
- **For solo farming, swap two of Icy Veins' choices:**
  - Use **Skullflame Shield** over The Immovable Object.
  - Use **Recovery or Lifestealing** over Crusader on the weapon.
  - Icy Veins' list is built for tanking groups, not for staying alive alone.
- **Enchants** (Icy Veins' survivability set):
  - Shield: Greater Stamina. Bracer: Superior Stamina. Chest: Greater Stats.
  - Head and legs: Lesser Arcanum of Constitution.
  - Neck: Deflection. Cloak and gloves: Agility. Boots: Speed.
  - Shoulders: Chromatic Mantle of the Dawn.

## 5. Buying and farming order
1. **Weapon enchant: Recovery or Lifestealing.** Cheapest sustain.
2. **Thorium Shield Spike** on your current shield (~9.50g).
3. **Pix Xizzix pieces and Defender's Grip Stabilizer:** Krol'dok benefits most.
4. **Valor BoE pieces** now that they're cheap: Gauntlets ~23g, Bracers ~7g, Belt ~5g on the
   Horde AH (section 6).
5. **Farm your own upgrades while you farm gold:**
   - Blackstone Ring on the Princess loop.
   - Fist of the Damned from Ogom.
   - Girdle of Extracted Answers from Alcaz.
   - Razor Gauntlets and Satyr's Bow on the DME test runs.
6. **Skullflame Shield only later,** once gold allows: ~515g on the Horde AH, about 10 hours of
   Krol'dok for one proc item. Then the Heroism questline, over time. (The **Force Reactive
   Disk** isn't in the game until Molten Core is released.)
7. Consumables for the DME and Strat tests (from the viability doc): Free Action Potions,
   Troll's Blood potions, and engineering explosives.

## 6. Horde AH prices for the BoE items
Horde AH only (house 114), from `scripts/item_report.py`, 25 Nov 2026 (history from 17 Nov).
"Lowest now" is the cheapest current listing; "after cut" is what you'd get selling at that
price (×0.95). The trend is shown only where it matters.

| Item | Lowest now | After cut | Listings now | Note |
|---|---|---|---|---|
| **Skullflame Shield** | **515g** | 489g | 8 | Median ~576g over the week. **Far too expensive for the gain at our farm rates** (~10 h of Krol'dok) |
| Thorium Shield Spike | **9.50g** | 9.03g | 8 (24 items) | Liquid: ~33 sold a day. Cheap |
| Force Reactive Disk | — | — | **none** | **Never listed:** it isn't in the game yet (the schematic comes from Molten Core, which isn't out) |
| Demon Forged Breastplate | 85g | 81g | 2 | Falling (median ~130g, from ~176g → ~85g) |
| The Lion Horn of Stormwind | 750g | 713g | 2 | Very thin; asking prices swing (up to 10,000g) |
| Gauntlets of Valor | **23g** | 22g | 18 | Falling (60g → ~33g); was ~45g on 22–24 Nov |
| Belt of Valor | **5.01g** | 4.76g | 62 | Falling (20g → ~5g) |
| Bracers of Valor | **6.88g** | 6.54g | 10 | Falling (12.5g → ~6.5g) |
| Myrmidon's Signet | 50g | 47.5g | 20 | Easing (75g → 59g) |
| Julie's Dagger | 6.00g | 5.70g | 11 | |
| Formula: Enchant Weapon – Lifestealing | **49.40g** | 46.93g | 6 | Down from ~199g at the start of the week |
| Invulnerable Mail | 85g | 81g | 5 | Falling (150g → ~99g) |
| Soul Dust | 4.2s | | 1,615 items | Recovery needs 6: **~0.25g** |
| Large Glimmering Shard | 36.8s | | 1,807 items | Recovery needs 4: **~1.47g** |
| Greater Astral Essence | 15.0s | | 1,189 items | Recovery needs 6: **~0.90g** |
| Pyrite | 2.6s | | 3,013 items | Recovery needs 4: **~0.10g** |
| Silver Ore | 7.3s | | 708 items | Recovery needs 4: **~0.29g** |

- **No listings:** Force Reactive Disk only, because it isn't in the game yet. Everything else is on the Horde AH, though The Lion
  Horn of Stormwind and Demon Forged Breastplate have only 2 listings each.
- **Enchant Weapon – Recovery costs ~3.0g in materials** (plus 45 Merchant's Favor and an
  enchanter). That's far cheaper than the Lifestealing formula (~49g, and you'd still need an
  enchanter to apply it).
- **The Valor pieces are cheap and getting cheaper:** Gauntlets ~23g, Bracers ~7g, Belt ~5g,
  about 35g for all three.

## 7. Real vs judgement
| Part | Status |
|---|---|
| Item effects, required levels, bind types | **real** (Wowhead Forever tooltips, 25 Nov 2026) |
| Pre-raid lists and stat priority | **Icy Veins** (24 Nov and 4 Nov 2026); built for group tanking |
| Sources and drop rates on our loops | **real** (this repo's Wowhead drop tables) |
| Reflect and on-block damage per second | **rough estimate** (hits per second and block rate assumed) |
| Recovery proccing less against low-level mobs | **reported** (Icy Veins), not measured |
| Horde AH prices (section 6) | **real** (`scripts/item_report.py`, Horde AH, 25 Nov 2026) |

## 8. Checklist by slot: what to get, where, and how likely
Drop rates come from Wowhead Forever's kill counts: this repo's drop tables, plus item pages
checked on 25 Nov 2026. "Runs" is the average number of kills you'd need (1 ÷ drop rate). At
4–5 runs an hour, 5 runs is about an hour.

**How likely:**
- **Certain:** you buy it (Horde AH or a vendor).
- **Very likely:** a "reliable" farm with a 25%+ drop rate. Expect it within a few runs.
- **Likely:** a "reliable" farm at 15–25%, or a "maybe" farm at 25%+ **if** the one-pack test
  passes.
- **Possible:** a "maybe" farm at 15–25%, or a quest or currency that takes time.
- **Unlikely:** an "unlikely" (or group) dungeon, or a drop rate around 1%.

**Tarnished Undermine Real** is the currency Pix Xizzix (Stranglethorn) sells for, with a
cap of 165. Per ConquestCapped (not confirmed officially), it drops from the bosses of level
55+ dungeons. **The Dire Maul East loop earns it; Krol'dok and Maraudon don't.** The cap
means one 125-Real trinket at a time.

| Slot | Get now | Where | Chance | How likely | Later / goal |
|---|---|---|---|---|---|
| **Head** | Krol'dok Warplate Helmet (set) | Nar'gurk, Krol'dok | 27% (~4 runs) | **Very likely** | Faceguard of Heroism (Dungeon Set 2 questline: group content). Helm of the Executioner: Baron Rivendare, Strat, 17%: unlikely |
| **Neck** | Horn of Ve'han | Quest "Work Well Done" (level 60, both factions) | quest | **Likely** | – |
| **Shoulders** | Krol'dok Warplate Pauldrons (set) | Krol'dok trash (Twilight Outrider) | ~1% per Outrider | **Unlikely** soon; picks up over many runs | Spaulders of Valor: Rend Blackhand, UBRS, 19%: unlikely. Pauldrons of Heroism (questline) |
| **Cloak** | Stalwart Cloak | Pix Xizzix, 75 Reals | currency | **Possible** (needs DME runs for Reals) | – |
| **Chest** | Krol'dok Warplate Chest (set) | Nar'gurk, Krol'dok | 26% (~4 runs) | **Very likely** | Breastplate of Heroism (questline). Demon Forged Breastplate (heal proc): **certain**, ~85g BoE |
| **Wrist** | Bracers of Valor | Horde AH | ~7g | **Certain** | Vigorsteel Vambraces: Darkmaster Gandling, Scholomance, 12%: unlikely |
| **Hands** | Gauntlets of Valor | Horde AH | ~23g | **Certain** | **Razor Gauntlets** (reflect): Alzzin, DME, 18% (~6 runs): possible. Krol'dok Warplate Gauntlets: trash ~1%: unlikely |
| **Waist** | Belt of Valor | Horde AH | ~5g | **Certain** | **Girdle of Extracted Answers** (20–30 per block): The Questioner, Alcaz Prison, 30% (~3 runs): likely if Alcaz passes the test. Valiant's Waistguard: 100 Reals |
| **Legs** | Krol'dok Warplate Legplates (set) | Krol'dok trash (Outrider ~1%, Kroog the rare 1.4%) | ~1% | **Unlikely** soon | Handcrafted Mastersmith Leggings: Goraluk Anvilcrack, UBRS, 23%; Warmaster Legguards: Rend, 19%: both unlikely |
| **Feet** | Shalehusk Boots | Panzor the Invincible, BRD (a rare spawn) | 19% when he's up | **Possible** (BRD is "maybe", and Panzor doesn't always spawn) | Sabatons of Heroism (questline) |
| **Ring 1** | **Blackstone Ring** | Princess Theradras, Maraudon | 44% (~2 runs) | **Very likely** | – |
| **Ring 2** | **Zarmok's Plated Signet** (+11 block value) | Twilight Commander Zarmok, Krol'dok | 34% (~3 runs) | **Very likely** | Cutthroat's Signet: 75 Reals. Myrmidon's Signet: **certain**, ~50g BoE. Naglering: Golem Lord Argelmach, BRD, 22%: possible |
| **Trinket 1** | Defender's Grip Stabilizer (block chance doubled in Strongholds) | Pix Xizzix, 125 Reals | currency | **Possible** | – |
| **Trinket 2** | Royal Seal of Eldre'Thalas | Dire Maul class-book quest (Codex of Defense, per Icy Veins) | quest | **Possible** (needs the book from Dire Maul) | Adaptive Combat Assistant: 125 Reals (after the first trinket, because of the 165 cap) |
| **Main hand** | **Fist of the Damned** (steals 56 life, +2 Def) + **Recovery** enchant | Ogom the Wretched, Sunken Temple; enchant ~3g in mats | 34% (~3 runs) | **Likely** (Sunken Temple is "maybe") | Scaleguard Scimitar (12 block value): Direhorn Matriarch, Shaper's Terrace, 34%: unlikely |
| **Shield** | Current shield + **Thorium Shield Spike** | Horde AH | ~9.50g | **Certain** | **The Immovable Object**: Grunnda Wolfheart (AV vendor), ~79.50g at Alterac Valley Exalted: certain once Exalted. **Skullflame Shield**: ~515g BoE: certain, but costly. Draconian Deflector: General Drakkisath, UBRS, 23%: unlikely. Barrier Shield: Dire Maul North tribute chest: unlikely solo |
| **Ranged** | **Satyr's Bow** | Zevrim Thornhoof, DME | 18% (~6 runs) | **Possible** (DME is "maybe") | Deep Jungle Rifle: Thunderhoof, Shaper's Terrace, 31%: unlikely |

**Krol'dok Battlegear:** the Helmet and Chest come quickly from Nar'gurk, and with any two
Warplate pieces you get +100 armor. The 4-piece heal on block needs two of the ~1% trash
pieces, so expect it only after many runs. Don't skip Outriders.

**In short:**
- **Within a day of farming:** Helmet, Chest, both rings, the Valor bracers, gloves and belt,
  the Shield Spike and the Recovery enchant. That covers most slots for about 50g.
- **From the "maybe" tests:** Fist of the Damned, the Girdle, Razor Gauntlets and Satyr's Bow,
  plus Reals for the vendor pieces.
- **Group content or a long grind:** the Heroism set, the Scholomance, Stratholme and UBRS
  drops, and Shaper's Terrace.
