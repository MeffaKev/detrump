from PIL import Image, ImageDraw, ImageFont
import math

BG       = (22,  27,  42)
RED      = (220, 50,  50)
RED2     = (255, 90,  60)
WHITE    = (255, 255, 255)
GRAY     = (180, 185, 200)
GRAY2    = (120, 125, 145)
CARD     = (38,  46,  68)


def try_font(size):
    for path in [
        "/usr/share/fonts/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/google-droid/DroidSans-Bold.ttf",
    ]:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()


def draw_face(base, cx, cy, r):
    """Composite a censored-face illustration onto base (RGB image)."""
    # Work on an RGBA layer so we can use alpha for the stripes
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    # Dark circle backdrop
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*CARD, 255))

    # Head
    hr  = r * 0.30
    hcy = cy - r * 0.20
    d.ellipse([cx-hr, hcy-hr, cx+hr, hcy+hr], fill=(190, 195, 210, 255))

    # Shoulders
    sw, sh = r * 0.70, r * 0.30
    d.ellipse([cx-sw, cy+r*0.15, cx+sw, cy+r*0.15+sh*2],
              fill=(190, 195, 210, 255))

    # Wavy red stripes over the face
    stripe_h  = hr * 0.38
    gap       = hr * 0.07
    x1, x2   = cx - hr * 1.1, cx + hr * 1.1
    start_y   = hcy - hr * 0.70
    steps     = 30

    for i in range(5):
        col = (*RED, 230) if i % 2 == 0 else (*RED2, 210)
        y0  = start_y + i * (stripe_h + gap)
        pts = []
        for s in range(steps + 1):
            t    = s / steps
            x    = x1 + (x2 - x1) * t
            wave = math.sin(t * math.pi * 3) * r * 0.016
            pts.append((x, y0 + wave))
        for s in range(steps, -1, -1):
            t    = s / steps
            x    = x1 + (x2 - x1) * t
            wave = math.sin(t * math.pi * 3) * r * 0.016
            pts.append((x, y0 + stripe_h + wave))
        d.polygon(pts, fill=col)

    # Clip layer to circle
    mask = Image.new("L", base.size, 0)
    ImageDraw.Draw(mask).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)

    # Composite onto base
    rgba_base = base.convert("RGBA")
    rgba_base.alpha_composite(layer, dest=(0, 0))
    result = rgba_base.convert("RGB")
    base.paste(result)


# ── Small promo tile 440×280 ─────────────────────────────────────────────────
W, H = 440, 280
img  = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

draw_face(img, cx=320, cy=148, r=100)

# Red left bar
draw.rectangle([0, 0, 6, H], fill=RED)

ft = try_font(54)
fs = try_font(20)

# "De" white + "Trump" red
bx = draw.textbbox((28, 68), "De", font=ft)
draw.text((28, 68), "De", font=ft, fill=WHITE)
draw.text((28 + bx[2] - bx[0], 68), "Trump", font=ft, fill=RED)

draw.text((30, 142), "Blur Trump.", font=fs, fill=GRAY)
draw.text((30, 167), "Browse in peace.", font=fs, fill=GRAY2)

img.save("small_promo_tile.png")
print("Saved small_promo_tile.png")


# ── Marquee promo tile 1400×560 ──────────────────────────────────────────────
W, H = 1400, 560
img  = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

for cx, r in [(1000, 148), (1195, 110), (1348, 80)]:
    draw_face(img, cx=cx, cy=H // 2, r=r)

draw = ImageDraw.Draw(img)

# Red left bar
draw.rectangle([0, 0, 9, H], fill=RED)

ft  = try_font(112)
fs  = try_font(36)
ftg = try_font(26)

bx = draw.textbbox((70, 110), "De", font=ft)
draw.text((70, 110), "De", font=ft, fill=WHITE)
draw.text((70 + bx[2] - bx[0], 110), "Trump", font=ft, fill=RED)

draw.text((72, 300), "Automatically blurs Trump on every page.", font=fs,  fill=GRAY)
draw.text((72, 352), "Click to reveal. Toggle off anytime.",     font=ftg, fill=GRAY2)

img.save("marquee_promo_tile.png")
print("Saved marquee_promo_tile.png")
