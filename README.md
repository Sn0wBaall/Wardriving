# Wardriving

A Python tool to visualize data collected with [WiGLE](https://wigle.net/). It lets you filter by network type (**Wi-Fi, GSM, Bluetooth, etc.**) and display details like BSSID, SSID, capabilities and network type in clean tables, making it easy to interpret directly from the terminal.

## Installation

```bash
git clone https://github.com/Sn0wBaall/Wardriving.git
cd Wardriving
pip install -r requirements.txt
```

## Usage

```bash
python3 wardriving.py
```

The script will first show a list of `.sqlite`/`.db` files found in the current directory. Then enter the full path to your database when prompted.

Next, select a network type from the interactive menu:

| Parameter | Technology | Description |
| :---: | :--- | :--- |
| **\*** | All | All network types |
| **W** | Wi-Fi | Standard wireless networks |
| **E** | BLE | Bluetooth Low Energy devices |
| **B** | Bluetooth | Bluetooth Classic devices |
| **A** | GSM/CDMA | Cellular network technologies |

> [!IMPORTANT]
> If your database contains many devices, some may not be displayed due to terminal limits. Additionally, devices with an empty SSID field are automatically hidden to keep the output clean.
