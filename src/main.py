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

    for text in listen_live(model, device=DEVICE):
        print(f"\nVORA heard: {text}")

        instruction = parse_command(text)
        command = instruction["command"]

        if command == "UNKNOWN":
            print("Command not recognized or invalid parameters.")
            continue

        print(f"Command: {command}")

        if instruction["angle"] is not None:
            print(f"Angle: {instruction['angle']} degrees")

        if instruction["speed"] is not None:
            print(f"Speed: {instruction['speed']}%")

        # Controller still simulates actions for now.
        execute_command(command)

        if command == "STOP":
            print("VORA shutting down.")
            break


if __name__ == "__main__":
    main()