""" Central device.
    Listen for BLE advertisements and display the discovered devices.
    Addresses can be specified to search for known devices.
"""

import asyncio
from bleak import BleakScanner

async def discover_devices(*device_addresses: str) -> list: 
    """ Discover advertising BLE devices.
        If no device addresses are passed, all advertising BLE devices are returned.
        If device addresses are passed, only matching BLE devices are returned.

    Args:
        device_addresses (str, optional): Specific BLE device address(es) to search for. Defaults to None.

    Returns:
        list: Discovered BLE devices
    """
    print("\nScanning for devices...")
    devices = await BleakScanner.discover(timeout=5)

    if not device_addresses:
        if devices:
            print("Devices found:")
            for device in devices:
                print(f"- {repr(device)}")
        else:
            print("No devices found.")
        return devices
    else:
        device_list = []
        for device in devices:
            if device.address in device_addresses:
                device_list.append(device)
        if device_list:
            print("Devices found:")
            print(*[f"- {device}" for device in device_list], sep="\n")
        else:
            print("No devices found.")
        return device_list

# Example usage:
# --------------
# devices = asyncio.run(discover_devices())
# devices = asyncio.run(discover_devices("DA:A8:C0:86:B2:30"))
# devices = asyncio.run(discover_devices("DA:A8:C0:86:B2:30", "FB:EF:7B:C8:EB:89"))
