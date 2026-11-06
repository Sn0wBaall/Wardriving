"""Read-only queries for WiGLE network databases."""

import sqlite3


NETWORK_TYPES = (
    ("Wi-Fi", "W"),
    ("BLE", "E"),
    ("Bluetooth", "B"),
    ("GSM", "G"),
    ("CDMA", "C"),
    ("LTE", "L"),
    ("WCDMA", "D"),
    ("5G NR", "N"),
    ("NFC", "F"),
)
_CODES = tuple(code for _, code in NETWORK_TYPES)
_PLACEHOLDERS = ", ".join("?" for _ in _CODES)


def network_counts(connection: sqlite3.Connection) -> dict[str, int]:
    """Count distinct, nonempty SSIDs for each supported network type."""
    rows = connection.execute(
        f"SELECT type, COUNT(DISTINCT ssid) FROM network "
        f"WHERE type IN ({_PLACEHOLDERS}) AND ssid IS NOT NULL AND ssid != '' "
        "GROUP BY type",
        _CODES,
    )
    return dict(rows)


def networks(connection: sqlite3.Connection, code: str) -> list[tuple]:
    """Return one deterministic row per SSID and type, matching the summary counts."""
    if code != "*" and code not in _CODES:
        raise ValueError(f"Unsupported network type: {code}")

    query = (
        "SELECT bssid, ssid, capabilities, type FROM network "
        f"WHERE type IN ({_PLACEHOLDERS}) AND ssid IS NOT NULL AND ssid != ''"
    )
    params = _CODES
    if code != "*":
        query += " AND type = ?"
        params += (code,)
    query += " ORDER BY type, ssid, bssid, capabilities"

    seen = set()
    result = []
    for row in connection.execute(query, params):
        key = (row[3], row[1])
        if key not in seen:
            seen.add(key)
            result.append(row)
    return result
