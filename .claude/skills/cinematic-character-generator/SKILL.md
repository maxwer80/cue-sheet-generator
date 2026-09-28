---
name: cinematic-character-generator
description: >-
  Design a film-grade, reusable character for Kling AI: write the character bible, generate a
  consistent reference set (hero portrait + turnaround angles), and register it as a Kling Element
  so the same face, wardrobe and proportions survive across every later image and video shot.
  Use when the user wants to create, design, cast or lock a character/actor/protagonist, build a
  character sheet or turnaround, or make a subject consistent across shots ("personaje",
  "protagonista", "character sheet", "mismo personaje en todos los planos", "Element").
---

# Cinematic Character Generator

Goal: one character that looks identical in every shot. On Kling, consistency comes from an
**Element** (a reusable subject built from a cover image + 1–3 secondary angles), not from
repeating a text description. This skill produces the reference images and the Element.

Pipeline position: **Character Generator** → Performance Director → Video Prompt Writer → Batch Video Generator.

## Ground rules

- Reply in the user's language. Write Kling prompts in **English** (best adherence).
- Call `mcp__KLING__who_am_i` (with `tools` = the tools you will use) before the first generation
  in a session. Model names, arguments and allowed values come from that response only; never
  invent them. Every argument `value` is a **string**.
- Every generation costs credits. Before submitting, show the user: model, prompt, resolution,
  aspect ratio, image count. Get a yes. Never submit "test" jobs on your own.
- Generations are async: submit → get `generationId` → poll `mcp__KLING__query_tasks` until a
  terminal status (`COMPLETED`/`PARTIAL_COMPLETED`/`succeed`, or `FAILED`/`CANCELLED`; compare
  case-insensitively). Show `works[].url`; give `urlWithoutWatermark` only if asked.
- Local files must go through `mcp__KLING__file_upload` first. Kling image models accept only
  URLs returned by `file_upload` for `image_*` inputs.

## Step 1 — Character bible (no credits)

Interview briefly (only ask what's missing), then write a compact bible and confirm it:

| Field | What to lock | Example |
|---|---|---|
| Role & arc | Who they are in the story, one line | Retired boxer hiding a debt |
| Age / build | Exact, not vague | 58, heavy-set, broad shoulders, slight stoop |
| Face | 4–6 **distinctive, persistent** features | deep-set grey eyes, broken nose bridge, white stubble, scar through left eyebrow |
| Hair | Cut, color, texture | short cropped silver hair, receding |
| Skin | Tone + texture | weathered olive skin, sun spots |
| Wardrobe | ONE signature outfit, colors named | faded navy wool peacoat, charcoal knit, brass buttons |
| Props | 0–1 signature item | worn leather gloves |
| Look / genre | Visual world | 1970s neo-noir, 35mm film grain |

Best practices:
- Prefer **specific, visible** traits over personality adjectives ("scar through left eyebrow" beats
  "tough-looking"). The model can only keep what it can see.
- Keep wardrobe to 2–3 named colors; busy patterns drift between shots.
- Avoid features that fight each other (e.g. "young" + "deep wrinkles") and avoid real
  celebrities' names or likenesses.

## Step 2 — Hero portrait (the Element cover)

Tool `mcp__KLING__text_to_image`. Default model: the tool's `defaultModel` from `who_am_i`
(currently `kling-image-v3_0_omni`, native 2K/4K). Use `gemini-3-pro-image` when the character
needs legible text/insignia, or when the user prefers it.

Settings: `aspect_ratio` `3:4` or `2:3`, `img_resolution` `2k`, `imageCount` `4` (pick the best
face — cheaper than re-rolling one at a time).

Cover prompt template (neutral, well-lit, unobstructed — this is a reference, not a beauty shot):

```
Character reference portrait, medium close-up, facing camera, neutral expression, eyes open,
looking into lens. [AGE] [ETHNICITY/SKIN] [GENDER] with [4–6 FACE TRAITS], [HAIR].
Wearing [WARDROBE with named colors]. Plain mid-grey seamless studio background,
soft even key light from front-left, gentle fill, no harsh shadows, no hands covering face,
no accessories covering eyes. Photorealistic, 85mm lens, sharp focus on eyes,
natural skin texture, [LOOK/GENRE color treatment].
```

Rules for the cover: full face visible, no sunglasses/hat brim over eyes, no motion blur, no
other people, no text. Let the user choose the winner.

## Step 3 — Turnaround (Element secondaries)

Tool `mcp__KLING__image_to_image` with the chosen cover as `image_1` (use its `works[].url`
directly if Kling produced it; upload local files first). Model: `kling-image-v3_0_omni`
(default for i2i), or `kling-image-o1` for tightest feature consistency.

Generate up to 3 angles, one job each (or `story_mode` `true` on v3_0_omni with all angles in one
prompt, which returns a series):

- `Same person as 图片1, exact same face, hair and wardrobe. Three-quarter view turned 45° to the left, neutral expression, same grey studio background and lighting.`
- `... Full profile, facing right ...`
- `... Full-body shot, standing relaxed, feet visible, arms at sides ...`

Always write `图片1` to reference image_1 (that token is how Kling binds references). Reject any
result where the face drifts; re-rolling one angle is cheaper than a polluted Element.

## Step 4 — Register the Element

1. Load `mcp__KLING__element_create` via ToolSearch and **read its live description** to get the
   valid tag list for the user's region; pass tags exactly as listed (don't translate them).
2. Create: `name` = short, unique (e.g. `Viktor_Noir`), `description` = one-line bible summary
   (face + wardrobe), `resource.cover` = hero URL, `resource.secondary` = 1–3 angle URLs, tags =
   the character tag.
3. Save the returned Element `id`. Verify with `mcp__KLING__element_get`.

Optional video Element: if the user has a short clip of the character (or wants a voice), a
video Element (`resource.video`, optional `voice`) works **only** on `image_to_video` with
`kling-video-v3_0_omni` or `kling-video-v3_0`. Image Elements work on `image_to_image`
(all models listing `elements`), `image_to_video` (v3_0_omni, v3_0, o1) and `motion_control`
(v3_0). `text_to_image` and `text_to_video` accept **no** Elements.

## Step 5 — Hand-off card

Write `characters/<name>.md` in the working directory (create the folder) so later skills and
sessions can reuse it:

```markdown
# <Name>
- Element id: <id>   bindName: <Name>
- Cover: <url>
- Angles: <url>, <url>, <url>
- Bible: <the table from step 1>
- Prompt anchor (use verbatim in every shot): "<age> <build> man, <2–3 key face traits>, <wardrobe>"
- Usage: in prompts write <<<id>>> where the character appears and pass
  elements='[{"id":"<id>","bindName":"<Name>"}]'
```

Tell the user the Element is ready and suggest the **Cinematic Performance Director** next.
