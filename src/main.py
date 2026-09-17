from speech_recognition import listen_live, load_model
from command_parser import parse_command
from robot_controller import execute_command


MODEL_PATH = "models/vosk-model-small-en-us-0.15"

DEVICE = 0


def main():
    print("=" * 35)
    print("VORA Voice Control")
    print("=" * 35)

    model = load_model(MODEL_PATH)

    while True:
        text = listen_live(model, device=DEVICE)

        print(f"\nVORA heard: {text}")

        command = parse_command(text)

        if command == "UNKNOWN":
            print("Command not recognized.")
            continue

        print(f"Command: {command}")

        execute_command(command)

        if command == "STOP":
            print("VORA shutting down.")
            break


if __name__ == "__main__":
    main()