
import time
import serial

VALID_COMMANDS = {
    "MOVE_LEFT",
    "MOVE_RIGHT",
    "STOP",
    "STATUS",
    "RESET_STOP",
}

_pico = None


def connect_pico(port="/dev/ttyACM0"):
    global _pico

    if _pico is not None and _pico.is_open:
        return True

    try:
        _pico = serial.Serial(
            port=port,
            baudrate=115200,
            timeout=0.2,
            write_timeout=1
        )

        # Give the Pico time to initialize its serial connection.
        time.sleep(2)

        _pico.reset_input_buffer()

        print("Connected to Pico:", port)
        return True

    except (serial.SerialException, OSError) as error:
        print("Pico connection failed:", error)
        _pico = None
        return False


def execute_command(command):
    if command not in VALID_COMMANDS:
        print("Command not enabled:", command)
        return False

    if _pico is None or not _pico.is_open:
        print("Pico is not connected.")
        return False

    try:
        _pico.write((command + "\n").encode("utf-8"))
        _pico.flush()

        print("Sent to Pico:", command)

        # Collect responses for a short period.
        deadline = time.monotonic() + 1.5
        last_response = None
        received = False

        while time.monotonic() < deadline:
            if _pico.in_waiting:
                response = _pico.readline().decode(
                    "utf-8",
                    errors="replace"
                ).strip()

                if response:
                    print("Pico:", response)
                    received = True
                    last_response = time.monotonic()

            elif (
                received
                and last_response is not None
                and time.monotonic() - last_response > 0.3
            ):
                break

            else:
                time.sleep(0.02)

        if not received:
            print("No response received from Pico.")

        return True

    except (serial.SerialException, OSError) as error:
        print("Serial communication error:", error)
        return False


def disconnect_pico():
    global _pico

    if _pico is not None:
        if _pico.is_open:
            _pico.close()

        _pico = None
        print("Pico disconnected.")
