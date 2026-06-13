from PIL import Image, ImageDraw, ImageFilter
import math

def make_icon(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    s = size
    cx = s / 2

    # Background circle - dark navy
    draw.ellipse([0, 0, s - 1, s - 1], fill=(30, 35, 50, 255))

    # Face silhouette (head + shoulders) in light gray
    # Head
    head_r = s * 0.22
    head_cx = cx
    head_cy = s * 0.38
    draw.ellipse(
        [head_cx - head_r, head_cy - head_r, head_cx + head_r, head_cy + head_r],
        fill=(200, 205, 215, 255)
    )
    # Shoulders arc
    shoulder_w = s * 0.52
    shoulder_h = s * 0.22
    shoulder_top = s * 0.62
    draw.ellipse(
        [cx - shoulder_w / 2, shoulder_top,
         cx + shoulder_w / 2, shoulder_top + shoulder_h * 2],
        fill=(200, 205, 215, 255)
    )
    # Clip to circle
    mask = Image.new("L", (s, s), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse([0, 0, s - 1, s - 1], fill=255)
    img.putalpha(mask)

    # Draw horizontal blur stripes over the face area
    stripe_colors = [
        (255, 80, 80, 210),
        (255, 110, 60, 200),
        (255, 80, 80, 210),
        (255, 100, 70, 195),
        (255, 80, 80, 210),
    ]
    stripe_height = int(s * 0.085)
    stripe_gap = int(s * 0.015)
    stripe_start_y = int(head_cy - head_r * 0.7)
    stripe_x1 = int(cx - head_r * 1.1)
    stripe_x2 = int(cx + head_r * 1.1)

    overlay = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)

    for i, color in enumerate(stripe_colors):
        y = stripe_start_y + i * (stripe_height + stripe_gap)
        # Slightly wavy stripe using a polygon
        points = []
        steps = 20
        for step in range(steps + 1):
            x = stripe_x1 + (stripe_x2 - stripe_x1) * step / steps
            wave = math.sin(step / steps * math.pi * 2) * s * 0.012
            points.append((x, y + wave))
        for step in range(steps, -1, -1):
            x = stripe_x1 + (stripe_x2 - stripe_x1) * step / steps
            wave = math.sin(step / steps * math.pi * 2) * s * 0.012
            points.append((x, y + stripe_height + wave))
        odraw.polygon(points, fill=color)

    img = Image.alpha_composite(img, overlay)

    # Re-apply circle mask
    final_mask = Image.new("L", (s, s), 0)
    ImageDraw.Draw(final_mask).ellipse([0, 0, s - 1, s - 1], fill=255)
    img.putalpha(final_mask)

    return img

for size in [16, 48, 128]:
    icon = make_icon(size)
    icon.save(f"icons/icon{size}.png")
    print(f"Saved icon{size}.png")
