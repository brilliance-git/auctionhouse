"""Rough g/h model for solo Protection Warrior dungeon farms (WoW: Forever).

    python3 scripts/dungeon_farm_model.py            # levelling band and level 60
    python3 scripts/dungeon_farm_model.py --band 60
    python3 scripts/dungeon_farm_model.py --reasons   # with the solo-viability reason per farm

Farms are ranked by solo viability tier (reliable > maybe > unlikely), then by g/h. The
tiers follow Classic-era mechanics; WoW: Forever's prot rework may change them.

Every number is an ESTIMATE. Nothing has been timed in-game yet (docs/farm-log.md).
Only Krol'dok's boss value uses real sell prices and drop rates (Wowhead tooltips, see
docs/kroldok-model-2026-11-23.md).

Per hour = min(5, 60 / minutes) x (boss blues + trash coin + other vendor loot per run)
           + AH drops (demand-capped)

Boss blues: one BoP blue per boss kill, valued with blue(ilvl):
  - "conservative" (the default, first column): scaled to the API catalog median at
    ilvl 60 (1.94g), i.e. Krol'dok anchor x 0.56;
  - "Krol'dok-anchored" (second column): 1.24g at ilvl 45.5, +7% per item level.
  The slope was fit on /v1/items, which only holds items seen on the AH (BoE) or in
  recipes, so it comes from BoE blues, not from the BoP boss blues being modelled.
  Krol'dok's own 8.31g per run is real and never scaled.

AH drops: each farm lists "Item=units/hour". If data/ is cached (scripts/fetch_snapshots.py)
they are valued live with farm_leaderboard.capped_gph at a 10% market share (units the AH
can't absorb count at vendor price). Without data/ the dated fallback values below are used.
"""
import argparse
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAP = 5                       # new instances per hour
KROL_BLUE = 1.24              # mean real vendor price of a Krol'dok boss blue (g), ilvl ~45.5
CONSERVATIVE = 1.94 / 3.47    # catalog median at ilvl 60 / anchored curve at ilvl 60 = 0.56
NON_ELITE = 0.4               # non-elite coin as a share of elite coin (a third to a half)
SHARE = 0.10
# Spawn of Hakkar's world-drop BoE greens: ~22% per kill (122 items at 0.2-1% each, Wowhead Forever)
# x ~1.04g net (median Horde AH min price 1.09g of 163 level 45-54 greens from the same name
# families, 17-23 Nov 2026; vendor median 0.74g). Rugged/Thick Leather (3% each) ignored.
SPAWN_GREENS = 0.25 * 0.70 + 0.27 * 0.85   # Wingveil Cloak (BoP green, vendor ~0.7g) + world greens at vendor

# Fallback demand-capped g/h per item at the given rate, from
#   python3 scripts/farm_leaderboard.py --top 0 --rate "Item=N" ...
# run 2026-11-23 on 152 Horde AH snapshots (17-23 Nov 2026). Refresh by caching data/.
FALLBACK = {
    ("Righteous Orb", 16): 33.6, ("Runecloth", 40): 2.09, ("Mageweave Cloth", 40): 1.66,
    ("Silk Cloth", 60): 1.11, ("Thick Leather", 5): 0.29, ("Heavy Leather", 5): 0.09,
    ("Red Wolf Meat", 5): 0.13, ("Living Essence", 10): 0.91, ("Heart of the Wild", 20): 0.80,
    ("Essence of Earth", 5): 2.32, ("Silk Cloth", 125): 2.32, ("Silk Cloth", 100): 1.85,
    ("Mageweave Cloth", 15): 0.62, ("Wool Cloth", 60): 0.97,
}


# ---- Real Wowhead Forever boss data (docs/wowhead-drops-forever-2026-11-25.md) ----
# boss -> (blues per kill, mean blue ilvl, other sellable value per kill in g).
# Every blue listed there was looked up on the Horde AH on 2026-11-25: none has ever been listed,
# so all are BoP. Their vendor prices aren't in the API (it only knows AH-seen items), so blue
# VALUE still comes from blue(ilvl); blues per kill and item levels are REAL.
# Sellable extras (Horde AH fill price, demand-capped by hand at a 10% share):
#   Blackmaw Pouch ~85s, ~330 sold/day (AH absorbs ~10%/boss): 0.10 x 0.81 = 0.08
#   Nanaya: Maker's Spark 94% (AH absorbs ~0.1/h, rest at the 2.50g vendor price) = 2.35;
#           green 99% x 1.37g (median vendor price of ilvl 56-63 greens; AH ~1.9g is upside) = 1.36;
#           Blueprint: Arcane Forge 5.5% x 12g vendor (AH ~90g but ~4 listed, no sales seen) = 0.66
#   Grox: Blueprint: Expert Campfire 4.3% (2,047 kills) x ~27g x 0.95 (in KROL_REAL_BOSS)
POUCH = 0.08
FOREVER_BOSSES = {
    # The Drowned City
    "Zul'Alai": (1.01, 39, 0), "Var'Taka": (1.01, 40, 0), "Captain Dreadrise": (1.01, 40, 0),
    "Deathless Marrow": (0.90, 41, 0), "Min'loth the Serpent": (1.01, 42, 0),
    "Primeval Elemental": (1.01, 40, 0), "Gill": (1.01, 40, 0),
    # Alcaz Prison
    "Overseer Wrex": (0.97, 52, 0), "The Questioner": (0.98, 53, 0),
    "Tidemistress Ca'zass": (0.94, 52, 0), "Katerina the Cleaner": (0.99, 54, 0),
    "Blazeroar": (0.98, 55, 0),
    # Blackmaw Hold
    "Withermaw": (0.92, 60, POUCH), "Bonesnout the Unbroken": (0.96, 60, POUCH),
    "Impaan the Imprisoner": (0.96, 59, POUCH), "Elder Shaman Bloodmane": (0.80, 61, POUCH),
    "Unbound Spirit": (0.97, 61, POUCH), "Varrox Bleakhoof": (0.96, 62, POUCH),
    # The Shaper's Terrace
    "Titanosaur": (1.52, 63, 0), "Venomridge": (0.94, 63, 0), "Thunderhoof": (0.94, 63, 0),
    "Direhorn Matriarch": (0.97, 63, 0), "Tor'Rel": (0.93, 63, 0),
    "Nanaya": (0.95, 63, 2.35 + 0.99 * 1.37 + 0.66),
}

# ---- Real Wowhead Forever data for five Classic dungeons (docs/wowhead-drops-classic-2026-11-25.md) ----
# Same structure: (BoP gear blues per kill, mean ilvl, other value per kill in g).
# - Ammo counted as "blues" by Wowhead (Doomshot, Rockshard Pellets, Miniature Cannon Balls) is removed:
#   never on the Horde AH (or 50c a unit for Rockshard Pellets), so ~0.
# - BoE blues (ever listed on the Horde AH) are moved out of the BoP count and valued at fill price x 0.95:
#   Shadowcraft Gloves 27.0g, Devout Gloves 25.6g, Gauntlets of Valor 45.0g, Piccolo of the Flaming Fire 5.0g,
#   Dreadmist Bracers 4.9g. Their markets are thin (8-30 listed), but these drop under 1 an hour.
# - Recipes that drop most runs are valued at their vendor price (Plans: Dark Iron Pulverizer 30s at 96%).
# - Boss greens are valued at the MEDIAN VENDOR price of greens in that level band: ilvl 48-55 0.85g,
#   ilvl 56-63 1.37g (511 / 487 greens). Strat and Scholomance bosses drop up to ~2.4 greens a kill,
#   ~20 an hour, more than the AH can absorb; selling some on the AH (lower quartile ~1.00g / ~2.00g,
#   after the cut ~0.95g / ~1.90g) is upside.
# The six Sunken Temple balcony trolls are NOT in Wowhead's list of mobs that drop a blue, so they drop none.
G55, G63 = 0.85, 1.37
CLASSIC_BOSSES = {
    # Sunken Temple
    "Atal'alarion": (1.02, 51, 0.05 * G55), "Jammal'an the Prophet": (1.00, 55, 0.05 * G55),
    "Ogom the Wretched": (0.98, 54, 0.01 * G55), "Shade of Hakkar": (1.91, 54, 0.05 * G55),
    "Shade of Eranikus": (1.74, 56, 0.56 * G55),
    "Spawn of Hakkar": (0.48, 52, 0.25 * 0.70 + 0.27 * G55),   # Wingveil Cloak (BoP green) + world greens
    # Lower Blackrock Spire
    "Highlord Omokk": (0.91, 60, 0.34 * G63),
    "Shadow Hunter Vosh'gajin": (0.70, 59, 0.17 * 27.0 * 0.95 + 0.02 * G63),
    "War Master Voone": (0.96, 60, 0.35 * G63),
    "Mother Smolderweb": (0.97, 60, 0.06 * G63 + 0.12 * 0.57),
    "Halycon": (0.91, 60, 0.03 * G63), "Gizrul the Slavener": (0.93, 61, 0.01 * G63),
    "Quartermaster Zigris": (0.94, 60, 0.11 * 4.85 * 0.95 + 0.05 * G63),
    # Blackrock Depths
    "Lord Roccor": (0.99, 54, 0.22 * G55), "Houndmaster Grebmar": (1.07, 53, 0.03 * G55),
    "High Interrogator Gerstahn": (1.03, 53, 0.04 * G55),
    "Ring of Law (random boss)": (1.00, 55, 0.06 * G55 + 0.96 / 6 * 0.30),
    "Pyromancer Loregrain": (1.03, 53, 0.21 * G55),
    # Stratholme Living
    "Malor the Zealous": (0.96, 60, 0.07 * G63), "Cannon Master Willey": (1.79, 61, 0.06 * G63),
    "Archivist Galford": (0.76, 61, 0.19 * 25.55 * 0.95 + 0.86 * G63),
    "The Unforgiven": (0.90, 57, 0.85 * G63), "Timmy the Cruel": (0.93, 60, 0.89 * G63),
    # Stratholme Undead
    "Magistrate Barthilas": (0.87, 59, 1.75 * G63), "Baroness Anastari": (1.25, 60, 1.81 * G63),
    "Nerub'enkan": (1.29, 60, 0.90 * G63), "Maleki the Pallid": (1.41, 61, 0.96 * G63),
    "Ramstein the Gorger": (0.70, 61, 0.15 * 45.0 * 0.95 + 2.44 * G63),
    # Scholomance
    "Rattlegore": (1.05, 61, 0.09 * G63), "Jandice Barov": (0.92, 61, 1.76 * G63),
    "Ras Frostwhisper": (1.86, 61, 1.84 * G63),
}
FOREVER_BOSSES.update(CLASSIC_BOSSES)
# LBRS Firebrand Pyromancer (trash): Pattern: Robe of the Archmage 19% (vendor 1.50g; ~26g on the AH but
# ~15 listed), Magister's Bindings 3% (BoE 6.4g), Cord of Elements 2% (BoE 13.5g) -> ~0.73g per kill.
PYRO = 0.19 * 1.50 + 0.03 * 6.39 * 0.95 + 0.02 * 13.51 * 0.95
# Krol'dok boss value per run: real Wowhead sell prices; Campfire updated 4.54% -> 4.3%.
KROL_REAL_BOSS = 8.31 - (0.0454 - 0.043) * 27 * 0.95


def blue(ilvl, scale):
    """Average vendor value (g) of one BoP boss blue at this item level."""
    return scale * KROL_BLUE * math.exp(0.071 * (ilvl - 45.5))


def coin(mob_level, elite=True):
    """Coin (g) per trash kill. ~4s per elite at level 45, from the Krol'dok guide video."""
    return 0.0009 * mob_level * (1 if elite else NON_ELITE)


def F(name, band, bosses, ilvl, kills, mob, minutes, conf, basis, notes,
      real_boss=None, elite=True, extra=0.0, ah=()):
    return dict(name=name, band=band, bosses=bosses, ilvl=ilvl, kills=kills, mob=mob,
                minutes=minutes, conf=conf, basis=basis, notes=notes, real_boss=real_boss,
                elite=elite, extra=extra, ah=ah)


# basis: "verified" = BoP and ~1 blue per boss checked on Wowhead; "assumed" otherwise.
FARMS = [
    # ---- levelling band (pre-60; dungeons whose mobs are ~35-55) ----
    F("Krol'dok Stronghold (full, Ogre Key)", "levelling", 6, None, 40, 44, 12, "medium", "verified",
      "Boss value from real prices and drop rates; trash and time estimated",
      real_boss=KROL_REAL_BOSS, ah=(("Thick Leather", 5), ("Heavy Leather", 5), ("Red Wolf Meat", 5))),
    F("The Drowned City (full)", "levelling", 6, 40, 30, 38, 12, "low", "assumed",
      "6 bosses; loot ilvl ~40 assumed (top of range + 2, like Krol'dok)"),
    F("Zul'Farrak (graveyard + 2 bosses)", "levelling", 2, 47, 60, 44, 12, "low", "assumed",
      "Big near-level zombie pull", ah=(("Mageweave Cloth", 40),)),
    F("Razorfen Downs (full)", "levelling", 5, 40, 35, 38, 12, "low", "assumed", "Some quilboar casters"),
    F("Uldaman (partial, 3 bosses)", "levelling", 3, 44, 30, 44, 12, "low", "assumed",
      "Long and spread out; mostly melee"),
    F("Scarlet Monastery Cathedral", "levelling", 3, 42, 40, 38, 10, "low", "verified",
      "SM boss gear never on the AH", ah=(("Silk Cloth", 60),)),
    F("Maraudon (Orange/Purple wing)", "levelling", 2, 49, 30, 47, 12, "low", "assumed",
      "Mobs near a levelling character's level; satyr casters"),
    F("City of Dalaran (full)", "levelling", 6, 34, 30, 31, 12, "low", "assumed",
      "Quest-unlocked; bosses and loot ilvl unconfirmed"),
    F("Razorfen Kraul (full)", "levelling", 5, 31, 30, 33, 12, "medium", "verified", "Thornspike 65s real"),
    F("Ruins of Lordaeron (full)", "levelling", 7, 24, 30, 18, 10, "medium", "verified",
      "Mirror of Rath'mael 18s real; Fermenter 7% x 6g", extra=0.4),
    F("Scarlet Monastery Armory", "levelling", 1, 40, 40, 38, 8, "low", "verified", "Herod only"),
    # Sunken Temple (Temple of Atal'Hakkar, ~50-55). Forever: every boss drops a guaranteed blue
    # (Warcraft Tavern). Spawn of Hakkar (the user's old farm, confirmed): level 50-51 elite beast in
    # the basement. Wowhead Forever NPC 5708, 1,265 kills: Slitherscale Boots 48%, Wingveil Cloak 25%
    # (ilvl 52, BoP) = ~0.73 blues per kill; plus ~20-25% chance of a world-drop BoE green.
    F("Sunken Temple: Spawn of Hakkar only", "levelling", 0.48, 52, 5, 50, 7, "low", "assumed",
      "One elite in the basement, then exit and reset; Wingveil Cloak BoP, boots never on the AH",
      extra=SPAWN_GREENS),
    F("Sunken Temple: 6 balcony trolls (chunk)", "levelling", 6, 53, 25, 52, 12, "low", "assumed",
      "Six troll minibosses on the balconies plus the trash between them"),
    # ---- level 60 ----
    F("Sunken Temple at 60: Spawn of Hakkar only", "60", 0.48, 52, 5, 50, 6, "low", "assumed",
      "One elite in the basement, then exit and reset", extra=SPAWN_GREENS),
    F("Sunken Temple at 60: 6 balcony trolls (chunk)", "60", 6, 53, 25, 52, 12, "low", "assumed",
      "Six troll minibosses, guaranteed blue each in Forever"),
    F("Stratholme Living, Scarlet side (chunked)", "60", 2, 60, 25, 58, 12, "low", "assumed",
      "Orbs ~3.2/run (Galford 84%, trash ~9.5%), mostly at the 2g vendor price; casters; "
      "no proven prot solo", ah=(("Righteous Orb", 16), ("Runecloth", 40))),
    F("Krol'dok Stronghold at 60", "60", 6, None, 40, 44, 11, "medium", "verified",
      "Same loot as in the levelling band, trivial mobs", real_boss=KROL_REAL_BOSS,
      ah=(("Thick Leather", 5), ("Heavy Leather", 5), ("Red Wolf Meat", 5))),
    F("Shaper's Terrace (4 bosses, teleport exit)", "60", 4, 62, 20, 59, 12, "low", "assumed",
      "10-11 encounters; mount inside; + ~5.8 g/h Thorium only with Mining"),
    F("Scholomance (partial, 4 bosses)", "60", 4, 60, 30, 59, 12, "low", "assumed",
      "Caster-heavy", ah=(("Runecloth", 40),)),
    F("Blackmaw Hold (partial, 4 bosses)", "60", 4, 60, 30, 58, 12, "low", "assumed",
      "Devotees drop nothing; normal boss kills only"),
    F("Dire Maul East (Lashers + 4 bosses)", "60", 4, 58, 40, 54, 12, "low", "assumed",
      "Non-elite melee lashers suit prot (non-elite coin)", elite=False,
      ah=(("Living Essence", 10), ("Heart of the Wild", 20))),
    F("Stratholme Undead (chunk, 3 bosses)", "60", 3, 60, 30, 58, 12, "low", "assumed",
      "Mostly melee undead", ah=(("Runecloth", 40),)),
    F("Alcaz Prison (full)", "60", 5, 53, 40, 51, 12, "low", "assumed",
      "5 bosses; no solo reports; Zarla Ober dragon phase"),
    F("Blackrock Depths (chunk, 4 bosses)", "60", 4, 56, 30, 54, 12, "low", "assumed", "Pick a wing"),
    F("Lower Blackrock Spire (chunk, 3 bosses)", "60", 3, 58, 30, 57, 12, "low", "assumed",
      "Orc packs, mostly melee"),
    F("Maraudon (Princess run)", "60", 4, 52, 25, 50, 12, "low", "assumed", "",
      ah=(("Essence of Earth", 5),)),
    # Scarlet Monastery at 60: mass-pull clears (gather a whole wing's humanoid packs and
    # AoE-tank them; normal pull-and-kill). Kill counts are estimates: Cathedral courtyard
    # ~25 + chapel ~35 elites (aggroing Mograine pulls the whole chapel); Armory ~65 elites.
    # Cloth: Silk on ~1 in 2-3 humanoid kills, Mageweave ~5%.
    F("SM Cathedral at 60 (mass pull, 3 bosses)", "60", 3, 42, 60, 38, 12, "low", "verified",
      "Whole-wing pulls of 34-40 elites; ~60 corpses to loot is the time limit",
      ah=(("Silk Cloth", 125), ("Mageweave Cloth", 15))),
    F("SM Armory at 60 (full clear, Herod)", "60", 1, 40, 65, 38, 12, "low", "verified",
      "Full trash clear plus Herod fits ~12 min", ah=(("Silk Cloth", 125), ("Mageweave Cloth", 15))),
    F("SM Library at 60 (2 bosses)", "60", 2, 38, 40, 36, 10, "low", "verified",
      "Loksey and Doan; fewer mobs", ah=(("Silk Cloth", 100),)),
    F("SM Graveyard at 60", "60", 1, 33, 40, 31, 8, "low", "verified",
      "Undead 26-36, low coin; Wool not Silk", ah=(("Wool Cloth", 60),)),
    F("Zul'Farrak at 60 (graveyard + 4 bosses)", "60", 4, 47, 60, 44, 12, "medium", "assumed",
      "Trivial at 60", ah=(("Mageweave Cloth", 40),)),
    F("Uldaman at 60 (6 bosses)", "60", 6, 44, 30, 44, 12, "low", "assumed", "Long"),
]


# ---- Solo viability for a Protection Warrior in pre-raid gear (Classic-era mechanics) ----
# reliable: out-levelled by ~10+, mobs barely hurt;
# maybe:    mobs a few levels under, or non-elite / melee-only packs; costs consumables;
# unlikely: elite packs at or near the farming level with casters, or huge near-level pulls.
# Rule of thumb (auto_tier) from the level gap; the explicit TIERS below override it with a reason.
TIER_ORDER = {"reliable": 0, "maybe": 1, "unlikely": 2}
# Consumables per hour for "maybe"/"unlikely" farms (ESTIMATE): ~10 healing potions + ~10 bandages
# + one elixir. Horde AH 2026-11-23: Greater/Superior Healing Potion ~4s, Heavy Mageweave
# Bandage ~6s, Heavy Runecloth Bandage ~14s, Elixir of Fortitude ~30s.
CONSUMABLES = {"levelling": 1.0, "60": 2.5}
# Reference level for auto_tier in the levelling band: the top of Krol'dok (40-45), where the
# band's main farm is current content. It is a band anchor, not the player's level.
BAND_REF = {"levelling": 45, "60": 60}


def auto_tier(player, mob, elite=True):
    gap = player - mob
    if gap >= 10:
        return "reliable"
    if gap >= 3 or not elite:
        return "maybe"
    return "unlikely"


TIERS = {
    # levelling band (gaps relative to a mid-40s character)
    "Krol'dok Stronghold (full, Ogre Key)": ("maybe",
        "Elites 42-45, a few levels below a mid-40s character; caster cultists, Terrorhowl fear, Mortal Strike; Battlegear "
        "4-piece heal is doubled there. Done while levelling, solo not yet timed"),
    "The Drowned City (full)": ("maybe", "Elites 35-40, well below a mid-40s character; boss mechanics unknown"),
    "Zul'Farrak (graveyard + 2 bosses)": ("unlikely",
        "Graveyard event pulls dozens of level 43-44 elites at once"),
    "Razorfen Downs (full)": ("maybe", "Elites 37-46; quilboar casters"),
    "Uldaman (partial, 3 bosses)": ("maybe", "Elites 41-47, mostly melee"),
    "Scarlet Monastery Cathedral": ("reliable", "Humanoids 34-40, small packs"),
    "Maraudon (Orange/Purple wing)": ("unlikely", "Elites 44-48, near a levelling character's level; satyr casters"),
    "City of Dalaran (full)": ("reliable", "Mobs ~28-33"),
    "Razorfen Kraul (full)": ("reliable", "Mobs 29-38"),
    "Ruins of Lordaeron (full)": ("reliable", "Mobs 15-20"),
    "Scarlet Monastery Armory": ("reliable", "Humanoids 34-40"),
    "Sunken Temple: Spawn of Hakkar only": ("maybe",
        "One level 50-51 elite beast, no packs, but above a mid-40s character; Acid of Hakkar. "
        "The user farmed it before (class and era not confirmed)"),
    "Sunken Temple: 6 balcony trolls (chunk)": ("unlikely",
        "Elite trolls 49-55 with priests and witch doctors (casters), plus Nightmare dragonkin elites"),
    # level 60
    "Sunken Temple at 60: Spawn of Hakkar only": ("reliable",
        "One level 50-51 elite (gap 9-10); the user farmed it before (class not confirmed)"),
    "Sunken Temple at 60: 6 balcony trolls (chunk)": ("maybe",
        "Elite trolls 49-55 (gap 5-11) with casters; dragonkin elites are hard solo"),
    "Krol'dok Stronghold at 60": ("reliable", "Elites 42-45 (gap 15+)"),
    "Zul'Farrak at 60 (graveyard + 4 bosses)": ("reliable", "Elites 43-48 (gap 12+)"),
    "Uldaman at 60 (6 bosses)": ("reliable", "Elites 41-47"),
    "Maraudon (Princess run)": ("reliable", "Elites 44-52 (gap 8-16); Princess hits hard"),
    "SM Cathedral at 60 (mass pull, 3 bosses)": ("reliable", "Humanoids 34-40 (gap 20+)"),
    "SM Armory at 60 (full clear, Herod)": ("reliable", "Humanoids 34-40"),
    "SM Library at 60 (2 bosses)": ("reliable", "Humanoids 33-39"),
    "SM Graveyard at 60": ("reliable", "Undead 26-36"),
    "Alcaz Prison (full)": ("maybe",
        "Elites 48-53 (gap 7-12); Tidemistress is a caster, Zarla Ober's dragon phase unknown"),
    "Dire Maul East (Lashers + 4 bosses)": ("maybe",
        "Lashers are non-elite melee 54 (ideal for rage); Alzzin and Lethtendris cast"),
    "Blackrock Depths (chunk, 4 bosses)": ("maybe",
        "Pick the lower-level wings (mobs ~50-54); many caster packs elsewhere"),
    "Stratholme Living, Scarlet side (chunked)": ("unlikely",
        "Elites 57-60 with Sorcerers, Battle Mages, Priests; no documented prot solo"),
    "Stratholme Undead (chunk, 3 bosses)": ("unlikely", "Elites 57-60; Maleki and acolytes cast"),
    "Scholomance (partial, 4 bosses)": ("unlikely", "Elites 58-60, caster-heavy necromancers"),
    "Shaper's Terrace (4 bosses, teleport exit)": ("unlikely",
        "Elites 58-60; no solo boss data (the mining route skips mobs)"),
    "Blackmaw Hold (partial, 4 bosses)": ("unlikely", "Elites 55-60; no solo reports"),
    "Lower Blackrock Spire (chunk, 3 bosses)": ("unlikely", "Elites 55-60 orc packs with casters"),
}



# ---- Named ~15-minute loops (docs/dungeon-loops-15min-2026-11-25.md) ----
# Each route replaces the old generic "chunk"/"partial" entry for its dungeon and is modelled
# twice: the 15-minute loop (4 runs/h) and a trimmed 12-minute variant (5 runs/h, the cap).
# Routes follow Classic-era layouts unless the dungeon is Forever-only; boss order, kill counts
# and minutes are ESTIMATES. Forever bosses drop a guaranteed blue (Warcraft Tavern).
# drops: (item, units per trash kill, units per run) -> priced on the Horde AH, demand-capped.
REPLACED = {
    "The Drowned City (full)", "Uldaman (partial, 3 bosses)", "Maraudon (Orange/Purple wing)",
    "Sunken Temple: 6 balcony trolls (chunk)", "Sunken Temple at 60: 6 balcony trolls (chunk)",
    "Stratholme Living, Scarlet side (chunked)", "Shaper's Terrace (4 bosses, teleport exit)",
    "Scholomance (partial, 4 bosses)", "Blackmaw Hold (partial, 4 bosses)",
    "Dire Maul East (Lashers + 4 bosses)", "Stratholme Undead (chunk, 3 bosses)",
    "Alcaz Prison (full)", "Blackrock Depths (chunk, 4 bosses)",
    "Lower Blackrock Spire (chunk, 3 bosses)", "Maraudon (Princess run)", "Uldaman at 60 (6 bosses)",
}
RUNECLOTH = ("Runecloth", 0.35, 0)
MAGEWEAVE = ("Mageweave Cloth", 0.35, 0)


def R(name, band, tier_, why, ilvl, mob, v15, v12, elite=True, drops=(), basis="assumed",
      conf="low", notes="", extra15=0.0, extra12=0.0):
    """v15 / v12 = (bosses, trash kills, minutes, route text); v12 may be None."""
    out = []
    for tag, v, extra in (("15 min", v15, extra15), ("12 min", v12, extra12)):
        if not v:
            continue
        bosses, kills, minutes, route = v
        boss_list = None
        if isinstance(bosses, (list, tuple)):
            boss_list = list(bosses)
            extra = extra + sum(FOREVER_BOSSES[b][2] for b in boss_list)
            bosses = sum(FOREVER_BOSSES[b][0] for b in boss_list)
            basis = "real-rate"
        runs = min(CAP, 60 / minutes)
        ah = tuple((item, round(runs * (kills * pk + pr))) for item, pk, pr in drops
                   if round(runs * (kills * pk + pr)) > 0)
        f = F(f"{name} ({tag})", band, bosses, ilvl, kills, mob, minutes, conf, basis,
              f"{route}. {notes}".strip(), elite=elite, ah=ah, extra=extra)
        f["route"] = route
        f["boss_list"] = boss_list
        out.append(f)
        TIERS[f["name"]] = (tier_, why)
    return out


ROUTES = [
    # ---- levelling band ----
    R("The Drowned City: full clear", "levelling", "maybe",
      "Elites 35-40, well below a mid-40s character; boss mechanics unknown", 40, 38,
      (["Zul'Alai", "Var'Taka", "Captain Dreadrise", "Deathless Marrow", "Primeval Elemental",
        "Min'loth the Serpent"], 40, 15,
       "Zul'Alai > Var'Taka > Captain Dreadrise > Deathless Marrow > Primeval Elemental > Min'loth, all trash"),
      (["Zul'Alai", "Var'Taka", "Captain Dreadrise", "Deathless Marrow", "Primeval Elemental"], 30, 12,
       "Same, skipping Min'loth at the end")),
    R("Uldaman: back-door loop", "levelling", "maybe", "Elites 41-47, mostly melee troggs and dwarves",
      44, 44, (4, 30, 15, "Back (Badlands) entrance > Ironaya > Obsidian Sentinel > Ancient Stone Keeper > Galgann Firehammer"),
      (3, 25, 12, "Ironaya > Obsidian Sentinel > Ancient Stone Keeper")),
    R("Maraudon: Orange wing", "levelling", "unlikely",
      "Elites 44-48, near a levelling character's level; satyr casters", 49, 47,
      (3, 30, 15, "Orange crystal side > Noxxion > Razorlash > Lord Vyletongue"),
      (2, 25, 12, "Noxxion > Razorlash"), drops=(MAGEWEAVE,)),
    R("Sunken Temple: trolls > Jammal'an + Ogom (+ Spawn)", "levelling", "unlikely",
      "Elite trolls 49-55 with priests and witch doctors (casters), Nightmare dragonkin elites",
      55, 52, (["Jammal'an the Prophet", "Ogom the Wretched", "Spawn of Hakkar"], 35, 15,
       "Six balcony trolls (no blues; they open the way) > Jammal'an > Ogom > basement for Spawn of Hakkar > exit"),
      (["Jammal'an the Prophet", "Ogom the Wretched"], 30, 12, "Six balcony trolls > Jammal'an > Ogom"),
      drops=(MAGEWEAVE,),
      notes="Real Wowhead data: the balcony trolls drop no blues"),
    R("Alcaz Prison: first four bosses", "levelling", "unlikely",
      "Elites 48-53, above a mid-40s character; Tidemistress is a caster", 53, 51,
      (["Overseer Wrex", "The Questioner", "Tidemistress Ca'zass", "Katerina the Cleaner"], 35, 15,
       "Overseer Wrex > The Questioner > Tidemistress Ca'zass > Katerina the Cleaner"),
      (["Overseer Wrex", "The Questioner", "Tidemistress Ca'zass"], 30, 12,
       "Overseer Wrex > The Questioner > Tidemistress Ca'zass")),
    # ---- level 60 ----
    R("Uldaman at 60: back-door loop", "60", "reliable", "Elites 41-47", 44, 44,
      (6, 30, 15, "Back entrance > Ironaya > Obsidian Sentinel > Ancient Stone Keeper > Galgann > Grimlok > Revelosh"),
      (5, 25, 12, "Same without Revelosh")),
    R("Maraudon at 60: Princess loop", "60", "reliable",
      "Elites 44-52 (gap 8-16); Princess Theradras hits hard", 52, 50,
      (5, 30, 15, "Orange side > Noxxion > Razorlash > Landslide > Rotgrip > Princess Theradras"),
      (4, 25, 12, "Noxxion > Landslide > Rotgrip > Princess Theradras"),
      drops=(("Essence of Earth", 0, 1), RUNECLOTH)),
    R("Sunken Temple at 60: trolls > Jammal'an + Ogom (+ Spawn)", "60", "maybe",
      "Elite trolls 49-55 (gap 5-11) with casters; dragonkin elites are hard solo", 53, 52,
      (["Jammal'an the Prophet", "Ogom the Wretched", "Spawn of Hakkar"], 35, 15,
       "Six balcony trolls (no blues) > Jammal'an > Ogom > Spawn of Hakkar > exit"),
      (["Jammal'an the Prophet", "Ogom the Wretched"], 30, 12, "Six balcony trolls > Jammal'an > Ogom"),
      drops=(MAGEWEAVE,)),
    R("Alcaz Prison at 60: full clear", "60", "maybe",
      "Elites 48-53 (gap 7-12); Tidemistress casts, Zarla Ober's dragon phase unknown", 53, 51,
      (["Overseer Wrex", "The Questioner", "Tidemistress Ca'zass", "Katerina the Cleaner", "Blazeroar"],
       45, 15, "Wrex > The Questioner > Tidemistress Ca'zass > Katerina the Cleaner > Zarla Ober (Blazeroar)"),
      (["Overseer Wrex", "The Questioner", "Tidemistress Ca'zass", "Katerina the Cleaner"], 35, 12,
       "Same without Zarla Ober")),
    R("Dire Maul East: Pusillin + lashers + Alzzin", "60", "maybe",
      "Lashers are non-elite melee 54 (ideal for rage); Alzzin and Lethtendris cast", 58, 54,
      (5, 50, 15, "Pusillin chase (key) > Zevrim Thornhoof > Hydrospawn > Lethtendris > Conservatory lashers > Alzzin"),
      (4, 40, 12, "Pusillin > Zevrim > Hydrospawn > lashers > Alzzin (skip Lethtendris)"),
      elite=False, drops=(("Living Essence", 0.2, 0), ("Heart of the Wild", 0.27, 0))),
    R("Blackrock Depths: entrance loop", "60", "maybe",
      "Lower-level front wings (mobs ~50-54); Dark Iron casters in some packs", 56, 53,
      (["Lord Roccor", "Houndmaster Grebmar", "High Interrogator Gerstahn", "Ring of Law (random boss)",
        "Pyromancer Loregrain"], 35, 15,
       "Lord Roccor > Houndmaster Grebmar > High Interrogator Gerstahn > Ring of Law > Pyromancer Loregrain"),
      (["Lord Roccor", "Houndmaster Grebmar", "High Interrogator Gerstahn", "Ring of Law (random boss)"], 30, 12,
       "Same without Pyromancer Loregrain"), drops=(("Runecloth", 0.24, 0),)),
    R("Dire Maul North: kill-everything", "60", "unlikely",
      "Ogre packs 56-60 with ogre mages; killing guards forfeits most of the tribute", 58, 57,
      (4, 30, 15, "Guard Mol'dar > Stomper Kreeg > Guard Fengus > Guard Slip'kik (no King Gordok in 15 min)"),
      (3, 25, 12, "Mol'dar > Kreeg > Fengus"), drops=(RUNECLOTH,)),
    R("Dire Maul West: Warpwood loop", "60", "unlikely",
      "Highborne casters and arcane aberrations 56-60", 58, 57,
      (3, 30, 15, "Tendris Warpwood > Illyanna Ravenoak > Magister Kalendris"),
      (2, 25, 12, "Tendris Warpwood > Illyanna Ravenoak"), drops=(RUNECLOTH,)),
    R("Stratholme Living: Willey + Galford orb loop", "60", "unlikely",
      "Elites 57-60 with Sorcerers, Battle Mages, Priests; no documented prot solo", 60, 58,
      (["Malor the Zealous", "Cannon Master Willey", "Archivist Galford", "The Unforgiven"], 32, 15,
       "Festival Lane > Malor the Zealous > Cannon Master Willey > Archivist Galford (orbs 84%) > The Unforgiven"),
      (["Cannon Master Willey", "Archivist Galford"], 25, 12, "Cannon Master Willey > Archivist Galford"),
      drops=(("Righteous Orb", 0.095, 0.84), RUNECLOTH)),
    R("Stratholme Undead: side-gate loop", "60", "unlikely", "Elites 57-60; Maleki and acolytes cast",
      60, 58, (["Magistrate Barthilas", "Baroness Anastari", "Nerub'enkan", "Maleki the Pallid"], 35, 15,
       "Magistrate Barthilas > Baroness Anastari > Nerub'enkan > Maleki the Pallid"),
      (["Magistrate Barthilas", "Baroness Anastari", "Nerub'enkan"], 30, 12, "Barthilas > Anastari > Nerub'enkan"),
      drops=(RUNECLOTH,)),
    R("Stratholme Undead: ziggurats + Ramstein", "60", "unlikely",
      "Elites 57-60; Maleki and acolytes cast; Ramstein hits very hard", 61, 58,
      (["Baroness Anastari", "Nerub'enkan", "Maleki the Pallid", "Ramstein the Gorger"], 40, 15,
       "Side gate > three ziggurats (Anastari, Nerub'enkan, Maleki) > Slaughterhouse > Ramstein the Gorger"),
      None, drops=(RUNECLOTH,),
      notes="Ramstein: Gauntlets of Valor (BoE ~45g) 15%, greens 244% per kill"),
    R("Scholomance: Rattlegore + Jandice loop", "60", "unlikely",
      "Elites 58-60, caster-heavy necromancers", 60, 59,
      (["Rattlegore", "Jandice Barov", "Ras Frostwhisper"], 30, 15,
       "Viewing Room trash > Rattlegore > Jandice Barov > Ras Frostwhisper"),
      (["Rattlegore", "Jandice Barov"], 25, 12, "Rattlegore > Jandice Barov"), drops=(RUNECLOTH,)),
    R("Lower Blackrock Spire: front loop", "60", "unlikely", "Elites 55-60 orc packs with casters",
      58, 57, (["Highlord Omokk", "Shadow Hunter Vosh'gajin", "War Master Voone", "Mother Smolderweb"], 35, 15,
       "Highlord Omokk > Shadow Hunter Vosh'gajin > War Master Voone > Mother Smolderweb, incl. ~6 Firebrand Pyromancers"),
      (["Highlord Omokk", "Shadow Hunter Vosh'gajin", "War Master Voone"], 30, 12,
       "Omokk > Vosh'gajin > Voone, incl. ~5 Firebrand Pyromancers"),
      drops=(RUNECLOTH,), extra15=6 * PYRO, extra12=5 * PYRO),
    R("Blackmaw Hold: first bosses", "60", "unlikely",
      "Elites 55-60; no solo reports; avoid the old Devotee room farm", 60, 58,
      (["Withermaw", "Impaan the Imprisoner", "Elder Shaman Bloodmane", "Bonesnout the Unbroken"], 30, 15,
       "Withermaw > Impaan the Imprisoner > Elder Shaman Bloodmane > Bonesnout (order unconfirmed)"),
      (["Withermaw", "Impaan the Imprisoner", "Bonesnout the Unbroken"], 25, 12,
       "Withermaw > Impaan > Bonesnout (skips Bloodmane, the lowest blue rate)")),
    R("Shaper's Terrace: Titanosaur + Nanaya loop", "60", "unlikely",
      "Elites 58-60; Nanaya's position on the route is unconfirmed; no solo data", 63, 59,
      (["Titanosaur", "Venomridge", "Thunderhoof", "Direhorn Matriarch", "Nanaya"], 20, 15,
       "Mount in > Titanosaur > Venomridge > Thunderhoof > Direhorn Matriarch > Nanaya > teleport out"),
      (["Titanosaur", "Direhorn Matriarch", "Nanaya"], 15, 12,
       "Titanosaur > Direhorn Matriarch > Nanaya > teleport out (route unconfirmed)"),
      notes="Nanaya: Maker's Spark 94%, green 99%, Arcane Forge blueprint 5.5%"),
    R("Shaper's Terrace: dinosaur loop", "60", "unlikely",
      "Elites 58-60; the bosses on this route are melee beasts, which suit rage better than casters, "
      "but no solo data", 62, 59,
      (["Titanosaur", "Venomridge", "Thunderhoof", "Direhorn Matriarch", "Tor'Rel"], 20, 15,
       "Mount in > Titanosaur > Venomridge > Thunderhoof > Direhorn Matriarch > Izha'Rel and Tor'Rel > teleport out"),
      (["Titanosaur", "Venomridge", "Thunderhoof", "Direhorn Matriarch"], 15, 12,
       "Same without Izha'Rel and Tor'Rel"),
      notes="+ ~5.8 g/h Thorium only with Mining"),
]
FARMS = [f for f in FARMS if f["name"] not in REPLACED] + [f for r in ROUTES for f in r]

def tier(f):
    t = TIERS.get(f["name"])
    return t if t else (auto_tier(BAND_REF[f["band"]], f["mob"], f["elite"]), "level-gap rule")


def ah_values():
    """{(item, rate): g/h}, live from data/ when cached, else FALLBACK."""
    wanted = {pair for f in FARMS for pair in f["ah"]}
    if not (ROOT / "data" / "snapshots").exists():
        out = {}
        for item, rate in wanted:
            known = [(r, g) for (i, r), g in FALLBACK.items() if i == item]
            out[(item, rate)] = FALLBACK.get((item, rate)) or (
                known[0][1] / known[0][0] * rate if known else 0.0)   # linear, ignores the cap
        return out, "fallback values from 2026-11-23 (scaled linearly for other rates)"
    sys.path.insert(0, str(ROOT / "scripts"))
    import farm_leaderboard as fl
    table, _, _ = fl.build(argparse.Namespace(include_crafted=False))
    by_name = {s["name"].lower(): s for s in table}
    out = {}
    for item, rate in wanted:
        s = by_name.get(item.lower())
        out[(item, rate)] = fl.capped_gph(s, rate, SHARE)[0] if s else FALLBACK.get((item, rate), 0.0)
    return out, "live from data/"


def evaluate(f, scale, ah):
    runs = min(CAP, 60 / f["minutes"])
    if f.get("boss_list"):
        boss = sum(FOREVER_BOSSES[b][0] * blue(FOREVER_BOSSES[b][1], scale) for b in f["boss_list"])
    else:
        boss = f["real_boss"] if f["real_boss"] is not None else f["bosses"] * blue(f["ilvl"], scale)
    trash = f["kills"] * coin(f["mob"], f["elite"])
    ahg = sum(ah[p] for p in f["ah"])
    cons = CONSUMABLES[f["band"]] if tier(f)[0] != "reliable" else 0.0
    return dict(total=runs * (boss + trash + f["extra"]) + ahg - cons, boss_h=runs * boss,
                trash_h=runs * trash, other_h=runs * f["extra"] + ahg, cons=cons, runs=runs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--band", choices=("levelling", "60", "47"),
                    help="levelling (pre-60) or 60; 47 is accepted as an old alias for levelling")
    ap.add_argument("--reasons", action="store_true", help="print the viability reason per farm")
    a = ap.parse_args()
    ah, src = ah_values()
    print(f"AH drops: {src}. Conservative = blues at catalog median (x{CONSERVATIVE:.2f}); "
          "Krol'dok's real boss value is never scaled.")
    want = "levelling" if a.band == "47" else a.band
    for band in ("levelling", "60"):
        if want and want != band:
            continue
        rows = [f for f in FARMS if f["band"] == band]
        rows.sort(key=lambda f: (TIER_ORDER[tier(f)[0]], -evaluate(f, CONSERVATIVE, ah)["total"]))
        label = "Levelling band (pre-60)" if band == "levelling" else "Level 60"
        print(f"\n== {label} (ranked by solo viability, then conservative g/h; "
              f"consumables -{CONSUMABLES[band]} g/h on maybe/unlikely) ==")
        print(f"{'tier':9} {'farm':62} {'conserv':>7} {'anchored':>8} | {'boss/h':>6} {'trash/h':>7} "
              f"{'AH+other':>8}  {'blues':9} conf")
        last = None
        for f in rows:
            t, why = tier(f)
            if a.reasons and t != last:
                print(f"--- {t} ---")
            last = t
            c, h = evaluate(f, CONSERVATIVE, ah), evaluate(f, 1.0, ah)
            print(f"{t:9} {f['name']:62} {c['total']:7.0f} {h['total']:8.0f} | {c['boss_h']:6.1f} "
                  f"{c['trash_h']:7.1f} {c['other_h']:8.1f}  {f['basis']:9} {f['conf']}")
            if a.reasons:
                print(f"{'':9}   why: {why}")

if __name__ == "__main__":
    main()
