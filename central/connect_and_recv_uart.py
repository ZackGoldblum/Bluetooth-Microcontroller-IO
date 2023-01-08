""" Central device.
    Listen for a UART BLE advertisement and receive data once connected to a specified device.
"""

import asyncio
import bleak
from discover_devices import discover_devices

RX_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"  # UART receive data UUID

def handle_RX(sender: int, data: bytearray) -> None: 
    """ Called whenever BLE data is received.

    Args:
        sender (int): BLE device handle.
        data (bytearray): Data received from BLE device.

    """
    data = data.decode("utf-8")
    print(f"Received: {data}")

async def handle_disconnect(client: bleak.BleakClient) -> None:
    """ Disconnect from BLE device.

    Args:
        client (bleak.BleakClient): BLE device client.
    """
    await client.disconnect()

async def connect_and_recv(device: bleak.backends.device.BLEDevice, recv_time: int) -> None:
    """ Connect to BLE device and receive data.

    Args:
        device (bleak.backends.device.BLEDevice): BLE device.
        recv_time (int): Number of seconds of BLE data to receive.
    """
    print(f"Attempting to connect to {device.address}")
    async with bleak.BleakClient(device.address, timeout=15.0, disconnected_callback=handle_disconnect) as client:
        print("Connected to", device.address)

        await client.start_notify(RX_UUID, handle_RX)  # start receiving data
        await asyncio.sleep(recv_time)                 # receive data for recv_time number of seconds
        await client.stop_notify(RX_UUID)              # stop receiving data
    
    await handle_disconnect(client)
    print("Disconnected from", device.address)

async def main(devices: list, recv_time: int = 10) -> None:
    """ Entrypoint into the script.

    Args:
        devices (list): BLE devices to connect to and receive data from.
        recv_time (int, optional): Number of seconds of BLE data to receive. Defaults to 10.
    """
    await asyncio.gather(*[connect_and_recv(device, recv_time) for device in devices])

# Example usage:
# --------------
# devices = asyncio.run(discover_devices("DA:A8:C0:86:B2:30", "FB:EF:7B:C8:EB:89"))
# asyncio.run(main(devices))
