# TypeVoice — Architecture Breakdown + Windows Build Guide

## What it is (one line)
Hold a key, talk, release — clean punctuated text gets typed into whatever app you are in. Fully offline. No account. No subscription. $79 once.

It is a privacy-first dictation app for Mac, positioned directly against Wispr Flow (which sends your voice to the cloud and charges $12–15/month). The pitch: 4x faster than typing, 0.3 seconds to text, nothing ever leaves your machine.

## The use case (who pays and why)
Anyone who types all day: writers, developers dictating into coding assistants, founders writing messages and emails, people with RSI. The buyer logic is simple — "I talk 4x faster than I type, and I don't want a company storing my voice." The one-time price vs subscription is the wedge: buy once, own it forever.

## The real architecture (from their open-source repo)

The pipeline has 6 stages. Every stage maps to a folder in their code:

**1. Capture** — Listens for your hotkey globally (hold Right-Cmd, tap to toggle, etc.), then records the mic at 16kHz. Also runs an FFT analysis so the pill UI can show a live waveform.

**2. Engine (speech → text)** — Runs **NVIDIA Parakeet TDT 0.6B v2** on the Mac's Neural Engine via a library called FluidAudio. The model (~450MB) downloads once on first launch. English-only by design — that's what makes it fast and accurate. This is the brain.

**3. Text (cleanup)** — Two layers. First a deterministic rule-based cleaner: removes fillers ("um", "uh"), stutters, formats numbers, turns pauses into paragraphs and the word "bullet" into list items. Then Apple's on-device AI model polishes punctuation and tone — under a hard 1.2-second deadline that *never blocks* insertion (if the AI is slow, the raw text still lands).

**4. Insert (text → your app)** — Types into the focused app through macOS Accessibility API. Smart details: it reads the words before your cursor to decide spacing and capitals, and it never touches your clipboard. Fallback: paste + instantly restore the clipboard.

**5. HUD (the pill)** — A small glass overlay that appears while you hold the key, shows the live waveform, displays the sentence as it's typed, then retreats. Menu-bar app, six screen positions, three visual styles.

**6. Store + Support** — SQLite database for history and a searchable log ("Summary" shows time saved), a custom Dictionary (teach it names once, it spells them right forever), style settings (casing, punctuation, tone), licensing, and auto-updates.

**Business layer:** code is GPL v3 (anyone can read/fork it, but forks must stay open source and can't use the name). What they sell is the signed, notarized build + support + auto-updates. Payments via Dodo Payments (license key, 7-day trial, weekly key re-check with 30-day offline grace). India price: ₹2,499.

## How YOU build this for Windows

Every Mac piece has a Windows equivalent. Here is the full mapping:

| TypeVoice stage | Mac tech | Your Windows version |
|---|---|---|
| Global hotkey | Accessibility key monitor | `RegisterHotKey` Win32 API, or the `keyboard` Python library |
| Mic capture | AVAudio → 16kHz | `sounddevice` or `pyaudio` (WASAPI under the hood) |
| Speech → text | Parakeet on Neural Engine | **faster-whisper** (`base.en` model) — free, offline, fast on CPU |
| Cleanup | Rules + Apple Intelligence | Rule-based Python cleaner first; optional local LLM via **Ollama** later |
| Type into app | Accessibility API | **`SendInput`** Win32 API — no special permission needed on Windows |
| Pill overlay | SwiftUI window | Always-on-top borderless window (`tkinter` to start, Tauri later) |
| History | SQLite | SQLite (same) |
| Auto-update | Sparkle | Tauri updater, or skip for v1 |
| Licensing | Dodo Payments | Dodo Payments (works the same on Windows) |
| Installer | .dmg | **Inno Setup** (free) or a single .exe via PyInstaller |

**Your stack (zero budget):** Python + faster-whisper + sounddevice + keyboard + SendInput via ctypes. Everything free, everything offline.

## Your build roadmap (phases, not a weekend death-march)

**Phase 1 — The core loop (the only thing that matters).** Hotkey → record while held → faster-whisper transcribes → text typed into focused app. No UI, no cleanup. If this works, you have a product. This is 100–150 lines of Python.

**Phase 2 — Cleanup.** Rule-based: strip fillers, add periods on long pauses, capitalize sentence starts. Instant quality jump, zero AI needed.

**Phase 3 — The pill.** Small always-on-top window: shows recording state, then the transcribed text. This is what makes it *feel* like a real product.

**Phase 4 — Memory.** SQLite history, custom dictionary ("spell Satyam right every time"), settings.

**Phase 5 — Polish + sell.** Installer, 7-day trial, Dodo license keys, landing page. Same playbook as TypeVoice.

## Three honest notes before you start

1. **GPL v3 means:** you can read and learn from their code, but if you copy it, your app must also be open source. Build your own implementation inspired by the architecture — that's clean and it's also the better learning path.
2. **Windows has no Neural Engine.** CPU transcription is slower than Mac. faster-whisper `base.en` is the sweet spot (fast + accurate on CPU). If the user has an NVIDIA GPU, it flies. Start with `base.en`, offer `small.en` as a quality option later.
3. **The moat is not the tech.** Whisper is free for everyone. The moat is the 0.3-second *feel*, the pill UX, the cleanup quality, and the business model (one-time price vs subscription). Nail the experience, not the model.
