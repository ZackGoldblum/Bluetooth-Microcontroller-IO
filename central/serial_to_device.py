import time
import serial

def get_COM_port() -> str:
    """ Get COM port of the BLE device.

    Returns:
        str: COM port.
    """
    COM_num = input("Enter COM number: ")
    COM_port = f"COM{COM_num}"
    return COM_port

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
                ser.write(msg.encode())
                i += 1
                time.sleep(1)
                print(f"Sent '{msg}'")
        elif output_type == "manual":
            while ser:
                msg = input("Enter your message: ")
                ser.write(msg.encode())
                print(f"Sent '{msg}'")
    except serial.SerialException:
        print("Serial connection closed.")

def main() -> None:
    """ Entrypoint into the script.
    """
    COM_port = get_COM_port()
    ser = None
    while not ser:
        try:
            ser = serial.Serial(COM_port, 9600, timeout=0.5)
        except serial.SerialException:
            print("Invalid COM port. Please try again.")
            COM_port = get_COM_port()

    output_type = None
    while output_type not in ("loop", "manual"):
        output_type = str(input("Enter output type ('loop' or 'manual'): "))
    write_to_device(output_type, ser)

if __name__ == "__main__":
    main()