# Wispr Flow iPhone Teardown (from Satyam's screen recording, 2026-10-01)

## The money shot: the mic wall is real, on video
At ~0:30 in the recording, tapping the mic button inside the Wispr Flow keyboard shows:

> "Couldn't start audio capture. Tap the mic to try again, or quit and reopen the Flow app if it keeps happening."

This is the iOS keyboard mic block, live. Even Wispr Flow — the market leader — cannot record audio inside their own keyboard. This confirms the architecture in ios-plan.md: on iPhone, the keyboard can NEVER be the recorder.

## Their actual flow (frame by frame)
1. User switches to the Wispr Flow keyboard via the globe icon (sits alongside English (India) + Emoji)
2. Keyboard shows a "Start" button with waveform icon + number/symbol layout
3. Tap mic → "Starting..." → audio capture FAILS (mic wall)
4. Workaround: the **Flow app opens full-screen** (waveform logo takeover) — the containing app does the recording
5. "Listening — iPhone Microphone" with live animated waveform dots
6. Tap ✓ → transcription happens → text inserted at cursor back in the original app
7. A "Formal." tone pill sits in the keyboard — tone selector for cleanup style

## Their app structure (bottom tabs)
- **Home** · **Dictionary** (custom words — same as our Phase 4 plan) · **Snippets** (text expansions) · **Style** (tone/formatting) · **Scratchpad** (history, dated notes e.g. "22 Sep 2026")

## What BolType steals (mapped to phases)
- [ ] **Tone selector** (Formal/Casual) → Phase 2/4: one dropdown in cleanup, huge perceived value, trivial to build
- [ ] **Dictionary tab** → already Phase 4, validated as table-stakes
- [ ] **Snippets** → Phase 4+: user-defined text expansions (";addr" → full address). Power-user candy.
- [ ] **Honest error messages** → when mic/hotkey fails, say exactly what to do (their "quit and reopen the Flow app" is the right pattern)
- [ ] **Scratchpad history with dates** → Phase 4, already planned

## The strategic insight
Wispr Flow's iPhone flow is **clunky by force**: keyboard → fail → app-switch → record → switch back → insert. Five steps, two app switches, Face ID interruptions.

**On Windows, BolType has no such restriction.** Global hotkey + SendInput = hold, talk, release, done. Zero app switching. Our Windows UX can be strictly BETTER than the market leader's mobile UX — not by out-building them, but because the platform lets us.

That's the wedge to sell: "the dictation flow Wispr wishes iOS allowed."
