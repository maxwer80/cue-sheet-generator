---
name: cinematic-batch-video-generator
description: >-
  Run a whole shot list on Kling AI safely and efficiently: validate every shot spec, estimate and
  confirm credits once, submit the jobs, poll them, track everything in a manifest file, and
  deliver an organized results table (with draft → final passes and variants).
  Use for "batch", "lote", "genera todos los planos", "render the shot list", "varias versiones",
  "generar en serie", or whenever more than one Kling video/image job should run.
---

# Cinematic Batch Video Generator

Goal: turn a list of shot specs (from **Cinematic Video Prompt Writer**) into finished clips
without wasting credits or losing track of jobs.

Pipeline position: Character Generator → Performance Director → Video Prompt Writer → **Batch Video Generator**.

Reply in the user's language.

## Hard rules

- **Credits are real money.** Show the full plan and get one explicit confirmation before
  submitting anything. No trial or duplicate jobs. Never silently change a prompt or parameter.
- **Never auto-resubmit.** On failure, timeout or odd result, report it and ask: retry as is,
  change parameters, or skip.
- Only models/arguments/values from `mcp__KLING__who_am_i`; all argument values are strings.
- Record every `generationId` in the manifest **immediately** after submission, before polling.

## Step 1 — Load and validate the shot list

Input: `shots/<project>-prompts.md` (YAML shot specs) or specs pasted by the user. If the user only
has ideas, run the Prompt Writer first.

1. `mcp__KLING__who_am_i` with the tools used in the list.
2. For each shot check: tool/model exists; argument names declared for that model; values within
   `allowedValues`; required inputs present; input URLs are public or from
   `mcp__KLING__file_upload` (upload local files now — uploading is free); Elements only on
   models that list `elements`, within `maxItems`; `motion_control` has exactly one of
   `motionId` / `video`.
3. Report all problems at once and fix them with the user before continuing.

## Step 2 — Plan passes and confirm credits

Recommend a **draft → final** workflow (best results per credit):

| Pass | Purpose | Settings |
|---|---|---|
| Draft | Check blocking, performance, timing | `kling-video-v3_0_turbo` (or same model at `720p`), shortest usable `duration`, `imageCount` `2` for key shots |
| Final | Only approved shots/prompts | Chosen model at `1080p` (or `4k` for members on v3.0/omni), final duration |

Variants: `imageCount` (up to 4) returns several takes of the **same** prompt in one job — use it
for performance-critical shots instead of resubmitting. For different ideas, make separate specs.

Before submitting:
1. `mcp__KLING__query_membership_and_credits` → show membership and `availableRemainCredits`.
2. Cost: prices vary by model, duration, resolution and membership and are not published by the
   API. If the manifest has `creditsConsumed` from a comparable earlier job, use it to estimate;
   otherwise offer to submit the first shot alone, read its `creditsConsumed`, then extrapolate.
3. Show the plan table (id, tool, model, duration, resolution, variants, est. credits) + total
   and wait for "yes". If the balance is too low, say so; the top-up link is in the live
   description of `query_membership_and_credits` (read it via ToolSearch — never hard-code it).

## Step 3 — Submit

- Generate one UUID v7 as `taskTraceId` for the batch and pass it on every call (it groups the
  jobs; use a new one for an unrelated batch). Pass a one-line `rationale` per shot if the tool
  schema declares it.
- Submit shots **one at a time, in order**. After each: write `generationId`, status and
  `creditsConsumed` to the manifest. If a submission is rejected (validation, balance, content
  policy), stop and report — don't continue blindly with dependent shots.
- Chained shots (e.g. a still from `image_to_image` feeding `image_to_video`) must wait for the
  upstream job to complete; use its `works[].url` as the downstream input.

## Step 4 — Poll

- Poll `mcp__KLING__query_tasks` per `generationId`. Videos typically take minutes; poll at
  sensible intervals (don't hammer), cycle through all pending jobs each round.
- Status is case-insensitive: running = `QUEUING`/`RUNNING`/`submitted`/`processing`; done =
  `COMPLETED`/`PARTIAL_COMPLETED`/`succeed`; failed = `FAILED`/`CANCELLED`/others.
- Update the manifest on every status change. If a job exceeds ~20 min, tell the user and ask
  whether to keep waiting; keep its id so it can be checked later.
- On stuck jobs, empty results or unexplained errors, silently file `mcp__KLING__feedback`
  (`agent_initiated`, sanitized summary, the `generationId`) once per issue, then inform the user
  of the problem itself.

## Step 5 — Deliver

Manifest file `renders/<project>-manifest.json` (create folder), one entry per job:

```json
{
  "project": "noir-letter",
  "taskTraceId": "0192...",
  "jobs": [
    {"shot": "S03", "pass": "draft", "tool": "text_to_video", "model": "kling-video-v3_0_turbo",
     "arguments": {"duration": "5", "resolution": "720p", "imageCount": "2"},
     "prompt": "...", "generationId": "...", "status": "COMPLETED", "creditsConsumed": 0,
     "works": [{"url": "...", "urlWithoutWatermark": "...", "coverUrl": "..."}],
     "review": "take 2 approved"}
  ]
}
```

Then show a results table: shot, pass, status, links (`url`; `urlWithoutWatermark` only if the user
asks), credits used, and a short QA note per clip (face consistency, performance, camera, artifacts).

Offer next steps:
- Download clips: `curl -L -o renders/<shot>-<take>.mp4 "<url>"` (result URLs may expire).
- Approve takes → run the **final** pass for approved shots only.
- For weak shots, go back to Performance Director / Prompt Writer with a specific fix
  (one change at a time, so the next take tells you what worked).
