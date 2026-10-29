#!/usr/bin/env python3
import os
import json
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
PUBLIC_DIR = os.path.join(PROJECT_DIR, "public")
DATA_FILE = os.path.join(PROJECT_DIR, "songs.json")
INDEX_FILE = os.path.join(PUBLIC_DIR, "index.html")
QUIEN_ES_FILE = os.path.join(PUBLIC_DIR, "quien-es-lorena.html")

def build_index():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        songs = json.load(f)

    # Export dynamic data files separated from the HTML template (reduces token load and keeps index.html lightweight)
    songs_js_path = os.path.join(PUBLIC_DIR, "assets", "js", "songs-data.js")
    os.makedirs(os.path.dirname(songs_js_path), exist_ok=True)
    with open(songs_js_path, "w", encoding="utf-8") as f_js:
        f_js.write(f"window.CATALOGO_SONGS = {json.dumps(songs, ensure_ascii=False, indent=2)};\n")

    public_songs_json = os.path.join(PUBLIC_DIR, "songs.json")
    with open(public_songs_json, "w", encoding="utf-8") as f_json:
        json.dump(songs, f_json, ensure_ascii=False, indent=2)

    total_canciones = len(songs)
    total_discos = len(set(s["album"] for s in songs))
    con_video = sum(1 for s in songs if s["has_video"])

    html_content = f'''<!DOCTYPE html>
<html lang="es" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Lorena Torbellino — Web Oficial | Canciones y Desastres</title>
  <meta name="description" content="Página web oficial de Lorena Torbellino: comedia musical absurda, pop costumbrista y sátira animada en 2D. Explora sus 4 discos y videoclips oficiales.">
  <link rel="canonical" href="https://www.lorenatorbellino.raupulus.dev/">
  
  <!-- Open Graph / Meta Social Adaptado -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Lorena Torbellino">
  <meta property="og:url" content="https://www.lorenatorbellino.raupulus.dev/">
  <meta property="og:title" content="Lorena Torbellino — Web Oficial | Canciones y Desastres">
  <meta property="og:description" content="Comedia absurda, pop costumbrista y sátira animada en 2D. 4 discos y 110 canciones de desventuras cotidianas.">
  <meta property="og:image" content="https://www.lorenatorbellino.raupulus.dev/assets/images/og_home.jpg">
  <meta property="og:image:secure_url" content="https://www.lorenatorbellino.raupulus.dev/assets/images/og_home.jpg">
  <meta property="og:image:type" content="image/jpeg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Lorena Torbellino — Web Oficial y Cancionero de 110 Canciones">
  <meta property="og:locale" content="es_ES">

  <!-- Twitter Cards -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@loretorbellino">
  <meta name="twitter:creator" content="@loretorbellino">
  <meta name="twitter:title" content="Lorena Torbellino — Web Oficial | Canciones y Desastres">
  <meta name="twitter:description" content="Comedia musical absurda, pop costumbrista y sátira animada en 2D. 4 discos y 110 canciones.">
  <meta name="twitter:image" content="https://www.lorenatorbellino.raupulus.dev/assets/images/og_home.jpg">
  <meta name="twitter:image:alt" content="Lorena Torbellino — Web Oficial y Cancionero">
  
  <link rel="icon" type="image/png" href="assets/images/favicon.png">
  <link rel="stylesheet" href="assets/css/tailwind.css">
  <script src="assets/js/songs-data.js"></script>
  <script defer src="assets/js/alpine.min.js"></script>

  <!-- Schema.org JSON-LD -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "MusicGroup",
    "name": "Lorena Torbellino",
    "url": "https://www.lorenatorbellino.raupulus.dev/",
    "logo": "https://www.lorenatorbellino.raupulus.dev/assets/images/lorena_logo_oficial.webp",
    "image": "https://www.lorenatorbellino.raupulus.dev/assets/images/lorena_banner.webp",
    "description": "Proyecto musical de comedia absurda, pop costumbrista y sátira animada en 2D.",
    "genre": ["Comedy", "Pop", "Satire"],
    "sameAs": [
      "https://www.youtube.com/@LorenaTorbellino",
      "https://www.tiktok.com/@lorenatorbellino",
      "https://www.instagram.com/lorenatorbellino/",
      "https://x.com/loretorbellino"
    ],
    "album": [
      {{"@type": "MusicAlbum", "name": "Cosas de la vida real", "numTracks": 21}},
      {{"@type": "MusicAlbum", "name": "Me pasa de todo", "numTracks": 33}},
      {{"@type": "MusicAlbum", "name": "Que locura", "numTracks": 32}},
      {{"@type": "MusicAlbum", "name": "Problemas de viejoven", "numTracks": 24}}
    ]
  }}
  </script>
</head>
<body class="min-h-screen bg-torbellino-cream font-sans antialiased text-[#291C22]" 
      x-data="musicApp()" 
      x-init="init()">

  <!-- Skip link de accesibilidad WCAG 2.4.1 -->
  <a href="#inicio" class="sr-only focus:not-sr-only focus:fixed focus:top-3 focus:left-3 focus:z-50 focus:bg-torbellino-plum focus:text-white focus:px-4 focus:py-2 focus:rounded-xl focus:font-bold focus:shadow-xl focus:ring-2 focus:ring-torbellino-coral">
    Saltar al contenido principal
  </a>

  <!-- Top Announcement Bar -->
  <aside aria-label="Aviso destacado" class="bg-gradient-to-r from-torbellino-coral via-torbellino-peach to-torbellino-coral text-torbellino-plum text-xs md:text-sm font-bold py-2 px-4 text-center shadow-inner flex items-center justify-center gap-2">
    <span>👟</span>
    <span>¡Canal oficial activo! 110 canciones catalogadas y videoclips semanales en YouTube</span>
    <a href="https://www.youtube.com/@LorenaTorbellino?sub_confirmation=1" target="_blank" rel="noopener noreferrer" class="underline hover:text-torbellino-wine transition ml-1 inline-flex items-center gap-1 font-extrabold">
      Suscribirse gratis →
    </a>
  </aside>

  <!-- Header / Navbar -->
  <header class="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-torbellino-sand shadow-sm transition">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
      
      <!-- Brand Logo -->
      <a href="#inicio" class="flex items-center gap-3 group">
        <div class="relative w-12 h-12 rounded-full overflow-hidden border-2 border-torbellino-coral shadow-md group-hover:scale-105 transition transform duration-200">
          <img src="assets/images/lorena_avatar.webp" alt="Lorena Torbellino" width="48" height="48" class="w-full h-full object-cover">
        </div>
        <div class="flex flex-col">
          <span class="text-xl md:text-2xl font-black tracking-tight bg-gradient-to-r from-torbellino-coral to-torbellino-wine bg-clip-text text-transparent">
            Lorena Torbellino
          </span>
          <span class="text-[11px] font-bold text-torbellino-denim tracking-wider uppercase">
            Canciones y Desastres
          </span>
        </div>
      </a>

      <!-- Desktop Nav Links -->
      <nav class="hidden md:flex items-center gap-7 font-bold text-sm text-[#4A3842]">
        <a href="#inicio" class="hover:text-torbellino-coral transition">Inicio</a>
        <a href="#discos" class="hover:text-torbellino-coral transition">Discos</a>
        <a href="#catalogo" class="hover:text-torbellino-coral transition">Cancionero</a>
        <a href="quien-es-lorena.html" class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-torbellino-sand/60 hover:bg-torbellino-coral hover:text-white transition">
          <span>✨</span>
          <span>Quién es Lorena</span>
        </a>
      </nav>

      <!-- Desktop Action CTA -->
      <div class="hidden md:flex items-center gap-4">
        <a href="https://www.youtube.com/@LorenaTorbellino?sub_confirmation=1" target="_blank" rel="noopener noreferrer" 
           class="inline-flex items-center gap-2 bg-gradient-to-r from-torbellino-coral to-torbellino-red text-white font-extrabold text-sm px-5 py-2.5 rounded-full shadow-md shadow-red-500/20 hover:shadow-lg hover:shadow-red-500/30 hover:scale-105 transition duration-200">
          <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
          <span>Suscribirme al Canal</span>
        </a>
      </div>

      <!-- Mobile Menu Toggle Button -->
      <div class="md:hidden flex items-center">
        <button @click="mobileMenuOpen = !mobileMenuOpen" 
                type="button" 
                :aria-expanded="mobileMenuOpen.toString()"
                aria-controls="mobile-menu"
                class="p-2.5 rounded-2xl text-torbellino-plum hover:bg-torbellino-sand/50 transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-torbellino-coral" 
                aria-label="Abrir menú de navegación">
          <svg x-show="!mobileMenuOpen" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7"/></svg>
          <svg x-show="mobileMenuOpen" x-cloak class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>

    </div>

    <!-- Mobile Dropdown -->
    <div id="mobile-menu" x-show="mobileMenuOpen" x-cloak @click.away="mobileMenuOpen = false" class="md:hidden border-b border-torbellino-sand bg-white px-5 pt-3 pb-6 space-y-3 font-bold text-sm shadow-xl">
      <a @click="mobileMenuOpen = false" href="#inicio" class="block py-2 text-[#4A3842] hover:text-torbellino-coral">Inicio</a>
      <a @click="mobileMenuOpen = false" href="#discos" class="block py-2 text-[#4A3842] hover:text-torbellino-coral">Discos Oficiales</a>
      <a @click="mobileMenuOpen = false" href="#catalogo" class="block py-2 text-[#4A3842] hover:text-torbellino-coral">Cancionero y Filtros</a>
      <a href="quien-es-lorena.html" class="block py-2 text-torbellino-coral font-black">✨ Quién es Lorena (Biografía y Gags)</a>
      <div class="pt-2">
        <a href="https://www.youtube.com/@LorenaTorbellino?sub_confirmation=1" target="_blank" rel="noopener noreferrer" 
           class="flex items-center justify-center gap-2 w-full bg-gradient-to-r from-torbellino-coral to-torbellino-red text-white py-3 rounded-2xl font-black shadow-md min-h-[44px]">
          <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
          <span>Suscribirme al Canal de YouTube</span>
        </a>
      </div>
    </div>
  </header>

  <!-- Hero Section -->
  <main id="inicio" class="relative overflow-hidden pt-8 pb-16 md:pt-14 md:pb-20">
    <div class="absolute -top-24 left-1/2 -translate-x-1/2 w-full max-w-7xl h-96 bg-gradient-to-br from-torbellino-peach/40 via-torbellino-lilac/30 to-transparent rounded-full blur-3xl -z-10 pointer-events-none"></div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-12 items-center">
        
        <!-- Left Column -->
        <div class="lg:col-span-7 space-y-6 text-center lg:text-left">
          
          <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white border border-torbellino-sand text-xs md:text-sm font-black text-torbellino-wine shadow-sm">
            <span class="inline-block w-2.5 h-2.5 rounded-full bg-torbellino-coral animate-pulse"></span>
            <span>Pop Cómico · Sátira Cotidiana · Animación 2D</span>
          </div>

          <h1 class="text-4xl sm:text-5xl md:text-6xl font-black tracking-tight leading-[1.15]">
            Canto mis desastres cotidianos con ritmo, zapatillas rojas y 
            <span class="block bg-gradient-to-r from-torbellino-coral via-[#FF5F45] to-torbellino-wine bg-clip-text text-transparent">
              cero sentido del ridículo.
            </span>
          </h1>

          <p class="text-base sm:text-lg md:text-xl text-[#5C4550] max-w-2xl mx-auto lg:mx-0 font-medium leading-relaxed">
            ¡Hola! Soy Lorena Torbellino: 20 años, voz dulce de niña buena y un talento casi sobrenatural para que todo en la vida me salga al revés. Bienvenido a mi universo musical.
          </p>

          <!-- CTAs -->
          <div class="flex flex-wrap items-center justify-center lg:justify-start gap-4 pt-2">
            <a href="#catalogo" class="bg-gradient-to-r from-torbellino-coral to-torbellino-wine text-white font-extrabold px-8 py-3.5 rounded-full shadow-lg shadow-torbellino-coral/30 hover:scale-105 hover:shadow-xl transition duration-200 flex items-center gap-2 min-h-[44px]">
              <span>Explorar el Cancionero ({total_canciones} Temas)</span>
              <span>↓</span>
            </a>
            <a href="quien-es-lorena.html" 
               class="bg-white hover:bg-torbellino-sand/40 text-torbellino-plum border-2 border-torbellino-sand font-black px-7 py-3 rounded-full hover:border-torbellino-coral/50 transition duration-200 flex items-center gap-2 shadow-sm min-h-[44px]">
              <span>✨ Conoce a Lorena</span>
            </a>
          </div>

          <!-- Mini Stats -->
          <div class="pt-6 grid grid-cols-3 gap-4 border-t border-torbellino-sand max-w-lg mx-auto lg:mx-0">
            <div>
              <div class="text-3xl font-black text-torbellino-coral">{total_canciones}</div>
              <div class="text-xs font-bold text-[#735A66]">Canciones Oficiales</div>
            </div>
            <div>
              <div class="text-3xl font-black text-torbellino-denim">{total_discos}</div>
              <div class="text-xs font-bold text-[#735A66]">Álbumes Completos</div>
            </div>
            <div>
              <div class="text-3xl font-black text-torbellino-wine">{con_video}</div>
              <div class="text-xs font-bold text-[#735A66]">Videoclips Producidos</div>
            </div>
          </div>

        </div>

        <!-- Right Column / Mascot Card -->
        <div class="lg:col-span-5 flex justify-center">
          <div class="relative w-full max-w-md">
            
            <div class="absolute -top-6 -right-6 w-24 h-24 bg-torbellino-peach/70 rounded-full blur-xl -z-10"></div>
            <div class="absolute -bottom-8 -left-6 w-32 h-32 bg-torbellino-mint/50 rounded-full blur-xl -z-10"></div>

            <div class="bg-white rounded-3xl p-5 border-4 border-white shadow-2xl shadow-torbellino-coral/15 ring-1 ring-torbellino-sand transform rotate-1 hover:rotate-0 transition duration-300">
              <div class="relative rounded-2xl overflow-hidden bg-gradient-to-b from-[#FDE8DF] via-[#FCEAE3] to-[#FBE4DD] aspect-[4/5] flex items-center justify-center p-4">
                <img src="assets/images/lorena_sticker_guino.webp" alt="Lorena Torbellino haciendo el signo de la victoria" width="400" height="500" fetchpriority="high" class="w-full h-full object-contain filter drop-shadow-md">
                
                <div class="absolute bottom-4 left-4 right-4 bg-white/95 backdrop-blur-sm rounded-2xl p-3 shadow-lg border border-torbellino-sand flex items-center justify-between">
                  <div class="flex items-center gap-2.5">
                    <span class="text-2xl">✨</span>
                    <div>
                      <div class="text-xs font-black text-torbellino-plum">Lorena Torbellino</div>
                      <div class="text-[11px] font-semibold text-torbellino-wine">Voz dulce · Zapatillas Converse rojas</div>
                    </div>
                  </div>
                  <span class="px-2.5 py-1 rounded-full text-[11px] font-black bg-torbellino-coral/15 text-torbellino-wine">
                    @LorenaTorbellino
                  </span>
                </div>
              </div>
            </div>

          </div>
        </div>

      </div>
    </div>
  </main>

  <!-- Albums Grid Section -->
  <section id="discos" class="scroll-mt-20 py-16 md:py-20 bg-white border-y border-torbellino-sand">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <div class="text-center max-w-2xl mx-auto mb-12 space-y-2">
        <h2 class="text-xs font-extrabold uppercase tracking-widest text-torbellino-coral-dark">Discografía</h2>
        <p class="text-3xl sm:text-4xl font-black text-torbellino-plum">Los 4 Álbumes Oficiales</p>
        <p class="text-sm text-[#6E5562]">
          Carátulas oficiales de alta fidelidad preparadas para plataformas digitales y distribución. Haz clic en cualquier disco para filtrar el cancionero.
        </p>
      </div>

      <!-- Albums Cards Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        
        <!-- Disco 1 -->
        <div @click="filterByAlbum('cd1')" 
             @keydown.enter.prevent="filterByAlbum('cd1')"
             @keydown.space.prevent="filterByAlbum('cd1')"
             tabindex="0"
             role="button"
             :aria-pressed="selectedAlbum === 'cd1'"
             :class="selectedAlbum === 'cd1' ? 'ring-4 ring-torbellino-coral border-torbellino-coral shadow-xl' : 'hover:border-torbellino-coral/50 shadow-sm hover:shadow-lg'"
             class="group cursor-pointer bg-torbellino-cream rounded-3xl p-5 border-2 border-torbellino-sand transition-all duration-200 flex flex-col justify-between focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-torbellino-coral">
          <div>
            <div class="flex items-center justify-between mb-3">
              <span class="px-3 py-1 rounded-full text-xs font-black bg-torbellino-coral text-white">CD 1</span>
              <span class="text-xs font-bold text-torbellino-wine">21 Temas</span>
            </div>
            
            <!-- Real Album Cover -->
            <div class="aspect-square rounded-2xl overflow-hidden shadow-md mb-4 border border-torbellino-sand/80 group-hover:scale-105 transition duration-300 relative">
              <img src="assets/images/albums/cd1_cosas_de_la_vida_real_web.webp" alt="Carátula oficial CD 1 - Cosas de la vida real" width="300" height="300" class="w-full h-full object-cover">
              <div class="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition flex items-end p-3">
                <span class="text-[11px] font-black text-white bg-torbellino-coral px-2.5 py-1 rounded-full">Ver 21 temas</span>
              </div>
            </div>

            <h3 class="text-lg font-black text-torbellino-plum mb-1.5 group-hover:text-torbellino-coral-dark transition">
              Cosas de la vida real
            </h3>
            <p class="text-xs text-[#6B5660] leading-relaxed">
              La odisea de madurar, buscar aparcamiento en el Carrefour, perder llaves y las peleas cotidianas.
            </p>
          </div>
          <div class="mt-5 pt-3 border-t border-torbellino-sand flex items-center justify-between text-xs font-black text-torbellino-coral-dark">
            <span>Filtrar canciones</span>
            <span class="group-hover:translate-x-1 transition">→</span>
          </div>
        </div>

        <!-- Disco 2 -->
        <div @click="filterByAlbum('cd2')" 
             @keydown.enter.prevent="filterByAlbum('cd2')"
             @keydown.space.prevent="filterByAlbum('cd2')"
             tabindex="0"
             role="button"
             :aria-pressed="selectedAlbum === 'cd2'"
             :class="selectedAlbum === 'cd2' ? 'ring-4 ring-torbellino-denim border-torbellino-denim shadow-xl' : 'hover:border-torbellino-denim/50 shadow-sm hover:shadow-lg'"
             class="group cursor-pointer bg-torbellino-cream rounded-3xl p-5 border-2 border-torbellino-sand transition-all duration-200 flex flex-col justify-between focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-torbellino-denim">
          <div>
            <div class="flex items-center justify-between mb-3">
              <span class="px-3 py-1 rounded-full text-xs font-black bg-torbellino-denim text-white">CD 2</span>
              <span class="text-xs font-bold text-torbellino-wine">33 Temas</span>
            </div>
            
            <!-- Real Album Cover -->
            <div class="aspect-square rounded-2xl overflow-hidden shadow-md mb-4 border border-torbellino-sand/80 group-hover:scale-105 transition duration-300 relative">
              <img src="assets/images/albums/cd2_me_pasa_de_todo_web.webp" alt="Carátula oficial CD 2 - Me pasa de todo" width="300" height="300" class="w-full h-full object-cover">
              <div class="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition flex items-end p-3">
                <span class="text-[11px] font-black text-white bg-torbellino-denim px-2.5 py-1 rounded-full">Ver 33 temas</span>
              </div>
            </div>

            <h3 class="text-lg font-black text-torbellino-plum mb-1.5 group-hover:text-torbellino-denim transition">
              Me pasa de todo
            </h3>
            <p class="text-xs text-[#6B5660] leading-relaxed">
              La ley de Murphy en clave de pop cómico: tostadas con mantequilla al suelo e inundaciones en casa.
            </p>
          </div>
          <div class="mt-5 pt-3 border-t border-torbellino-sand flex items-center justify-between text-xs font-black text-torbellino-denim">
            <span>Filtrar canciones</span>
            <span class="group-hover:translate-x-1 transition">→</span>
          </div>
        </div>

        <!-- Disco 3 -->
        <div @click="filterByAlbum('cd3')" 
             @keydown.enter.prevent="filterByAlbum('cd3')"
             @keydown.space.prevent="filterByAlbum('cd3')"
             tabindex="0"
             role="button"
             :aria-pressed="selectedAlbum === 'cd3'"
             :class="selectedAlbum === 'cd3' ? 'ring-4 ring-torbellino-wine border-torbellino-wine shadow-xl' : 'hover:border-torbellino-wine/50 shadow-sm hover:shadow-lg'"
             class="group cursor-pointer bg-torbellino-cream rounded-3xl p-5 border-2 border-torbellino-sand transition-all duration-200 flex flex-col justify-between focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-torbellino-wine">
          <div>
            <div class="flex items-center justify-between mb-3">
              <span class="px-3 py-1 rounded-full text-xs font-black bg-torbellino-wine text-white">CD 3</span>
              <span class="text-xs font-bold text-torbellino-wine">32 Temas</span>
            </div>
            
            <!-- Real Album Cover -->
            <div class="aspect-square rounded-2xl overflow-hidden shadow-md mb-4 border border-torbellino-sand/80 group-hover:scale-105 transition duration-300 relative">
              <img src="assets/images/albums/cd3_que_locura_web.webp" alt="Carátula oficial CD 3 - Que locura" width="300" height="300" class="w-full h-full object-cover">
              <div class="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition flex items-end p-3">
                <span class="text-[11px] font-black text-white bg-torbellino-wine px-2.5 py-1 rounded-full">Ver 32 temas</span>
              </div>
            </div>

            <h3 class="text-lg font-black text-torbellino-plum mb-1.5 group-hover:text-torbellino-wine transition">
              Que locura
            </h3>
            <p class="text-xs text-[#6B5660] leading-relaxed">
              Situaciones surrealistas, citas desastrosas, vecinos peculiares y compras impulsivas inútiles por internet.
            </p>
          </div>
          <div class="mt-5 pt-3 border-t border-torbellino-sand flex items-center justify-between text-xs font-black text-torbellino-wine">
            <span>Filtrar canciones</span>
            <span class="group-hover:translate-x-1 transition">→</span>
          </div>
        </div>

        <!-- Disco 4 -->
        <div @click="filterByAlbum('cd4')" 
             @keydown.enter.prevent="filterByAlbum('cd4')"
             @keydown.space.prevent="filterByAlbum('cd4')"
             tabindex="0"
             role="button"
             :aria-pressed="selectedAlbum === 'cd4'"
             :class="selectedAlbum === 'cd4' ? 'ring-4 ring-torbellino-plum border-torbellino-plum shadow-xl' : 'hover:border-torbellino-plum/50 shadow-sm hover:shadow-lg'"
             class="group cursor-pointer bg-torbellino-cream rounded-3xl p-5 border-2 border-torbellino-sand transition-all duration-200 flex flex-col justify-between focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-torbellino-plum">
          <div>
            <div class="flex items-center justify-between mb-3">
              <span class="px-3 py-1 rounded-full text-xs font-black bg-torbellino-plum text-white">CD 4</span>
              <span class="text-xs font-bold text-torbellino-wine">24 Temas</span>
            </div>
            
            <!-- Real Album Cover -->
            <div class="aspect-square rounded-2xl overflow-hidden shadow-md mb-4 border border-torbellino-sand/80 group-hover:scale-105 transition duration-300 relative">
              <img src="assets/images/albums/cd4_problemas_de_viejoven_web.webp" alt="Carátula oficial CD 4 - Problemas de viejoven" width="300" height="300" class="w-full h-full object-cover">
              <div class="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition flex items-end p-3">
                <span class="text-[11px] font-black text-white bg-torbellino-plum px-2.5 py-1 rounded-full">Ver 24 temas</span>
              </div>
            </div>

            <h3 class="text-lg font-black text-torbellino-plum mb-1.5 group-hover:text-torbellino-coral-dark transition">
              Problemas de viejoven
            </h3>
            <p class="text-xs text-[#6B5660] leading-relaxed">
              Dolores de espalda prematuros a los 20, ilusión con la freidora de aire y preferir dormir a salir de fiesta.
            </p>
          </div>
          <div class="mt-5 pt-3 border-t border-torbellino-sand flex items-center justify-between text-xs font-black text-torbellino-plum">
            <span>Filtrar canciones</span>
            <span class="group-hover:translate-x-1 transition">→</span>
          </div>
        </div>

      </div>

    </div>
  </section>

  <!-- Complete Song Catalog & Filtering System -->
  <section id="catalogo" class="scroll-mt-20 py-16 md:py-24">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <!-- Catalog Header -->
      <div class="flex flex-col lg:flex-row lg:items-end justify-between mb-8 gap-6">
        <div>
          <span class="text-xs font-extrabold uppercase tracking-widest text-torbellino-coral-dark">Catálogo Interactivo</span>
          <h2 class="text-3xl sm:text-4xl font-black text-torbellino-plum mt-1">Cancionero Oficial</h2>
          <p class="text-sm text-[#6E5562] mt-1.5">
            Filtra por álbum o por temática de relato cotidiano, o busca cualquier título o estrofa.
          </p>
        </div>

        <!-- Search Input -->
        <div class="w-full lg:w-80 relative">
          <label for="search-input" class="sr-only">Buscar canción o letra</label>
          <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-gray-400">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
          </div>
          <input id="search-input" 
                 type="text" 
                 x-model="searchQuery" 
                 placeholder="Buscar canción o letra..." 
                 class="w-full pl-10 pr-4 py-2.5 rounded-2xl bg-white border border-torbellino-sand text-sm font-medium focus:outline-none focus:ring-2 focus:ring-torbellino-coral focus:border-transparent shadow-sm">
        </div>
      </div>

      <!-- Filters Bar: (1) Discos + (2) Relatos -->
      <div class="bg-white rounded-3xl p-5 border border-torbellino-sand shadow-sm space-y-4 mb-10">
        
        <!-- Album Filter Tabs -->
        <div class="flex flex-wrap items-center gap-2">
          <span class="text-xs font-black text-torbellino-plum uppercase tracking-wider mr-2">Discos:</span>
          
          <button @click="selectedAlbum = 'todos'" 
                  :class="selectedAlbum === 'todos' ? 'bg-torbellino-plum text-white shadow-sm' : 'bg-torbellino-sand/50 text-[#5C4550] hover:bg-torbellino-sand'"
                  class="px-4 py-1.5 rounded-full text-xs font-bold transition">
            Todos los Discos
          </button>
          
          <button @click="selectedAlbum = 'cd1'" 
                  :class="selectedAlbum === 'cd1' ? 'bg-torbellino-coral text-white shadow-sm' : 'bg-torbellino-sand/50 text-[#5C4550] hover:bg-torbellino-sand'"
                  class="px-4 py-1.5 rounded-full text-xs font-bold transition">
            CD 1: Cosas de la vida real (21)
          </button>
          
          <button @click="selectedAlbum = 'cd2'" 
                  :class="selectedAlbum === 'cd2' ? 'bg-torbellino-denim text-white shadow-sm' : 'bg-torbellino-sand/50 text-[#5C4550] hover:bg-torbellino-sand'"
                  class="px-4 py-1.5 rounded-full text-xs font-bold transition">
            CD 2: Me pasa de todo (33)
          </button>

          <button @click="selectedAlbum = 'cd3'" 
                  :class="selectedAlbum === 'cd3' ? 'bg-torbellino-wine text-white shadow-sm' : 'bg-torbellino-sand/50 text-[#5C4550] hover:bg-torbellino-sand'"
                  class="px-4 py-1.5 rounded-full text-xs font-bold transition">
            CD 3: Que locura (32)
          </button>

          <button @click="selectedAlbum = 'cd4'" 
                  :class="selectedAlbum === 'cd4' ? 'bg-torbellino-plum text-white shadow-sm' : 'bg-torbellino-sand/50 text-[#5C4550] hover:bg-torbellino-sand'"
                  class="px-4 py-1.5 rounded-full text-xs font-bold transition">
            CD 4: Problemas de viejoven (24)
          </button>
        </div>

        <!-- Relato Category Tabs -->
        <div class="flex flex-wrap items-center gap-2 pt-3 border-t border-torbellino-sand/60">
          <span class="text-xs font-black text-torbellino-plum uppercase tracking-wider mr-2">Tipo de Relato:</span>
          
          <button @click="selectedRelato = 'todos'" 
                  :class="selectedRelato === 'todos' ? 'bg-torbellino-coral text-white' : 'bg-torbellino-cream text-[#5C4550] hover:bg-torbellino-sand/60'"
                  class="px-3 py-1 rounded-full text-xs font-semibold border border-torbellino-sand transition">
            Cualquier Historia
          </button>

          <button @click="selectedRelato = 'viejoven'" 
                  :class="selectedRelato === 'viejoven' ? 'bg-torbellino-coral text-white' : 'bg-torbellino-cream text-[#5C4550] hover:bg-torbellino-sand/60'"
                  class="px-3 py-1 rounded-full text-xs font-semibold border border-torbellino-sand transition">
            🦴 Crisis de Viejoven
          </button>

          <button @click="selectedRelato = 'desastres-absurdos'" 
                  :class="selectedRelato === 'desastres-absurdos' ? 'bg-torbellino-coral text-white' : 'bg-torbellino-cream text-[#5C4550] hover:bg-torbellino-sand/60'"
                  class="px-3 py-1 rounded-full text-xs font-semibold border border-torbellino-sand transition">
            💥 Desastres Cotidianos
          </button>

          <button @click="selectedRelato = 'citas-social'" 
                  :class="selectedRelato === 'citas-social' ? 'bg-torbellino-coral text-white' : 'bg-torbellino-cream text-[#5C4550] hover:bg-torbellino-sand/60'"
                  class="px-3 py-1 rounded-full text-xs font-semibold border border-torbellino-sand transition">
            💬 Citas & Vida Social
          </button>

          <button @click="selectedRelato = 'vida-cotidiana'" 
                  :class="selectedRelato === 'vida-cotidiana' ? 'bg-torbellino-coral text-white' : 'bg-torbellino-cream text-[#5C4550] hover:bg-torbellino-sand/60'"
                  class="px-3 py-1 rounded-full text-xs font-semibold border border-torbellino-sand transition">
            🛋️ Vida Real & Rutina
          </button>

          <button @click="selectedRelato = 'campo-animales'" 
                  :class="selectedRelato === 'campo-animales' ? 'bg-torbellino-coral text-white' : 'bg-torbellino-cream text-[#5C4550] hover:bg-torbellino-sand/60'"
                  class="px-3 py-1 rounded-full text-xs font-semibold border border-torbellino-sand transition">
            🐾 Animales & Campo
          </button>

          <!-- Toggle solo videoclips -->
          <button @click="onlyWithVideo = !onlyWithVideo" 
                  :class="onlyWithVideo ? 'bg-red-600 text-white font-black' : 'bg-white text-[#735A66] border border-dashed border-red-300'"
                  class="ml-auto px-3.5 py-1 rounded-full text-xs font-bold transition flex items-center gap-1.5 shadow-sm">
            <span>🎬</span>
            <span>Solo con Videoclip</span>
          </button>
        </div>

      </div>

      <!-- Results Count Info -->
      <div class="flex items-center justify-between text-xs font-bold text-[#735A66] mb-6 px-1">
        <div>
          Mostrando <span class="text-torbellino-coral-dark font-black" x-text="filteredSongs.length"></span> de <span x-text="songs.length"></span> canciones
        </div>
        <div x-show="searchQuery || selectedAlbum !== 'todos' || selectedRelato !== 'todos' || onlyWithVideo">
          <button @click="resetFilters()" class="text-torbellino-coral-dark hover:underline">
            ✕ Limpiar filtros
          </button>
        </div>
      </div>

      <!-- Songs Cards Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        
        <template x-for="song in filteredSongs" :key="song.id">
          <article class="bg-white rounded-3xl overflow-hidden border-2 border-torbellino-sand hover:border-torbellino-coral/60 shadow-sm hover:shadow-xl transition-all duration-300 flex flex-col justify-between group">
            
            <div>
              <!-- Thumbnail Banner with Overlay for Pending Videos -->
              <div class="relative aspect-video bg-gradient-to-tr from-torbellino-peach/30 to-torbellino-sand overflow-hidden">
                <img :src="song.cover_image" :alt="song.title" width="400" height="225" class="w-full h-full object-cover group-hover:scale-105 transition duration-300" loading="lazy">
                
                <!-- Badge CD -->
                <div class="absolute top-3 left-3 flex items-center gap-2 z-10">
                  <span class="px-2.5 py-0.5 rounded-full text-[11px] font-black text-white shadow-sm"
                        :class="song.album_id === 'cd1' ? 'bg-torbellino-coral' : (song.album_id === 'cd2' ? 'bg-torbellino-denim' : (song.album_id === 'cd3' ? 'bg-torbellino-wine' : 'bg-torbellino-plum'))"
                        x-text="song.album_badge">
                  </span>
                  <span class="px-2.5 py-0.5 rounded-full text-[10px] font-extrabold bg-white/95 text-torbellino-plum shadow-sm backdrop-blur-sm"
                        x-text="song.relato_label">
                  </span>
                </div>

                <!-- Duration Badge -->
                <div class="absolute bottom-3 right-3 bg-black/75 backdrop-blur-sm text-white text-[11px] font-mono font-bold px-2 py-0.5 rounded-md z-10"
                     x-text="song.duration">
                </div>

                <!-- Video Ready Indicator or Diagonal 'PRÓXIMAMENTE' Banner -->
                <template x-if="song.has_video">
                  <div class="absolute top-3 right-3 bg-red-600 text-white text-[10px] font-black px-2 py-0.5 rounded-full flex items-center gap-1 shadow-md z-10">
                    <span>▶ Videoclip</span>
                  </div>
                </template>

                <template x-if="!song.has_video">
                  <!-- Semi-transparent dark overlay with diagonal 'PRÓXIMAMENTE' ribbon -->
                  <div class="absolute inset-0 bg-black/40 backdrop-blur-[1px] flex items-center justify-center overflow-hidden pointer-events-none">
                    <div class="transform -rotate-12 bg-black/75 border-y-2 border-torbellino-peach/60 text-white text-xs md:text-sm font-black tracking-widest uppercase py-1.5 px-16 shadow-2xl text-center w-[120%] text-torbellino-peach">
                      ⚡ Próximamente
                    </div>
                  </div>
                </template>

              </div>

              <!-- Content Body -->
              <div class="p-6">
                <div class="text-[11px] font-bold text-torbellino-denim mb-1" x-text="'Pista ' + song.track_number + ' · ' + song.album"></div>
                <h3 class="text-lg font-black text-torbellino-plum group-hover:text-torbellino-coral-dark transition leading-snug" x-text="song.title"></h3>
                <p class="text-xs text-[#6B5660] mt-2 line-clamp-3 leading-relaxed" x-text="song.synopsis"></p>
              </div>
            </div>

            <!-- Footer Card Action -->
            <div class="px-6 pb-6 pt-2 flex items-center justify-between border-t border-torbellino-sand/60">
              <button @click="openModal(song)" 
                      class="text-xs font-black transition flex items-center gap-1.5 py-2"
                      :class="song.has_video ? 'text-torbellino-coral-dark hover:text-torbellino-wine' : 'text-[#8A6D7D] hover:text-torbellino-coral-dark'">
                <template x-if="song.has_video">
                  <span class="flex items-center gap-1">
                    <span>Ver letra y detalles</span>
                    <span>→</span>
                  </span>
                </template>
                <template x-if="!song.has_video">
                  <span class="flex items-center gap-1.5 bg-torbellino-sand/60 px-3 py-1 rounded-full text-[11px] font-extrabold text-[#5C4550]">
                    <span>⚡ Próximamente</span>
                    <span>→</span>
                  </span>
                </template>
              </button>

              <a :href="song.youtube_url" target="_blank" rel="noopener noreferrer" 
                 class="p-3 min-w-[44px] min-h-[44px] rounded-xl bg-torbellino-cream hover:bg-torbellino-sand text-torbellino-plum transition inline-flex items-center justify-center" 
                 :title="song.has_video ? 'Ver videoclip de ' + song.title + ' en YouTube' : 'Ver canal oficial de YouTube de Lorena Torbellino'"
                 :aria-label="song.has_video ? 'Ver videoclip de ' + song.title + ' en YouTube' : 'Ver canal oficial de YouTube de Lorena Torbellino'">
                <svg class="w-4 h-4 text-red-600 fill-current" viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
              </a>
            </div>

          </article>
        </template>

      </div>

      <!-- Empty State -->
      <div x-show="filteredSongs.length === 0" x-cloak class="text-center py-16 bg-white rounded-3xl border border-torbellino-sand p-8">
        <span class="text-5xl">🧐</span>
        <h3 class="text-lg font-black text-torbellino-plum mt-3">No hay canciones con esos filtros</h3>
        <p class="text-xs text-[#6B5660] mt-1">Prueba a buscar con otra palabra o restablece los filtros.</p>
        <button @click="resetFilters()" class="mt-4 px-5 py-2.5 rounded-full bg-gradient-to-r from-torbellino-coral to-torbellino-wine text-white font-bold text-xs min-h-[44px]">
          Ver todo el cancionero
        </button>
      </div>

    </div>
  </section>

  <!-- Interactive Song Modal (Letra, Datos, YouTube) -->
  <div x-show="modalOpen" x-cloak 
       role="dialog"
       aria-modal="true"
       aria-labelledby="modal-song-title"
       class="fixed inset-0 z-50 overflow-y-auto bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 sm:p-6"
       @keydown.escape.window="modalOpen = false">
    
    <div @click.away="modalOpen = false" 
         class="bg-white rounded-3xl max-w-2xl w-full max-h-[90vh] overflow-hidden flex flex-col shadow-2xl border-4 border-white animate-in fade-in zoom-in-95 duration-200">
      
      <!-- Modal Header -->
      <div class="p-6 bg-gradient-to-r from-torbellino-cream via-white to-torbellino-peach/20 border-b border-torbellino-sand flex items-center justify-between">
        <div>
          <div class="flex items-center gap-2 mb-1">
            <span class="px-2.5 py-0.5 rounded-full text-[10px] font-black text-white bg-torbellino-coral" x-text="activeSong.album_badge"></span>
            <span class="text-xs font-bold text-torbellino-denim" x-text="activeSong.album"></span>
            <span class="text-xs text-gray-400">·</span>
            <span class="text-xs font-medium text-[#735A66]" x-text="activeSong.duration"></span>
          </div>
          <h2 id="modal-song-title" class="text-2xl font-black text-torbellino-plum" x-text="activeSong.title"></h2>
        </div>

        <button @click="modalOpen = false" class="p-2.5 rounded-full hover:bg-torbellino-sand text-torbellino-plum transition min-w-[44px] min-h-[44px] flex items-center justify-center" aria-label="Cerrar modal">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>

      <!-- Modal Body -->
      <div class="p-6 overflow-y-auto space-y-6">
        
        <!-- Video or Thumbnail -->
        <div class="rounded-2xl overflow-hidden aspect-video bg-black relative border border-torbellino-sand">
          <img :src="activeSong.cover_image" :alt="activeSong.title" width="640" height="360" class="w-full h-full object-cover">
          <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent flex items-end p-4">
            <a :href="activeSong.youtube_url" target="_blank" rel="noopener noreferrer" 
               class="inline-flex items-center gap-2 bg-gradient-to-r from-red-600 to-red-700 text-white text-xs font-black px-4 py-2.5 rounded-full shadow-lg hover:scale-105 transition min-h-[44px]">
              <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
              <span x-text="activeSong.has_video ? 'Ver videoclip en YouTube' : 'Ir al canal oficial de YouTube'"></span>
            </a>
          </div>
        </div>

        <!-- Sinopsis -->
        <div>
          <h3 class="text-xs font-black text-torbellino-coral-dark uppercase tracking-wider mb-1.5">Sinopsis del Gag</h3>
          <p class="text-xs sm:text-sm text-[#4A3842] leading-relaxed bg-torbellino-cream p-4 rounded-2xl border border-torbellino-sand" x-text="activeSong.synopsis"></p>
        </div>

        <!-- Lyrics Section (Solo para canciones estrenadas/publicadas) -->
        <template x-if="activeSong.has_video">
          <div>
            <h3 class="text-xs font-black text-torbellino-plum uppercase tracking-wider mb-2">Letra Oficial</h3>
            <div class="bg-gray-50 rounded-2xl p-5 border border-torbellino-sand text-xs sm:text-sm font-normal text-[#291C22] whitespace-pre-line leading-relaxed max-h-60 overflow-y-auto" x-text="activeSong.lyrics || 'Letra en proceso de publicación oficial.'"></div>
          </div>
        </template>

        <template x-if="!activeSong.has_video">
          <div class="bg-gradient-to-r from-torbellino-cream to-torbellino-peach/20 rounded-2xl p-5 border border-torbellino-sand/80 text-center space-y-2">
            <span class="text-2xl">🔒</span>
            <h3 class="text-xs font-black text-torbellino-plum uppercase tracking-wider">Letra y Videoclip Próximamente</h3>
            <p class="text-xs text-[#6B5660] max-w-md mx-auto leading-relaxed">
              Este tema aún no se ha estrenado oficialmente. La letra y el videoclip completo estarán disponibles tras su publicación en el canal de YouTube.
            </p>
          </div>
        </template>

      </div>

      <!-- Modal Footer -->
      <div class="p-4 bg-torbellino-cream border-t border-torbellino-sand flex flex-col sm:flex-row items-center justify-between gap-3 text-center sm:text-left">
        <span class="text-[11px] font-semibold text-[#735A66]">
          Web oficial por <a href="https://raupulus.dev" target="_blank" rel="noopener noreferrer" class="text-torbellino-coral-dark font-bold hover:underline">raupulus.dev</a> (<a href="mailto:public@raupulus.dev" class="text-torbellino-coral-dark hover:underline">public@raupulus.dev</a>). Música bajo propiedad privada de Lorena Torbellino.
        </span>
        <button @click="modalOpen = false" class="px-5 py-2 rounded-full bg-white border border-torbellino-sand text-xs font-black text-torbellino-plum hover:bg-torbellino-sand transition shrink-0 min-h-[44px]">
          Cerrar
        </button>
      </div>

    </div>

  </div>

  <!-- Teaser: Quién es Lorena -->
  <section class="py-16 md:py-24 bg-white border-t border-torbellino-sand">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="bg-gradient-to-br from-torbellino-cream via-white to-torbellino-peach/30 rounded-3xl border-2 border-torbellino-sand p-8 md:p-14 shadow-lg">
        
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-10 items-center">
          
          <div class="lg:col-span-4 flex justify-center">
            <div class="relative w-56 h-56 rounded-full overflow-hidden border-4 border-torbellino-coral shadow-xl group">
              <img src="assets/images/lorena_avatar.webp" alt="Foto de perfil de Lorena Torbellino" width="224" height="224" class="w-full h-full object-cover group-hover:scale-105 transition duration-300">
            </div>
          </div>

          <div class="lg:col-span-8 space-y-4 text-center lg:text-left">
            <span class="text-xs font-extrabold uppercase tracking-widest text-torbellino-coral-dark">Ficha de Identidad & Poses</span>
            <h2 class="text-3xl sm:text-4xl font-black text-torbellino-plum">
              ¿Quieres conocer las desgracias de Lorena a fondo?
            </h2>
            <p class="text-sm sm:text-base text-[#5C4550] leading-relaxed">
              Descubre su galería de poses, sus crisis de viejoven a los 20 años y las anécdotas más disparatadas de sus videoclips: desde chocarse contra una farola hasta el monstruo calamar del fregadero.
            </p>
            <div class="pt-2 flex flex-wrap justify-center lg:justify-start gap-4">
              <a href="quien-es-lorena.html" class="inline-flex items-center gap-2 bg-gradient-to-r from-torbellino-coral to-torbellino-wine text-white font-extrabold px-6 py-3 rounded-full shadow-md shadow-torbellino-coral/25 hover:scale-105 transition min-h-[44px]">
                <span>Ver Biografía Completa y Galería de Gags</span>
                <span>→</span>
              </a>
            </div>
          </div>

        </div>

      </div>
    </div>
  </section>

  <!-- Footer -->
  <footer class="bg-torbellino-dark text-white pt-16 pb-12 border-t-4 border-torbellino-coral">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <div class="grid grid-cols-1 md:grid-cols-4 gap-10 pb-12 border-b border-white/10">
        
        <!-- Brand Info -->
        <div class="md:col-span-2 space-y-4">
          <div class="flex items-center gap-3">
            <span class="text-2xl font-black tracking-tight text-white">Lorena Torbellino</span>
          </div>
          <p class="text-xs text-white/70 max-w-md leading-relaxed">
            Proyecto musical de comedia absurda, pop costumbrista y sátira animada en 2D.
          </p>
          <div class="pt-2 space-y-1">
            <div class="text-xs text-white/70">
              Desarrollo y autoría web: 
              <a href="https://raupulus.dev" target="_blank" rel="noopener noreferrer" class="text-torbellino-peach font-bold hover:underline">raupulus.dev</a>
            </div>
            <div class="text-xs text-white/70">
              Contacto profesional y licencias: 
              <a href="mailto:public@raupulus.dev" class="text-torbellino-peach font-semibold hover:underline">public@raupulus.dev</a>
            </div>
          </div>
        </div>

        <!-- Links -->
        <div>
          <h3 class="text-xs font-bold uppercase tracking-wider text-torbellino-peach mb-4">Secciones</h3>
          <ul class="space-y-2 text-xs text-white/80">
            <li><a href="#inicio" class="hover:text-torbellino-coral transition">Inicio</a></li>
            <li><a href="#discos" class="hover:text-torbellino-coral transition">Catálogo de Discos</a></li>
            <li><a href="#catalogo" class="hover:text-torbellino-coral transition">Cancionero ({total_canciones})</a></li>
            <li><a href="quien-es-lorena.html" class="hover:text-torbellino-coral transition">Quién es Lorena (Gags & Poses)</a></li>
          </ul>
        </div>

        <!-- Social / Redes Oficiales -->
        <div>
          <h3 class="text-xs font-bold uppercase tracking-wider text-torbellino-peach mb-4">Canal y Redes Oficiales</h3>
          <p class="text-xs text-white/70 mb-3">
            Sigue los desastres cotidianos, canciones y videoclips oficiales:
          </p>
          <div class="flex flex-col gap-2.5">
            <a href="https://www.youtube.com/@LorenaTorbellino?sub_confirmation=1" target="_blank" rel="noopener noreferrer" 
               class="inline-flex items-center gap-2.5 bg-torbellino-coral hover:bg-torbellino-red text-white text-xs font-bold px-3.5 py-2 rounded-xl transition shadow-sm w-fit" title="Canal Oficial de YouTube">
              <svg class="w-4 h-4 fill-current shrink-0" viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
              <span>YouTube: @LorenaTorbellino</span>
            </a>
            
            <div class="flex flex-wrap items-center gap-2 pt-1">
              <a href="https://www.tiktok.com/@lorenatorbellino" target="_blank" rel="noopener noreferrer" 
                 class="inline-flex items-center gap-1.5 bg-white/10 hover:bg-white/20 text-white text-xs font-semibold px-3 py-1.5 rounded-lg transition" title="TikTok @lorenatorbellino">
                <svg class="w-3.5 h-3.5 fill-current shrink-0" viewBox="0 0 24 24"><path d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-1.01-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.24 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/></svg>
                <span>TikTok</span>
              </a>
              <a href="https://www.instagram.com/lorenatorbellino/" target="_blank" rel="noopener noreferrer" 
                 class="inline-flex items-center gap-1.5 bg-white/10 hover:bg-white/20 text-white text-xs font-semibold px-3 py-1.5 rounded-lg transition" title="Instagram @lorenatorbellino">
                <svg class="w-3.5 h-3.5 fill-current shrink-0" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
                <span>Instagram</span>
              </a>
              <a href="https://x.com/loretorbellino" target="_blank" rel="noopener noreferrer" 
                 class="inline-flex items-center gap-1.5 bg-white/10 hover:bg-white/20 text-white text-xs font-semibold px-3 py-1.5 rounded-lg transition" title="X (Twitter) @loretorbellino">
                <svg class="w-3.5 h-3.5 fill-current shrink-0" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                <span>X</span>
              </a>
            </div>
          </div>
        </div>

      </div>

      <!-- Copyright -->
      <div class="pt-8 flex flex-col sm:flex-row items-center justify-between text-xs text-white/50 gap-4">
        <div>
          Web oficial por <a href="https://raupulus.dev" target="_blank" rel="noopener noreferrer" class="text-white/80 hover:text-torbellino-peach font-bold underline">raupulus.dev</a> (<a href="mailto:public@raupulus.dev" class="text-white/80 hover:text-torbellino-peach">public@raupulus.dev</a>). Música y canciones bajo propiedad privada de Lorena Torbellino.
        </div>
        <div>
          <a href="LICENSE" class="hover:text-white transition underline">Licencia AGPLv3</a>
        </div>
      </div>

    </div>
  </footer>

  <!-- Alpine.js Component Script -->
  <script>
    function musicApp() {{
      return {{
        mobileMenuOpen: false,
        modalOpen: false,
        selectedAlbum: 'todos',
        selectedRelato: 'todos',
        searchQuery: '',
        onlyWithVideo: false,
        activeSong: {{}},
        songs: window.CATALOGO_SONGS || [],

        init() {{
          // inicialización reactiva
        }},

        filterByAlbum(albId) {{
          this.selectedAlbum = albId;
          const el = document.getElementById('catalogo');
          if (el) el.scrollIntoView({{ behavior: 'smooth' }});
        }},

        resetFilters() {{
          this.selectedAlbum = 'todos';
          this.selectedRelato = 'todos';
          this.searchQuery = '';
          this.onlyWithVideo = false;
        }},

        openModal(song) {{
          this.activeSong = song;
          this.modalOpen = true;
        }},

        get filteredSongs() {{
          return this.songs.filter(song => {{
            // Filtro Álbum
            if (this.selectedAlbum !== 'todos' && song.album_id !== this.selectedAlbum) {{
              return false;
            }}
            // Filtro Relato
            if (this.selectedRelato !== 'todos' && song.relato_id !== this.selectedRelato) {{
              return false;
            }}
            // Filtro Solo con Video
            if (this.onlyWithVideo && !song.has_video) {{
              return false;
            }}
            // Filtro de Búsqueda (Título o Letra)
            if (this.searchQuery.trim() !== '') {{
              const q = this.searchQuery.toLowerCase();
              const matchTitle = song.title.toLowerCase().includes(q);
              const matchLyrics = song.lyrics.toLowerCase().includes(q);
              const matchSynopsis = song.synopsis.toLowerCase().includes(q);
              if (!matchTitle && !matchLyrics && !matchSynopsis) {{
                return false;
              }}
            }}
            return true;
          }});
        }}
      }};
    }}
  </script>

</body>
</html>
'''
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)
    print("index.html generado con éxito.")


def build_quien_es():
    traits_data = [
        {
            "tag": "DESPISTADA CRÓNICA",
            "tag_color": "bg-torbellino-coral text-white",
            "title": "Chocarse con una farola y hacerse un cuerno",
            "image": "assets/images/traits/trait_farola_cuerno.webp",
            "song_ref": "Una farola me puso cuerno (CD 1)",
            "description": "Iba tan ensimismada mirando el móvil y riéndose de tonterías que se estampó de lleno contra una farola en pleno paso de cebra. El chichón resultante fue tan monumental que parecía un cuerno de unicornio mágico."
        },
        {
            "tag": "CEGUERA SELECTIVA",
            "tag_color": "bg-torbellino-denim text-white",
            "title": "Buscar las gafas teniéndolas en la cabeza",
            "image": "assets/images/traits/trait_gafas_perdidas.webp",
            "song_ref": "He Perdido las Gafas (CD 2)",
            "description": "Media hora levantando cojines, abriendo cajones y entrando en pánico porque 'sin gafas no ve ni para freír un huevo'... mientras las gafas reposaban pacíficamente sosteniendo su característico moño alto."
        },
        {
            "tag": "ORIENTACIÓN NULA",
            "tag_color": "bg-torbellino-wine text-white",
            "title": "Perder el coche en el parking del Carrefour",
            "image": "assets/images/traits/trait_parking_carrefour.webp",
            "song_ref": "He Perdido el Coche en el Parking del Carrefour (CD 1)",
            "description": "Entrar a comprar cuatro cosas y pasar dos horas recorriendo el nivel subterráneo B-3 apretando el mando a distancia con el brazo en alto como una antena viva para ver si algún coche parpadeaba."
        },
        {
            "tag": "VIEJOVEN PREMATURA",
            "tag_color": "bg-torbellino-plum text-white",
            "title": "Lumbago fulminante a los 20 años",
            "image": "assets/images/traits/trait_lumbago_viejoven.webp",
            "song_ref": "Me Ha Dado el Lumbago (CD 1)",
            "description": "Se animó a bailar danza del vientre en el salón inspirada por un tutorial de internet y un crujido seco en la zona lumbar la dejó clavada en posición de estatua griega durante toda la tarde."
        },
        {
            "tag": "PÁNICO DOMÉSTICO",
            "tag_color": "bg-torbellino-coral text-white",
            "title": "El calamar acecha en el fregadero",
            "image": "assets/images/traits/trait_calamar_fregadero.webp",
            "song_ref": "El Calamar del Fregadero (CD 1)",
            "description": "Acumular platos sucios durante tres días hasta que el desagüe cobró vida propia y emergió una criatura con tentáculos. Lorena huyó de su propia cocina equipada con el delantal y sus Converse."
        },
        {
            "tag": "PELIGRO EN LA COCINA",
            "tag_color": "bg-torbellino-wine text-white",
            "title": "Emergencia lentejera con cacerola pegada",
            "image": "assets/images/traits/trait_emergencia_lentejera.webp",
            "song_ref": "Emergencia Lentejera (CD 1)",
            "description": "Poner la olla al fuego, irse a mirar vídeos de gatos y regresar cuando una nube de humo negro cubría el techo. Raspando el fondo quemado con una cuchara de palo descubrió un nuevo mineral."
        },
        {
            "tag": "PEREZA LEGENDARIA",
            "tag_color": "bg-torbellino-denim text-white",
            "title": "Vivir en pijama y babuchas de pompón",
            "image": "assets/images/traits/trait_babuchas_pompon.webp",
            "song_ref": "Babuchas de Pompón (CD 2)",
            "description": "Dominio supremo del arte de no levantarse: apagar interruptores con la punta del pie, deslizarse por el parquet con babuchas de algodón y considerar que cambiar de postura en el sofá cuenta como cardio."
        },
        {
            "tag": "OPTIMISTA INGENUA",
            "tag_color": "bg-torbellino-mint text-torbellino-plum",
            "title": "Aprender a nadar dentro de la bañera",
            "image": "assets/images/traits/trait_nadar_banera.webp",
            "song_ref": "He Aprendido a Nadar en la Bañera (CD 1)",
            "description": "Ponerse gafas de buceo, flotador de flamenco y llenar la bañera hasta el borde para entrenar natación sincronizada con patitos de goma antes de atreverse a ir a la piscina municipal."
        },
        {
            "tag": "CAPRICHOSA IMPULSIVA",
            "tag_color": "bg-torbellino-peach text-torbellino-plum",
            "title": "Pasión desmedida por los chicharrones",
            "image": "assets/images/traits/trait_chicharrones.webp",
            "song_ref": "Desde Que Probé Los Chicharrones (CD 1)",
            "description": "Iba a empezar una dieta détox súper estricta de brotes verdes, pero se cruzó con una carnicería de pueblo, probó un torreznito crujiente y su vida cambió para siempre entre bailes de puro éxtasis gastronómico."
        },
        {
            "tag": "MEMORIA PEZ",
            "tag_color": "bg-torbellino-sand text-torbellino-plum",
            "title": "Quedarse fuera de casa sin llaves",
            "image": "assets/images/traits/trait_llaves_perdidas.webp",
            "song_ref": "Casa con Llaves (CD 1)",
            "description": "Cerrar la puerta de un golpe seguro y darse cuenta de que las llaves se han quedado saludándola encima de la mesa del recibidor. Hora de charlar con el cerrajero de guardia."
        },
        {
            "tag": "BOTÁNICA ACCIDENTAL",
            "tag_color": "bg-torbellino-mint text-torbellino-plum",
            "title": "Declararle la guerra a los topos del jardín",
            "image": "assets/images/traits/trait_topos_huerta.webp",
            "song_ref": "Plaga de Topos (CD 1)",
            "description": "Intentar cultivar una huerta ecológica ejemplar y acabar manteniendo negociaciones diplomáticas con una familia de topos súper organizados armados con gafas de sol."
        },
        {
            "tag": "DESASTRE CULINARIO",
            "tag_color": "bg-torbellino-coral text-white",
            "title": "La catástrofe del gazpacho salpicado",
            "image": "assets/images/traits/trait_gazpacho_salpicon.webp",
            "song_ref": "Gazpacho y Tomates (CD 2)",
            "description": "Poner en marcha la batidora sin colocar bien la tapa superior. Resultado: un cuadro de arte expresionista rojo tomate cubriendo azulejos, lámparas y el flequillo de Lorena."
        }
    ]

    cards_html = ""
    for t in traits_data:
        cards_html += f'''
        <article class="bg-white rounded-[2rem] overflow-hidden border border-torbellino-sand hover:border-torbellino-coral/60 shadow-sm hover:shadow-xl transition-all duration-300 flex flex-col justify-between group">
          <div>
            <div class="relative aspect-video overflow-hidden bg-torbellino-sand/30">
              <img src="{t['image']}" alt="{t['title']}" width="640" height="360" class="w-full h-full object-cover group-hover:scale-105 transition duration-500" loading="lazy">
              <div class="absolute top-4 left-4 z-10">
                <span class="px-3.5 py-1.5 rounded-full text-[11px] font-black uppercase tracking-wider shadow-md backdrop-blur-sm {t['tag_color']}">
                  {t['tag']}
                </span>
              </div>
            </div>
            <div class="p-8 space-y-3">
              <div class="text-xs font-bold text-torbellino-denim tracking-wide">
                Gag oficial · {t['song_ref']}
              </div>
              <h3 class="text-xl font-black text-torbellino-plum group-hover:text-torbellino-coral-dark transition leading-snug">
                {t['title']}
              </h3>
              <p class="text-sm text-[#5C4550] leading-relaxed pt-1">
                {t['description']}
              </p>
            </div>
          </div>
          <div class="px-8 pb-7 pt-4 flex items-center justify-between border-t border-torbellino-sand/60 bg-gray-50/50">
            <span class="text-xs font-bold text-torbellino-wine">Perfil Canónico</span>
            <span class="text-xs font-black text-torbellino-coral-dark group-hover:translate-x-1 transition flex items-center gap-1">
              <span>👟 Lorena Torbellino</span>
            </span>
          </div>
        </article>
        '''

    page_html = f'''<!DOCTYPE html>
<html lang="es" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Quién es Lorena Torbellino — Biografía, Poses y Desastres Canónicos</title>
  <meta name="description" content="Conoce la personalidad, señas de identidad y los desastres más cómicos de Lorena Torbellino a través de las poses de sus videoclips oficiales.">
  <link rel="canonical" href="https://www.lorenatorbellino.raupulus.dev/quien-es-lorena.html">

  <!-- Open Graph / Meta Social Adaptado -->
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Lorena Torbellino">
  <meta property="og:url" content="https://www.lorenatorbellino.raupulus.dev/quien-es-lorena.html">
  <meta property="og:title" content="Quién es Lorena Torbellino — Biografía, Poses y Desastres Canónicos">
  <meta property="og:description" content="Conoce la personalidad, señas de identidad y los desastres más cómicos de Lorena Torbellino a través de las poses de sus videoclips oficiales.">
  <meta property="og:image" content="https://www.lorenatorbellino.raupulus.dev/assets/images/og_quien_es.jpg">
  <meta property="og:image:secure_url" content="https://www.lorenatorbellino.raupulus.dev/assets/images/og_quien_es.jpg">
  <meta property="og:image:type" content="image/jpeg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Quién es Lorena Torbellino — Biografía, Poses y Desastres Canónicos">
  <meta property="og:locale" content="es_ES">

  <!-- Twitter Cards -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@loretorbellino">
  <meta name="twitter:creator" content="@loretorbellino">
  <meta name="twitter:title" content="Quién es Lorena Torbellino — Biografía y Poses">
  <meta name="twitter:description" content="Conoce la personalidad, señas de identidad y los desastres más cómicos de Lorena Torbellino.">
  <meta name="twitter:image" content="https://www.lorenatorbellino.raupulus.dev/assets/images/og_quien_es.jpg">
  <meta name="twitter:image:alt" content="Quién es Lorena Torbellino — Biografía y Poses">

  <link rel="icon" type="image/png" href="assets/images/favicon.png">
  <link rel="stylesheet" href="assets/css/tailwind.css">
  <script defer src="assets/js/alpine.min.js"></script>
</head>
<body class="min-h-screen bg-torbellino-cream font-sans antialiased text-[#291C22]" x-data="{{ mobileMenuOpen: false }}">

  <!-- Skip link de accesibilidad WCAG 2.4.1 -->
  <a href="#contenido-principal" class="sr-only focus:not-sr-only focus:fixed focus:top-3 focus:left-3 focus:z-50 focus:bg-torbellino-plum focus:text-white focus:px-4 focus:py-2 focus:rounded-xl focus:font-bold focus:shadow-xl focus:ring-2 focus:ring-torbellino-coral">
    Saltar al contenido principal
  </a>

  <!-- Top Announcement Bar -->
  <aside aria-label="Aviso destacado" class="bg-gradient-to-r from-torbellino-coral via-torbellino-peach to-torbellino-coral text-torbellino-plum text-xs md:text-sm font-bold py-2.5 px-4 text-center shadow-inner flex items-center justify-center gap-2">
    <span>👟</span>
    <span>Perfil Oficial y Rasgos de Lorena Torbellino</span>
    <a href="index.html#catalogo" class="underline hover:text-torbellino-wine transition ml-1 inline-flex items-center gap-1 font-extrabold">
      ← Volver al Cancionero
    </a>
  </aside>

  <!-- Header / Navbar -->
  <header class="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-torbellino-sand shadow-sm transition">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
      
      <a href="index.html" class="flex items-center gap-3 group">
        <div class="relative w-12 h-12 rounded-full overflow-hidden border-2 border-torbellino-coral shadow-md group-hover:scale-105 transition transform duration-200">
          <img src="assets/images/lorena_avatar.webp" alt="Lorena Torbellino" width="48" height="48" class="w-full h-full object-cover">
        </div>
        <div class="flex flex-col">
          <span class="text-xl md:text-2xl font-black tracking-tight bg-gradient-to-r from-torbellino-coral to-torbellino-wine bg-clip-text text-transparent">
            Lorena Torbellino
          </span>
          <span class="text-[11px] font-bold text-torbellino-denim tracking-wider uppercase">
            Canciones y Desastres
          </span>
        </div>
      </a>

      <nav class="hidden md:flex items-center gap-8 font-bold text-sm text-[#4A3842]">
        <a href="index.html" class="hover:text-torbellino-coral transition">Inicio</a>
        <a href="index.html#discos" class="hover:text-torbellino-coral transition">Discos</a>
        <a href="index.html#catalogo" class="hover:text-torbellino-coral transition">Cancionero</a>
        <a href="quien-es-lorena.html" class="text-torbellino-coral-dark font-black border-b-2 border-torbellino-coral-dark pb-1">Quién es Lorena</a>
      </nav>

      <div class="hidden md:flex items-center gap-4">
        <a href="https://www.youtube.com/@LorenaTorbellino?sub_confirmation=1" target="_blank" rel="noopener noreferrer" 
           class="inline-flex items-center gap-2 bg-gradient-to-r from-torbellino-coral to-torbellino-red text-white font-extrabold text-sm px-6 py-2.5 rounded-full shadow-md shadow-red-500/20 hover:scale-105 transition duration-200">
          <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
          <span>Suscribirme al Canal</span>
        </a>
      </div>

      <div class="md:hidden flex items-center">
        <button @click="mobileMenuOpen = !mobileMenuOpen" 
                type="button" 
                :aria-expanded="mobileMenuOpen.toString()"
                aria-controls="mobile-menu-quien-es"
                class="p-2.5 rounded-2xl text-torbellino-plum hover:bg-torbellino-sand/50 transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-torbellino-coral" 
                aria-label="Abrir menú de navegación">
          <svg x-show="!mobileMenuOpen" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7"/></svg>
          <svg x-show="mobileMenuOpen" x-cloak class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>

    </div>

    <!-- Mobile Dropdown -->
    <div id="mobile-menu-quien-es" x-show="mobileMenuOpen" x-cloak @click.away="mobileMenuOpen = false" class="md:hidden border-b border-torbellino-sand bg-white px-5 pt-3 pb-6 space-y-3 font-bold text-sm shadow-xl">
      <a @click="mobileMenuOpen = false" href="index.html" class="block py-2 text-[#4A3842] hover:text-torbellino-coral">Inicio</a>
      <a @click="mobileMenuOpen = false" href="index.html#discos" class="block py-2 text-[#4A3842] hover:text-torbellino-coral">Discos Oficiales</a>
      <a @click="mobileMenuOpen = false" href="index.html#catalogo" class="block py-2 text-[#4A3842] hover:text-torbellino-coral">Cancionero y Filtros</a>
      <a href="quien-es-lorena.html" class="block py-2 text-torbellino-coral-dark font-black">✨ Quién es Lorena</a>
      <div class="pt-2">
        <a href="https://www.youtube.com/@LorenaTorbellino?sub_confirmation=1" target="_blank" rel="noopener noreferrer" 
           class="flex items-center justify-center gap-2 w-full bg-gradient-to-r from-torbellino-coral to-torbellino-red text-white py-3 rounded-2xl font-black shadow-md min-h-[44px]">
          <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
          <span>Suscribirme al Canal de YouTube</span>
        </a>
      </div>
    </div>
  </header>

  <!-- Contenido Principal con Landmark Semántico -->
  <main id="contenido-principal">
    
    <!-- Hero: Perfil de Lorena -->
    <section class="py-16 md:py-24 bg-white border-b border-torbellino-sand relative overflow-hidden">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-16 items-center">
          
          <div class="lg:col-span-5 flex justify-center">
            <div class="relative w-full max-w-sm">
              <div class="bg-gradient-to-tr from-torbellino-peach/40 via-white to-torbellino-lilac/30 rounded-3xl p-8 border-2 border-torbellino-sand shadow-xl">
                <img src="assets/images/lorena_sticker_guino.webp" alt="Lorena Torbellino sonriendo y saludando" width="400" height="500" fetchpriority="high" class="w-full h-auto drop-shadow-md">
              </div>
            </div>
          </div>

          <div class="lg:col-span-7 space-y-8 text-center lg:text-left">
            
            <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-torbellino-cream border border-torbellino-sand text-xs font-black text-torbellino-wine">
              <span>✨</span>
              <span>La Ficha de Personaje Oficial</span>
            </div>

            <h1 class="text-4xl sm:text-5xl lg:text-6xl font-black text-torbellino-plum tracking-tight leading-[1.15]">
              Quién es Lorena:
              <span class="block bg-gradient-to-r from-torbellino-coral to-torbellino-wine bg-clip-text text-transparent pt-1">
                Carisma, Dulzura y Desastre
              </span>
            </h1>

            <p class="text-base sm:text-lg text-[#5C4550] leading-relaxed max-w-2xl mx-auto lg:mx-0">
              Lorena Torbellino es una joven española de 20 años emancipada, alegre, descarada y con una voz dulce como la miel. Su rasgo más característico es su don sobrenatural para que las cosas más cotidianas se conviertan en una comedia de enredos de proporciones bíblicas.
            </p>

            <!-- Badges de Atributos Fijos (Espaciados y Cómodos) -->
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-2">
              <div class="bg-torbellino-cream p-5 rounded-2xl border border-torbellino-sand text-center space-y-1 shadow-sm">
                <div class="text-3xl mb-1">👟</div>
                <div class="text-sm font-black text-torbellino-plum">Converse Rojas</div>
                <div class="text-xs text-[#735A66]">Bajas y gastadas</div>
              </div>
              <div class="bg-torbellino-cream p-5 rounded-2xl border border-torbellino-sand text-center space-y-1 shadow-sm">
                <div class="text-3xl mb-1">🎀</div>
                <div class="text-sm font-black text-torbellino-plum">Pinza Negra</div>
                <div class="text-xs text-[#735A66]">Moño alto despeinado</div>
              </div>
              <div class="bg-torbellino-cream p-5 rounded-2xl border border-torbellino-sand text-center space-y-1 shadow-sm">
                <div class="text-3xl mb-1">✨</div>
                <div class="text-sm font-black text-torbellino-plum">Pecas Cálidas</div>
                <div class="text-xs text-[#735A66]">En nariz y mejillas</div>
              </div>
              <div class="bg-torbellino-cream p-5 rounded-2xl border border-torbellino-sand text-center space-y-1 shadow-sm">
                <div class="text-3xl mb-1">🎙️</div>
                <div class="text-sm font-black text-torbellino-plum">Voz Dulce</div>
                <div class="text-xs text-[#735A66]">Cero pudor cómico</div>
              </div>
            </div>

          </div>

        </div>

      </div>
    </section>

    <!-- Poses & Gags Gallery -->
    <section class="py-20 md:py-28">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        <div class="text-center max-w-3xl mx-auto mb-16 space-y-4">
          <span class="text-xs font-extrabold uppercase tracking-widest text-torbellino-coral-dark bg-torbellino-coral/10 px-4 py-1.5 rounded-full">Galería de Desventuras</span>
          <h2 class="text-3xl sm:text-4xl md:text-5xl font-black text-torbellino-plum tracking-tight">Cosas que le Han Pasado a Lorena</h2>
          <p class="text-base text-[#6E5562] max-w-2xl mx-auto leading-relaxed">
            Un recorrido visual por las poses y gags de sus videoclips oficiales que definen su personalidad arrolladora, tierna y divertida.
          </p>
        </div>

        <!-- Traits Grid con espaciado amplio -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">
          {cards_html}
        </div>

      </div>
    </section>

    <!-- Back to Music CTA -->
    <section class="py-20 bg-white border-t border-torbellino-sand text-center">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 space-y-6">
        <span class="text-5xl">🎵</span>
        <h2 class="text-3xl sm:text-4xl font-black text-torbellino-plum">
          ¡Escucha todas estas historias cantadas con ritmo!
        </h2>
        <p class="text-base text-[#6B5660] max-w-xl mx-auto leading-relaxed">
          Explora los 4 álbumes y las 110 canciones completas en el cancionero interactivo con letras y búsqueda directa.
        </p>
        <div class="pt-2 flex justify-center">
          <a href="index.html#catalogo" class="bg-gradient-to-r from-torbellino-coral to-torbellino-wine text-white font-extrabold px-9 py-4 rounded-full shadow-lg shadow-torbellino-coral/25 hover:scale-105 transition text-base min-h-[44px] inline-flex items-center">
            Ver las 110 Canciones Oficiales →
          </a>
        </div>
      </div>
    </section>

  </main>

  <!-- Footer -->
  <footer class="bg-torbellino-dark text-white pt-16 pb-12 border-t-4 border-torbellino-coral">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <div class="grid grid-cols-1 md:grid-cols-4 gap-10 pb-12 border-b border-white/10">
        <div class="md:col-span-2 space-y-4">
          <span class="text-2xl font-black tracking-tight text-white">Lorena Torbellino</span>
          <p class="text-xs text-white/70 max-w-md leading-relaxed">
            Proyecto musical de comedia absurda, pop costumbrista y sátira animada en 2D.
          </p>
          <div class="pt-2 space-y-1">
            <div class="text-xs text-white/70">
              Desarrollo y autoría web: 
              <a href="https://raupulus.dev" target="_blank" rel="noopener noreferrer" class="text-torbellino-peach font-bold hover:underline">raupulus.dev</a>
            </div>
            <div class="text-xs text-white/70">
              Contacto profesional y licencias: 
              <a href="mailto:public@raupulus.dev" class="text-torbellino-peach font-semibold hover:underline">public@raupulus.dev</a>
            </div>
          </div>
        </div>

        <div>
          <h3 class="text-xs font-bold uppercase tracking-wider text-torbellino-peach mb-4">Secciones</h3>
          <ul class="space-y-2 text-xs text-white/80">
            <li><a href="index.html#inicio" class="hover:text-torbellino-coral transition">Inicio</a></li>
            <li><a href="index.html#discos" class="hover:text-torbellino-coral transition">Catálogo de Discos</a></li>
            <li><a href="index.html#catalogo" class="hover:text-torbellino-coral transition">Cancionero Oficial</a></li>
            <li><a href="quien-es-lorena.html" class="hover:text-torbellino-coral transition">Quién es Lorena (Gags & Poses)</a></li>
          </ul>
        </div>

        <!-- Social / Redes Oficiales -->
        <div>
          <h3 class="text-xs font-bold uppercase tracking-wider text-torbellino-peach mb-4">Canal y Redes Oficiales</h3>
          <p class="text-xs text-white/70 mb-3">
            Sigue los desastres cotidianos, canciones y videoclips oficiales:
          </p>
          <div class="flex flex-col gap-2.5">
            <a href="https://www.youtube.com/@LorenaTorbellino?sub_confirmation=1" target="_blank" rel="noopener noreferrer" 
               class="inline-flex items-center gap-2.5 bg-torbellino-coral hover:bg-torbellino-red text-white text-xs font-bold px-3.5 py-2 rounded-xl transition shadow-sm w-fit" title="Canal Oficial de YouTube">
              <svg class="w-4 h-4 fill-current shrink-0" viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
              <span>YouTube: @LorenaTorbellino</span>
            </a>
            
            <div class="flex flex-wrap items-center gap-2 pt-1">
              <a href="https://www.tiktok.com/@lorenatorbellino" target="_blank" rel="noopener noreferrer" 
                 class="inline-flex items-center gap-1.5 bg-white/10 hover:bg-white/20 text-white text-xs font-semibold px-3 py-1.5 rounded-lg transition" title="TikTok @lorenatorbellino">
                <svg class="w-3.5 h-3.5 fill-current shrink-0" viewBox="0 0 24 24"><path d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-1.01-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.24 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/></svg>
                <span>TikTok</span>
              </a>
              <a href="https://www.instagram.com/lorenatorbellino/" target="_blank" rel="noopener noreferrer" 
                 class="inline-flex items-center gap-1.5 bg-white/10 hover:bg-white/20 text-white text-xs font-semibold px-3 py-1.5 rounded-lg transition" title="Instagram @lorenatorbellino">
                <svg class="w-3.5 h-3.5 fill-current shrink-0" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
                <span>Instagram</span>
              </a>
              <a href="https://x.com/loretorbellino" target="_blank" rel="noopener noreferrer" 
                 class="inline-flex items-center gap-1.5 bg-white/10 hover:bg-white/20 text-white text-xs font-semibold px-3 py-1.5 rounded-lg transition" title="X (Twitter) @loretorbellino">
                <svg class="w-3.5 h-3.5 fill-current shrink-0" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                <span>X</span>
              </a>
            </div>
          </div>
        </div>
      </div>

      <div class="pt-8 flex flex-col sm:flex-row items-center justify-between text-xs text-white/50 gap-4">
        <div>
          Web oficial por <a href="https://raupulus.dev" target="_blank" rel="noopener noreferrer" class="text-white/80 hover:text-torbellino-peach font-bold underline">raupulus.dev</a> (<a href="mailto:public@raupulus.dev" class="text-white/80 hover:text-torbellino-peach">public@raupulus.dev</a>). Música bajo propiedad privada de Lorena Torbellino.
        </div>
        <div>
          <a href="LICENSE" class="hover:text-white transition underline">Licencia AGPLv3</a>
        </div>
      </div>

    </div>
  </footer>

</body>
</html>
'''
    with open(QUIEN_ES_FILE, "w", encoding="utf-8") as f:
        f.write(page_html)
    print("quien-es-lorena.html generado con éxito.")


if __name__ == "__main__":
    build_index()
    build_quien_es()

