from PIL import Image, ImageDraw, ImageFont
import numpy as np
import imageio

NAME = "PARVEZ"
W, H = 1280, 720          # video size (HD)
FPS = 30
DURATION = 6              # total seconds
BG = (15, 15, 30)         # dark navy background
COLORS = [(255, 99, 71), (255, 195, 0), (50, 205, 50),
          (0, 191, 255), (186, 85, 211), (255, 105, 180)]

# Try a bold font, fall back to default if not found
try:
    font = ImageFont.truetype("arialbd.ttf", 180)
except OSError:
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 180)
    except OSError:
        font = ImageFont.load_default(size=180)

def lerp_color(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))

# Measure letter positions so the word is centered
spacing = 20
widths = [font.getlength(ch) for ch in NAME]
total_width = sum(widths) + spacing * (len(NAME) - 1)
x_start = (W - total_width) / 2
x_positions = []
x = x_start
for w in widths:
    x_positions.append(x)
    x += w + spacing

BASE_Y = H // 2 - 100
LETTER_DELAY = 0.25       # seconds between letters
LETTER_TIME = 0.6         # animation time per letter
FADE_START = 4.8          # when the fade-out begins
FADE_TIME = 1.0

writer = imageio.get_writer("parvez.mp4", fps=FPS, codec="libx264", quality=8)

total_frames = DURATION * FPS
for frame in range(total_frames):
    t = frame / FPS
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    for i, ch in enumerate(NAME):
        # Progress of this letter's animation (0 to 1)
        p = (t - i * LETTER_DELAY) / LETTER_TIME
        p = min(max(p, 0), 1)
        ease = 1 - (1 - p) ** 3          # smooth ease-out

        y = BASE_Y + (1 - ease) * 80     # slide up into place
        color = lerp_color(BG, COLORS[i % len(COLORS)], ease)  # fade in
        draw.text((x_positions[i], y), ch, font=font, fill=color)

    # Fade the whole screen to background at the end
    if t > FADE_START:
        fade = max(0, 1 - (t - FADE_START) / FADE_TIME)
        img = Image.blend(Image.new("RGB", (W, H), BG), img, fade)

    writer.append_data(np.array(img))

writer.close()
print("Done! Video saved as parvez.mp4")
