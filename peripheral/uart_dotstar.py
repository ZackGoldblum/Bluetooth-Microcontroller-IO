import time
from adafruit_ble import BLERadio
from adafruit_ble.services.nordic import UARTService
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement

import board
import adafruit_dotstar

# LED setup
led = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)

def led_blue():
    """Turn LED blue"""
    led.brightness = 0.05
    led[0] = (0, 0, 255) 

def led_green():
    """Turn LED green"""
    led.brightness = 0.05
    led[0] = (0, 255, 0) 

def blink_led_fast():
    """Blink the LED fast"""
    led.brightness = 0.0
    time.sleep(0.25)
    led.brightness = 0.05
    time.sleep(0.25)
    
led_blue()

# BLE setup
ble = BLERadio()
device_name = "MY_BLE_DEVICE"
BLERadio.name = device_name
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

while True:
    ble.start_advertising(advertisement)
    while not ble.connected:
        blink_led_fast()

    led_green()
    time.sleep(1)
    led_blue()
    
    loop_count = 0
    while ble.connected:
        time.sleep(1)
        packet = f"Hello world - {loop_count}".encode("utf-8")
        uart.write(packet)
        loop_count += 1