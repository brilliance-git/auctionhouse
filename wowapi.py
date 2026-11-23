"""Minimal client for the WoW: Forever auction house API (https://wow-api.skyl3lazer.com/docs).

No dependencies. The key is read from the WOW_API_KEY environment variable or a
.env file next to this module, and sent in the X-API-Key header.
Prices are in copper (1g = 10000c).

Routes follow the API as of 2026-11-23: /history, /items and /listings. Only the
home (Horde) auction house is used; the /v1/neutral/... routes are never called.
The old /prices and /book routes are deprecated upstream; the old function names
below are kept as aliases on the new routes.
"""
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


def _load_env():
    env = Path(__file__).with_name(".env")
    if env.exists():
        for line in env.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


_load_env()
BASE = os.environ.get("WOW_API_BASE", "https://wow-api.skyl3lazer.com").rstrip("/")
RETRIES = 3  # for HTTP 429 (rate limit) and 503 (snapshot being replaced / busy)


def _open(url, accept_json, timeout):
    req = urllib.request.Request(url)
    if accept_json:
        req.add_header("Accept", "application/json")
    key = os.environ.get("WOW_API_KEY")
    if key:
        req.add_header("X-API-Key", key)
    for attempt in range(RETRIES + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code not in (429, 503) or attempt == RETRIES:
                raise
            try:
                wait = float(e.headers.get("Retry-After") or 0)
            except ValueError:
                wait = 0
            time.sleep(min(max(wait, 2 ** attempt), 60))


def _get(path, **params):
    params = {k: v for k, v in params.items() if v is not None}
    url = BASE + path + ("?" + urllib.parse.urlencode(params) if params else "")
    return json.loads(_open(url, True, 120))


def _get_bytes(path):
    return _open(BASE + path, False, 300)


# --- one function per endpoint ---------------------------------------------

def status():
    """What the API serves: house ids, snapshot count and span. Use the home `house` fields."""
    return _get("/v1/status")


# Home house

def snapshots(since=None, until=None):
    """Home snapshots on record, oldest first: [{epoch, modified, diffed}]."""
    return _get("/v1/snapshots", since=since, until=until)


def snapshot_items(snapshot="latest"):
    """Every item's row in one home snapshot: {epoch, columns, rows}."""
    return _get(f"/v1/snapshots/{snapshot}/items")


def item_history(item_id, since=None, until=None):
    """One item's row in every home snapshot: {item_id, columns, rows}."""
    return _get(f"/v1/items/{item_id}/history", since=since, until=until)


def item_listings(item_id):
    """Current home listings: {item_id, epoch, listings: [[unit_price, qty], ...]}, cheapest first."""
    return _get(f"/v1/items/{item_id}/listings")


# The neutral house (/v1/neutral/...) is deliberately not wrapped: price checks
# use only the home (Horde) auction house.


# Raw files

def snapshot_archive(snapshot="latest"):
    """One snapshot's raw auction files, zipped (bytes). Kept 30 days. Use only the home
    files (commodities.json, items.json); ignore the neutral_*.json files.
    Counts as 20 requests against the rate limit."""
    return _get_bytes(f"/v1/snapshots/{snapshot}/archive")


# Items, crafting, studies

def items():
    """Every item that has been listed or appears in a recipe:
    {id: {name, sell_price, purchase_price, quality, ...}}."""
    return _get("/v1/items")


def item(item_id):
    return _get(f"/v1/items/{item_id}")


def tooltips():
    """Tooltip lines (binding, stats, ...) for items the server has looked up so far."""
    return _get("/v1/tooltips")


def vendor_goods():
    """Item ids a vendor sells without limit (for the home house's faction)."""
    return _get("/v1/vendor-goods")


def recipes():
    return _get("/v1/recipes")


def buyouts():
    """The service's study of past buyouts and price jumps."""
    return _get("/v1/buyouts")


# --- deprecated names, kept working on the new routes ----------------------

snapshot_prices = snapshot_items
item_prices = item_history


def item_book(item_id):
    """Old shape {item_id, epoch, home}, from the home (Horde) /listings route only.
    The neutral house is never checked."""
    home = item_listings(item_id)
    return {"item_id": item_id, "epoch": home.get("epoch"), "home": home.get("listings", [])}


# --- helpers ---------------------------------------------------------------

def rows_as_dicts(table):
    cols = table["columns"]
    return [dict(zip(cols, r)) for r in table["rows"]]


def est_sold(row):
    """Estimated units sold in a snapshot row: sold_qty + taken_qty (None-safe).
    Only commodities show these; gear shows up in gone_qty (sold or cancelled)."""
    return (row.get("sold_qty") or 0) + (row.get("taken_qty") or 0)


def gold(copper):
    if copper is None:
        return "-"
    g, rest = divmod(int(round(copper)), 10000)
    s, c = divmod(rest, 100)
    return f"{g}g {s:02d}s {c:02d}c" if g else (f"{s}s {c:02d}c" if s else f"{c}c")


def find_items(name, catalog=None, exact=False):
    catalog = catalog or items()
    n = name.lower()
    return [(int(k), v) for k, v in catalog.items()
            if (v["name"].lower() == n if exact else n in v["name"].lower())]
