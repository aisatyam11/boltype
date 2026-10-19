"""
BolType Phase 1 — the core loop.
HOLD Right-Ctrl -> talk -> RELEASE -> your words get typed wherever your cursor is.

Usage:
    python src/main.py                  # live mode (Windows)
    python src/main.py --test clip.wav   # transcribe a file, no mic needed
"""
import sys

from recorder import Recorder
from transcriber import Transcriber
from typer import Typer

HOTKEY = "right ctrl"  # change to "f9" if you prefer a single key


def main():
    # --test mode: no mic, no hotkey, just transcribe a file
    if len(sys.argv) == 3 and sys.argv[1] == "--test":
        print(Transcriber().transcribe_file(sys.argv[2]))
        return

    print("BolType Phase 1 — core loop")
    print(f"HOLD [{HOTKEY}] to talk, RELEASE to type. Ctrl+C to quit.\n")

    recorder = Recorder()
    transcriber = Transcriber()  # first run downloads base.en (~150MB)
    typer = Typer()

    import keyboard
    state = {"recording": False}

    def on_press(_e):
        if not state["recording"]:
            state["recording"] = True
            print("...listening")
            recorder.start()

    def on_release(_e):
        if state["recording"]:
            state["recording"] = False
            audio = recorder.stop()
            print("...thinking")
            text = transcriber.transcribe(audio)
            if text.strip():
                print(f">>> {text}")
                typer.type_text(text + " ")
            else:
                print("(heard nothing)")

    keyboard.on_press_key(HOTKEY, on_press)
    keyboard.on_release_key(HOTKEY, on_release)
    keyboard.wait()  # blocks here until Ctrl+C


if __name__ == "__main__":
    main()
