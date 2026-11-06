# Wardriving

A terminal viewer for network data stored in a [WiGLE](https://wigle.net/) SQLite database. Browse unique, nonempty SSIDs by technology and inspect their BSSID, capabilities and type. The database is opened **read-only**.

## Requirements

Python 3.10+ and a WiGLE-compatible SQLite database with a `network` table containing `bssid`, `ssid`, `capabilities` and `type` columns.

## Installation

```bash
git clone https://github.com/Sn0wBaall/Wardriving.git
cd Wardriving
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Usage

```bash
python wardriving.py /path/to/database.sqlite
# Or omit the path to choose a database interactively:
python wardriving.py
python wardriving.py --help
```

The interactive mode lists `.sqlite` and `.db` files in the current directory, but accepts any database path. Enter a type code to see its networks, `*` for all supported types, `back` to choose another database, or `q` to exit.

| Code | Technology | Code | Technology |
| :---: | --- | :---: | --- |
| W | Wi-Fi | E | BLE |
| B | Bluetooth | G | GSM |
| C | CDMA | L | LTE |
| D | WCDMA | N | 5G NR |
| F | NFC | * | All supported types |

Counts represent distinct, nonempty SSIDs within each type. The detail view shows one representative row per SSID and type, sorted consistently; different devices sharing an SSID are not shown separately. Unsupported types and empty SSIDs are excluded. Large results may require scrolling in your terminal.

## Tests

Run the database tests with the Python standard library (no additional test dependencies):

```bash
python -m unittest discover -s tests -v
```
