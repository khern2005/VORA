
from speech_recognition import listen_live, load_model
from command_parser import parse_command

from robot_controller import (
    connect_pico,
    execute_command,
    disconnect_pico
)

MODEL_PATH = "models/vosk-model-small-en-us-0.15"
DEVICE = 0
PICO_PORT = "/dev/ttyACM0"

# Start with False for a dry run.
# Change to True when ready for physical J1 movement.
ENABLE_MOVEMENT = True

BASE_COMMANDS = {
    "MOVE_LEFT",
    "MOVE_RIGHT",
    "STOP",
}


def main():
    print("=" * 35)
    print("VORA Voice Control - Base Joint")
    print("=" * 35)

    if not connect_pico(PICO_PORT):
        print("Cannot start: Pico not connected.")
        return

    try:
        execute_command("STATUS")

        # Reset the previous session's software STOP
        # before accepting new voice commands.
        print("Preparing Pico for a new session...")
        execute_command("RESET_STOP")
        execute_command("STATUS")

        model = load_model(MODEL_PATH)

        for text in listen_live(model, device=DEVICE):
            print(f"\nVORA heard: {text}")

            instruction = parse_command(text)
            command = instruction["command"]

            if command == "UNKNOWN":
                print("Command not recognized.")
                continue

            if command not in BASE_COMMANDS:
                print("Command disabled:", command)
                continue

            print("Command:", command)

            if instruction["angle"] is not None:
                print("Angle:", instruction["angle"])

            if instruction["speed"] is not None:
                print("Speed:", instruction["speed"])

            if command == "STOP":
                print("STOP recognized. Shutting down VORA.")
                break

            if ENABLE_MOVEMENT:
                print("Sending movement command to Pico...")
                execute_command(command)
            else:
                print("Dry run:", command)

    except KeyboardInterrupt:
        print("\nVoice control interrupted.")

    finally:
        # Request a stop before closing the serial connection.
        execute_command("STOP")
        disconnect_pico()


if __name__ == "__main__":
    main()
