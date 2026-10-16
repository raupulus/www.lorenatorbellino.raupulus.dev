#!/usr/bin/env python3
import os
import json
import re
import html

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
DATA_FILE = os.path.join(PROJECT_DIR, "data", "songs.json")
INDEX_FILE = os.path.join(PROJECT_DIR, "index.html")

def build():
    if not os.path.exists(DATA_FILE):
        print(f"Error: No existe {DATA_FILE}")
        return

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        songs = json.load(f)

    # Serializar songs a JSON seguro para incrustar en Alpine.js
    songs_json_escaped = json.dumps(songs, ensure_ascii=False)

    # Estadísticas para el resumen del Hero
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
  
  <!-- Open Graph / Meta Social -->
  <meta property="og:type" content="website">
  <meta property="og:title" content="Lorena Torbellino — Web Oficial">
  <meta property="og:description" content="20 años, voz dulce, zapatillas Converse rojas y un talento sobrenatural para que todo en la vida salga al revés.">
  <meta property="og:image" content="assets/images/lorena_banner.jpg">
  
  <link rel="icon" type="image/png" href="assets/images/lorena_logo_oficial.png">
  <link rel="stylesheet" href="assets/css/tailwind.css">
  <script defer src="assets/js/alpine.min.js"></script>
</head>
<body class="min-h-screen bg-torbellino-cream font-sans antialiased text-[#291C22]" 
      x-data="musicApp()" 
      x-init="init()">

  <!-- Top Announcement Bar -->
  <aside aria-label="Aviso destacado" class="bg-gradient-to-r from-torbellino-coral via-torbellino-peach to-torbellino-coral text-torbellino-plum text-xs md:text-sm font-bold py-2 px-4 text-center shadow-inner flex items-center justify-center gap-2">
    <span>👟</span>
    <span>¡Canal oficial activo! 110 canciones catalogadas y videoclips semanales en YouTube</span>
    <a href="https://www.youtube.com/@LorenaTorbellino?sub_confirmation=1" target="_blank" rel="noopener noreferrer" class="underline hover:text-torbellino-wine transition ml-1 inline-flex items-center gap-1">
      Suscribirse gratis →
    </a>
  </aside>

  <!-- Header / Navbar -->
  <header class="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-torbellino-sand shadow-sm transition">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
      
      <!-- Brand Logo -->
      <a href="#inicio" class="flex items-center gap-3 group">
        <div class="relative w-12 h-12 rounded-full overflow-hidden border-2 border-torbellino-coral shadow-md group-hover:scale-105 transition transform duration-200">
          <img src="assets/images/lorena_avatar.jpg" alt="Lorena Torbellino" class="w-full h-full object-cover">
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
        <a href="#sobre-mi" class="hover:text-torbellino-coral transition">Quién es Lorena</a>
        <a href="#contacto" class="hover:text-torbellino-coral transition">Contacto</a>
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
        <button @click="mobileMenuOpen = !mobileMenuOpen" type="button" class="p-2.5 rounded-2xl text-torbellino-plum hover:bg-torbellino-sand/50 transition" aria-label="Abrir menú">
          <svg x-show="!mobileMenuOpen" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7"/></svg>
          <svg x-show="mobileMenuOpen" x-cloak class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>

    </div>

    <!-- Mobile Dropdown -->
    <div x-show="mobileMenuOpen" x-cloak @click.away="mobileMenuOpen = false" class="md:hidden border-b border-torbellino-sand bg-white px-5 pt-3 pb-6 space-y-3 font-bold text-sm shadow-xl">
      <a @click="mobileMenuOpen = false" href="#inicio" class="block py-2 text-[#4A3842] hover:text-torbellino-coral">Inicio</a>
      <a @click="mobileMenuOpen = false" href="#discos" class="block py-2 text-[#4A3842] hover:text-torbellino-coral">Discos Oficiales</a>
      <a @click="mobileMenuOpen = false" href="#catalogo" class="block py-2 text-[#4A3842] hover:text-torbellino-coral">Cancionero y Filtros</a>
      <a @click="mobileMenuOpen = false" href="#sobre-mi" class="block py-2 text-[#4A3842] hover:text-torbellino-coral">Quién es Lorena</a>
      <a @click="mobileMenuOpen = false" href="#contacto" class="block py-2 text-[#4A3842] hover:text-torbellino-coral">Contacto</a>
      <div class="pt-2">
        <a href="https://www.youtube.com/@LorenaTorbellino?sub_confirmation=1" target="_blank" rel="noopener noreferrer" 
           class="flex items-center justify-center gap-2 w-full bg-gradient-to-r from-torbellino-coral to-torbellino-red text-white py-3 rounded-2xl font-black shadow-md">
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
            <a href="#catalogo" class="bg-gradient-to-r from-torbellino-coral to-torbellino-wine text-white font-extrabold px-8 py-3.5 rounded-full shadow-lg shadow-torbellino-coral/30 hover:scale-105 hover:shadow-xl transition duration-200 flex items-center gap-2">
              <span>Explorar el Cancionero ({total_canciones} Temas)</span>
              <span>↓</span>
            </a>
            <a href="https://www.youtube.com/@LorenaTorbellino?sub_confirmation=1" target="_blank" rel="noopener noreferrer" 
               class="bg-white hover:bg-torbellino-sand/40 text-torbellino-plum border-2 border-torbellino-sand font-black px-7 py-3 rounded-full hover:border-torbellino-coral/50 transition duration-200 flex items-center gap-2 shadow-sm">
              <svg class="w-4 h-4 text-red-600 fill-current" viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
              <span>Canal Oficial de YouTube</span>
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
                <img src="assets/images/lorena_sticker_guiño.png" alt="Lorena Torbellino haciendo el signo de la victoria" class="w-full h-full object-contain filter drop-shadow-md">
                
                <div class="absolute bottom-4 left-4 right-4 bg-white/95 backdrop-blur-sm rounded-2xl p-3 shadow-lg border border-torbellino-sand flex items-center justify-between">
                  <div class="flex items-center gap-2.5">
                    <span class="text-2xl">✨</span>
                    <div>
                      <div class="text-xs font-black text-torbellino-plum">Lorena Torbellino</div>
                      <div class="text-[11px] font-semibold text-torbellino-wine">Voz dulce · Zapatillas Converse rojas</div>
                    </div>
                  </div>
                  <span class="px-2.5 py-1 rounded-full text-[11px] font-black bg-torbellino-coral/15 text-torbellino-coral">
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
  <section id="discos" class="py-16 md:py-20 bg-white border-y border-torbellino-sand">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <div class="text-center max-w-2xl mx-auto mb-12 space-y-2">
        <h2 class="text-xs font-extrabold uppercase tracking-widest text-torbellino-coral">Discografía</h2>
        <p class="text-3xl sm:text-4xl font-black text-torbellino-plum">Los 4 Álbumes Oficiales</p>
        <p class="text-sm text-[#6E5562]">
          Haz clic en cualquier disco para filtrar el cancionero completo al instante.
        </p>
      </div>

      <!-- Albums Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        
        <!-- Disco 1 -->
        <div @click="filterByAlbum('cd1')" 
             :class="selectedAlbum === 'cd1' ? 'ring-4 ring-torbellino-coral border-torbellino-coral shadow-xl' : 'hover:border-torbellino-coral/50 shadow-sm hover:shadow-lg'"
             class="group cursor-pointer bg-torbellino-cream rounded-3xl p-6 border-2 border-torbellino-sand transition-all duration-200 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-4">
              <span class="px-3 py-1 rounded-full text-xs font-black bg-torbellino-coral text-white">CD 1</span>
              <span class="text-xs font-bold text-torbellino-wine">21 Temas</span>
            </div>
            <div class="aspect-square rounded-2xl bg-gradient-to-br from-[#FFE3DC] to-[#FCD499]/60 flex items-center justify-center p-4 mb-4 border border-torbellino-sand group-hover:scale-105 transition duration-200">
              <span class="text-5xl">☕</span>
            </div>
            <h3 class="text-lg font-black text-torbellino-plum mb-1.5 group-hover:text-torbellino-coral transition">
              Cosas de la vida real
            </h3>
            <p class="text-xs text-[#6B5660] leading-relaxed">
              La odisea de madurar, buscar aparcamiento en el Carrefour, perder llaves y las peleas cotidianas.
            </p>
          </div>
          <div class="mt-5 pt-3 border-t border-torbellino-sand flex items-center justify-between text-xs font-black text-torbellino-coral">
            <span>Filtrar canciones</span>
            <span class="group-hover:translate-x-1 transition">→</span>
          </div>
        </div>

        <!-- Disco 2 -->
        <div @click="filterByAlbum('cd2')" 
             :class="selectedAlbum === 'cd2' ? 'ring-4 ring-torbellino-denim border-torbellino-denim shadow-xl' : 'hover:border-torbellino-denim/50 shadow-sm hover:shadow-lg'"
             class="group cursor-pointer bg-torbellino-cream rounded-3xl p-6 border-2 border-torbellino-sand transition-all duration-200 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-4">
              <span class="px-3 py-1 rounded-full text-xs font-black bg-torbellino-denim text-white">CD 2</span>
              <span class="text-xs font-bold text-torbellino-wine">33 Temas</span>
            </div>
            <div class="aspect-square rounded-2xl bg-gradient-to-br from-[#D9E6F2] to-[#B1CAB2]/60 flex items-center justify-center p-4 mb-4 border border-torbellino-sand group-hover:scale-105 transition duration-200">
              <span class="text-5xl">⚡</span>
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
             :class="selectedAlbum === 'cd3' ? 'ring-4 ring-torbellino-wine border-torbellino-wine shadow-xl' : 'hover:border-torbellino-wine/50 shadow-sm hover:shadow-lg'"
             class="group cursor-pointer bg-torbellino-cream rounded-3xl p-6 border-2 border-torbellino-sand transition-all duration-200 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-4">
              <span class="px-3 py-1 rounded-full text-xs font-black bg-torbellino-wine text-white">CD 3</span>
              <span class="text-xs font-bold text-torbellino-wine">32 Temas</span>
            </div>
            <div class="aspect-square rounded-2xl bg-gradient-to-br from-[#F5D8E6] to-[#CAA5D9]/60 flex items-center justify-center p-4 mb-4 border border-torbellino-sand group-hover:scale-105 transition duration-200">
              <span class="text-5xl">🌪️</span>
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
             :class="selectedAlbum === 'cd4' ? 'ring-4 ring-torbellino-plum border-torbellino-plum shadow-xl' : 'hover:border-torbellino-plum/50 shadow-sm hover:shadow-lg'"
             class="group cursor-pointer bg-torbellino-cream rounded-3xl p-6 border-2 border-torbellino-sand transition-all duration-200 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-4">
              <span class="px-3 py-1 rounded-full text-xs font-black bg-torbellino-plum text-white">CD 4</span>
              <span class="text-xs font-bold text-torbellino-wine">24 Temas</span>
            </div>
            <div class="aspect-square rounded-2xl bg-gradient-to-br from-[#FDE3CF] to-[#F87157]/40 flex items-center justify-center p-4 mb-4 border border-torbellino-sand group-hover:scale-105 transition duration-200">
              <span class="text-5xl">🦴</span>
            </div>
            <h3 class="text-lg font-black text-torbellino-plum mb-1.5 group-hover:text-torbellino-coral transition">
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
  <section id="catalogo" class="py-16 md:py-24">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <!-- Catalog Header -->
      <div class="flex flex-col lg:flex-row lg:items-end justify-between mb-8 gap-6">
        <div>
          <span class="text-xs font-extrabold uppercase tracking-widest text-torbellino-coral">Catálogo Interactivo</span>
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
          Mostrando <span class="text-torbellino-coral font-black" x-text="filteredSongs.length"></span> de <span x-text="songs.length"></span> canciones
        </div>
        <div x-show="searchQuery || selectedAlbum !== 'todos' || selectedRelato !== 'todos' || onlyWithVideo">
          <button @click="resetFilters()" class="text-torbellino-coral hover:underline">
            ✕ Limpiar filtros
          </button>
        </div>
      </div>

      <!-- Songs Cards Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        
        <template x-for="song in filteredSongs" :key="song.id">
          <article class="bg-white rounded-3xl overflow-hidden border-2 border-torbellino-sand hover:border-torbellino-coral/60 shadow-sm hover:shadow-xl transition-all duration-300 flex flex-col justify-between group">
            
            <div>
              <!-- Thumbnail Banner -->
              <div class="relative aspect-video bg-gradient-to-tr from-torbellino-peach/30 to-torbellino-sand overflow-hidden">
                <img :src="song.cover_image" :alt="song.title" class="w-full h-full object-cover group-hover:scale-105 transition duration-300" loading="lazy">
                
                <!-- Badge CD -->
                <div class="absolute top-3 left-3 flex items-center gap-2">
                  <span class="px-2.5 py-0.5 rounded-full text-[11px] font-black text-white shadow-sm"
                        :class="song.album_id === 'cd1' ? 'bg-torbellino-coral' : (song.album_id === 'cd2' ? 'bg-torbellino-denim' : (song.album_id === 'cd3' ? 'bg-torbellino-wine' : 'bg-torbellino-plum'))"
                        x-text="song.album_badge">
                  </span>
                  <span class="px-2.5 py-0.5 rounded-full text-[10px] font-extrabold bg-white/95 text-torbellino-plum shadow-sm backdrop-blur-sm"
                        x-text="song.relato_label">
                  </span>
                </div>

                <!-- Duration Badge -->
                <div class="absolute bottom-3 right-3 bg-black/75 backdrop-blur-sm text-white text-[11px] font-mono font-bold px-2 py-0.5 rounded-md"
                     x-text="song.duration">
                </div>

                <!-- Video Ready Indicator -->
                <template x-if="song.has_video">
                  <div class="absolute top-3 right-3 bg-red-600 text-white text-[10px] font-black px-2 py-0.5 rounded-full flex items-center gap-1 shadow-md">
                    <span>▶ Videoclip</span>
                  </div>
                </template>
              </div>

              <!-- Content Body -->
              <div class="p-6">
                <div class="text-[11px] font-bold text-torbellino-denim mb-1" x-text="'Pista ' + song.track_number + ' · ' + song.album"></div>
                <h3 class="text-lg font-black text-torbellino-plum group-hover:text-torbellino-coral transition leading-snug" x-text="song.title"></h3>
                <p class="text-xs text-[#6B5660] mt-2 line-clamp-3 leading-relaxed" x-text="song.synopsis"></p>
              </div>
            </div>

            <!-- Footer Card Action -->
            <div class="px-6 pb-6 pt-2 flex items-center justify-between border-t border-torbellino-sand/60">
              <button @click="openModal(song)" 
                      class="text-xs font-black text-torbellino-coral hover:text-torbellino-wine transition flex items-center gap-1">
                <span>Ver letra y detalles</span>
                <span>→</span>
              </button>

              <a :href="song.youtube_url" target="_blank" rel="noopener noreferrer" 
                 class="p-2 rounded-xl bg-torbellino-cream hover:bg-torbellino-sand text-torbellino-plum transition" 
                 title="Ver en YouTube">
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
        <button @click="resetFilters()" class="mt-4 px-5 py-2 rounded-full bg-torbellino-coral text-white font-bold text-xs">
          Ver todo el cancionero
        </button>
      </div>

    </div>
  </section>

  <!-- Interactive Song Modal (Letra, Datos, YouTube) -->
  <div x-show="modalOpen" x-cloak 
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
          <h2 class="text-2xl font-black text-torbellino-plum" x-text="activeSong.title"></h2>
        </div>

        <button @click="modalOpen = false" class="p-2 rounded-full hover:bg-torbellino-sand text-torbellino-plum transition" aria-label="Cerrar modal">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>

      <!-- Modal Body -->
      <div class="p-6 overflow-y-auto space-y-6">
        
        <!-- Video or Thumbnail -->
        <div class="rounded-2xl overflow-hidden aspect-video bg-black relative border border-torbellino-sand">
          <img :src="activeSong.cover_image" :alt="activeSong.title" class="w-full h-full object-cover">
          <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent flex items-end p-4">
            <a :href="activeSong.youtube_url" target="_blank" rel="noopener noreferrer" 
               class="inline-flex items-center gap-2 bg-gradient-to-r from-red-600 to-red-700 text-white text-xs font-black px-4 py-2 rounded-full shadow-lg hover:scale-105 transition">
              <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
              <span>Ver videoclip en YouTube</span>
            </a>
          </div>
        </div>

        <!-- Sinopsis -->
        <div>
          <h4 class="text-xs font-black text-torbellino-coral uppercase tracking-wider mb-1.5">Sinopsis del Gag</h4>
          <p class="text-xs sm:text-sm text-[#4A3842] leading-relaxed bg-torbellino-cream p-4 rounded-2xl border border-torbellino-sand" x-text="activeSong.synopsis"></p>
        </div>

        <!-- Lyrics Section -->
        <div>
          <h4 class="text-xs font-black text-torbellino-plum uppercase tracking-wider mb-2">Letra Oficial</h4>
          <div class="bg-gray-50 rounded-2xl p-5 border border-torbellino-sand text-xs sm:text-sm font-normal text-[#291C22] whitespace-pre-line leading-relaxed max-h-60 overflow-y-auto" x-text="activeSong.lyrics || 'Letra en proceso de publicación oficial.'"></div>
        </div>

      </div>

      <!-- Modal Footer -->
      <div class="p-4 bg-torbellino-cream border-t border-torbellino-sand flex items-center justify-between">
        <span class="text-[11px] font-bold text-[#735A66]">Lorena Torbellino · ℗ & © 2026</span>
        <button @click="modalOpen = false" class="px-5 py-2 rounded-full bg-white border border-torbellino-sand text-xs font-black text-torbellino-plum hover:bg-torbellino-sand transition">
          Cerrar
        </button>
      </div>

    </div>

  </div>

  <!-- About Lorena Section -->
  <section id="sobre-mi" class="py-16 md:py-24 bg-white border-t border-torbellino-sand">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="bg-gradient-to-br from-torbellino-cream via-white to-torbellino-peach/20 rounded-3xl border-2 border-torbellino-sand p-8 md:p-14 shadow-lg">
        
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-10 items-center">
          
          <div class="lg:col-span-4 flex justify-center">
            <div class="relative w-56 h-56 rounded-full overflow-hidden border-4 border-torbellino-coral shadow-xl">
              <img src="assets/images/lorena_avatar.jpg" alt="Foto de perfil de Lorena Torbellino" class="w-full h-full object-cover">
            </div>
          </div>

          <div class="lg:col-span-8 space-y-4 text-center lg:text-left">
            <span class="text-xs font-extrabold uppercase tracking-widest text-torbellino-coral">Ficha de Identidad</span>
            <h2 class="text-3xl sm:text-4xl font-black text-torbellino-plum">
              ¿Quién es Lorena Torbellino?
            </h2>
            <p class="text-sm sm:text-base text-[#5C4550] leading-relaxed">
              Lorena es una joven española de 20 años, carismática, alegre y con un toque descarado. Con su dulce voz casi infantil y sus inseparables zapatillas Converse rojas bajas, pone melodía a las pequeñas tragedias absurdas del día a día: la pereza legendaria, las compras compulsivas, las comidas quemadas y las crisis existenciales de viejoven.
            </p>
            <div class="pt-2 flex flex-wrap justify-center lg:justify-start gap-2">
              <span class="px-3.5 py-1.5 rounded-full text-xs font-bold bg-white border border-torbellino-sand text-torbellino-plum shadow-sm">
                👟 Converse Rojas Bajas
              </span>
              <span class="px-3.5 py-1.5 rounded-full text-xs font-bold bg-white border border-torbellino-sand text-torbellino-plum shadow-sm">
                🎀 Moño Alto con Pinza Negra
              </span>
              <span class="px-3.5 py-1.5 rounded-full text-xs font-bold bg-white border border-torbellino-sand text-torbellino-plum shadow-sm">
                ✨ Pecas en Nariz y Mejillas
              </span>
              <span class="px-3.5 py-1.5 rounded-full text-xs font-bold bg-white border border-torbellino-sand text-torbellino-plum shadow-sm">
                🎵 Voz Dulce e Infantil
              </span>
            </div>
          </div>

        </div>

      </div>
    </div>
  </section>

  <!-- Footer -->
  <footer id="contacto" class="bg-torbellino-dark text-white pt-16 pb-12 border-t-4 border-torbellino-coral">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <div class="grid grid-cols-1 md:grid-cols-4 gap-10 pb-12 border-b border-white/10">
        
        <!-- Brand Info -->
        <div class="md:col-span-2 space-y-4">
          <div class="flex items-center gap-3">
            <span class="text-2xl font-black tracking-tight text-white">Lorena Torbellino</span>
          </div>
          <p class="text-xs text-white/70 max-w-md leading-relaxed">
            Proyecto musical de comedia y sátira animada en 2D. Todas las situaciones y personajes son creaciones humorísticas de ficción para alegrar la rutina cotidiana.
          </p>
          <div class="pt-2">
            <span class="text-xs text-white/50">Contacto profesional y licencias:</span>
            <div class="text-sm font-semibold text-torbellino-peach">public@raupulus.dev</div>
          </div>
        </div>

        <!-- Links -->
        <div>
          <h4 class="text-xs font-bold uppercase tracking-wider text-torbellino-peach mb-4">Secciones</h4>
          <ul class="space-y-2 text-xs text-white/80">
            <li><a href="#inicio" class="hover:text-torbellino-coral transition">Inicio</a></li>
            <li><a href="#discos" class="hover:text-torbellino-coral transition">Catálogo de Discos</a></li>
            <li><a href="#catalogo" class="hover:text-torbellino-coral transition">Cancionero ({total_canciones})</a></li>
            <li><a href="#sobre-mi" class="hover:text-torbellino-coral transition">Sobre Lorena</a></li>
          </ul>
        </div>

        <!-- Social / YouTube -->
        <div>
          <h4 class="text-xs font-bold uppercase tracking-wider text-torbellino-peach mb-4">Canal Oficial</h4>
          <p class="text-xs text-white/70 mb-4">
            Disfruta de las animaciones oficiales y canciones completas en YouTube:
          </p>
          <a href="https://www.youtube.com/@LorenaTorbellino?sub_confirmation=1" target="_blank" rel="noopener noreferrer" 
             class="inline-flex items-center gap-2 bg-torbellino-coral hover:bg-torbellino-red text-white text-xs font-black px-4 py-2.5 rounded-full transition shadow-md">
            <svg class="w-3.5 h-3.5 fill-current" viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
            <span>@LorenaTorbellino</span>
          </a>
        </div>

      </div>

      <!-- Copyright -->
      <div class="pt-8 flex flex-col sm:flex-row items-center justify-between text-xs text-white/50 gap-4">
        <div>
          ℗ & © 2026 Lorena Torbellino. Todos los derechos reservados.
        </div>
        <div>
          Desplegado 100% estático sin recursos externos.
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
        songs: {songs_json_escaped},

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

    print(f"index.html compilado con éxito ({len(songs)} canciones incrustadas).")

if __name__ == "__main__":
    build()
