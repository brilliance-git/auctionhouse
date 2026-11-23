"""Minimal client for the WoW: Forever auction house API (https://wow-api.skyl3lazer.com/docs).

No dependencies. The key is read from the WOW_API_KEY environment variable or a
.env file next to this module, and sent in the X-API-Key header.
Prices are in copper (1g = 10000c).
"""
import json
import os
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


def _get(path, **params):
    params = {k: v for k, v in params.items() if v is not None}
    url = BASE + path + ("?" + urllib.parse.urlencode(params) if params else "")
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    key = os.environ.get("WOW_API_KEY")
    if key:
        req.add_header("X-API-Key", key)
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def _get_bytes(path):
    req = urllib.request.Request(BASE + path)
    key = os.environ.get("WOW_API_KEY")
    if key:
        req.add_header("X-API-Key", key)
    with urllib.request.urlopen(req, timeout=300) as r:
        return r.read()


# --- one function per endpoint ---------------------------------------------

def status():
    """The market served and the span of its history."""
    return _get("/v1/status")


def snapshots(since=None, until=None):
    """Snapshots on record, oldest first: [{epoch, modified, diffed}]."""
    return _get("/v1/snapshots", since=since, until=until)


def snapshot_prices(snapshot="latest"):
    """Every item's row in one snapshot: {epoch, columns, rows}."""
    return _get(f"/v1/snapshots/{snapshot}/prices")


def snapshot_archive(snapshot="latest"):
    """One snapshot's raw auction files, zipped (bytes)."""
    return _get_bytes(f"/v1/snapshots/{snapshot}/archive")


def items():
    """Every known item: {id: {name, sell_price, purchase_price, quality, ...}}."""
    return _get("/v1/items")


def item(item_id):
    return _get(f"/v1/items/{item_id}")


def item_prices(item_id, since=None, until=None):
    """One item's row in every snapshot: {item_id, columns, rows}."""
    return _get(f"/v1/items/{item_id}/prices", since=since, until=until)


def item_book(item_id):
    """Current listings: {home: [[unit_price, qty], ...], neutral: [...]}."""
    return _get(f"/v1/items/{item_id}/book")


def tooltips():
    return _get("/v1/tooltips")


def vendor_goods():
    """Item ids a vendor sells without limit."""
    return _get("/v1/vendor-goods")


def recipes():
    return _get("/v1/recipes")


def buyouts():
    """The service's study of past buyouts and price jumps."""
    return _get("/v1/buyouts")


# --- helpers ---------------------------------------------------------------

def rows_as_dicts(table):
    cols = table["columns"]
    return [dict(zip(cols, r)) for r in table["rows"]]


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
