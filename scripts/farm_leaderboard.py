"""Demand-capped farm leaderboard: farmable commodities ranked by the gold the Horde AH
actually absorbs per day, not by price alone.

    python3 scripts/fetch_snapshots.py                      # first: cache the snapshots in data/
    python3 scripts/farm_leaderboard.py                     # top 30, whole market, no level filter
    python3 scripts/farm_leaderboard.py --top 50 --min-level 55 --class herb --class metal
    python3 scripts/farm_leaderboard.py --rate "Thick Leather=40" --rate "Mageweave Cloth=60"
    python3 scripts/farm_leaderboard.py --avoid             # only oversupplied / falling markets
    python3 scripts/farm_leaderboard.py --tsv > out.tsv     # every item, tab-separated

Works offline from data/ (no API calls), so it can be re-run freely. Horde AH only.

Item set: stackable items that are not sold by vendors, not ammo or keys, and not crafted-only.
"Crafted-only" means the output of a recipe, except:
  - smelted bars (Mining), which a miner farms;
  - base leathers (Light/Medium/Heavy/Thick/Rugged), which Leatherworking can also make
    but which come from Skinning and mob drops;
  - elemental essences and Elemental Fire, which Alchemy can transmute but which drop.
Refined Deeprock Salt is also left out: a Salt Shaker makes it, not a recipe.
Use --include-crafted to see crafted goods too (marked "crafted").

Per item, over the whole history:
  value      median fill_price (the realistic price when selling volume); median min_price
             if an item never had a fill_price
  net        value after the 5% AH cut
  sold/day   estimated units sold = sold_qty + taken_qty (wowapi.est_sold), averaged over the
             hours in which the item's sales columns are not null, x 24
  sure/day   sold_qty only (sales certain from partly-bought listings); a floor for sold/day
  g/day      market gold per day = net x sold/day
  new/gone   units posted per day / units leaving per day (bought or cancelled)
  trend      value in the last third of the history vs the first third
  flag       "oversupplied" when new/gone is >= 1.5x the market-wide median ratio (about 2,
             because expired listings are never counted as gone), or above the median while
             the listed qty grew 50%+ (first vs last third); "falling" when the trend
             is -15% or worse; "rising" at +15% or better; "vendor" when net is within 5% of
             the vendor price (vendor it); "smelt" for bars; "quest" for quest-class items

--rate "Item=units_per_hour" adds a demand-capped gold per hour for that item:
  ah_units/h = min(rate, sold/day / 24 x share)       share defaults to 0.10 (--share)
  g/h        = ah_units/h x net + (rate - ah_units/h) x vendor price
so units the market cannot absorb are vendored instead of piling up on the AH.
"""
import argparse
import json
import statistics as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import wowapi as w

DATA = ROOT / "data"
CUT = 0.95
SKIP_CLASSES = {"Projectile", "Key", "Quiver", "Container", "Recipe"}
# Recipe outputs that are also farmed directly (see module docstring).
ALSO_DROPS = {2318, 2319, 4234, 4304, 8170,                    # base leathers
              7068, 7076, 7078, 7080, 7082, 12803, 12808}       # Elemental Fire, essences
# Made by using another item rather than by a recipe, so the recipe list misses them.
NOT_FARMABLE = {15409}                                          # Refined Deeprock Salt (Salt Shaker)


def load():
    need = ["items.json", "vendor_goods.json", "recipes.json"]
    missing = [n for n in need if not (DATA / n).exists()]
    snaps = sorted((DATA / "snapshots").glob("*.json"), key=lambda f: int(f.stem)) \
        if (DATA / "snapshots").exists() else []
    if missing or not snaps:
        sys.exit(f"Missing {', '.join(missing) or 'data/snapshots'}: run scripts/fetch_snapshots.py first.")
    cat = json.loads((DATA / "items.json").read_text())
    vendor = set(json.loads((DATA / "vendor_goods.json").read_text()))
    recipes = json.loads((DATA / "recipes.json").read_text())
    crafted = {}
    for r in recipes.values():
        crafted.setdefault(r["item"], r["profession"])
    return cat, vendor, crafted, snaps


def candidates(cat, vendor, crafted, include_crafted):
    """{item_id: tag} for farmable commodities. tag is '', 'smelt' or 'crafted'."""
    out = {}
    for k, v in cat.items():
        iid = int(k)
        if (not v.get("is_stackable") or v.get("item_class") in SKIP_CLASSES or iid in vendor
                or iid in NOT_FARMABLE):
            continue
        prof = crafted.get(iid)
        if prof is None or iid in ALSO_DROPS:
            out[iid] = ""
        elif prof == "Mining":
            out[iid] = "smelt"
        elif include_crafted:
            out[iid] = "crafted"
    return out


def collect(snaps, ids):
    """Per item: list of (epoch, row-dict) across every snapshot."""
    hist = {i: [] for i in ids}
    cols = None
    for f in snaps:
        t = json.loads(f.read_text())
        cols = cols or t["columns"]
        ep = t["epoch"]
        for r in t["rows"]:
            if r[0] in hist:
                hist[r[0]].append((ep, dict(zip(cols, r))))
    return hist


def third_medians(vals):
    n = max(1, len(vals) // 3)
    return st.median(vals[:n]), st.median(vals[-n:])


def stats(rows, epochs):
    """Market stats for one item. epochs: every snapshot epoch, oldest first."""
    if not rows:
        return None
    gap = {b: b - a for a, b in zip(epochs, epochs[1:])}
    mins = [r["min_price"] for _, r in rows if r["min_price"]]
    if not mins:
        return None
    fills = [r["fill_price"] for _, r in rows if r["fill_price"]]
    value_series = [r["fill_price"] or r["min_price"] for _, r in rows if r["min_price"]]
    sales = [(ep, r) for ep, r in rows if r["sold_qty"] is not None and ep in gap]
    hours = sum(gap[ep] for ep, _ in sales) / 3600
    sold = sum(w.est_sold(r) for _, r in sales)
    sure = sum(r["sold_qty"] or 0 for _, r in sales)
    new = sum(r["new_qty"] or 0 for _, r in sales)
    gone = sum(r["gone_qty"] or 0 for _, r in sales)
    per_day = (lambda x: x / hours * 24) if hours else (lambda x: 0.0)
    early, late = third_medians(value_series)
    q = [r["qty"] or 0 for _, r in rows]
    q_early, q_late = third_medians(q)
    return {
        "min": st.median(mins), "fill": st.median(fills) if fills else None,
        "value": st.median(fills) if fills else st.median(mins),
        "sold_d": per_day(sold), "sure_d": per_day(sure),
        "new_d": per_day(new), "gone_d": per_day(gone), "hours": hours,
        "trend": (late / early - 1) if early else 0.0, "early": early, "late": late,
        "qty": st.median(q), "lots": st.median(r["lots"] or 0 for _, r in rows),
        "q_growth": (q_late / q_early - 1) if q_early else 0.0,
        "listed_share": len(mins) / len(epochs),
    }


def flags(s, vendor_price, base_ratio):
    """base_ratio: the market-wide median of new/gone. new_qty counts every fresh listing
    (reposts too) while gone_qty leaves out expiries, so new/gone is ~2 for a balanced
    market; compare each item with the market rather than with 1."""
    f = []
    ratio = s["new_d"] / s["gone_d"] if s["gone_d"] else 0
    if ratio >= 1.5 * base_ratio or (ratio >= base_ratio and s["q_growth"] >= 0.5):
        f.append("oversupplied")
    if s["trend"] <= -0.15:
        f.append("falling")
    elif s["trend"] >= 0.15:
        f.append("rising")
    if vendor_price and s["net"] <= vendor_price * 1.05:
        f.append("vendor")
    return f


def build(args):
    cat, vendor, crafted, snaps = load()
    tags = candidates(cat, vendor, crafted, args.include_crafted)
    epochs = [int(f.stem) for f in snaps]
    hist = collect(snaps, set(tags))
    table = []
    for iid, tag in tags.items():
        s = stats(hist[iid], epochs)
        if not s:
            continue
        v = cat[str(iid)]
        s.update(id=iid, name=v["name"], level=v.get("level") or 0, cls=v.get("item_class"),
                 sub=v.get("item_subclass"), vendor=v.get("sell_price") or 0, tag=tag)
        s["net"] = s["value"] * CUT
        s["gday"] = s["net"] * s["sold_d"] / 10000
        s["gday_sure"] = s["net"] * s["sure_d"] / 10000
        table.append(s)
    ratios = [s["new_d"] / s["gone_d"] for s in table if s["sold_d"] >= 50 and s["gone_d"]]
    base = st.median(ratios) if ratios else 2.0
    for s in table:
        s["flags"] = flags(s, s["vendor"], base) + ([s["tag"]] if s["tag"] else []) \
            + (["quest"] if s["cls"] == "Quest" else [])
    return table, epochs, base


def capped_gph(s, rate, share):
    ah = min(rate, s["sold_d"] / 24 * share)
    sell = max(s["net"], s["vendor"])          # never list below the vendor price
    return (ah * sell + (rate - ah) * s["vendor"]) / 10000, ah


def g(c):
    return w.gold(c) if c is not None else "-"


def fmt_row(i, s, extra=""):
    nv = f"{s['new_d']:.0f}/{s['gone_d']:.0f}"
    return (f"{i:>3} {s['name'][:28]:28} {s['level']:>3} {(s['sub'] or '')[:13]:13} "
            f"{g(s['net']):>12} {g(s['vendor']):>10} {s['sold_d']:>8.0f} {s['sure_d']:>7.0f} "
            f"{s['gday']:>8.1f} {s['qty']:>7.0f} {s['lots']:>5.0f} {nv:>13} "
            f"{s['trend']*100:>+5.0f}% {','.join(s['flags'])}{extra}")


HEADER = (f"{'#':>3} {'item':28} {'ilv':>3} {'subclass':13} {'net (5% cut)':>12} {'vendor':>10} "
          f"{'sold/d':>8} {'sure/d':>7} {'g/day':>8} {'qty':>7} {'lots':>5} {'new/gone d':>13} "
          f"{'trend':>6} flags")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--top", type=int, default=30, help="rows to show (0: only the --rate table)")
    ap.add_argument("--min-level", type=int, help="minimum item level (default: none)")
    ap.add_argument("--max-level", type=int, help="maximum item level (default: none)")
    ap.add_argument("--class", dest="classes", action="append", default=[],
                    help="item class or subclass substring, e.g. herb, metal, cloth, leather (repeatable)")
    ap.add_argument("--rate", action="append", default=[], metavar="ITEM=UNITS_PER_HOUR",
                    help="your measured farm rate; adds demand-capped gold/hour (repeatable)")
    ap.add_argument("--share", type=float, default=0.10,
                    help="share of the item's daily sales you can expect to win (default 0.10)")
    ap.add_argument("--min-sold", type=float, default=1.0, help="hide items selling fewer per day (default 1)")
    ap.add_argument("--avoid", action="store_true", help="list only oversupplied or falling markets")
    ap.add_argument("--include-crafted", action="store_true", help="also show crafted-only goods")
    ap.add_argument("--tsv", action="store_true", help="print every matching item as tab-separated values")
    args = ap.parse_args()

    table, epochs, base = build(args)
    rows = [s for s in table
            if (args.min_level is None or s["level"] >= args.min_level)
            and (args.max_level is None or s["level"] <= args.max_level)
            and (not args.classes or any(c.lower() in f"{s['cls']} {s['sub']}".lower() for c in args.classes))
            and s["sold_d"] >= args.min_sold]
    if args.avoid:
        rows = [s for s in rows if {"oversupplied", "falling"} & set(s["flags"])]
    rows.sort(key=lambda s: -s["gday"])

    if args.tsv:
        keys = ["id", "name", "level", "cls", "sub", "min", "fill", "value", "net", "vendor", "sold_d",
                "sure_d", "gday", "gday_sure", "qty", "lots", "new_d", "gone_d", "trend", "hours", "listed_share"]
        print("\t".join(keys + ["flags"]))
        for s in rows:
            print("\t".join(str(round(s[k], 4) if isinstance(s[k], float) else s[k]) for k in keys)
                  + "\t" + ",".join(s["flags"]))
        return

    days = (epochs[-1] - epochs[0]) / 86400
    if args.top > 0:
        print_board(rows, args.top, epochs, days, base)
    if args.rate:
        print_rates(table, args.rate, args.share)


def print_board(rows, top, epochs, days, base):
    print(f"Horde AH, {len(epochs)} snapshots over {days:.1f} days (to epoch {epochs[-1]}). "
          f"g/day = net x sold/day. Market median new/gone = {base:.2f}.")
    print(HEADER)
    for i, s in enumerate(rows[:top], 1):
        print(fmt_row(i, s))


def print_rates(table, specs, share):
    by_name = {s["name"].lower(): s for s in table}
    print(f"\nDemand-capped gold per hour (share of the market = {share:.0%}):")
    print(f"  {'item':28} {'rate/h':>7} {'AH/h':>7} {'vendored/h':>10} {'g/hour':>8}  uncapped g/h")
    for spec in specs:
        name, _, rate = spec.rpartition("=")
        s = by_name.get(name.strip().lower())
        if not s:
            print(f"  {name}: not in the farmable set (check the name, or try --include-crafted)")
            continue
        try:
            rate = float(rate)
        except ValueError:
            sys.exit(f'Bad --rate "{spec}": use "Item name=units_per_hour"')
        gph, ah = capped_gph(s, rate, share)
        print(f"  {s['name'][:28]:28} {rate:>7.0f} {ah:>7.1f} {rate - ah:>10.1f} {gph:>8.2f}  "
              f"{rate * max(s['net'], s['vendor']) / 10000:.2f}")


if __name__ == "__main__":
    main()
