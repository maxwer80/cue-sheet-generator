---
name: cinematic-performance-director
description: >-
  Direct an AI actor's performance for Kling AI video: turn a scene idea into timed acting beats
  (micro-expressions, eye lines, breath, restrained body and hair/environment motion, emotional
  progression) that Kling can actually render, plus dialogue and sound for native audio.
  Use when the user wants a scene to feel acted, emotional or subtle — "actuación", "emoción",
  "que llore", "mirada", "expresión", "performance", "beats", "dirigir la escena", "dialogue" —
  or before writing prompts for any character-driven shot.
---

# Cinematic Performance Director

Goal: a performance plan that reads as **acting**, not as a model "doing an action". Output is a
beat sheet per shot, handed to the **Cinematic Video Prompt Writer**. This skill spends no credits.

Pipeline position: Character Generator → **Performance Director** → Video Prompt Writer → Batch Video Generator.

Reply in the user's language; write the beat text that will go into prompts in **English**.

## Why this matters on Kling

Kling 3.0 renders what is described as **visible physical change over time**. Abstract emotion
words ("she feels betrayed") give generic results; physical tells in sequence ("jaw tightens,
eyes drop to the table, a slow breath out through the nose") give performance. The model also
over-animates by default — restraint has to be written in.

## Step 1 — Read the scene

Establish (ask only what's missing):
- **Who**: character(s) and their Element ids (from Character Generator, `characters/*.md`).
- **Want vs. obstacle**: what the character wants in this moment and what stops them.
- **Subtext**: what they feel but hide. Great performance = the gap between the two.
- **Start state → end state**: e.g. guarded → broken; composed → cracks → recovers.
- **Shot length**: Kling v3.0 / v3.0 omni / turbo: 3–15 s; o1: 3–10 s; v2.5/v2.6: 5 or 10 s.
  One clear emotional turn per 5 s is the ceiling; 1 turn in 3–5 s, 2 turns max in 10–15 s.

## Step 2 — Build the beat sheet

Split the shot into timed beats (≈2–4 s each). For each beat, pick from the physical vocabulary
below — at most **one face action + one body action + one environment action** per beat.

| Channel | Restrained vocabulary (prefer) | Avoid |
|---|---|---|
| Eyes | holds eye contact, gaze drops, eyes glisten, slow blink, looks away then back, eyes narrow slightly | "stares intensely", rapid eye darting |
| Mouth / jaw | lips press together, jaw tightens, corner of mouth twitches, lips part as if to speak, swallows | big smiles/screams unless intended |
| Breath | slow exhale through nose, sharp inhale, breath catches, shoulders rise and fall | panting unless running |
| Tears | eyes well up → single tear rolls down left cheek (always stage it: well → hold → fall) | "crying" (gives sobbing) |
| Head / body | slight head tilt, chin lowers, shoulders drop, leans back an inch, hand tightens on glass | walking + turning + gesturing in one beat |
| Hair / cloth | a few strands lift in the breeze, coat hem sways gently | "hair blowing wildly" |
| Environment | steam curls from cup, dust drifts in light beam, rain streaks window, candle flicker | many simultaneous moving elements |

Intensity dial — state it per shot: **subtle** (close-ups, drama), **natural** (dialogue),
**heightened** (action/genre). Default to subtle for close-ups: the lens magnifies everything.

## Step 3 — Dialogue and sound (native audio)

Kling v2.5+, v3.0 and v3.0 omni generate synced audio when `enable_audio` = `true`.
- Put spoken lines in the beat with a speaker label and tone:
  `Viktor (low, hoarse, barely above a whisper): "You were never coming back."`
- Keep lines short — ≈2–3 words per second of screen time; leave 1 s of silence before/after.
- One speaker per beat. Mark silence explicitly when silence is the performance.
- List ambience and SFX separately (rain on glass, distant traffic, clock ticking). On
  `kling-video-v2_5`, ambience/SFX go into `audio_prompt` and score into `music_prompt`.
- If the user will add music/voice in post, set audio off and say so in the plan.

## Step 4 — Camera that serves the performance

Pick one camera behavior per shot and tie it to the emotional turn:
- Slow push-in on the turn (the classic "realization" move).
- Locked-off static for restraint and tension; the performance carries it.
- Handheld with subtle sway for instability/panic.
- Rack focus from object → face to reveal thought.
Framing: ECU/CU for eyes and tears, MCU for dialogue, MS/WS when the body tells the story.

## Output format

Write the plan to `shots/<scene>-performance.md` and show it:

```markdown
## Shot 3 — "The letter" (CU, 8 s, intensity: subtle, audio: on)
Character: Viktor <<<ELEMENT_ID>>>  | Want: stay composed | Subtext: devastated
Arc: guarded eye contact → tear release → composure regained
Camera: locked-off, slow push-in starting at 0:04

| Time | Face | Body | Environment | Audio |
|---|---|---|---|---|
| 0–3 s | holds eye contact, jaw tight | hands flat on table | steam rises from cup | clock ticking |
| 3–6 s | gaze drops to letter, eyes well up, breath catches | shoulders drop slightly | — | exhale |
| 6–8 s | single tear down left cheek, looks back up, lips press together | still | a strand of hair shifts | (silence) |
```

Then hand off to **Cinematic Video Prompt Writer** to compile each shot into a Kling prompt.
