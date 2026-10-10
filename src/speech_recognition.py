
import json
import wave
import queue
import time
import sounddevice as sd

from vosk import Model, KaldiRecognizer


COMMAND_PHRASES = [
    "move left", "move right", "move up", "move down",
    "open gripper", "close gripper", "go home", "stop",
    "don't move left", "don't move right",
    "don't move up", "don't move down",
    "don't open gripper", "don't close gripper",
    "do not move left", "do not move right",
    "do not move up", "do not move down",
    "do not open gripper", "do not close gripper"
]

NUMBER_WORDS = [
    "zero", "one", "two", "three", "four",
    "five", "six", "seven", "eight", "nine",
    "ten", "eleven", "twelve", "thirteen",
    "fourteen", "fifteen", "sixteen",
    "seventeen", "eighteen", "nineteen",
    "twenty", "thirty", "forty", "fifty",
    "sixty", "seventy", "eighty", "ninety",
    "hundred", "degree", "degrees",
    "percent", "speed", "at", "of", "and"
]

VOCABULARY = COMMAND_PHRASES + NUMBER_WORDS + ["[unk]"]

# Wait this long after the latest recognized fragment.
COMMAND_WAIT_SECONDS = 1.2


def transcribe_file(audio_file, model_path):
    with wave.open(audio_file, "rb") as audio:
        model = Model(model_path)
        recognizer = KaldiRecognizer(
            model, audio.getframerate()
        )

        while True:
            data = audio.readframes(4000)
            if not data:
                break
            recognizer.AcceptWaveform(data)

        return json.loads(
            recognizer.FinalResult()
        ).get("text", "")


def load_model(model_path):
    print("Loading VORA speech model...")
    model = Model(model_path)
    print("Speech model loaded.")
    return model


def listen_live(model, device=None):
    audio_queue = queue.Queue()

    device_info = sd.query_devices(device, "input")
    sample_rate = int(device_info["default_samplerate"])

    print(f"Microphone sample rate: {sample_rate} Hz")

    recognizer = KaldiRecognizer(
        model,
        sample_rate,
        json.dumps(VOCABULARY)
    )

    pending_parts = []
    last_fragment_time = None

    def audio_callback(indata, frames, time_info, status):
        if status:
            print(status)
        audio_queue.put(bytes(indata))

    print("VORA is listening...")

    with sd.RawInputStream(
        samplerate=sample_rate,
        blocksize=8000,
        device=device,
        dtype="int16",
        channels=1,
        callback=audio_callback
    ):
        while True:
            try:
                data = audio_queue.get(timeout=0.1)
            except queue.Empty:
                data = None

            if data is not None:
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    text = result.get("text", "").strip()

                    if text:
                        print(f"Speech fragment: {text}")

                        # Standalone STOP bypasses the buffer.
                        if text == "stop":
                            pending_parts.clear()
                            yield "stop"
                            return

                        pending_parts.append(text)
                        last_fragment_time = time.monotonic()

            # Wait briefly for any remaining fragments.
            if (
                pending_parts
                and last_fragment_time is not None
                and time.monotonic() - last_fragment_time
                >= COMMAND_WAIT_SECONDS
            ):
                combined = " ".join(pending_parts)

                pending_parts.clear()
                last_fragment_time = None

                yield combined
