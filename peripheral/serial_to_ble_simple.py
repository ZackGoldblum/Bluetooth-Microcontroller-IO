import time
import supervisor
from adafruit_ble import BLERadio
from adafruit_ble.services.nordic import UARTService
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement

def serial_read() -> str:
    """ Read serial data input to the BLE device.

    Returns:
        str: Received serial data.
    """
    if supervisor.runtime.serial_bytes_available:
        value = input()
        return value

# BLE setup
ble = BLERadio()
device_name = "MY_BLE_DEVICE"
BLERadio.name = device_name
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

while True:
    ble.start_advertising(advertisement)
    while not ble.connected:
        pass
    while ble.connected:
        value = serial_read()
        if value:
            uart.write(value.encode())