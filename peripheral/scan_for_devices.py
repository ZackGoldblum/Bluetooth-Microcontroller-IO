import asyncio
from bleak import BleakScanner

async def discover_devices() -> list: 
    """Discover advertising BLE devices

    Returns:
        list: discovered BLE devices 
    """
    print("\nScanning for devices...")
    devices = await BleakScanner.discover(timeout=5)
    print("Devices found:")

    for device in devices:
        print(f"- {repr(device)}")

    return devices

devices = asyncio.run(discover_devices())