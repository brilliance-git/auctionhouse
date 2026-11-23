# auctionhouse

Tools and notes for making gold in **WoW: Forever** using the auction house API at
<https://wow-api.skyl3lazer.com/docs> (Blizzard Game Data API mirror, US Forever namespace).
Python 3 stdlib only — no dependencies.

## Setup
```sh
cp .env.example .env      # then put your key in WOW_API_KEY
python3 -c "import wowapi; print(wowapi.status())"
```
`.env` and `data/` are git-ignored. **Never commit the API key.**

In a Claude cloud session the key is stored as an environment network secret and injected
by the proxy — set any placeholder (`WOW_API_KEY=proxy-injected`) when running scripts there.

## API (all GET, header `X-API-Key`; prices in copper, 1g = 10000c)
| Endpoint | `wowapi` function | Returns |
|---|---|---|
| `/v1/status` | `status()` | namespace, house ids, snapshot count, first/latest epoch |
| `/v1/snapshots?since&until` | `snapshots()` | `[{epoch, modified, diffed}]` oldest first |
| `/v1/snapshots/{epoch\|latest}/prices` | `snapshot_prices()` | `{columns, rows}` one row per item |
| `/v1/snapshots/{epoch\|latest}/archive` | `snapshot_archive()` | raw auction files, zip bytes |
| `/v1/items` | `items()` | `{id: {name, sell_price, purchase_price, quality, level, is_stackable, item_class, …}}` — only items seen on the AH |
| `/v1/items/{id}` | `item()` | one item |
| `/v1/items/{id}/prices?since&until` | `item_prices()` | the item's row in every snapshot |
| `/v1/items/{id}/book` | `item_book()` | current listings `{home: [[unit_price, qty]…], neutral: […]}` |
| `/v1/tooltips` | `tooltips()` | tooltip lines for items the dashboard looked up |
| `/v1/vendor-goods` | `vendor_goods()` | item ids vendors sell without limit |
| `/v1/recipes` | `recipes()` | crafting recipes and reagents |
| `/v1/buyouts` | `buyouts()` | the service's study of past buyouts / price jumps |

Price row columns: `epoch|item_id, min_price, qty, lots, fill_price, sold_qty, gone_qty,
gone_value, new_qty, taken_qty`.

## Scripts
| Script | Use |
|---|---|
| `scripts/item_report.py "Name" …` | AH vs vendor price, trend and liquidity for any item |
| `scripts/dungeon_drops.py [Krol Strat …]` | prices every researched dungeon drop; "never on AH" ≈ BoP |
| `scripts/fetch_snapshots.py` | downloads all snapshots to `data/` (~45 MB) |

## Docs
- `docs/instance-loot-values-2026-11-23.md` — which instance pays best for a solo prot warrior (current plan: Krol'dok at 47)
- `docs/research-prot-warrior-solo-farms-2026-11-23.md` — the web-research brief it was built from
- `docs/findings-2026-11-22.md` — fishing (Yellowtail vs Cod) and market-cornering scan
