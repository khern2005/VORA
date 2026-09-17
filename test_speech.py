from src.speech_recognition import transcribe_file
from src.command_parser import parse_command


text = transcribe_file(
    "test.wav",
    "models/vosk-model-small-en-us-0.15"
)

command = parse_command(text)

print(f"VORA heard: {text}")
print(f"VORA command: {command}")