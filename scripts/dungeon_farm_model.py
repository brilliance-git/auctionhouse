"""Rough g/h model for solo Protection Warrior dungeon farms (WoW: Forever).

    python3 scripts/dungeon_farm_model.py            # both level bands
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
    # ---- level 47 ----
    F("Krol'dok Stronghold (full, Ogre Key)", 47, 6, None, 40, 44, 12, "medium", "verified",
      "Boss value from real prices and drop rates; trash and time estimated",
      real_boss=8.31, ah=(("Thick Leather", 5), ("Heavy Leather", 5), ("Red Wolf Meat", 5))),
    F("The Drowned City (full)", 47, 6, 40, 30, 38, 12, "low", "assumed",
      "6 bosses; loot ilvl ~40 assumed (top of range + 2, like Krol'dok)"),
    F("Zul'Farrak (graveyard + 2 bosses)", 47, 2, 47, 60, 44, 12, "low", "assumed",
      "Big near-level zombie pull", ah=(("Mageweave Cloth", 40),)),
    F("Razorfen Downs (full)", 47, 5, 40, 35, 38, 12, "low", "assumed", "Some quilboar casters"),
    F("Uldaman (partial, 3 bosses)", 47, 3, 44, 30, 44, 12, "low", "assumed",
      "Long and spread out; mostly melee"),
    F("Scarlet Monastery Cathedral", 47, 3, 42, 40, 38, 10, "low", "verified",
      "SM boss gear never on the AH", ah=(("Silk Cloth", 60),)),
    F("Maraudon (Orange/Purple wing)", 47, 2, 49, 30, 47, 12, "low", "assumed",
      "Mobs at your level; satyr casters"),
    F("City of Dalaran (full)", 47, 6, 34, 30, 31, 12, "low", "assumed",
      "Quest-unlocked; bosses and loot ilvl unconfirmed"),
    F("Razorfen Kraul (full)", 47, 5, 31, 30, 33, 12, "medium", "verified", "Thornspike 65s real"),
    F("Ruins of Lordaeron (full)", 47, 7, 24, 30, 18, 10, "medium", "verified",
      "Mirror of Rath'mael 18s real; Fermenter 7% x 6g", extra=0.4),
    F("Scarlet Monastery Armory", 47, 1, 40, 40, 38, 8, "low", "verified", "Herod only"),
    # ---- level 60 ----
    F("Stratholme Living, Scarlet side (chunked)", 60, 2, 60, 25, 58, 12, "low", "assumed",
      "Orbs ~3.2/run (Galford 84%, trash ~9.5%), mostly at the 2g vendor price; casters; "
      "no proven prot solo", ah=(("Righteous Orb", 16), ("Runecloth", 40))),
    F("Krol'dok Stronghold at 60", 60, 6, None, 40, 44, 11, "medium", "verified",
      "Same loot as at 47, trivial mobs", real_boss=8.31,
      ah=(("Thick Leather", 5), ("Heavy Leather", 5), ("Red Wolf Meat", 5))),
    F("Shaper's Terrace (4 bosses, teleport exit)", 60, 4, 62, 20, 59, 12, "low", "assumed",
      "10-11 encounters; mount inside; + ~5.8 g/h Thorium only with Mining"),
    F("Scholomance (partial, 4 bosses)", 60, 4, 60, 30, 59, 12, "low", "assumed",
      "Caster-heavy", ah=(("Runecloth", 40),)),
    F("Blackmaw Hold (partial, 4 bosses)", 60, 4, 60, 30, 58, 12, "low", "assumed",
      "Devotees drop nothing; normal boss kills only"),
    F("Dire Maul East (Lashers + 4 bosses)", 60, 4, 58, 40, 54, 12, "low", "assumed",
      "Non-elite melee lashers suit prot (non-elite coin)", elite=False,
      ah=(("Living Essence", 10), ("Heart of the Wild", 20))),
    F("Stratholme Undead (chunk, 3 bosses)", 60, 3, 60, 30, 58, 12, "low", "assumed",
      "Mostly melee undead", ah=(("Runecloth", 40),)),
    F("Alcaz Prison (full)", 60, 5, 53, 40, 51, 12, "low", "assumed",
      "5 bosses; no solo reports; Zarla Ober dragon phase"),
    F("Blackrock Depths (chunk, 4 bosses)", 60, 4, 56, 30, 54, 12, "low", "assumed", "Pick a wing"),
    F("Lower Blackrock Spire (chunk, 3 bosses)", 60, 3, 58, 30, 57, 12, "low", "assumed",
      "Orc packs, mostly melee"),
    F("Maraudon (Princess run)", 60, 4, 52, 25, 50, 12, "low", "assumed", "",
      ah=(("Essence of Earth", 5),)),
    # Scarlet Monastery at 60: mass-pull clears (gather a whole wing's humanoid packs and
    # AoE-tank them; normal pull-and-kill). Kill counts are estimates: Cathedral courtyard
    # ~25 + chapel ~35 elites (aggroing Mograine pulls the whole chapel); Armory ~65 elites.
    # Cloth: Silk on ~1 in 2-3 humanoid kills, Mageweave ~5%.
    F("SM Cathedral at 60 (mass pull, 3 bosses)", 60, 3, 42, 60, 38, 12, "low", "verified",
      "Whole-wing pulls of 34-40 elites; ~60 corpses to loot is the time limit",
      ah=(("Silk Cloth", 125), ("Mageweave Cloth", 15))),
    F("SM Armory at 60 (full clear, Herod)", 60, 1, 40, 65, 38, 12, "low", "verified",
      "Full trash clear plus Herod fits ~12 min", ah=(("Silk Cloth", 125), ("Mageweave Cloth", 15))),
    F("SM Library at 60 (2 bosses)", 60, 2, 38, 40, 36, 10, "low", "verified",
      "Loksey and Doan; fewer mobs", ah=(("Silk Cloth", 100),)),
    F("SM Graveyard at 60", 60, 1, 33, 40, 31, 8, "low", "verified",
      "Undead 26-36, low coin; Wool not Silk", ah=(("Wool Cloth", 60),)),
    F("Zul'Farrak at 60 (graveyard + 4 bosses)", 60, 4, 47, 60, 44, 12, "medium", "assumed",
      "Trivial at 60", ah=(("Mageweave Cloth", 40),)),
    F("Uldaman at 60 (6 bosses)", 60, 6, 44, 30, 44, 12, "low", "assumed", "Long"),
]


# ---- Solo viability for a Protection Warrior in pre-raid gear (Classic-era mechanics) ----
# reliable: out-levelled by ~10+, mobs barely hurt;
# maybe:    mobs a few levels under, or non-elite / melee-only packs; costs consumables;
# unlikely: elite packs at or near your level with casters, or huge near-level pulls.
# Rule of thumb (auto_tier) from the level gap; the explicit TIERS below override it with a reason.
TIER_ORDER = {"reliable": 0, "maybe": 1, "unlikely": 2}
# Consumables per hour for "maybe"/"unlikely" farms (ESTIMATE): ~10 healing potions + ~10 bandages
# + one elixir. Horde AH 2026-11-23: Greater/Superior Healing Potion ~4s, Heavy Mageweave
# Bandage ~6s, Heavy Runecloth Bandage ~14s, Elixir of Fortitude ~30s.
CONSUMABLES = {47: 1.0, 60: 2.5}


def auto_tier(player, mob, elite=True):
    gap = player - mob
    if gap >= 10:
        return "reliable"
    if gap >= 3 or not elite:
        return "maybe"
    return "unlikely"


TIERS = {
    # level 47
    "Krol'dok Stronghold (full, Ogre Key)": ("maybe",
        "Elites 42-45 (gap 2-5); caster cultists, Terrorhowl fear, Mortal Strike; Battlegear "
        "4-piece heal is doubled there. Done while levelling, solo not yet timed"),
    "The Drowned City (full)": ("maybe", "Elites 35-40 (gap 7-12); boss mechanics unknown"),
    "Zul'Farrak (graveyard + 2 bosses)": ("unlikely",
        "Graveyard event pulls dozens of level 43-44 elites at once (gap 3)"),
    "Razorfen Downs (full)": ("maybe", "Elites 37-46; quilboar casters"),
    "Uldaman (partial, 3 bosses)": ("maybe", "Elites 41-47, mostly melee"),
    "Scarlet Monastery Cathedral": ("reliable", "Humanoids 34-40 (gap 7-13), small packs"),
    "Maraudon (Orange/Purple wing)": ("unlikely", "Elites 44-48 at your level; satyr casters"),
    "City of Dalaran (full)": ("reliable", "Mobs ~28-33 (gap 14+)"),
    "Razorfen Kraul (full)": ("reliable", "Mobs 29-38"),
    "Ruins of Lordaeron (full)": ("reliable", "Mobs 15-20"),
    "Scarlet Monastery Armory": ("reliable", "Humanoids 34-40"),
    # level 60
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


def tier(f):
    t = TIERS.get(f["name"])
    return t if t else (auto_tier(f["band"], f["mob"], f["elite"]), "level-gap rule")


def ah_values():
    """{(item, rate): g/h}, live from data/ when cached, else FALLBACK."""
    wanted = {pair for f in FARMS for pair in f["ah"]}
    if not (ROOT / "data" / "snapshots").exists():
        return dict(FALLBACK), "fallback values from 2026-11-23"
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
    boss = f["real_boss"] if f["real_boss"] is not None else f["bosses"] * blue(f["ilvl"], scale)
    trash = f["kills"] * coin(f["mob"], f["elite"])
    ahg = sum(ah[p] for p in f["ah"])
    cons = CONSUMABLES[f["band"]] if tier(f)[0] != "reliable" else 0.0
    return dict(total=runs * (boss + trash + f["extra"]) + ahg - cons, boss_h=runs * boss,
                trash_h=runs * trash, other_h=runs * f["extra"] + ahg, cons=cons, runs=runs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--band", type=int, choices=(47, 60))
    ap.add_argument("--reasons", action="store_true", help="print the viability reason per farm")
    a = ap.parse_args()
    ah, src = ah_values()
    print(f"AH drops: {src}. Conservative = blues at catalog median (x{CONSERVATIVE:.2f}); "
          "Krol'dok's real boss value is never scaled.")
    for band in (47, 60):
        if a.band and a.band != band:
            continue
        rows = [f for f in FARMS if f["band"] == band]
        rows.sort(key=lambda f: (TIER_ORDER[tier(f)[0]], -evaluate(f, CONSERVATIVE, ah)["total"]))
        print(f"\n== Level {band} (ranked by solo viability, then conservative g/h; "
              f"consumables -{CONSUMABLES[band]} g/h on maybe/unlikely) ==")
        print(f"{'tier':9} {'farm':44} {'conserv':>7} {'anchored':>8} | {'boss/h':>6} {'trash/h':>7} "
              f"{'AH+other':>8}  {'blues':8} conf")
        last = None
        for f in rows:
            t, why = tier(f)
            if a.reasons and t != last:
                print(f"--- {t} ---")
            last = t
            c, h = evaluate(f, CONSERVATIVE, ah), evaluate(f, 1.0, ah)
            print(f"{t:9} {f['name']:44} {c['total']:7.0f} {h['total']:8.0f} | {c['boss_h']:6.1f} "
                  f"{c['trash_h']:7.1f} {c['other_h']:8.1f}  {f['basis']:8} {f['conf']}")
            if a.reasons:
                print(f"{'':9}   why: {why}")

if __name__ == "__main__":
    main()
