import time
import supervisor
from adafruit_ble import BLERadio
from adafruit_ble.services.nordic import UARTService
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement

def create_packet(data: str) -> bytearray:
    """ Convert serial data into BLE packet.

    Args:
        data (str): Serial data.

    Returns:
        bytearray: BLE packet.
    """
    if "\r" in data:
        return data.encode("utf-8")
    else:
        return f"{data}\r".encode("utf-8")
        
# Serial setup
def serial_read() -> str:
    """ Read serial data input to the BLE device.

    Returns:
        str: Received serial data.
    """
    if supervisor.runtime.serial_bytes_available:
        data = input().strip()
        return data
            
serial_connected = False

# BLE setup
ble = BLERadio()
device_name = "MY_BLE_DEVICE"
ble.name = device_name
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

while True:
    ble.start_advertising(advertisement)
    while not ble.connected:
        blink_led_fast()

    while ble.connected:
        while not serial_connected:
            data = serial_read()
            if data:
                if "serial" in data:
                    print("connected")
                    serial_connected = True
        
        data = serial_read()
        if data:
            packet = create_packet(data)
            uart.write(packet)