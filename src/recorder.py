"""
Mic capture: records mono 16kHz audio while the hotkey is held.

Why 16kHz mono? Speech models are trained on exactly this format.
Giving them anything else (stereo, 44.1kHz) just wastes compute.
"""
import numpy as np
import sounddevice as sd

SAMPLE_RATE = 16000


class Recorder:
    def __init__(self):
        self._frames = []
        self._stream = None

    def _callback(self, indata, frames, time_info, status):
        # Called by sounddevice for every chunk of audio. We just collect.
        if status:
            print(f"[audio] {status}")
        self._frames.append(indata.copy())

    def start(self):
        self._frames = []
        self._stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
            callback=self._callback,
        )
        self._stream.start()

    def stop(self):
        """Stop recording and return everything as one float32 numpy array."""
        if self._stream:
            self._stream.stop()
            self._stream.close()
            self._stream = None
        if not self._frames:
            return np.zeros(0, dtype=np.float32)
        return np.concatenate(self._frames, axis=0).flatten()
