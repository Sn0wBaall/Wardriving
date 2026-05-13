#!/usr/bin/env python3

#    --------------------------------------------------
#   |      Author: Sn0wBaall                           |
#   |      Github: https://github.com/Sn0wBaall        |
#    --------------------------------------------------

import signal, os, sys, sqlite3

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich import box
    from termcolor import colored
except ImportError as e:
    print()
    print(f"[-] Libraries can't be imported\n[i] {e}\n")
    sys.exit(1)

def signal_handler(key, frame):
    print(f"{colored('[', 'white')}{colored(' EXIT ', 'white', 'on_red', attrs=['bold'])}{colored(']', 'white')}")
    sys.exit(1)

def clean_text(s):
    if s is None:
        return ""
    return str(s).replace('\x00', '')

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

    networks_list = ['All','Wi-Fi', 'BLE', 'Bluetooth', 'GSM/CDMA']
    parameters = ['*', 'W', 'E', 'B', 'A']

    network_info = Table(border_style="white")
    network_info.add_column('Network', style='red')
    network_info.add_column('Type', style='green')

    database = Table(border_style="white")
    database.add_column('Database', style='cyan')
    database.add_row(db)

    for n, p in zip(networks_list, parameters):
        network_info.add_row(n, p)

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
