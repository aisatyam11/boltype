# BolType for iPhone — the real plan

## The one wall you must know first
**An iPhone keyboard is NOT allowed to touch the microphone.** Apple blocks it at the system level — since iOS 8, still true today, even if the user enables "Full Access." Apple's reason: a keyboard that can listen is a keylogger. So "hold a key on my keyboard and talk" is impossible on iPhone. Not a skill issue — an Apple rule.

Apple's own keyboard mic button works because Apple is Apple. Third-party keyboards can't have one.

## The architecture that actually works
Two pieces instead of one:

**Piece 1 — The BolType app (does the listening)**
- Big mic button. Tap → records via `AVAudioEngine` (normal apps CAN use the mic)
- Transcribes ON-DEVICE with whisper.cpp / WhisperKit running on the iPhone's Neural Engine — no internet, no server. (Real apps like Aiko already do this.)
- Cleanup with Apple's on-device AI (Foundation Models framework)
- Stores everything in local SQLite + your own iCloud ("your stuff" — see below)

**Piece 2 — The BolType keyboard (does the typing)**
- A custom keyboard extension with one special key: "insert last dictation"
- The app and keyboard share data through an **App Group** container (Apple's sanctioned pipe between them)
- You dictate in the app (or via Action Button), switch to WhatsApp/Notes/whatever, tap the key → text lands at the cursor via `insertText()`
- Keyboards CAN'T record, but they CAN insert text. That's the legal split.

**Bonus shortcut (no keyboard needed):** iPhone Action Button → starts recording via Shortcuts → transcription lands in the app → copy/share anywhere. Zero keyboard hassle.

## "Use my stuff" for storage — yes, and it's the default
On iPhone you don't need your own server at all:
- **On-device:** SQLite/GRDB database inside the app. Your history, dictionary, settings — on your phone, nowhere else.
- **Your iCloud:** Apple's CloudKit private database = storage inside YOUR iCloud account. Syncs to your other devices, Apple can't read it, no third-party server exists.
- This is actually MORE private than the Windows version. Nothing to self-host.

## What it costs (honest)
- **Apple Developer Program: $99/year** — required for App Store or TestFlight (letting others install it)
- **Free option for just you:** sideload with a free Apple ID via Xcode. Works, but the install expires every 7 days and needs a cable refresh. Fine for personal use, annoying forever.
- **New language:** Swift/SwiftUI. Not Python. Real learning curve — estimate 2–3 months part-time before you're comfortable.

## The smart order
1. **Finish Windows BolType first.** You're already learning Python, it costs ₹0, and desktop is where people provably pay for dictation (Wispr Flow = $12–15/month).
2. **iPhone = Phase 6.** Same brand, same engine idea, new platform. By then you'll have real users telling you if they even want it.
3. Also honest: the iPhone wedge is thinner. Apple's built-in dictation is already good and increasingly on-device. Your edge (custom dictionary, history, formatting rules) still applies — it's just a harder fight than Windows.

## If you still want to start iPhone research now
- Read: whisper.cpp iOS example + WhisperKit (GitHub) — proves on-device STT
- Read: Apple's "Custom Keyboard" extension docs — the `UITextDocumentProxy` API
- Tell Brent and we'll spec Phase 6 properly when Windows is shipped.
