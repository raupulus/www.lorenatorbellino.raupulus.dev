#!/usr/bin/env python3
import os
import json
import unicodedata
import re
import shutil
import urllib.parse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
VIDEOCLIPS_DIR = "/Volumes/WAREHOUSE/pCloudDrive/Projects/4 - Discos/Lorena/videoclips"
COVERS_DEST = os.path.join(PROJECT_DIR, "assets", "images", "covers")
DATA_FILE = os.path.join(PROJECT_DIR, "data", "songs.json")

os.makedirs(COVERS_DEST, exist_ok=True)
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '-', text)

def infer_relato_category(title, lyrics, album):
    combined = (title + " " + lyrics + " " + album).lower()
    if any(k in combined for k in ['dolor', 'espalda', 'lumbago', 'viejoven', 'vejez', 'varicela', 'vegetariana', 'hueso', 'artrosis', 'sofa', 'reuma', 'achaques']):
        return 'viejoven', 'Crisis de Viejoven'
    if any(k in combined for k in ['burro', 'burrito', 'huerta', 'oveja', 'ratas', 'poni', 'topo', 'topos', 'animal', 'calamar', 'perro', 'gato', 'caballo']):
        return 'campo-animales', 'Animales & Campo'
    if any(k in combined for k in ['novio', 'amor', 'cita', 'jefe', 'oficina', 'amiga', 'amigos', 'vecino', 'farola', 'miras', 'enamoro', 'beso', 'dejar', 'dejo', 'pobre']):
        return 'citas-social', 'Citas & Vida Social'
    if any(k in combined for k in ['lentejas', 'cocina', 'estropajo', 'fregadero', 'pelapapas', 'gazpacho', 'puchero', 'fuego', 'policia', 'ikea', 'parking', 'perdi', 'suiza', 'china', 'sueco', 'desastre', 'coche', 'llaves', 'despertador']):
        return 'desastres-absurdos', 'Desastres Cotidianos'
    return 'vida-cotidiana', 'Vida Real & Rutina'

albums_info = {
    'Cosas de la vida real': {'id': 'cd1', 'cd_num': 1, 'badge': 'CD 1', 'color': 'torbellino-coral'},
    'Me pasa de todo': {'id': 'cd2', 'cd_num': 2, 'badge': 'CD 2', 'color': 'torbellino-denim'},
    'Que locura': {'id': 'cd3', 'cd_num': 3, 'badge': 'CD 3', 'color': 'torbellino-wine'},
    'Problemas de viejoven': {'id': 'cd4', 'cd_num': 4, 'badge': 'CD 4', 'color': 'torbellino-plum'}
}

all_songs = []
global_id = 1

for album_name, alb_meta in albums_info.items():
    alb_dir = os.path.join(VIDEOCLIPS_DIR, album_name)
    if not os.path.exists(alb_dir):
        continue
    
    song_folders = sorted(os.listdir(alb_dir))
    track_num = 1
    for s_folder in song_folders:
        s_path = os.path.join(alb_dir, s_folder)
        if not os.path.isdir(s_path):
            continue
        
        clean_title = re.sub(r'^\d+\s*-\s*', '', s_folder).strip()
        slug = f"{alb_meta['id']}-{slugify(clean_title)}"
        
        dur_str = "03:00"
        dur_sec = 180.0
        tiempos_file = os.path.join(s_path, "tiempos.json")
        if os.path.exists(tiempos_file):
            try:
                with open(tiempos_file, "r", encoding="utf-8") as f:
                    tj = json.load(f)
                    dur_sec = tj.get("duracion_total_segundos", 180.0)
                    m = int(dur_sec // 60)
                    s = int(dur_sec % 60)
                    dur_str = f"{m:02d}:{s:02d}"
            except Exception:
                pass
                
        lyrics = ""
        letra_file = os.path.join(s_path, "youtube", "letra.txt")
        if not os.path.exists(letra_file):
            letra_file = os.path.join(s_path, "transcripcion.md")
        if os.path.exists(letra_file):
            try:
                with open(letra_file, "r", encoding="utf-8") as f:
                    lyrics = f.read().strip()
            except Exception:
                pass

        synopsis = f"Canción de comedia del álbum '{album_name}' de Lorena Torbellino."
        info_yt = os.path.join(s_path, "youtube", "info_youtube.md")
        if os.path.exists(info_yt):
            try:
                with open(info_yt, "r", encoding="utf-8") as f:
                    content = f.read()
                    m_desc = re.search(r'## 2\. Descripción del Vídeo.*?\n```text\n(.*?)\n\n', content, re.DOTALL)
                    if m_desc:
                        synopsis = m_desc.group(1).strip().replace('\n', ' ')
            except Exception:
                pass
                
        mini_src = os.path.join(s_path, "youtube", "miniatura_youtube.jpg")
        cover_filename = f"{slug}.jpg"
        has_custom_cover = False
        if os.path.exists(mini_src):
            dest_cover = os.path.join(COVERS_DEST, cover_filename)
            shutil.copyfile(mini_src, dest_cover)
            has_custom_cover = True
            
        has_video = any(f.endswith("_1080p_watermark.mp4") for f in os.listdir(s_path))
        relato_id, relato_label = infer_relato_category(clean_title, lyrics, album_name)
        
        album_cover_map = {
            'cd1': 'assets/images/albums/cd1_cosas_de_la_vida_real_web.jpg',
            'cd2': 'assets/images/albums/cd2_me_pasa_de_todo_web.jpg',
            'cd3': 'assets/images/albums/cd3_que_locura_web.jpg',
            'cd4': 'assets/images/albums/cd4_problemas_de_viejoven_web.jpg'
        }
        default_cover = album_cover_map.get(alb_meta['id'], 'assets/images/lorena_avatar.jpg')

        # Enlace directo al videoclip específico o búsqueda directa del vídeo en YouTube
        yt_search_query = urllib.parse.quote_plus(f"{clean_title} Lorena Torbellino")
        direct_yt_url = f"https://www.youtube.com/results?search_query={yt_search_query}"

        song_entry = {
            "id": global_id,
            "track_number": track_num,
            "title": clean_title,
            "slug": slug,
            "album": album_name,
            "album_id": alb_meta['id'],
            "album_badge": alb_meta['badge'],
            "album_color": alb_meta['color'],
            "duration": dur_str,
            "duration_seconds": round(dur_sec, 2),
            "relato_id": relato_id,
            "relato_label": relato_label,
            "synopsis": synopsis,
            "lyrics": lyrics,
            "has_video": has_video,
            "has_custom_cover": has_custom_cover,
            "cover_image": f"assets/images/covers/{cover_filename}" if has_custom_cover else default_cover,
            "youtube_id": "",
            "youtube_url": direct_yt_url
        }
        all_songs.append(song_entry)
        global_id += 1
        track_num += 1

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(all_songs, f, ensure_ascii=False, indent=2)

print(f"Catálogo generado con éxito: {len(all_songs)} canciones.")
print(f"Miniaturas copiadas a assets/images/covers/: {len(os.listdir(COVERS_DEST))}")
