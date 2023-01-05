import time
from adafruit_ble import BLERadio
from adafruit_ble.services.nordic import UARTService
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement

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
    loop_count = 0
    while ble.connected:
        time.sleep(1)
        packet = f"Hello world - {loop_count}".encode("utf-8")
        uart.write(packet)
        loop_count += 1