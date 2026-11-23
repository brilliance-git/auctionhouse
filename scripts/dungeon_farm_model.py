"""Rough g/h model for solo Protection Warrior dungeon farms (WoW: Forever).

    python3 scripts/dungeon_farm_model.py            # both level bands
    python3 scripts/dungeon_farm_model.py --band 47

Every number here is an ESTIMATE unless a farm is marked measured. Only Krol'dok
uses real boss sell prices and drop rates (from Wowhead tooltips, see
docs/kroldok-model-2026-11-23.md). Nothing has been timed in-game yet (docs/farm-log.md).

Per run = boss blues (vendor) + trash coin + other vendor loot.
g/h     = min(5, 60 / minutes) x per-run value + AH bonus g/h.
AH bonus g/h comes from `farm_leaderboard.py --rate ... --share 0.10`, i.e. what the
Horde AH absorbs at a 10% market share; the rest of those drops are counted at vendor price.
"""
import argparse
import math

CAP = 5                      # new instances per hour
KROL_BLUE = 1.24             # mean real vendor price of a Krol'dok boss blue (g), ilvl ~45.5


SCALE = 1.0                  # --blue-scale; 0.55 = conservative (catalog median, not Krol'dok anchor)


def blue(ilvl):
    """Average vendor value of one BoP boss blue at this item level, in gold.
    Anchored on the 19 real Krol'dok sell prices; slope from the median vendor price of
    rare armor/weapons in /v1/items (about +7% per item level). Probably +-40%."""
    return SCALE * KROL_BLUE * math.exp(0.071 * (ilvl - 45.5))


def coin(mob_level):
    """Coin per elite trash kill, in gold. ~4s at level 45 from the Krol'dok guide video."""
    return 0.0009 * mob_level


# name, band, bosses_per_run, blue_ilvl, blue_override_g_per_run, trash_kills, mob_level,
# minutes_per_run, extra_vendor_g_per_run, ah_bonus_g_per_hour, confidence, notes
FARMS = [
    # ---- level 47 ----
    ("Krol'dok Stronghold (full, Ogre Key)", 47, 6, None, 8.31, 40, 44, 12, 0.3, 1.0, "medium",
     "Boss value from real Wowhead prices and drop rates; time and trash estimated"),
    ("Drowned City (full)", 47, 6, 40, None, 30, 38, 12, 0.0, 0.0, "low",
     "6 bosses; loot ilvl assumed ~40 (top of range + 2, like Krol'dok)"),
    ("Zul'Farrak (graveyard + 2 bosses)", 47, 2, 47, None, 60, 44, 12, 0.0, 1.7, "low",
     "Big zombie pull at near-level; Mageweave AH bonus"),
    ("Razorfen Downs (full)", 47, 5, 40, None, 35, 38, 12, 0.0, 0.0, "low",
     "Quilboar and undead, mixed casters"),
    ("Scarlet Monastery Cathedral", 47, 3, 42, None, 40, 38, 10, 0.0, 1.1, "low",
     "Fast at 47; Silk AH bonus"),
    ("Uldaman (partial, 3 bosses)", 47, 3, 44, None, 30, 44, 12, 0.0, 0.0, "low",
     "Long, spread-out dungeon; mostly melee troggs and dwarves"),
    ("Maraudon (Orange/Purple wing)", 47, 2, 49, None, 30, 47, 12, 0.0, 0.0, "low",
     "Mobs at your level; satyr casters"),
    ("City of Dalaran (full)", 47, 6, 34, None, 30, 31, 12, 0.0, 0.0, "low",
     "Quest-unlocked; boss count and loot ilvl assumed"),
    ("Razorfen Kraul (full)", 47, 5, 31, None, 30, 33, 12, 0.0, 0.0, "medium",
     "BoP confirmed (Thornspike 65s real)"),
    ("Scarlet Monastery Armory", 47, 1, 40, None, 40, 38, 8, 0.0, 0.0, "low", "Herod only"),
    ("Ruins of Lordaeron (full)", 47, 7, 24, None, 30, 18, 10, 0.4, 0.0, "medium",
     "Mirror of Rath'mael 17s real; Fermenter blueprint 7% x 6g"),
    # ---- level 60 ----
    ("Stratholme Living, Scarlet side (chunked)", 60, 2, 60, None, 25, 58, 12, 6.4, 3.6, "low",
     "Orbs: ~3.2/run at 2g vendor (6.4g); AH absorbs ~0.2 orbs/h (+1.5 g/h) + Runecloth 2.1 g/h; casters; unproven solo"),
    ("Alcaz Prison (full)", 60, 5, 53, None, 40, 51, 12, 0.0, 0.0, "low",
     "5 bosses; no solo reports; Zarla Ober dragon phase"),
    ("Shaper's Terrace (4 bosses, teleport exit)", 60, 4, 62, None, 20, 59, 12, 0.0, 0.0, "low",
     "10-11 encounters, mount inside, teleport exit; + ~5.8 g/h Thorium only with Mining"),
    ("Scholomance (partial, 4 bosses)", 60, 4, 60, None, 30, 59, 12, 0.0, 2.1, "low",
     "Caster-heavy; Runecloth AH bonus"),
    ("Blackmaw Hold (partial, 4 bosses)", 60, 4, 60, None, 30, 58, 12, 0.0, 0.0, "low",
     "Devotee loot removed; normal boss kills only, avoid the old Devotee farm"),
    ("Dire Maul East (Lashers + 4 bosses)", 60, 4, 58, None, 40, 54, 12, 0.0, 1.7, "low",
     "Non-elite melee lashers suit prot; coin lower (non-elite)"),
    ("Blackrock Depths (chunk, 4 bosses)", 60, 4, 56, None, 30, 54, 12, 0.0, 0.0, "low",
     "Huge; pick a wing; fire elementals"),
    ("Lower Blackrock Spire (chunk, 3 bosses)", 60, 3, 58, None, 30, 57, 12, 0.0, 0.0, "low",
     "Orc packs, mostly melee"),
    ("Stratholme Undead (chunk, 3 bosses)", 60, 3, 60, None, 30, 58, 12, 0.0, 2.1, "low",
     "Mostly melee undead; Runecloth"),
    ("Krol'dok Stronghold at 60", 60, 6, None, 8.31, 40, 44, 11, 0.3, 1.0, "medium",
     "Same loot as at 47, far safer; real boss prices"),
    ("Maraudon (Princess run)", 60, 4, 52, None, 25, 50, 12, 0.0, 2.3, "low",
     "Essence of Earth AH bonus"),
    ("Zul'Farrak at 60 (graveyard + 4 bosses)", 60, 4, 47, None, 60, 44, 12, 0.0, 1.7, "medium",
     "Trivial at 60; low ceiling"),
    ("Uldaman at 60 (6 bosses)", 60, 6, 44, None, 30, 44, 12, 0.0, 0.0, "low", "Long"),
]


def per_run(f):
    _, _, n, ilvl, override, kills, mlvl, _, extra, _, _, _ = f
    boss = override if override is not None else n * blue(ilvl)
    return boss, kills * coin(mlvl), extra


def gph(f):
    boss, trash, extra = per_run(f)
    runs = min(CAP, 60 / f[7])
    return runs * (boss + trash + extra) + f[9], runs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--band", type=int, choices=(47, 60))
    ap.add_argument("--blue-scale", type=float, default=1.0,
                    help="multiply estimated blue values (0.55 = catalog-median case); "
                         "Krol'dok's real prices are never scaled")
    a = ap.parse_args()
    global SCALE
    SCALE = a.blue_scale
    for band in (47, 60):
        if a.band and a.band != band:
            continue
        rows = sorted((f for f in FARMS if f[1] == band), key=lambda f: -gph(f)[0])
        print(f"\n== Level {band} ==")
        print(f"{'farm':44} {'g/h':>5} {'boss/run':>8} {'trash/run':>9} {'runs/h':>6}  conf")
        for f in rows:
            g, runs = gph(f)
            boss, trash, extra = per_run(f)
            print(f"{f[0]:44} {g:5.0f} {boss:8.1f} {trash:9.1f} {runs:6.1f}  {f[10]}")


if __name__ == "__main__":
    main()
