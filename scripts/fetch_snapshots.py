"""Download every home (Horde) snapshot's item table into data/snapshots/<epoch>.json.

    python3 scripts/fetch_snapshots.py           # skips files already present
Roughly 45 MB for ~5 days of hourly snapshots. data/ is git-ignored.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import wowapi as w

out = ROOT / "data" / "snapshots"
out.mkdir(parents=True, exist_ok=True)
(ROOT / "data" / "items.json").write_text(json.dumps(w.items()))
snaps = w.snapshots()
for i, s in enumerate(snaps, 1):
    f = out / f"{s['epoch']}.json"
    if f.exists():
        continue
    f.write_text(json.dumps(w.snapshot_items(s["epoch"])))
    print(f"[{i}/{len(snaps)}] {s['modified']}")
print(f"{len(snaps)} snapshots in {out}")
