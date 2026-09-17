from src.speech_recognition import listen_live
from src.command_parser import parse_command


MODEL_PATH = "models/vosk-model-small-en-us-0.15"

while True:
    text = listen_live(
        MODEL_PATH,
        device=0
    )

    command = parse_command(text)

    print(f"\nVORA heard: {text}")
    print(f"VORA command: {command}\n")

    if command == "STOP":
        print("VORA stopped.")
        break