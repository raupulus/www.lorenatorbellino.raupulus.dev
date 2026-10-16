#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFilter

PORTADAS_DIR = "/Users/fryntiz/git/3-Raupulus/www.lorenatorbellino.raupulus.dev/docs/portadas"
os.makedirs(PORTADAS_DIR, exist_ok=True)

# 1. Main Official GitLab Avatar (Coral Background, matches YouTube Profile)
src_avatar = Image.open("/Volumes/WAREHOUSE/pCloudDrive/Projects/4 - Discos/Lorena/avatar/youtube/foto_perfil_lorena_800x800.jpg")
avatar_192 = src_avatar.resize((192, 192), Image.Resampling.LANCZOS)

# Save as PNG and JPG
out_png = os.path.join(PORTADAS_DIR, "gitlab_avatar_192x192.png")
out_jpg = os.path.join(PORTADAS_DIR, "gitlab_avatar_192x192.jpg")
avatar_192.save(out_png, format="PNG", optimize=True)
avatar_192.save(out_jpg, format="JPEG", quality=95, optimize=True)
print(f"Generado: {out_png} ({os.path.getsize(out_png)} bytes)")
print(f"Generado: {out_jpg} ({os.path.getsize(out_jpg)} bytes)")

# 2. Dark Plum Variant (matches Dark Mode & Website plum palette)
sticker = Image.open("/Volumes/WAREHOUSE/pCloudDrive/Projects/4 - Discos/Lorena/avatar/marca_agua/opcion_2_troquelado_sticker.png").convert("RGBA")
sw, sh = sticker.size
ratio = 176 / float(max(sw, sh))
sticker_res = sticker.resize((int(sw * ratio), int(sh * ratio)), Image.Resampling.LANCZOS)

dark_img = Image.new("RGBA", (192, 192), (36, 20, 36, 255))
# Soft ambient coral glow behind the sticker
glow = Image.new("RGBA", (192, 192), (0, 0, 0, 0))
glow_draw = ImageDraw.Draw(glow)
glow_draw.ellipse([26, 26, 166, 166], fill=(248, 113, 87, 80))
glow = glow.filter(ImageFilter.GaussianBlur(15))
dark_img = Image.alpha_composite(dark_img, glow)

# Paste sticker
px = (192 - sticker_res.width) // 2
py = (192 - sticker_res.height) // 2
dark_img.paste(sticker_res, (px, py), sticker_res)

# Bottom coral accent bar
dark_draw = ImageDraw.Draw(dark_img)
dark_draw.rectangle([0, 188, 192, 192], fill=(248, 113, 87, 255))

out_dark_png = os.path.join(PORTADAS_DIR, "gitlab_avatar_plum_192x192.png")
dark_img.save(out_dark_png, format="PNG", optimize=True)
print(f"Generado: {out_dark_png} ({os.path.getsize(out_dark_png)} bytes)")
