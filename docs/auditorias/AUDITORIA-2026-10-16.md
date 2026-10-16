# Auditoría Integral — Lorena Torbellino Web Oficial (2026-10-16)

- **Objetivo del sitio:** Sitio web oficial y catálogo interactivo de **Lorena Torbellino** (proyecto musical de comedia absurda, pop costumbrista y sátira cotidiana animada en 2D), diseñado para explorar sus 4 álbumes (110 temas), consultar letras de canciones estrenadas, conocer la biografía/poses del personaje y canalizar tráfico y suscriptores hacia su canal oficial de YouTube (`@LorenaTorbellino`).
- **Tono y audiencia:** Comedia pop, fresca, juvenil, desenfadada y familiar (apta para todos los públicos / *all ages*).
- **Stack tecnológico:** Generador estático en Python (`scripts/sync_songs.py` + `scripts/build_site.py`), HTML5 estático autónomo en `public/`, Tailwind CSS v3.4 compilado localmente (`public/assets/css/tailwind.css`) y Alpine.js v3 local (`public/assets/js/alpine.min.js`) sin CDNs externos.
- **Nombre del repositorio:** `www.lorenatorbellino.raupulus.dev`

---

## Resumen Ejecutivo de Incidencias

| Severidad | Cantidad | Descripción |
| :--- | :---: | :--- |
| 🔴 **Crítico** | 4 | Bloqueantes: rutas locales de usuario expuestas en repositorio, referencias de imágenes sin usar `.webp` (sobrepeso de +20 MB), contraste WCAG AA insuficiente en textos coral y ausencia de remotos Git configurados. |
| 🟠 **Importante** | 6 | Degradan el SEO técnico (falta de `canonical`, `sitemap.xml`, `JSON-LD`), cumplimiento WCAG AA (tamaños táctiles < 44px, atributos ARIA de diálogo y pestañas) y archivos de trabajo pesados dentro de `public/`. |
| 🟡 **Menor** | 4 | Ajustes de pulido visual/UX: `scroll-margin-top` en anclas con header sticky, nombre de archivo con `ñ` (UTF-8 NFD/NFC), `width/height` explícitos en `<img>` y cobertura de `.gitignore`. |

---

## 🔴 Problemas Críticos (Atención Inmediata)

### [C-01] Seguridad / Privacidad — Exposición de nombre de usuario del sistema local y rutas absolutas en archivos versionados
- **Dónde:** `AGENTS.md:145`, `AGENTS.md:162` y `scripts/sync_songs.py:11`
- **Evidencia:**
  - `AGENTS.md:145`: `[public/index.html](file:///Users/<usuario_local>/git/3-Raupulus/www.lorenatorbellino.raupulus.dev/public/index.html)`
  - `AGENTS.md:162`: `[tailwind.config.js](file:///Users/<usuario_local>/git/3-Raupulus/www.lorenatorbellino.raupulus.dev/tailwind.config.js)`
  - `scripts/sync_songs.py:11`: `VIDEOCLIPS_DIR = "/Volumes/WAREHOUSE/pCloudDrive/Projects/4 - Discos/Lorena/videoclips"`
- **Impacto:** Incumple la regla crítica de privacidad y seguridad (no exponer rutas absolutas de carpetas personales ni nombres de usuario del sistema operativo en archivos versionados del repositorio público).
- **Fix propuesto:**
  1. En `AGENTS.md`, reemplazar enlaces `file:///Users/...` por rutas relativas del repositorio (`public/index.html`, `public/quien-es-lorena.html`, `tailwind.config.js`).
  2. En `scripts/sync_songs.py`, obtener la ruta de producción mediante variable de entorno `LORENA_VIDEOCLIPS_DIR` o ruta relativa parametrizable:
  ```python
  VIDEOCLIPS_DIR = os.environ.get(
      "LORENA_VIDEOCLIPS_DIR",
      os.path.abspath(os.path.join(PROJECT_DIR, "..", "Lorena", "videoclips"))
  )
  ```

### [C-02] Performance — El HTML y JSON siguen sirviendo imágenes `.jpg`/`.png` pesadas en lugar de las versiones `.webp` (calidad 85) ya generadas
- **Dónde:** `scripts/sync_songs.py:98, 109-114`, `scripts/build_site.py:60, 183, 653, 837-925, 993, 1047` y `data/songs.json`
- **Evidencia:**
  - Aunque los archivos `.webp` (calidad 85) existen en `public/assets/images/`, el generador y el JSON siguen referenciando `.jpg` y `.png`:
    - `lorena_sticker_guiño.png` pesa **1.1 MB** frente a **120 KB** en `.webp` (reducción del 89%).
    - `lorena_logo_oficial.png` pesa **944 KB** frente a **100 KB** en `.webp`.
    - Los 12 traits en `quien-es-lorena.html` (`trait_*.jpg`) suman **~9.5 MB** en JPEG frente a **~1.8 MB** en `.webp`.
    - Las 24 portadas de canciones en `data/songs.json` (`cover_image`) apuntan a `.jpg` (**~600-930 KB** c/u) en vez de `.webp` (**~80-140 KB** c/u).
- **Impacto:** Penalización severa de LCP (Largest Contentful Paint) y consumo innecesario de ancho de banda (~18 MB extra en carga de páginas), incumpliendo además el requisito explícito del usuario de servir todas las imágenes de la web en `.webp` a calidad 85.
- **Fix propuesto:**
  1. En `scripts/sync_songs.py`, exportar directamente las miniaturas a `.webp` (calidad 85, p. ej. `640x360` o `800x450`) y actualizar `cover_filename = f"{slug}.webp"` y `album_cover_map` a `*_web.webp`.
  2. En `scripts/build_site.py`, reemplazar todas las referencias `.jpg`/`.png` de `lorena_avatar`, `lorena_sticker_guiño` y `traits/trait_*` por `.webp` (excepto `og:image` si se desea mantener `.jpg`/`.webp` compatible y favicon redimensionado a `64x64`).

### [C-03] Accesibilidad (WCAG 1.4.3) — Contraste insuficiente en textos pequeños con color `text-torbellino-coral` sobre fondos claros
- **Dónde:** `public/index.html` y `public/quien-es-lorena.html` (generados desde `scripts/build_site.py:212, 247, 358, 471, 474, 537, 608, 634, 646, 1009, 1106`)
- **Evidencia:**
  - El color `torbellino-coral` (`#F87157`) sobre blanco (`#FFFFFF`) tiene un ratio de contraste de **2.80:1**, y sobre crema (`#FFF9F5`) de **2.69:1**.
  - Se utiliza en textos de `11px` y `12px` (`text-xs`), como los subtítulos de sección (`Discografía`, `Catálogo Interactivo`), el botón `"Ver letra y detalles →"`, `"Filtrar canciones →"` y enlaces de autoría del modal, donde WCAG 2.1 AA exige un mínimo de **4.5:1**.
- **Impacto:** Dificulta la lectura a usuarios con baja visión o en pantallas móviles bajo luz solar, e impide superar una auditoría automática WCAG 2.1 Nivel AA (Axe / Lighthouse).
- **Fix propuesto:**
  - Mantener `#F87157` (`bg-torbellino-coral`) para fondos decorativos, bordes o elementos grandes, y para texto pequeño sobre fondo claro emplear `text-torbellino-wine` (`#78364D`, ratio **8.63:1**) o añadir en `tailwind.config.js` la variante accesible `torbellino-coral-dark: '#C83E2B'` (ratio **5.12:1** sobre blanco y **4.92:1** sobre crema):
  ```javascript
  // tailwind.config.js
  'torbellino-coral-dark': '#C83E2B', // 5.12:1 WCAG AA para texto sobre blanco/crema
  ```

### [C-04] DevOps / Git — Ausencia de remotos Git configurados (GitLab + GitHub Mirror)
- **Dónde:** Configuración `.git/config` (`git remote -v` devuelve vacío)
- **Evidencia:** El repositorio local no tiene configurado el remoto `origin` apuntando a GitLab ni el mirror de push hacia GitHub.
- **Impacto:** Sin respaldo remoto ni flujo de despliegue sincronizado entre GitLab y GitHub.
- **Fix propuesto:**
  *(Pendiente de confirmación antes de hacer push)*:
  ```bash
  git remote add origin https://gitlab.com/raupulus/www.lorenatorbellino.raupulus.dev.git
  git remote set-url --add --push origin https://gitlab.com/raupulus/www.lorenatorbellino.raupulus.dev.git
  git remote set-url --add --push origin https://github.com/raupulus/www.lorenatorbellino.raupulus.dev.git
  ```

---

## 🟠 Problemas Importantes

### [I-01] SEO Técnico — Ausencia de `<link rel="canonical">`, `og:url`, Twitter Cards, `sitemap.xml` y Datos Estructurados (`JSON-LD`)
- **Dónde:** `scripts/build_site.py:24-39` (`index.html`), `scripts/build_site.py:967-975` (`quien-es-lorena.html`) y directorio `public/`
- **Evidencia:**
  - `index.html` carece de `<link rel="canonical" href="https://www.lorenatorbellino.raupulus.dev/">`, `<meta property="og:url">`, `<meta name="twitter:card" content="summary_large_image">` y bloque `<script type="application/ld+json">` (`MusicGroup` / `MusicAlbum`).
  - `quien-es-lorena.html` no incluye etiquetas Open Graph (`og:title`, `og:description`, `og:image`, `og:url`), Twitter Cards ni `<link rel="canonical">`.
  - `og:image` usa ruta relativa (`assets/images/lorena_banner.jpg`) en lugar de URL absoluta (`https://www.lorenatorbellino.raupulus.dev/assets/images/lorena_banner.webp`), lo que provoca fallos de previsualización en WhatsApp, Telegram, X/Twitter y Facebook.
  - No existe `public/sitemap.xml` ni referencia `Sitemap:` en `public/robots.txt`.
- **Impacto:** Indexación incompleta en buscadores, pérdida de resultados enriquecidos de grupo musical/álbumes en Google y previsualizaciones rotas al compartir enlaces en redes sociales y mensajería.
- **Fix propuesto:**
  1. Añadir en `<head>` de ambas páginas `canonical`, `og:url`, `og:image` con URL absoluta y `twitter:card`.
  2. Inyectar `JSON-LD` (`@type: "MusicGroup"`) en `index.html` con los 4 álbumes y el enlace oficial a `https://www.youtube.com/@LorenaTorbellino`.
  3. Generar `public/sitemap.xml` desde `scripts/build_site.py` y enlazarlo al final de `public/robots.txt`.

### [I-02] Seguridad / Higiene de `public/` — Archivos máster de DistroKid (3000×3000px) y copias antiguas (`*_old.jpg`) expuestos dentro del DocumentRoot
- **Dónde:** `public/assets/images/albums/` y `public/assets/images/covers/`
- **Evidencia:**
  - En `public/assets/images/albums/` se almacenan 16 archivos redundantes que no usa la web: `cd*_old.jpg` (3.1 MB c/u), `cd*_web_old.jpg`, los másteres de impresión/DistroKid `cd*.jpg` de 3000×3000px (2.1 MB c/u) y sus duplicados `.webp` de 3000×3000px, sumando **22 MB**.
  - En `public/assets/images/covers/` y `traits/` conviven los `.jpg` antiguos (**29 MB** en conjunto) junto a los nuevos `.webp`.
- **Impacto:** Incrementa innecesariamente el peso del directorio expuesto por Apache de **~6 MB** a **51 MB**, exponiendo borradores antiguos (`_old.jpg` con textos de prueba).
- **Fix propuesto:**
  - Mover los másteres 3000×3000px de DistroKid y las copias `_old.jpg` fuera de `public/` (por ejemplo a `assets_source/distrokid_masters/` y `assets_source/old_backups/` en la raíz privada del proyecto) y dejar en `public/assets/images/` exclusivamente los archivos `.webp` optimizados que consume la web en producción.

### [I-03] Accesibilidad (WCAG 2.5.5 / 2.1.1) — Áreas táctiles inferiores a 44×44px y tarjetas de álbum no navegables por teclado
- **Dónde:**
  - Tarjetas de álbumes: `scripts/build_site.py:223, 254, 285, 316` (`<div @click="filterByAlbum('cd1')" class="group cursor-pointer...">`)
  - Botones de filtro y acción: `scripts/build_site.py:386-463` (`py-1`, `py-1.5` ≈ 26-30px de alto) y `scripts/build_site.py:553` (icono YouTube `p-2` ≈ 32×32px)
- **Evidencia:**
  - Los 4 bloques de álbumes son `<div>` con `@click` sin `tabindex="0"`, `role="button"` ni manejador `@keydown.enter` / `@keydown.space`, por lo que son inaccesibles mediante navegación con `Tab`.
  - Los botones de filtro y el botón de YouTube de cada tarjeta miden entre 26px y 32px de altura, por debajo del estándar táctil recomendado de 44×44px en móviles.
- **Impacto:** Usuarios de teclado o lectores de pantalla no pueden filtrar por álbum haciendo clic en las carátulas; en pantallas táctiles aumenta la tasa de pulsaciones erróneas.
- **Fix propuesto:**
  ```html
  <!-- En las 4 tarjetas de álbum -->
  <div @click="filterByAlbum('cd1')"
       @keydown.enter.prevent="filterByAlbum('cd1')"
       @keydown.space.prevent="filterByAlbum('cd1')"
       tabindex="0"
       role="button"
       :aria-pressed="selectedAlbum === 'cd1'"
       class="... focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-torbellino-coral">
  ```
  - Aumentar el área táctil del enlace a YouTube en cada tarjeta de `p-2` a `p-3 min-w-[44px] min-h-[44px] inline-flex items-center justify-center` y subir el padding vertical de los filtros en móvil (`py-2`).

### [I-04] Accesibilidad (WCAG 4.1.2 / 2.4.1) — Falta de atributos ARIA semánticos en Modal (`role="dialog"`), menú móvil (`aria-expanded`) y ausencia de enlace "Saltar al contenido"
- **Dónde:** `scripts/build_site.py:44` (inicio de `<body>`), `scripts/build_site.py:94, 1021` (botón menú móvil) y `scripts/build_site.py:578-595` (modal de canción)
- **Evidencia:**
  - El modal carece de `role="dialog"`, `aria-modal="true"` y `aria-labelledby="modal-song-title"`.
  - El botón hamburguesa móvil no declara `:aria-expanded="mobileMenuOpen.toString()"` ni `aria-controls="mobile-menu"`.
  - En `quien-es-lorena.html` (`scripts/build_site.py:1039`), el contenido principal usa `<section>` en lugar del landmark semántico `<main id="contenido-principal">`.
  - Ninguna de las dos páginas incluye un *skip link* (`Saltar al contenido principal`) al inicio del `<body>`.
- **Impacto:** Los lectores de pantalla no anuncian la apertura del diálogo modal ni el estado desplegado del menú móvil, y falta el landmark `<main>` en la página secundaria.
- **Fix propuesto:**
  ```html
  <!-- Skip link al inicio de <body> -->
  <a href="#inicio" class="sr-only focus:not-sr-only focus:fixed focus:top-3 focus:left-3 focus:z-50 focus:bg-torbellino-plum focus:text-white focus:px-4 focus:py-2 focus:rounded-xl focus:font-bold">
    Saltar al contenido principal
  </a>
  <!-- Modal con atributos ARIA -->
  <div x-show="modalOpen" x-cloak role="dialog" aria-modal="true" aria-labelledby="modal-song-title" ...>
    ...
    <h2 id="modal-song-title" class="text-2xl font-black text-torbellino-plum" x-text="activeSong.title"></h2>
  ```

### [I-05] Accesibilidad (WCAG 1.3.1) — Salto de nivel de encabezado (`<h2>` a `<h4>`) en el Pie de Página y Modal
- **Dónde:** `scripts/build_site.py:619, 626, 634` (modal: `<h2>` pasa directamente a `<h4>`) y `scripts/build_site.py:720, 731, 1162, 1172` (footer: `<h4>` sin `<h3>` previo)
- **Evidencia:**
  - En el modal, el título de la canción es `<h2>` y las subsecciones (`Sinopsis del Gag`, `Letra Oficial`) son `<h4>`, saltándose el nivel `<h3>`.
  - En el `<footer>` de ambas páginas se usan `<h4>Secciones</h4>` y `<h4>Canal Oficial</h4>`, violando la regla de orden secuencial descendente de encabezados documentada en `AGENTS.md` (Sección 6.1).
- **Impacto:** Incumple el estándar W3C y la directriz explícita de `AGENTS.md` (`H1 -> H2 -> H3`).
- **Fix propuesto:** Cambiar dichos `<h4>` por `<h3>` tanto en el interior del modal como en las columnas del `<footer>`.

### [I-06] Responsive Mobile (`quien-es-lorena.html`) — Menú desplegable móvil sin botón CTA de suscripción
- **Dónde:** `scripts/build_site.py:1030-1035`
- **Evidencia:** En `index.html` el menú móvil incluye el botón CTA `"Suscribirme al Canal de YouTube"`, pero en `quien-es-lorena.html` el desplegable móvil se corta tras los 4 enlaces de texto sin mostrar el CTA ni cerrar el menú al pulsar enlaces con ancla.
- **Impacto:** Inconsistencia de navegación entre ambas vistas en dispositivos móviles (`XS` y `SM`) y pérdida del CTA principal en móvil dentro de la página de biografía.
- **Fix propuesto:** Igualar el bloque `<!-- Mobile Dropdown -->` de `quien-es-lorena.html` con el de `index.html`, incluyendo el botón CTA de suscripción a YouTube.

---

## 🟡 Problemas Menores y Pulido

### [M-01] UI / Navegación por Anclas — Falta de `scroll-mt-24` en secciones destino con cabecera fija (`sticky top-0 h-20`)
- **Dónde:** `scripts/build_site.py:208` (`<section id="discos">`) y `scripts/build_site.py:352` (`<section id="catalogo">`)
- **Evidencia:** Al pulsar en `"Discos"` o `"Cancionero"` en el navbar o filtrar un álbum, el navegador hace scroll hasta el borde superior de la sección, quedando los primeros `80px` (`h-20` del `<header class="sticky top-0">`) parcialmente solapados sobre el inicio de la sección.
- **Fix propuesto:** Añadir la clase `scroll-mt-20` en `<section id="discos" class="scroll-mt-20 ...">` y `<section id="catalogo" class="scroll-mt-20 ...">`.

### [M-02] Compatibilidad / Servidores Web — Nombre de archivo con carácter no ASCII (`ñ`) en `lorena_sticker_guiño.webp`
- **Dónde:** `public/assets/images/lorena_sticker_guiño.webp` y `scripts/build_site.py:183, 1047`
- **Evidencia:** En sistemas macOS (APFS usa normalización Unicode NFD) frente a servidores Linux Apache (NFC), el carácter `ñ` en nombres de archivo estáticos suele causar errores `404 Not Found` al desplegar por Git o rsync entre distintos sistemas de archivos.
- **Fix propuesto:** Renombrar a `public/assets/images/lorena_sticker_guino.webp` (ASCII limpio en kebab/snake-case) y actualizar las 2 referencias en `scripts/build_site.py`.

### [M-03] Performance / CLS — Falta de atributos explícitos `width`, `height` y `fetchpriority="high"` en imágenes principales y favicon sobredimensionado
- **Dónde:** `scripts/build_site.py:36, 60, 183, 234, 264, 294, 324, 489, 937`
- **Evidencia:**
  - El favicon (`<link rel="icon" href="assets/images/lorena_logo_oficial.png">`) carga una imagen de `1024x1024px` (**944 KB**) en cada pestaña del navegador.
  - La imagen principal del Hero (`lorena_sticker_guiño`) no tiene `fetchpriority="high"` ni dimensiones `width`/`height` explícitas.
- **Fix propuesto:** Generar un `public/assets/images/favicon.webp` (o `.png` de `64x64px`, < 8 KB) y añadir `width`, `height` y `fetchpriority="high"` en la imagen del Hero.

### [M-04] Higiene de Repositorio — `.gitignore` minimalista
- **Dónde:** `.gitignore:1-4`
- **Evidencia:** Solo ignora `node_modules/`, `.DS_Store` y `*.log`. No excluye `__pycache__/`, `.venv/`, `.idea/`, `.vscode/`, `Thumbs.db` ni archivos temporales `.env*`.
- **Fix propuesto:** Ampliar `.gitignore` con las exclusiones estándar de Python, Node y editores.

---

## 📋 Plan de Acción Priorizado (Impacto vs. Esfuerzo)

| Orden | ID | Acción concreta | Archivo(s) | Impacto | Esfuerzo (S/M/L) |
| :---: | :---: | :--- | :--- | :---: | :---: |
| 1 | **C-01** | Eliminar rutas absolutas locales (`/Users/...` y `/Volumes/...`) usando enlaces relativos y variables de entorno. | `AGENTS.md`, `scripts/sync_songs.py` | Alto | S |
| 2 | **C-02** | Actualizar `sync_songs.py` y `build_site.py` para usar exclusivamente imágenes `.webp` (q=85) en toda la web y regenerar `songs.json`. | `scripts/sync_songs.py`, `scripts/build_site.py`, `data/songs.json` | Alto | S |
| 3 | **I-02** | Sacar de `public/` los másteres 3000×3000 de DistroKid, los `_old.jpg` y los `.jpg`/`.png` duplicados a una carpeta privada `assets_source/`. | `public/assets/images/`, `assets_source/` | Alto | S |
| 4 | **C-03** | Corregir contraste WCAG AA de textos pequeños coral usando `torbellino-coral-dark` (`#C83E2B`, > 4.5:1) o `torbellino-wine`. | `tailwind.config.js`, `scripts/build_site.py` | Alto | S |
| 5 | **I-01** | Añadir `canonical`, Open Graph completo con URLs absolutas, Twitter Cards, `JSON-LD` (`MusicGroup`) y generar `public/sitemap.xml`. | `scripts/build_site.py`, `public/robots.txt`, `public/sitemap.xml` | Alto | M |
| 6 | **I-03 / I-04 / I-05** | Añadir navegación por teclado en álbumes (`tabindex`, `role="button"`), `role="dialog"` en modal, *skip link*, landmark `<main>`, áreas táctiles de 44px y corregir `<h4>` a `<h3>`. | `scripts/build_site.py` | Medio | M |
| 7 | **I-06 / M-01 / M-02 / M-03 / M-04** | Igualar menú móvil en `quien-es-lorena.html`, añadir `scroll-mt-20`, renombrar `lorena_sticker_guino.webp` sin `ñ`, crear favicon 64×64px y completar `.gitignore`. | `scripts/build_site.py`, `.gitignore`, `public/assets/images/` | Medio | S |
| 8 | **C-04** | Configurar remotos Git (`origin` hacia GitLab y mirror hacia GitHub). | `.git/config` | Medio | S |
