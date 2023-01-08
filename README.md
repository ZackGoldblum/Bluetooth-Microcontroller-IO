# Bluetooth-Microcontroller-IO

## Introduction
Useful Python scripts for working synchronously with multiple Bluetooth-enabled microcontrollers running CircuitPython.

This project is subdivided into two directories: **central** and **peripheral**.

* **Central** contains server-side scripts for discovering devices, connecting to devices, and transmitting/receiving data. 

* **Peripheral** contains client-side scripts that are run on BLE-enabled microcontrollers.

## Dependencies
* [Bleak](https://github.com/hbldh/bleak) for Bluetooth communication on central devices.
* [Adafruit CircuitPython BLE](https://github.com/adafruit/Adafruit_CircuitPython_BLE) for Bluetooth communication on peripheral devices.

## Usage
A docstring at the top of each script details its function. Generally, a script from the **central** directory is run on a PC or single-board computer and a script from the **peripheral** directory is run on a microcontroller. The following Python file name conventions indicate the function:
* **Simple:** Purely Bluetooth functionality. 
* **Dotstar:** Adds LED indication for boards with Adafruit DotStar LEDs.
* **Serial:** Reads data via USB connection and transmits it via Bluetooth.
* **Handshake:** Adds an echo to confirm serial connection.