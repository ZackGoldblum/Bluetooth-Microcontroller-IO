""" Peripheral device.
    Advertise UART BLE connection, read serial port data via USB, and transmit data once connected.
    Connection status is indicated using an on-board Adafruit DotStar LED.
"""

import time
import supervisor
from adafruit_ble import BLERadio
from adafruit_ble.services.nordic import UARTService
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement

import board
import adafruit_dotstar

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
ble.name = device_name
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

while True:
    ble.start_advertising(advertisement)
    while not ble.connected:
        blink_led_fast()

    led_green()
    time.sleep(1)
    led_blue()

    while ble.connected:      
        data = serial_read()
        if data:
            packet = create_packet(data)
            uart.write(packet)