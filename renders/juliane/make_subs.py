"""Build ASS subtitles for the Juliane reel from voiceover phrase timings (silencedetect on voz-faraon-take2.mp3)."""
segs = [  # (start, end, text) — one entry per spoken phrase
 (0.00, 3.35, "Esta chica cayó de un avión desde 3.000 metros…"),
 (3.98, 4.84, "y sobrevivió."),
 (5.54, 8.35, "Nochebuena de 1971."),
 (8.80, 13.24, "Juliane Koepcke, 17 años, vuela sobre la selva de Perú con su mamá."),
 (13.69, 16.91, "Una tormenta golpea el avión…"),
 (17.37, 19.70, "y se parte en el aire."),
 (20.15, 21.65, "Ella cae atada a su asiento, girando."),
 (21.99, 24.03, "Despierta sola en la selva: clavícula rota, un ojo herido…"),
 (24.55, 25.32, "y sin su mamá."),
 (25.93, 28.95, "Entonces recuerda lo que le enseñó su papá, biólogo:"),
 (29.36, 31.19, "«Si te pierdes, sigue el agua."),
 (31.54, 33.00, "El agua lleva a la gente.»"),
 (33.51, 37.49, "Camina río abajo, días enteros, comiendo solo unos dulces."),
 (37.90, 40.65, "Al noveno día encuentra una cabaña de madereros."),
 (40.98, 42.65, "Tiene la herida llena de larvas;"),
 (42.96, 44.73, "se echa gasolina para sacarlas…"),
 (45.15, 45.73, "y espera."),
 (46.28, 48.12, "Al día siguiente, la encuentran."),
 (48.45, 51.73, "De 92 personas, fue la ÚNICA que sobrevivió."),
 (52.18, 53.98, "Años después estudió biología…"),
 (54.27, 56.87, "y volvió a esa misma selva para protegerla."),
 (57.33, 59.05, "A veces sobrevivir es eso…"),
 (59.53, 60.64, "seguir el agua."),
]
titles = [  # (start, end, text) — on-screen headline cards
 (0.00, 3.70, "CAYÓ 3.000 METROS"),
 (5.54, 8.80, "24 DIC 1971 · PERÚ"),
 (29.36, 33.20, "SIGUE EL AGUA"),
 (37.90, 40.80, "DÍA 9"),
 (48.45, 51.90, "1 DE 92"),
 (57.33, 62.20, "¿TÚ HABRÍAS SOBREVIVIDO?"),
]
MAXW = 5

def ts(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def chunks(text):
    """Split at punctuation first, then wrap to MAXW words; never leave a 1-word orphan."""
    import re
    pieces = [p.strip() for p in re.split(r"(?<=[,:;…])\s+", text) if p.strip()]
    out = []
    for p in pieces:
        w = p.split()
        while len(w) > MAXW + 1:
            out.append(" ".join(w[:MAXW])); w = w[MAXW:]
        out.append(" ".join(w))
    merged = []
    for p in out:
        if merged and (len(p.split()) == 1 or len(merged[-1].split()) == 1) and len(merged[-1].split()) + len(p.split()) <= MAXW + 2:
            merged[-1] += " " + p
        else:
            merged.append(p)
    return merged

head = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1916
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,DejaVu Sans,74,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,6,2,2,80,80,520,1
Style: Title,DejaVu Sans,92,&H0000E1FF,&H0000E1FF,&H00000000,&H64000000,-1,0,0,0,100,100,1,0,1,7,3,8,60,60,230,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
lines = []
for s, e, text in segs:
    parts = chunks(text)
    total = sum(len(p) for p in parts)
    t = s
    for i, p in enumerate(parts):
        d = (e - s) * len(p) / total
        end = t + d + (0.3 if i == len(parts) - 1 else 0)
        lines.append(f"Dialogue: 0,{ts(t)},{ts(end)},Sub,,0,0,0,,{{\\fad(60,60)}}{p}")
        t += d
for s, e, text in titles:
    lines.append(f"Dialogue: 1,{ts(s)},{ts(e)},Title,,0,0,0,,{{\\fad(150,150)}}{text}")
open("subs.ass", "w", encoding="utf-8").write(head + "\n".join(lines) + "\n")
print(len(lines), "events")
