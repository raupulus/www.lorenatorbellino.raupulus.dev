#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
OUTPUT_DIR = os.path.join(PROJECT_DIR, "docs", "portadas")
IMAGES_DIR = os.path.join(PROJECT_DIR, "public", "assets", "images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

FONT_TITLE_PATH = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_BODY_PATH = "/System/Library/Fonts/Helvetica.ttc"

def get_font(path, size, index=0):
    try:
        return ImageFont.truetype(path, size, index=index)
    except Exception:
        return ImageFont.load_default()

def draw_gradient_background(draw, width, height, start_color, end_color):
    for y in range(height):
        ratio = y / float(height)
        r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
        g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
        b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

def generate_cover(width, height, filename, platform_badge):
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Background gradient (Plum to Wine)
    draw_gradient_background(draw, width, height, (36, 20, 36), (82, 26, 56))

    # 2. Ambient glows
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse([width - 450, 60, width + 50, height - 40], fill=(248, 113, 87, 85))
    glow_draw.ellipse([width - 550, 160, width - 100, height], fill=(252, 212, 153, 50))
    glow_draw.ellipse([-80, -80, 420, 420], fill=(74, 116, 153, 35))
    glow = glow.filter(ImageFilter.GaussianBlur(65))
    img = Image.alpha_composite(img, glow)
    draw = ImageDraw.Draw(img)

    # 3. Bottom accent bar
    draw.rectangle([0, height - 10, width, height], fill=(248, 113, 87, 255))

    # 4. Top pill
    font_badge = get_font(FONT_TITLE_PATH, 16)
    badge_text = f"WEB OFICIAL  •  POP CÓMICO 2D  •  {platform_badge.upper()}"
    bx, by = 80, 68
    bw = int(draw.textlength(badge_text, font=font_badge)) + 40
    bh = 36
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=18, fill=(255, 255, 255, 20), outline=(248, 113, 87, 190), width=2)
    draw.text((bx + 20, by + 8), badge_text, fill=(252, 212, 153, 255), font=font_badge)

    # 5. Title
    font_title = get_font(FONT_TITLE_PATH, 64)
    draw.text((80, 130), "Lorena Torbellino", fill=(255, 255, 255, 255), font=font_title)

    # 6. Subtitle
    font_sub = get_font(FONT_TITLE_PATH, 28)
    draw.text((80, 218), "Pop Costumbrista & Sátira Cotidiana", fill=(248, 113, 87, 255), font=font_sub)

    # 7. Description
    font_desc = get_font(FONT_BODY_PATH, 22)
    l1 = "Repositorio oficial de la web y catálogo interactivo de canciones."
    l2 = "20 años, zapatillas Converse rojas y desastres cotidianos."
    draw.text((80, 272), l1, fill=(243, 226, 216, 230), font=font_desc)
    draw.text((80, 306), l2, fill=(243, 226, 216, 230), font=font_desc)

    # 8. Tech Pills
    font_pill = get_font(FONT_TITLE_PATH, 17)
    pills = [
        ("4 Álbumes", (248, 113, 87, 255)),
        ("110 Canciones", (74, 116, 153, 255)),
        ("Alpine.js + Tailwind", (120, 54, 77, 255))
    ]
    px = 80
    py = 375
    for ptext, pcol in pills:
        pw = int(draw.textlength(ptext, font=font_pill)) + 34
        draw.rounded_rectangle([px, py, px + pw, py + 38], radius=13, fill=pcol)
        draw.text((px + 17, py + 8), ptext, fill=(255, 255, 255, 255), font=font_pill)
        px += pw + 14

    # 9. Bottom URL & Licensing
    font_url = get_font(FONT_TITLE_PATH, 21)
    draw.text((80, height - 70), "lorenatorbellino.raupulus.dev", fill=(252, 212, 153, 255), font=font_url)
    font_meta = get_font(FONT_BODY_PATH, 19)
    draw.text((430, height - 68), "•  AGPL-3.0  •  Zero Runtime CDNs", fill=(200, 200, 200, 210), font=font_meta)

    # 10. Mascot on right
    mascot_path = os.path.join(IMAGES_DIR, "lorena_sticker_guino.webp")
    if os.path.exists(mascot_path):
        mascot = Image.open(mascot_path).convert("RGBA")
        mw, mh = mascot.size
        target_h = int(height * 0.86)
        target_w = int(mw * (target_h / float(mh)))
        mascot_resized = mascot.resize((target_w, target_h), Image.Resampling.LANCZOS)
        mx = width - target_w - 55
        my = height - target_h - 12
        img.paste(mascot_resized, (mx, my), mascot_resized)

    # Save
    out_path = os.path.join(OUTPUT_DIR, filename)
    rgb = img.convert("RGB")
    rgb.save(out_path, format="JPEG", quality=93, optimize=True)
    print(f"Portada generada con éxito ({width}x{height}): {out_path}")

if __name__ == "__main__":
    # GitHub Social Preview: 1280x640 (exact 2:1 aspect ratio)
    generate_cover(1280, 640, "github_social_preview.jpg", "GitHub")
    # GitLab Social Preview: 1200x630 (standard Open Graph 1.91:1)
    generate_cover(1200, 630, "gitlab_social_preview.jpg", "GitLab")
