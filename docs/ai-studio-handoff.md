# BolType — Project Context for AI Studio
*Paste this whole file into Google AI Studio first, then give it the Phase 2 prompt below.*

## What we are building
BolType ("bol" = speak in Hindi): offline dictation for Windows. Hold Right-Ctrl, talk, release — clean text gets typed wherever the cursor is. No cloud, no account, no subscription. Python, zero budget, everything free and offline. Inspired by TypeVoice (Mac), rebuilt from scratch.

## Architecture (6 stages — Phase 1 done, you are building Phase 2+)
1. Capture (DONE) — global hotkey + mic recording
2. Engine (DONE) — speech → text, offline
3. Cleanup (YOU ARE HERE) — filler removal, capitalization, paragraphs
4. Insert (DONE) — keystrokes into focused app
5. HUD (later) — floating pill overlay
6. Store + Support (later) — history, dictionary, installer, licensing

## Current code (Phase 1 — all working, do not rewrite)

**src/main.py** — hotkey wiring:
```python
import sys
from recorder import Recorder
from transcriber import Transcriber
from typer import Typer
HOTKEY = "right ctrl"
# --test clip.wav mode transcribes a file without mic
# live mode: keyboard.on_press_key(HOTKEY) -> recorder.start()
#            keyboard.on_release_key(HOTKEY) -> stop, transcribe, type_text(text + " ")
```

**src/recorder.py** — `Recorder` class: `start()` opens `sd.InputStream(samplerate=16000, channels=1, dtype="float32")`, collects chunks via callback; `stop()` returns one flat numpy float32 array.

**src/transcriber.py** — `Transcriber` class: `WhisperModel("base.en", device="cpu", compute_type="int8")`; `transcribe(audio_np)` and `transcribe_file(path)` return plain text, `language="en"`.

**src/typer.py** — `Typer` class: `type_text(text)` → on Windows uses `ctypes.windll.user32.SendInput` with `KEYEVENTF_UNICODE` (sends raw chars, no layout issues); on other OS prints a dry-run message.

## Code conventions (follow these)
- One file = one job. Small files, clear names.
- Every non-obvious line gets a comment explaining WHY, not what. The builder is learning.
- Windows-first. New dependencies must be free, pip-installable, and work offline.
- Prefer stdlib (ctypes) over new packages. Ask before adding a dependency.
- No cloud APIs, no accounts, no telemetry. Ever. Offline is the whole point.

## Roadmap
- Phase 2 (NOW): `src/cleaner.py` — text cleanup between transcribe and type
- Phase 3: pill overlay (always-on-top window, recording indicator)
- Phase 4: SQLite history + custom dictionary + settings
- Phase 5: installer, trial, license keys

---

## PHASE 2 PROMPT (paste this after the context above)

Build Phase 2: the cleanup module.

Create `src/cleaner.py` with a `Cleaner` class and a `clean(text)` method that:
1. Removes filler words: um, uh, erm, ah, like (only standalone "like"), "you know" — case-insensitive, configurable list at the top of the file
2. Collapses stutter repeats: "I I I think" → "I think", "the the" → "the"
3. Fixes spacing: no space before . , ! ? ; :, exactly one space after them
4. Capitalizes the first letter of each sentence
5. Strips leading/trailing whitespace, collapses 3+ spaces to one

Then update `src/main.py` so the pipeline becomes: transcribe → clean → type.

Rules for your answer:
1. First explain the plan in 5 simple lines (no code yet) — I am learning
2. Then show the full cleaner.py file
3. Then show ONLY the changed lines in main.py (not the whole file)
4. Then give me 3 test sentences to try via --test mode so I can verify it works
5. Flag anything that might behave differently on Windows vs other systems
