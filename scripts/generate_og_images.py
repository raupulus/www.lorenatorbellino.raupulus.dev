#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
IMAGES_DIR = os.path.join(PROJECT_DIR, "public", "assets", "images")

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

def create_og_home():
    width, height = 1200, 630
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Background gradient: Dark Plum (#241424) to Rich Wine (#5A1E3E)
    draw_gradient_background(draw, width, height, (36, 20, 36), (90, 30, 62))

    # 2. Decorative glowing ambient circles
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse([780, 80, 1260, 560], fill=(248, 113, 87, 85))
    glow_draw.ellipse([640, 180, 1060, 610], fill=(252, 212, 153, 55))
    glow_draw.ellipse([-50, -50, 450, 450], fill=(74, 116, 153, 40))
    glow = glow.filter(ImageFilter.GaussianBlur(60))
    img = Image.alpha_composite(img, glow)
    draw = ImageDraw.Draw(img)

    # 3. Bottom accent bar: Coral line
    draw.rectangle([0, height - 10, width, height], fill=(248, 113, 87, 255))

    # 4. Top Accent Pill
    font_badge = get_font(FONT_TITLE_PATH, 17)
    badge_text = "POP CÓMICO & SÁTIRA 2D  •  CANCIONES Y DESASTRES"
    bx, by = 75, 70
    bw = int(draw.textlength(badge_text, font=font_badge)) + 40
    bh = 38
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=19, fill=(255, 255, 255, 25), outline=(248, 113, 87, 190), width=2)
    draw.text((bx + 20, by + 9), badge_text, fill=(252, 212, 153, 255), font=font_badge)

    # 5. Main Title: "Lorena Torbellino"
    font_title = get_font(FONT_TITLE_PATH, 66)
    draw.text((75, 135), "Lorena Torbellino", fill=(255, 255, 255, 255), font=font_title)

    # 6. Subtitle with Coral accent
    font_sub = get_font(FONT_TITLE_PATH, 30)
    draw.text((75, 225), "Web Oficial & Catálogo Interactivo", fill=(248, 113, 87, 255), font=font_sub)

    # 7. Description lines
    font_desc = get_font(FONT_BODY_PATH, 23)
    line1 = "20 años, voz dulce, zapatillas Converse rojas y un talento"
    line2 = "sobrenatural para que todo en la vida salga al revés."
    draw.text((75, 280), line1, fill=(243, 226, 216, 230), font=font_desc)
    draw.text((75, 314), line2, fill=(243, 226, 216, 230), font=font_desc)

    # 8. Stats / Highlights Pills
    font_pill = get_font(FONT_TITLE_PATH, 18)
    pills = [
        ("4 Álbumes", (248, 113, 87, 255)),
        ("110 Canciones", (74, 116, 153, 255)),
        ("Videoclips en YouTube", (120, 54, 77, 255))
    ]
    px = 75
    py = 385
    for ptext, pcol in pills:
        pw = int(draw.textlength(ptext, font=font_pill)) + 36
        draw.rounded_rectangle([px, py, px + pw, py + 40], radius=14, fill=pcol)
        draw.text((px + 18, py + 9), ptext, fill=(255, 255, 255, 255), font=font_pill)
        px += pw + 14

    # 9. Bottom URL & Brand handle
    font_url = get_font(FONT_TITLE_PATH, 22)
    draw.text((75, 520), "lorenatorbellino.raupulus.dev", fill=(252, 212, 153, 255), font=font_url)
    font_handle = get_font(FONT_BODY_PATH, 20)
    draw.text((395, 522), "•  YouTube: @LorenaTorbellino", fill=(210, 210, 210, 220), font=font_handle)

    # 10. Mascot / Character Image on Right side
    mascot_path = os.path.join(IMAGES_DIR, "lorena_sticker_guino.webp")
    if os.path.exists(mascot_path):
        mascot = Image.open(mascot_path).convert("RGBA")
        mw, mh = mascot.size
        target_h = 540
        target_w = int(mw * (target_h / float(mh)))
        mascot_resized = mascot.resize((target_w, target_h), Image.Resampling.LANCZOS)
        mx = width - target_w - 50
        my = height - target_h - 15
        img.paste(mascot_resized, (mx, my), mascot_resized)

    # Save JPEG and WebP
    rgb_img = img.convert("RGB")
    out_jpg = os.path.join(IMAGES_DIR, "og_home.jpg")
    out_webp = os.path.join(IMAGES_DIR, "og_home.webp")
    rgb_img.save(out_jpg, format="JPEG", quality=92, optimize=True)
    rgb_img.save(out_webp, format="WEBP", quality=90)
    print(f"Generado: {out_jpg}")
    print(f"Generado: {out_webp}")

def create_og_quien_es():
    width, height = 1200, 630
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Background gradient: Wine (#3F173B) to Warm Plum (#6A2448)
    draw_gradient_background(draw, width, height, (63, 23, 59), (106, 36, 72))

    # 2. Glowing ambient circles
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse([750, 80, 1220, 550], fill=(252, 212, 153, 75))
    glow_draw.ellipse([840, 150, 1260, 570], fill=(248, 113, 87, 65))
    glow_draw.ellipse([-50, 200, 350, 600], fill=(177, 202, 178, 40))
    glow = glow.filter(ImageFilter.GaussianBlur(60))
    img = Image.alpha_composite(img, glow)
    draw = ImageDraw.Draw(img)

    # 3. Bottom accent bar: Coral line
    draw.rectangle([0, height - 10, width, height], fill=(248, 113, 87, 255))

    # 4. Top Accent Pill
    font_badge = get_font(FONT_TITLE_PATH, 17)
    badge_text = "BIOGRAFÍA OFICIAL  •  GALERÍA DE GAGS & POSES"
    bx, by = 75, 70
    bw = int(draw.textlength(badge_text, font=font_badge)) + 40
    bh = 38
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=19, fill=(255, 255, 255, 25), outline=(252, 212, 153, 200), width=2)
    draw.text((bx + 20, by + 9), badge_text, fill=(252, 212, 153, 255), font=font_badge)

    # 5. Main Title: "Quién es Lorena Torbellino"
    font_title = get_font(FONT_TITLE_PATH, 58)
    draw.text((75, 135), "Quién es Lorena", fill=(255, 255, 255, 255), font=font_title)
    draw.text((75, 205), "Torbellino", fill=(248, 113, 87, 255), font=font_title)

    # 6. Tagline
    font_sub = get_font(FONT_TITLE_PATH, 28)
    draw.text((75, 290), "Carisma, Dulzura y Desastre a los 20 Años", fill=(252, 212, 153, 255), font=font_sub)

    # 7. Attributes Grid (Pills with clean textual labels)
    font_pill = get_font(FONT_TITLE_PATH, 17)
    traits = [
        ("Converse Rojas", (248, 113, 87, 255)),
        ("Moño con Pinza Negra", (74, 116, 153, 255)),
        ("Pecas en Mejillas", (120, 54, 77, 255)),
        ("Crisis de Viejoven", (63, 23, 59, 255))
    ]
    px = 75
    py = 350
    for i, (t, col) in enumerate(traits):
        pw = int(draw.textlength(t, font=font_pill)) + 32
        draw.rounded_rectangle([px, py, px + pw, py + 38], radius=14, fill=col, outline=(252, 212, 153, 100), width=1)
        draw.text((px + 16, py + 9), t, fill=(255, 255, 255, 255), font=font_pill)
        px += pw + 12
        if i == 1:
            px = 75
            py += 48

    # 8. Bottom URL
    font_url = get_font(FONT_TITLE_PATH, 22)
    draw.text((75, 520), "lorenatorbellino.raupulus.dev/quien-es-lorena.html", fill=(252, 212, 153, 255), font=font_url)

    # 9. Mascot / Character Image on Right side
    mascot_path = os.path.join(IMAGES_DIR, "lorena_sticker_guino.webp")
    if os.path.exists(mascot_path):
        mascot = Image.open(mascot_path).convert("RGBA")
        mw, mh = mascot.size
        target_h = 540
        target_w = int(mw * (target_h / float(mh)))
        mascot_resized = mascot.resize((target_w, target_h), Image.Resampling.LANCZOS)
        mx = width - target_w - 50
        my = height - target_h - 15
        img.paste(mascot_resized, (mx, my), mascot_resized)

    # Save JPEG and WebP
    rgb_img = img.convert("RGB")
    out_jpg = os.path.join(IMAGES_DIR, "og_quien_es.jpg")
    out_webp = os.path.join(IMAGES_DIR, "og_quien_es.webp")
    rgb_img.save(out_jpg, format="JPEG", quality=92, optimize=True)
    rgb_img.save(out_webp, format="WEBP", quality=90)
    print(f"Generado: {out_jpg}")
    print(f"Generado: {out_webp}")

if __name__ == "__main__":
    create_og_home()
    create_og_quien_es()
