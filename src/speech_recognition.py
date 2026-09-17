import json
import wave
import queue
import sounddevice as sd

from vosk import Model, KaldiRecognizer


def transcribe_file(audio_file, model_path):
    with wave.open(audio_file, "rb") as audio:
        model = Model(model_path)

        recognizer = KaldiRecognizer(
            model,
            audio.getframerate()
        )

        while True:
            data = audio.readframes(4000)

            if len(data) == 0:
                break

            recognizer.AcceptWaveform(data)

        result = json.loads(recognizer.FinalResult())

        return result.get("text", "")

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

    recognizer = KaldiRecognizer(model, sample_rate)

    def audio_callback(indata, frames, time, status):
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
            data = audio_queue.get()

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")

                if text:
                    return text