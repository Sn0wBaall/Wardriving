#!/usr/bin/env python3
"""Interactive viewer for WiGLE SQLite network databases."""

import argparse
import sqlite3
import sys
from contextlib import closing
from pathlib import Path

from rich.console import Console
from rich.table import Table

from networks import NETWORK_TYPES, network_counts, networks


console = Console()


def available_databases() -> None:
    files = sorted(
        (
            path
            for path in Path.cwd().iterdir()
            if path.is_file() and path.suffix.lower() in {".db", ".sqlite"}
        ),
        key=lambda path: path.name.lower(),
    )
    if files:
        console.print(
            "Databases in the current directory: " + ", ".join(path.name for path in files),
            markup=False,
        )


def select_database() -> Path | None:
    while True:
        name = input("Database path (q to quit): ").strip()
        if name.lower() == "q":
            return None
        path = Path(name).expanduser()
        if path.is_file():
            return path
        console.print("[red]File not found. Enter the path to a SQLite database.[/red]")


def show_summary(counts: dict[str, int], path: Path) -> None:
    console.print(f"Database: {path}", style="cyan", markup=False)
    table = Table(title="Network summary", title_style="bold cyan", border_style="blue")
    table.add_column("Technology", style="cyan", header_style="bold cyan")
    table.add_column("Code", style="magenta", header_style="bold magenta")
    table.add_column("Unique SSIDs", justify="right", style="green", header_style="bold green")
    table.add_row("All", "*", str(sum(counts.values())), style="bold")
    for name, code in NETWORK_TYPES:
        table.add_row(name, code, str(counts.get(code, 0)))
    console.print(table)


def show_networks(connection: sqlite3.Connection, code: str) -> None:
    rows = networks(connection, code)
    if not rows:
        console.print("[yellow]No networks found for that selection.[/yellow]")
        return

    table = Table(title=f"Networks · {code}", title_style="bold cyan", border_style="blue")
    for column, color in (
        ("BSSID", "magenta"),
        ("SSID", "green"),
        ("Capabilities", "yellow"),
        ("Type", "cyan"),
    ):
        table.add_column(column, style=color, header_style=f"bold {color}")
    for row in rows:
        table.add_row(*(str(value).replace("\x00", "") if value is not None else "" for value in row))
    console.print(table)


def browse(path: Path) -> None:
    # Read-only mode prevents accidentally creating or modifying a database.
    with closing(sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)) as connection:
        counts = network_counts(connection)
        valid_codes = {code for _, code in NETWORK_TYPES} | {"*"}
        while True:
            show_summary(counts, path)
            choice = input("Type code (* for all, back to change database, q to quit): ").strip().upper()
            if choice == "BACK":
                return
            elif choice == "Q":
                raise SystemExit(0)
            elif choice in valid_codes:
                show_networks(connection, choice)
            else:
                console.print("[red]Invalid type. Enter a code from the table, 'back', or 'q'.[/red]")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Browse networks in a WiGLE SQLite database.")
    parser.add_argument("database", nargs="?", type=Path, help="database path (prompts if omitted)")
    args = parser.parse_args(argv)
    console.print("[bold green]Wardriving[/bold green] · WiGLE database viewer")
    if args.database is None:
        available_databases()

    path = args.database.expanduser() if args.database else None
    while True:
        if path is None:
            path = select_database()
            if path is None:
                return 0
        if not path.is_file():
            console.print(f"File not found: {path}", style="red", markup=False)
            if args.database:
                return 1
            path = None
            continue
        try:
            browse(path)
        except sqlite3.DatabaseError as exc:
            console.print(f"Cannot read {path}: {exc}", style="red", markup=False)
            if args.database:
                return 1
        path = None


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (KeyboardInterrupt, EOFError):
        console.print("\nGoodbye.")
        sys.exit(0)
