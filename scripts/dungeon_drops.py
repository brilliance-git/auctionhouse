"""Price every drop named in the prot-warrior farm research, grouped by instance.

    python3 scripts/dungeon_drops.py            # all instances
    python3 scripts/dungeon_drops.py Krol Strat # only these groups

"never on AH" for dungeon gear = almost certainly bind-on-pickup (vendor only).
Checked 2026-11-23: every dungeon boss item looked up on Wowhead was BoP.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import wowapi as w
from item_report import summarize

DROPS = {
    "RoL": ["Segmented Spider Leg", "Witherbite Bracers", "Atrophic Girdle", "Leftover Abomination Skin",
            "Abomination Bones", "Meathook Slicer", "Rotmender's Leggings", "Scepter of the Abandoned",
            "Grip of Fear", "Corpse Chopper", "Tuskwrap Belt", "Bonerust Leggings", "Vilewalkers",
            "Bloodied Chestwraps", "Vileblood Scimitar", "Mirror of Rath'mael", "Coldspire Staff",
            "Rotmender's Treads", "Blueprint: Fermenter", "Blueprint: Arcane Salvager",
            "Rotmender's Gloves", "Haunting Blade", "Phantom Armor"],
    "ZF": ["Mageweave Cloth", "Gloves of Holy Might", "Ardent Custodian", "Dazzling Longsword",
           "Fiery War Axe", "Robes of Insight", "Blackskull Shield"],
    "RFK": ["Thornspike", "Swinetusk Shank", "Ferine Leggings", "Pronged Reaver", "Heart of Agamaggan",
            "Corpsemaker", "Batwing Mantle"],
    "SM": ["Silk Cloth", "Fadeleaf", "Ebon Vise", "Ghostshard Talisman", "Ironspine's Eye"],
    "Krol": ["Blueprint: Expert Campfire", "Zarmok's Plated Signet", "Krol'dok Warplate Chest",
             "Krol'dok Warplate Helmet", "Krol'dok Warplate Pauldrons", "Krol'dok Warplate Gauntlets",
             "Krol'dok Warplate Legplates", "Emblem of Slamming", "Toofbreaker", "Shadowlight Athame",
             "Chain of the Corruptor", "Black Horn Necklace", "Flask of Mojo", "Flask of Big Mojo"],
    "DME": ["Heart of the Wild", "Living Essence", "Silverleaf", "Mageroyal", "Briarthorn"],
    "Strat": ["Runecloth", "Righteous Orb", "Major Mana Potion", "Large Brilliant Shard"],
}


def main(groups):
    cat = w.items()
    for g in groups:
        print(f"\n== {g} ==")
        for name in DROPS[g]:
            hits = w.find_items(name, cat, exact=True)
            if not hits:
                print(f"  {name:32} never on AH (likely BoP)")
                continue
            iid, v = hits[0]
            s = summarize(iid) or {}
            med = s.get("median")
            print(f"  {name:32} vendor {w.gold(v['sell_price']):>12}  AH median {w.gold(med):>12}  "
                  f"avg listed {s.get('avg_qty', 0):6.0f}  trend {w.gold(s.get('early'))} → {w.gold(s.get('late'))}")


if __name__ == "__main__":
    main(sys.argv[1:] or list(DROPS))
