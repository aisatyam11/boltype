"""
Speech -> text using faster-whisper. Fully offline, free.

faster-whisper is a speed-optimized rebuild of OpenAI's Whisper.
"base.en" = English-only, ~150MB, the sweet spot for CPU speed vs accuracy.
"bigger model = better words but slower" — we can offer small.en later.
"""
from faster_whisper import WhisperModel


class Transcriber:
    def __init__(self, model_name="base.en"):
        print(f"Loading speech model '{model_name}' (first run downloads it)...")
        # int8 = quantized math: ~4x faster on CPU, barely any accuracy loss
        self.model = WhisperModel(model_name, device="cpu", compute_type="int8")
        print("Model ready.")

    def transcribe(self, audio):
        """audio: numpy float32 array at 16kHz -> plain text."""
        segments, _info = self.model.transcribe(audio, language="en", beam_size=5)
        return " ".join(seg.text.strip() for seg in segments).strip()

    def transcribe_file(self, path):
        """Transcribe a wav/mp3 file (for --test mode)."""
        segments, _info = self.model.transcribe(path, language="en", beam_size=5)
        return " ".join(seg.text.strip() for seg in segments).strip()
