
import serial
import time
from serial.tools import list_ports


def main():
    print("VORA Pico 2 Command Sender")
    print("--------------------------")

    print("\nAvailable serial ports:")
    ports = list(list_ports.comports())

    for port in ports:
        print(f"{port.device}: {port.description}")

    port_name = input(
        "\nEnter Pico serial port (e.g. COM3): "
    ).strip()

    try:
        pico = serial.Serial(
            port=port_name,
            baudrate=115200,
            timeout=0.2
        )

    except serial.SerialException as error:
        print("Could not connect to Pico:", error)
        return

    time.sleep(2)

    print("\nConnected to Pico!")
    print("\nAvailable commands:")
    print("MOVE_LEFT      - Base left")
    print("MOVE_RIGHT     - Base right")
    print("SHOULDER_UP    - Shoulder up")
    print("SHOULDER_DOWN  - Shoulder down")
    print("STATUS        - Motor status")
    print("STOP          - Software stop both motors")
    print("RESET_STOP    - Reset software stop")
    print("EXIT          - Close program")

    try:
        while True:
            command = input("\nCommand: ").strip().upper()

            if command == "EXIT":
                break

            if not command:
                continue

            pico.write((command + "\n").encode("utf-8"))
            pico.flush()

            time.sleep(0.3)

            while pico.in_waiting:
                response = pico.readline().decode(
                    "utf-8",
                    errors="replace"
                ).strip()

                if response:
                    print("Pico:", response)

    except KeyboardInterrupt:
        print("\nProgram interrupted.")

    finally:
        pico.close()
        print("Serial connection closed.")


if __name__ == "__main__":
    main()
