"""Price/vendor/liquidity report for items by name.

    python3 scripts/item_report.py "Flask of Mojo" "Righteous Orb"
    python3 scripts/item_report.py --file names.txt      # one name per line

Exact name match first, falls back to substring match. Only the home (Horde)
auction house is checked, never the neutral one. Items with no listings in the
history are reported as such (for dungeon gear this usually means bind-on-pickup).
The item catalog also holds recipe items that were never listed, so "not in the
catalog" and "never listed" are different answers.
"""
import statistics as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import wowapi as w


def summarize(item_id):
    rows = w.rows_as_dicts(w.item_history(item_id))
    if not rows:
        return None
    days = max((rows[-1]["epoch"] - rows[0]["epoch"]) / 86400, 1e-9)
    mp = [r["min_price"] for r in rows if r["min_price"]]
    third = max(1, len(mp) // 3)
    tot = lambda k: sum(r[k] or 0 for r in rows)
    return {
        "snaps": len(rows), "listed": len(mp),
        "median": st.median(mp) if mp else None, "last": mp[-1] if mp else None,
        "early": st.median(mp[:third]) if mp else None,
        "late": st.median(mp[-third:]) if mp else None,
        "avg_qty": st.mean(r["qty"] or 0 for r in rows),
        # estimated sales = sold_qty + taken_qty (commodities only)
        "sold_d": sum(w.est_sold(r) for r in rows) / days, "gone_d": tot("gone_qty") / days,
        "new_d": tot("new_qty") / days,
    }


def main(names):
    cat = w.items()
    for name in names:
        hits = w.find_items(name, cat, exact=True) or w.find_items(name, cat)[:5]
        if not hits:
            print(f"{name}: not in the item catalog (never listed, not in any recipe)")
            continue
        for iid, v in hits:
            s = summarize(iid)
            print(f"\n{v['name']} (id {iid}, {v['quality']}) vendor {w.gold(v['sell_price'])}")
            if not s or not s["median"]:
                print("  no listings in history")
                continue
            print(f"  min-price median {w.gold(s['median'])}  last {w.gold(s['last'])}  "
                  f"early→late {w.gold(s['early'])} → {w.gold(s['late'])}")
            print(f"  AH net after 5% cut {w.gold(s['last'] * 0.95)}  vs vendor {w.gold(v['sell_price'])}")
            print(f"  listed in {s['listed']}/{s['snaps']} snapshots, avg qty {s['avg_qty']:.0f}, "
                  f"per day: est. sold {s['sold_d']:.1f}, gone {s['gone_d']:.0f}, new {s['new_d']:.0f}")
            now = w.item_listings(iid).get("listings") or []
            if now:
                print(f"  listed right now (Horde AH): {sum(q for _, q in now)} in {len(now)} listings, "
                      f"cheapest {w.gold(now[0][0])}")
            else:
                print("  listed right now (Horde AH): none")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[:1] == ["--file"]:
        args = [l.strip() for l in Path(args[1]).read_text().splitlines() if l.strip()]
    if not args:
        sys.exit(__doc__)
    main(args)
