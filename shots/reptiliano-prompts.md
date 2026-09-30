# ¿Qué es un reptiliano? — guion y planos

- Formato: vertical 9:16, 60 s, 7 planos
- Look: documental conspiranoico de archivo, película de 16 mm y VHS de los 80–90, sombras duras, verde enfermizo
- Audio: la voz en off y la música van en edición; Kling genera sin audio (`enable_audio: "false"`, más barato: 8 créditos/s en vez de 12)
- Modelo: `text_to_video` · `kling-video-v3_0_omni` · 1080p
- Costo estimado: 60 s × 8 créditos/s ≈ 480 créditos (sin variantes)
- Regla: la teoría se presenta como teoría, y no se muestra a ninguna persona real como reptil

## Guion (voz en off, ~132 palabras ≈ 2,2 palabras/s)

| # | Tiempo | Voz en off | Imagen |
|---|---|---|---|
| S1 | 0:00–0:05 | ¿Y si quien gobierna tu país… no fuera humano? | Ojo en primer plano; la pupila se vuelve una ranura vertical |
| S2 | 0:05–0:15 | Eso dice la teoría reptiliana: seres con escamas que cambian de forma, se hacen pasar por personas y controlan gobiernos, bancos y medios. | Sala de juntas en penumbra; una sombra en la pared se estira en silueta de lagarto |
| S3 | 0:15–0:25 | La idea no nació en internet. En 1929 una revista pulp ya hablaba de "hombres serpiente", y en 1983 la serie *V* los llevó a la tele. | Televisor de los 80 en una sala; en pantalla, una figura se arranca una cara de goma y aparecen escamas |
| S4 | 0:25–0:33 | En 1999, el británico David Icke la convirtió en doctrina: reptiles venidos de la constelación Draco. | Auditorio de los 90; un proyector muestra un mapa estelar que se ilumina |
| S5 | 0:33–0:43 | ¿La prueba? Videos donde alguien parpadea raro. Casi siempre es la compresión del video, que deforma ojos y bocas. | Pantalla de celular con un presentador genérico; bloques de pixelado deforman sus ojos |
| S6 | 0:43–0:53 | Aun así, en 2013 una encuesta encontró que el 4 % de los votantes de Estados Unidos lo creía: unos doce millones de personas. | Calle llena de gente; la cámara recorre caras comunes; una persona mira a cámara |
| S7 | 0:53–1:00 | Quizá es más fácil creer que el poder tiene escamas… que aceptar que son solo humanos. | Espejo de baño de noche; el reflejo parpadea un instante tarde; la luz titila; negro |

Textos en pantalla para edición (Kling no escribe texto de forma fiable): "1929", "1983", "1999 · David Icke", "4 % ≈ 12 millones".

Fuentes: [Reptilian conspiracy theory (Wikipedia)](https://en.wikipedia.org/wiki/Reptilian_conspiracy_theory), [David Icke (Wikipedia)](https://en.wikipedia.org/wiki/David_Icke), [TIME — The Reptilian Elite](https://content.time.com/time/specials/packages/article/0,28804,1860871_1860876_1861029,00.html), [Encuesta PPP 2013 (Daily Caller)](https://dailycaller.com/2013/04/03/poll-4-percent-of-americans-believe-lizard-people-control-world/).

## Especificaciones de planos

Argumentos comunes a todos: `aspect_ratio: "9:16"`, `resolution: "1080p"`, `imageCount: "1"`, `prefer_multi_shots: "false"`, `enable_audio: "false"`.

```yaml
- id: S1
  title: El ojo
  tool: text_to_video
  model: kling-video-v3_0_omni
  arguments:
    duration: "5"
    prompt: "Extreme close-up, eye level. The eye of a middle-aged man in a dark office, lit by a single desk lamp. He looks straight into the lens, still and calm; then he blinks once, slowly, and as the eye reopens the round pupil narrows into a thin vertical slit and the iris shifts to a faint golden green; finally it holds, unblinking. Dust drifts in the lamp beam. Locked-off camera with an almost imperceptible push-in. Hard side light from warm tungsten lamp, deep shadows, macro lens. 1980s 16mm documentary film, heavy grain, sickly green tint in the shadows."

- id: S2
  title: La sombra en la sala de juntas
  tool: text_to_video
  model: kling-video-v3_0_omni
  arguments:
    duration: "10"
    prompt: "Wide shot, low angle. A long polished boardroom table at night with six men in dark suits seated in silhouette, faces unreadable, a city skyline glowing through tall windows behind them. First the men sit motionless while cigarette smoke curls up into the light; then the man at the head of the table slowly turns his head, and his shadow on the wood-paneled wall stretches and warps into the silhouette of a lizard head with a long snout; finally the shadow snaps back to human shape as he faces forward. Slow dolly in along the table. Single overhead practical light, cold blue window light, 24mm lens. 1980s 16mm film, grain, desaturated with green-tinted shadows."

- id: S3
  title: La tele de los 80
  tool: text_to_video
  model: kling-video-v3_0_omni
  arguments:
    duration: "10"
    prompt: "Medium shot of an old 1980s wooden-cabinet CRT television in a dim living room with a patterned sofa and a lamp. On the glowing screen, a B-movie scene plays: a man in a suit grabs the edge of his own face and slowly peels away a rubber human mask, revealing green reptilian scales and yellow eyes underneath. Scan lines roll across the curved screen, the picture flickers, light from the TV pulses on the walls. Slow push-in toward the TV screen until it fills most of the frame. Blue TV glow as the only light source, 35mm lens. VHS and 16mm hybrid look, soft focus, color bleed, tracking lines."

- id: S4
  title: El auditorio de 1999
  tool: text_to_video
  model: kling-video-v3_0_omni
  arguments:
    duration: "8"
    prompt: "Wide shot from the back of a packed 1990s lecture hall. Rows of silhouetted audience heads in the foreground face a stage where a lone speaker in a turquoise shirt stands beside a large projection screen. First the projector beam cuts through the haze above the crowd; then the screen lights up with a star map of the night sky and one serpent-shaped constellation traces itself in glowing lines, star by star; finally the audience leans forward. Slow crane up over the heads of the crowd. Projector backlight, haze, 28mm lens. Late-1990s camcorder and 16mm hybrid look, grain, slightly washed-out colors."

- id: S5
  title: El glitch
  tool: text_to_video
  model: kling-video-v3_0_omni
  arguments:
    duration: "10"
    prompt: "Close-up of a smartphone held in a hand in a dark room, the screen fills most of the frame. On the screen, a generic TV news anchor in a grey suit speaks at a desk. First the video plays normally; then the stream stutters and blocky compression artifacts smear across his eyes and mouth, his eyelids appear to flicker sideways for a split second; finally the image freezes on a distorted frame and the pixel blocks slowly resolve back to a normal face. The screen glow lights the fingers holding the phone. Handheld with a subtle sway. Cool screen light, 50mm lens. Grainy, contrasty, digital glitch texture on screen, film grain on the surroundings."

- id: S6
  title: La multitud
  tool: text_to_video
  model: kling-video-v3_0_omni
  arguments:
    duration: "10"
    prompt: "Medium shot at eye level on a busy downtown sidewalk at dusk. Ordinary people of all ages walk toward the camera: office workers, a student with a backpack, an elderly woman with shopping bags. The camera tracks slowly sideways across the passing faces; then, in the middle of the crowd, one ordinary man in a beige jacket stops walking and looks directly into the lens while everyone keeps moving around him; finally he blinks and continues on. Streetlights flicker on, neon signs start to glow. Lateral tracking shot, smooth and slow. Mixed sodium streetlight and fading daylight, 35mm lens. 16mm film grain, muted colors, slight green cast."

- id: S7
  title: El espejo
  tool: text_to_video
  model: kling-video-v3_0_omni
  arguments:
    duration: "7"
    prompt: "Medium close-up over the shoulder of a person standing at a small bathroom mirror at night, their reflection facing the camera. They splash water on their face and look up at the mirror; then they blink, and the reflection blinks a split second later, out of sync; finally the fluorescent light above the mirror flickers twice and the room drops to black. Water drips from their chin. Locked-off camera. Single buzzing fluorescent tube overhead, cold greenish light, 40mm lens. 1980s 16mm film, heavy grain, harsh contrast."
```
