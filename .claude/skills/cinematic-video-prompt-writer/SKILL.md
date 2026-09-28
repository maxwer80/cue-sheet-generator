---
name: cinematic-video-prompt-writer
description: >-
  Write production-ready Kling AI video prompts and pick the right model, tool and parameters for
  each shot: text-to-video, image-to-video (first/last frame), multi-reference omni, Elements,
  multi-shot and native audio. Compiles performance beat sheets into prompts with a proven
  structure (subject → action over time → setting → camera → light/lens → style → audio).
  Use for "prompt", "escribe el prompt", "video prompt", "plano", "shot", "cámara", "Kling prompt",
  "mejorar prompt", or whenever a video is about to be generated on Kling.
---

# Cinematic Video Prompt Writer

Goal: every shot gets (1) the right Kling tool + model, (2) a prompt written the way Kling
parses best, (3) exact argument values. Output feeds the **Cinematic Batch Video Generator**.
This skill spends no credits; generating is the Batch Generator's job (or a single confirmed call).

Pipeline position: Character Generator → Performance Director → **Video Prompt Writer** → Batch Video Generator.

Reply in the user's language; write the prompts themselves in **English**.

## Step 0 — Specs come from `who_am_i`

Call `mcp__KLING__who_am_i` with `tools` = `["text_to_video","image_to_video"]` (add
`motion_control` if relevant) once per session. Use only models/arguments/values it returns;
all values are strings. The table below reflects the current catalogue — if `who_am_i`
disagrees, `who_am_i` wins.

## Step 1 — Choose tool and model

| Situation | Tool | Model | Notes |
|---|---|---|---|
| No image, best quality, audio/dialogue | `text_to_video` | `kling-video-v3_0_omni` (default) | 3–15 s, up to 4k (members), `prefer_multi_shots` default false |
| No image, multi-shot storytelling | `text_to_video` | `kling-video-v3_0` | `prefer_multi_shots` default **true** |
| No image, cheaper/faster drafts | `text_to_video` | `kling-video-v3_0_turbo` | no audio argument |
| Animate ONE still, no Element | `image_to_video` | `kling-video-v3_0_turbo` | Kling's recommended single-image model; input `first_image` |
| Start + end frame, or Element on a first frame | `image_to_video` | `kling-video-v3_0` | `first_image` + optional `tail_image`; ≤3 Elements; prompt optional |
| Several reference images and/or several characters | `image_to_video` | `kling-video-v3_0_omni` | inputs `image_1..image_7`, refer to them as `图片1..图片7`; ≤7 Elements; prompt required |
| Copy a real motion (dance, fight choreography) onto a character | `motion_control` | `kling-video-v3_0` | `motionDirection` required; `motionId` **or** `video`, never both |
| Budget, fixed 5/10 s, separate SFX & music prompts | either | `kling-video-v2_5` | `audio_prompt`, `music_prompt`, `enable_asmr` |

Consistency rule: if a recurring character exists, generate its shots through
`image_to_video` with the Element (text_to_video cannot take Elements). Best result for hero
shots: first generate the exact first frame with `image_to_image` + Element (Character
Generator), then animate it with `image_to_video`.

Aspect ratio: `16:9` film/YouTube, `9:16` Reels/TikTok/Shorts, `1:1` feed. In `image_to_video`
v3_0/turbo there is no `aspect_ratio` — the output follows the input image, so generate the
still at the target ratio.

## Step 2 — Prompt structure

Order matters: Kling weights the start of the prompt most. Aim for **50–150 words**; one shot,
one main action, one camera move.

```
[SHOT SIZE + ANGLE]. [SUBJECT with 2–3 anchoring traits] [MAIN ACTION as visible change over time,
in beat order: "first…, then…, finally…"]. [SETTING + time of day + weather/atmosphere with
1–2 moving elements]. [CAMERA MOVE with speed + direction]. [LIGHTING + LENS]. [STYLE / GRADE /
FILM STOCK]. [AUDIO: dialogue with speaker + tone in quotes; ambience; SFX].
```

Example (text_to_video, v3_0_omni, 8 s, 16:9):

```
Close-up, eye level. A 58-year-old heavy-set man with deep-set grey eyes, white stubble and a scar
through his left eyebrow, wearing a faded navy peacoat, sits at a diner table holding a letter.
He holds eye contact with someone off-camera, jaw tight; then his gaze drops to the letter, his
eyes well up and his breath catches; finally a single tear runs down his left cheek and he looks
back up, pressing his lips together. Rainy night, neon sign glow through the window, steam rising
from a coffee cup. Locked-off camera with a slow push-in during the final seconds. Low-key
tungsten light from the side, cool blue neon rim light, 50mm anamorphic lens, shallow depth of
field. 1970s neo-noir, 35mm film grain, muted teal-and-amber grade. Audio: rain on glass, distant
traffic, a clock ticking; he whispers, hoarse: "You were never coming back."
```

### Writing rules (what moves the needle)

1. **Motion is the prompt.** Describe what changes, in order. Static description → static video.
2. **Camera verbs with speed + direction**: slow dolly in, tracking shot following from behind,
   crane up revealing the city, orbit 90° around subject, handheld with subtle sway, locked-off
   static, rack focus from the glass to her face, whip pan. One move per shot.
3. **Say it positively.** There is no negative-prompt field here; write "calm, steady camera",
   "hands stay still on the table" instead of "no shaking".
4. **Image-to-video: don't re-describe the image.** The frame already defines look and subject;
   the prompt describes **motion, camera and audio** only (plus the Element tag). Re-describing
   causes drift.
5. **Physics & cause**: give forces a cause — "the wind from the open door lifts the papers".
6. **Light is specific**: source + direction + color ("golden hour backlight", "overhead
   fluorescent flicker", "single practical lamp, warm"), and a lens (24mm wide, 50mm, 85mm portrait,
   macro, anamorphic).
7. **Restraint for faces** in close-ups: use the Performance Director vocabulary.
8. **Text/logos** in-frame are unreliable; add them in post.
9. **Duration fits the action**: ≈1 beat per 2–4 s. Don't pad 15 s with one action; don't cram 4
   actions into 5 s.

### Elements and references

- Element: write `<<<ELEMENT_ID>>>` exactly where the character appears in the prompt, and pass
  `elements` = `[{"id":"<ELEMENT_ID>","bindName":"<Name>"}]` (JSON string). Keep 1–2 anchor
  traits in words too.
- Omni references: `image_1` → write `图片1` in the prompt, e.g. `The woman from 图片1 walks into
  the room from 图片2, wearing the jacket from 图片3.` Assign one role per image.
- `image_to_image` inputs for Kling image models must be URLs from `mcp__KLING__file_upload` or
  previous Kling results.

### Multi-shot (v3.0 / v3.0 omni with `prefer_multi_shots` = `true`)

Write numbered shots with durations that sum to `duration`, and keep subject wording identical:

```
Shot 1 (0–4 s): Wide establishing shot, rainy neon street at night, the man <<<ID>>> walks toward
the diner. Shot 2 (4–8 s): Medium shot inside, he sits and unfolds a letter. Shot 3 (8–12 s):
Close-up, his eyes well up as he reads.
```

Use single-shot generations instead when each shot needs its own exact framing or reference image.

### Audio (`enable_audio`)

- On for dialogue/ambience-driven scenes (default true on audio-capable models); off when the
  edit will be scored in post or for cleaner visual-only drafts.
- Dialogue: speaker label + delivery + quoted line; ≈2–3 words per second.
- v2.5: put SFX into `audio_prompt`, score into `music_prompt`.

## Step 3 — Output: the shot spec

For every shot produce a spec block (and write all of them to `shots/<project>-prompts.md`):

```yaml
- id: S03
  title: The letter
  tool: text_to_video
  model: kling-video-v3_0_omni
  arguments:
    prompt: "..."
    duration: "8"
    aspect_ratio: "16:9"
    resolution: "1080p"
    imageCount: "1"
    enable_audio: "true"
    # elements: '[{"id":"123","bindName":"Viktor"}]'   # an argument, passed as a JSON string
  inputs: []            # e.g. [{name: first_image, inputType: URL, url: ...}] for image_to_video
```

Validate before handing off: model exists for that tool; every argument name is declared for that
model; values are in `allowedValues`; required inputs present; Element use is allowed for that
model/tool. Then offer to run it with **Cinematic Batch Video Generator** (or submit a single shot
after the user confirms).
