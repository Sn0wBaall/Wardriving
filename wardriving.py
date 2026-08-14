#!/usr/bin/env python3

#    --------------------------------------------------
#   |      Author: Sn0wBaall                           |
#   |      Github: https://github.com/Sn0wBaall        |
#    --------------------------------------------------

import signal, os, sys, sqlite3

try:
    from rich.console import Console
    from rich.table import Table
    from rich import box
    from termcolor import colored
    from pathlib import Path
except ImportError as e:
    print()
    print(f"[-] Libraries can't be imported\n[i] {e}\n")
    sys.exit(1)

def signal_handler(key, frame):
    print(f"{colored('[', 'white')}{colored(' EXIT ', 'white', 'on_red', attrs=['bold'])}{colored(']', 'white')}")
    sys.exit(1)

def databases():

    extensions = ('.sqlite', '.db')

    file_list = [f.name for f in Path('.').iterdir() if f.suffix in extensions]
    
    db_table = Table(border_style='white')
    db_table.add_column('Databases', style='cyan')
    
    for file in file_list:
        
        db_table.add_row(file)

    console.print(db_table)

def clean_text(s):
    if s is None:
        return ""
    return str(s).replace('\x00', '')

NETWORK_TYPES = (
    ('All', '*'),
    ('Wi-Fi', 'W'),
    ('BLE', 'E'),
    ('Bluetooth', 'B'),
    ('GSM', 'G'),
    ('CDMA', 'C'),
    ('LTE', 'L'),
    ('WCDMA', 'D'),
    ('5G NR', 'N'),
    ('NFC', 'F'),
)

def networks_amount(cursor):

    codes = tuple(code for _, code in NETWORK_TYPES[1:])

    placeholders = ','.join('?' for _ in codes)

    query = f"SELECT type, count(DISTINCT ssid) FROM network WHERE type IN ({placeholders}) AND ssid != '' GROUP BY type"

    cursor.execute(query, codes)

    return dict(cursor.fetchall())

signal.signal(signal.SIGINT, signal_handler)

console = Console()

BANNER = r'''
$$\      $$\ $$\   $$\                 $$\           $$\            $$\                     
$$ | $\  $$ |$$ |  $$ |                $$ |        $$$$ |           \__|                    
$$ |$$$\ $$ |$$ |  $$ | $$$$$$\   $$$$$$$ | $$$$$$\\_$$ |$$\    $$\ $$\ $$$$$$$\   $$$$$$\  
$$ $$ $$\$$ |$$$$$$$$ |$$  __$$\ $$  __$$ |$$  __$$\ $$ |\$$\  $$  |$$ |$$  __$$\ $$  __$$\ 
$$$$  _$$$$ |\_____$$ |$$ |  \__|$$ /  $$ |$$ |  \__|$$ | \$$\$$  / $$ |$$ |  $$ |$$ /  $$ |
$$$  / \$$$ |      $$ |$$ |      $$ |  $$ |$$ |      $$ |  \$$$  /  $$ |$$ |  $$ |$$ |  $$ |
$$  /   \$$ |      $$ |$$ |      \$$$$$$$ |$$ |    $$$$$$\  \$  /   $$ |$$ |  $$ |\$$$$$$$ |
\__/     \__|      \__|\__|       \_______|\__|    \______|  \_/    \__|\__|  \__| \____$$ |
                                                                                  $$\   $$ |
                                                                                  \$$$$$$  |
                                                                                   \______/ 
'''

info = Table(border_style="white", box=box.ROUNDED, show_header=False, width=50)

info.add_column("Key", style="bold red", width=12)
info.add_column("Value", style="cyan")

info.add_row('Author', 'Sn0wBaall')
info.add_row('Github', 'https://github.com/Sn0wBaall')

os.system("clear")

print(colored(BANNER, 'green', attrs=['bold']))
console.print(info)
databases()

while True:
    print()
    db = input(f"{colored('>>', 'blue', attrs=['bold'])} {colored('Enter the full path of your database', 'white')}\n {colored('>>', 'magenta', attrs=['bold'])} ")

    if not os.path.isfile(db):
        print(f"{colored('>>', 'red', attrs=['bold'])} {colored('File doesn\'t exist', 'white', 'on_red', attrs=['bold'])} {colored('<<', 'red', attrs=['bold'])}")
        print()
        continue

    print()

    connection = sqlite3.connect(db)
    cursor = connection.cursor()

    network_info = Table(border_style="white")
    network_info.add_column('Network', style='red')
    network_info.add_column('Type', style='green')
    network_info.add_column('Amount', style='green')

    amounts = networks_amount(cursor)

    database = Table(border_style="white")
    database.add_column('Database', style='cyan')
    database.add_row(db)

    for name, code in NETWORK_TYPES:
        amount = sum(amounts.values()) if code == '*' else amounts.get(code, 0)
        network_info.add_row(name, code, str(amount))

    while True:
        console.print(network_info)
        console.print(database)

        print()
        
        network_type = input(f"{colored('>>', 'blue', attrs=['bold'])} {colored('Which network type do you want to view?', 'white')}\n {colored('>>', 'magenta', attrs=['bold'])} ")
        
        if network_type == "":
            print(f"{colored('>>', 'red', attrs=['bold'])} {colored('Invalid option', 'white', 'on_red', attrs=['bold'])} {colored('<<', 'red', attrs=['bold'])}")
            print()
            continue
        
        query = "SELECT bssid, ssid, capabilities, type FROM network WHERE ssid != '' "

        if network_type and network_type != '*':
            query += f"AND type = '{network_type}' "
        
        query += "GROUP BY ssid"

        cursor.execute(query)
        results = cursor.fetchall()

        if not results:
            print(f" {colored('>>', 'red')} {colored('No networks of this type were found', 'white', 'on_red', attrs=['bold'])} {colored('<<', 'red')}")
            print() 
            continue

        table = Table(style="white")
        table.add_column('BSSID', style='magenta')
        table.add_column('SSID', style='green')
        table.add_column('Capabilities', style='yellow')
        table.add_column('Type', justify='center')

        for row in results:
            table.add_row(
                clean_text(row[0]),
                clean_text(row[1]),
                clean_text(row[2]),
                clean_text(row[3])
            )

        console.print(table)

    connection.close()
