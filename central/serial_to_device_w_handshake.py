""" Central device.
    Send serial port data to device via USB to the device.
    Messages can be sent in a loop or manually.
    Includes an echo handshake with the peripheral device to confirm serial connection. 
"""

import time
import serial

def get_COM_port() -> str:
    """ Have user enter the COM port of the BLE device.

    Returns:
        str: COM port.
    """
    COM_num = input("Enter COM number: ")
    COM_port = f"COM{COM_num}"
    return COM_port

def out_packet(msg: str) -> bytearray:
    """ Convert input message into a serial packet.

    Args:
        msg (str): Message to send to the device.

    Returns:
        bytearray: Data packet to output via serial.
    """
    return f"{msg}\r".encode("utf-8")

def write_to_device(output_type: str, ser: serial.Serial) -> None:
    """ Send data to the BLE device via serial.

    Args:
        output_type (str): "loop" or "manual".
        ser (serial.Serial): Serial port connection.
    """
    try:
        if output_type == "loop":
            i = 0
            while ser:
                msg = f"{i} - Hello!"
                ser.write(out_packet(msg))
                i += 1
                time.sleep(1)
                print(f"Sent '{msg}'")
        elif output_type == "manual":
            while ser:
                msg = input("Enter your message: ")
                ser.write(out_packet(msg))
                print(f"Sent '{msg}'")
                data = ser.readline().decode().strip()
    except serial.SerialException:
        print("Serial connection closed.")
    except KeyboardInterrupt:
        print("\nProgram ended.")

def main() -> None:
    """ CLI to write serial messages to the device.
    """
    COM_port = get_COM_port()
    serial_connected = False
    ser = None

    while not ser:  # prompt user until valid serial port is entered 
        try:
            ser = serial.Serial(COM_port, 9600, timeout=0.1)
            #print(f"SER {ser}")
        except serial.SerialException:
            print("Invalid COM port. Please try again.")
            COM_port = get_COM_port()

    ser.write(out_packet("serial"))
    timeout = time.time() + 3  # 3-second timeout if no response from device

    while not serial_connected:  # listen for response from device
        data = ser.readline().decode().strip()
        if data == "connected":
            print("Serial connection established.")
            serial_connected = True
        elif time.time() > timeout:
            print("Failed to establish serial connection.")
            break

    if serial_connected:  # enter messaging interface
        output_type = None
        while output_type not in ("loop", "manual"):
            output_type = str(input("Enter output type ('loop' or 'manual'): "))
        print("Press CTRL+C to end.")
        write_to_device(output_type, ser)

if __name__ == "__main__":
    main()