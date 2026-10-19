# BolType — talk, it's typed.

**Offline dictation for Windows.** Hold Right-Ctrl, talk, release — clean text lands wherever your cursor is. No cloud, no account, no subscription.

`bol` (बोल) = "speak" in Hindi.

## Why this exists

Wispr Flow charges $12–15/month and sends your voice to their servers. TypeVoice proved the better model on Mac: on-device, private, buy once. **BolType brings that model to Windows** — free, offline, open source.

## How it works

```
Hold Right-Ctrl → mic records at 16kHz → release
      → faster-whisper transcribes (offline, on your CPU)
      → text is typed into your focused app (SendInput)
```

| File | Job |
|---|---|
| `src/main.py` | Hotkey wiring: hold = record, release = transcribe + type |
| `src/recorder.py` | Mic → numpy array (16kHz mono, exactly what speech models want) |
| `src/transcriber.py` | Speech → text via faster-whisper `base.en`, int8 for CPU speed |
| `src/typer.py` | Text → focused app via `SendInput` (UNICODE flag, no layout issues) |

Each file does one job. Every non-obvious line has a comment explaining *why*.

## Quickstart (Windows, 5 minutes)

1. Install Python 3.11+ from python.org — **tick "Add python.exe to PATH"**
2. In this folder: `pip install -r requirements.txt`
3. Run: `python src/main.py` (first run downloads the speech model, ~150MB, once)
4. Open Notepad, hold **Right-Ctrl**, talk, release. Your words appear.

No-mic test: `python src/main.py --test clip.wav`

## Roadmap

- [x] **Phase 1** — core loop: hotkey → record → transcribe → type
- [ ] **Phase 2** — cleanup: strip "um"/"uh", fix spacing, auto-capitalization (+ tone selector)
- [ ] **Phase 3** — the pill: always-on-top overlay with live waveform
- [ ] **Phase 4** — memory: SQLite history, custom dictionary, snippets, settings
- [ ] **Phase 5** — polish + sell: installer, trial, license keys, landing page
- [ ] **Phase 6** — iPhone (see `docs/ios-plan.md` — Apple blocks mic in keyboards, so it's a two-piece architecture)

## Docs

- [`docs/typevoice-architecture-breakdown.md`](docs/typevoice-architecture-breakdown.md) — the TypeVoice architecture this is modeled on + Windows component map
- [`docs/wispr-flow-teardown.md`](docs/wispr-flow-teardown.md) — frame-by-frame teardown of Wispr Flow's iPhone app (from a real screen recording)
- [`docs/ios-plan.md`](docs/ios-plan.md) — why iPhone is Phase 6 and how it'd work
- [`docs/ai-studio-handoff.md`](docs/ai-studio-handoff.md) — context pack for continuing the build in Google AI Studio

## License

MIT — do what you want with it, just keep the copyright line.
