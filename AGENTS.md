# AGENTS.md — Reglas, Estándares e Instrucciones Oficiales: Lorena Torbellino Web

> [!IMPORTANT]
> Este documento define el contexto, estándares técnicos, directrices de diseño, accesibilidad, privacidad y directrices de desarrollo para cualquier agente de IA o desarrollador que opere en este repositorio (`www.lorenatorbellino.raupulus.dev`).

---

## 1. Contexto del Proyecto e Identidad

- **Naturaleza del Proyecto:** Sitio web oficial de **Lorena Torbellino**, proyecto musical de comedia absurda, pop costumbrista y sátira de la vida cotidiana.
- **Personaje / Intérprete:** Personaje ficticio representado mediante un **avatar 2D**.
  - **Nombre Artístico Oficial y Definitivo:** **Lorena Torbellino** (Definitivo. Prohibido usar nombres o apellidos de prueba como "Lorena Guzmán").
  - **Perfil Canónico:** Joven española de 20 años, carismática, alegre, descarada y con voz dulce e infantil, con un talento casi sobrenatural para que todo le salga al revés.
  - **Elementos Icónicos Obligatorios:** Zapatillas retro rojas bajas (tipo Converse), moño alto despeinado (*messy bun*) con pinza de garra negra (*claw clip*), aros plateados y pecas en nariz y mejillas.
- **Canal Oficial de YouTube:**
  - **Nombre:** `Lorena Torbellino`
  - **Handle Oficial:** `@LorenaTorbellino` (alternativo: `@LorenaTorbellinoOficial`)
  - **Enlace:** `https://www.youtube.com/@LorenaTorbellino`
  - **Enlace de suscripción directa:** `https://www.youtube.com/@LorenaTorbellino?sub_confirmation=1`
- **Catálogo Oficial de Discos (Actualmente 4 Álbumes y en expansión):**
  1. `Cosas de la vida real` (CD 1 - 21 Canciones)
  2. `Me pasa de todo` (CD 2 - 33 Canciones)
  3. `Que locura` (CD 3 - 32 Canciones)
  4. `Problemas de viejoven` (CD 4 - 24 Canciones)
  *(El proyecto continuará agregando nuevos discos como CD 5, etc.).*

---

## 2. PRIVACIDAD Y SEGURIDAD ESTRICTA (PERMANENTE Y UNIVERSAL)

> [!CAUTION]
> **REGLAS DE ORO DE PRIVACIDAD:**
> 1. **Correo personal estrictamente prohibido:** NUNCA utilizar bajo ningún concepto ningún correo personal o privado del creador.
> 2. **PROHIBICIÓN ESTRICTA DE EJEMPLOS LITERALES:** Jamás escribir correos personales literales en archivos de reglas, prompts, scripts, tests o documentación, ni siquiera como ejemplo de lo prohibido.
> 3. **Único correo público permitido:** El ÚNICO correo que puede utilizarse o escribirse en la web, metadatos, avisos legales, commits o documentación es: `public@raupulus.dev`.
> 4. **Consentimiento explícito:** Jamás exponer nombres reales completos, teléfonos, IPs privadas, rutas absolutas de usuario ni credenciales.

---

## 3. ARQUITECTURA TÉCNICA DE LA WEB (100% AUTÓNOMA Y ESTÁTICA)

> [!IMPORTANT]
> **POLÍTICA DE CERO ASSETS Y CDNs EXTERNOS EN TIEMPO DE EJECUCIÓN:**
> Toda la web se sirve 100% con archivos locales incluidos en el repositorio Git.
> - **PROHIBIDO:** Cargar Tailwind desde CDN, scripts desde `unpkg` / `cdnjs` o fuentes desde Google Fonts / Typekit.
> - **PROHIBIDO:** Referenciar imágenes externas sin haber sido integradas en `assets/images/` o `assets/images/covers/`.

### Estructura de Directorios del Repositorio:
```text
www.lorenatorbellino.raupulus.dev/
├── AGENTS.md                   # Este documento maestro de reglas
├── LICENSE                     # Licencia dual (AGPLv3 para código, privada para música)
├── songs.json                  # FUENTE ÚNICA DE VERDAD: Base de datos JSON de canciones en la raíz
├── tailwind.config.js          # Configuración de Tailwind CSS con paleta oficial
├── package.json                # Configuración de compilación Tailwind y scripts npm
├── package-lock.json
├── .gitignore                  # Exclusiones git (node_modules, logs, etc.)
├── scripts/
│   ├── sync_songs.py           # Sincroniza videoclips a songs.json y public/assets/images/covers/
│   ├── build_site.py           # Compila la web, exporta public/songs.json y public/assets/js/songs-data.js
│   └── generate_og_images.py   # Genera imágenes Open Graph 1200x630 (og_home.jpg y og_quien_es.jpg)
├── src/
│   └── input.css               # CSS de entrada con directivas Tailwind y @layer
├── docs/
│   ├── auditorias/             # Informes de auditoría técnica multidimensional
│   └── info/
│       └── DESIGN.md           # Sistema de diseño, paleta y componentes UI
└── public/                     # ÚNICO DIRECTORIO PUBLICABLE Y EXPUESTO A INTERNET (Apache DocumentRoot)
    ├── index.html              # Página principal compilada (ligera, consume songs-data.js)
    ├── quien-es-lorena.html    # Ficha biográfica y cómica de Lorena
    ├── robots.txt              # Reglas de bloqueo anti-scraping de IA y enlace a sitemap
    ├── sitemap.xml             # Mapa del sitio XML para indexación en buscadores
    ├── songs.json              # Copia pública estática de datos para clientes y APIs
    ├── LICENSE                 # Copia pública de términos y licencias
    └── assets/
        ├── css/
        │   └── tailwind.css    # CSS compilado local y minificado listo para producción
        ├── js/
        │   ├── alpine.min.js   # Framework reactivo local (~44KB)
        │   └── songs-data.js   # Catálogo dinámico inyectado en window.CATALOGO_SONGS
        └── images/
            ├── favicon.png     # Favicon 64x64px optimizado
            ├── favicon.webp    # Favicon WebP 64x64px
            ├── og_home.jpg     # Tarjeta para compartir en redes sociales (1200x630px)
            ├── og_quien_es.jpg # Tarjeta para compartir biografía en redes (1200x630px)
            ├── lorena_avatar.webp
            ├── lorena_banner.webp
            ├── lorena_sticker_guino.webp
            ├── albums/         # Portadas de discos 1:1 optimizadas (.webp q=85)
            ├── traits/         # Poses y gags de características de Lorena (.webp q=85)
            └── covers/         # Miniaturas 16:9 oficiales de cada canción (.webp q=85)
```

> [!CAUTION]
> **PROHIBICIÓN ESTRICTA DE MEZCLAR ASSETS DE DISTROKID EN EL REPOSITORIO WEB:**
> Los másteres de 3000×3000px y archivos de distribución para plataformas (DistroKid, Spotify, Apple Music) pertenecen estrictamente al proyecto musical del disco (`avatar/caratulas_albumes_distrokid/`).
> En este repositorio web **SOLO** se admiten imágenes en formato `.webp` (calidad 85) redimensionadas y optimizadas para su visualización web, además de los assets de fallback para redes sociales (`og_*.jpg`) y favicon (`favicon.png`).

---

## 4. PATRÓN DE INSERCIÓN, CATEGORIZACIÓN Y ACTUALIZACIÓN DE CONTENIDO

### 4.1. Taxonomía Oficial de Relatos Temáticos (Filtro de Relatos)
Cada canción debe asignarse obligatoriamente a una de las **5 categorías de relato cómico**:

| ID Relato (`relato_id`) | Nombre Visible (`relato_label`) | Icono | Temática y Palabras Clave |
| :--- | :--- | :---: | :--- |
| `viejoven` | **Crisis de Viejoven** | 🦴 | Dolores corporales prematuros a los 20, lumbago, huesos, cansancio, salud, achaques, reuma, vejez. |
| `desastres-absurdos` | **Desastres Cotidianos** | 💥 | Fregadero atascado, cocina ardiendo, comida quemada, perder el coche en el parking, estropajos, peleas con electrodomésticos, huir de la policía. |
| `citas-social` | **Citas & Vida Social** | 💬 | Citas románticas desastrosas, novios tacaños, hablar por los codos, jefes pesados en la oficina, cotilleos vecinales, amigos. |
| `vida-cotidiana` | **Vida Real & Rutina** | 🛋️ | Pereza legendaria, sofá, procrastinar, rebajas online, perder llaves, madrugar, videojuegos acumulados, día a día. |
| `campo-animales` | **Animales & Campo** | 🐾 | Animales cómicos, huerta ecológica, topos en el jardín, burrito Porroncio, ponis, ovejas-ratas, mascotas. |

### 4.2. Esquema Normalizado de Canción (`songs.json` en la Raíz)
Toda nueva canción añadida debe respetar esta estructura exacta:
```json
{
  "id": 111,
  "track_number": 1,
  "title": "Nombre Limpio de la Canción",
  "slug": "cdX-nombre-limpio-de-la-cancion",
  "album": "Nombre del Álbum",
  "album_id": "cdX",
  "album_badge": "CD X",
  "album_color": "torbellino-coral",
  "duration": "03:15",
  "duration_seconds": 195.0,
  "relato_id": "viejoven",
  "relato_label": "Crisis de Viejoven",
  "synopsis": "Gancho cómico descriptivo de 2-3 líneas sobre lo que le ocurre a Lorena.",
  "lyrics": "Letra completa de la canción (VACÍO \"\" SI NO TIENE VIDEOCLIP/SUBIDA)",
  "has_video": true,
  "has_custom_cover": true,
  "cover_image": "assets/images/covers/cdX-nombre-limpio-de-la-cancion.webp",
  "youtube_id": "",
  "youtube_url": "https://www.youtube.com/watch?v=... (O https://www.youtube.com/@LorenaTorbellino si has_video es false)"
}
```

> [!IMPORTANT]
> **REGLA DE SPOILERS Y CANCIONES NO ESTRENADAS (`has_video: false`):**
> Para las canciones que aún no tienen videoclip oficial subido a YouTube:
> 1. **CERO SPOILERS DE LETRA:** El campo `"lyrics"` en `songs.json` DEBE ser una cadena vacía `""`. El modal web muestra un aviso de próximo estreno (`⚡ Próximamente`) sin desvelar la letra.
> 2. **ENLACE A YOUTUBE:** Su `"youtube_url"` debe apuntar al perfil oficial del canal (`https://www.youtube.com/@LorenaTorbellino`), no a búsquedas ni vídeos inexistentes.
> 3. **BOTÓN DE TARJETA:** En el catálogo muestra `⚡ Próximamente` en lugar de `Ver letra y detalles`.

### 4.3. Arquitectura Dinámica y Ahorro de Tokens
- El archivo `songs.json` ubicado en la raíz del repositorio web es la **única fuente de verdad**.
- `scripts/build_site.py` extrae dinámicamente este JSON y genera:
  1. `public/assets/js/songs-data.js` (`window.CATALOGO_SONGS = [...]`).
  2. `public/songs.json` (copia estática pura).
- La plantilla `public/index.html` incluye `<script src="assets/js/songs-data.js"></script>` y Alpine.js inicializa `songs: window.CATALOGO_SONGS || []`.
- **Beneficio crítico:** `public/index.html` es ligero (~50 KB en vez de ~170 KB) y no sufre diffs masivos de 110 canciones cada vez que se actualiza una letra o enlace, ahorrando drásticamente tokens en sesiones de desarrollo con IA.

### 4.4. PROTOCOLO OBLIGATORIO AL ACTUALIZAR EL ESTADO DEL CONTENIDO
Cuando se complete un videoclip, se estrene una canción en YouTube o se agreguen nuevos temas/álbumes:
1. **Actualizar el archivo raíz `songs.json`:**
   - Cambiar `"has_video": true`.
   - Asignar la URL final en `"youtube_url"` (ej. `https://www.youtube.com/watch?v=...`).
   - Añadir la letra completa oficial en `"lyrics"` (con doble salto de línea entre estrofas).
2. **Reconstruir la web estática y exportar los datos:**
   ```bash
   python3 scripts/build_site.py
   ```
   *(Este comando actualiza automáticamente las estadísticas del Hero, el mapa `public/sitemap.xml`, genera `public/songs.json` y `public/assets/js/songs-data.js`).*
3. **Recompilar CSS si hay nuevas clases:**
   ```bash
   npm run build:css
   ```
4. **Regenerar tarjetas de redes sociales si se modifican titulares o identidad:**
   ```bash
   python3 scripts/generate_og_images.py
   ```
5. **Confirmar cambios en Git:**
   ```bash
   git add songs.json public/ && git commit -m "feat(catalog): estrenar videoclip de <Canción> y publicar letra"
   ```

---

## 5. SISTEMA DE DISEÑO Y PALETA DE COLOR OFICIAL

La paleta se define en `tailwind.config.js` bajo el espacio de nombres `torbellino-*`:

- **Primario Coral:** `torbellino-coral` (`#F87157`) — Botones CTA principales, bordes de foco, detalles destacados.
- **Melocotón Cálido:** `torbellino-peach` (`#FCD499`) — Degradados, brillos de letras y tarjetas suaves.
- **Ciruela / Mora:** `torbellino-plum` (`#3F173B`) — Títulos principales, contornos de logo y alto contraste.
- **Vino Berenjena:** `torbellino-wine` (`#78364D`) — Subtítulos, badges oscuros y sombreados.
- **Rojo Converse:** `torbellino-red` (`#DC2626`) — Zapatillas rojas icónicas de Lorena, alertas y botones de acción rápida.
- **Azul Denim Vaquero:** `torbellino-denim` (`#4A7499`) — Chaqueta vaquera, botones secundarios y etiquetas de disco.
- **Menta Pastel:** `torbellino-mint` (`#B1CAB2`) — Frescura pop, badges y contrastes suaves.
- **Lila / Lavanda:** `torbellino-lilac` (`#CAA5D9`) — Degradados de fondo y ambientación.
- **Fondo Crema:** `torbellino-cream` (`#FFF9F5`) — Fondo general de la página (cálido, suave, anti-fatiga visual).
- **Arena / Separador:** `torbellino-sand` (`#F3E2D8`) — Bordes de tarjetas y líneas divisorias.
- **Oscuro Footer:** `torbellino-dark` (`#241424`) — Pie de página y contrastes profundos.

---

## 6. ESTÁNDARES DE ACCESIBILIDAD (A11Y), W3C Y RESPONSIVE

1. **Jerarquía Semántica de Encabezados (W3C Sequentially Descending Order):**
   - Jamás saltar niveles de encabezados (`H1` ➔ `H2` ➔ `H3`).
   - `H1`: Título principal del sitio / página.
   - `H2`: Secciones principales (Discos, Cancionero Oficial, Sobre Lorena, etc.).
   - `H3`: Tarjetas individuales de álbumes, videoclips o bloques del footer.
2. **Contraste de Color WCAG AA:**
   - Mínimo 4.5:1 en texto estándar y 7:1 en textos reducidos/badges.
   - Sobre fondos claros (`#FFF9F5` o `#FFFFFF`), usar `#291C22`, `#3F173B` o `#4A3842`.
3. **Navegación por Teclado y Foco Visible:**
   - Todo botón y enlace debe ser accesible vía `Tab`.
   - Modales deben cerrarse con la tecla `Escape` (`@keydown.escape.window="modalOpen = false"`) y contar con botón de cierre claro.
4. **Textos Alternativos (`alt`) Obligatorios:**
   - Todas las imágenes `<img>` deben incluir un atributo `alt` específico y descriptivo en castellano.
   - Íconos decorativos o elementos auxiliares deben llevar `aria-hidden="true"`.
5. **Prevención de CLS y Optimización Móvil:**
   - Botones y controles táctiles con área mínima de 44x44px.
   - Carga diferida (`loading="lazy"`) en miniaturas del cancionero.
   - Tipografía adaptada para evitar zoom accidental en navegadores móviles.

---

## 7. REGLA ESTRICTA DE NOMENCLATURA Y TÍTULOS EN YOUTUBE Y MEDIOS

> [!IMPORTANT]
> **Formato Oficial de Títulos de Canciones:**
> - En YouTube:  
>   `{Título de la Canción} - Lorena Torbellino (Videoclip Oficial)`  
>   *(El título de la canción SIEMPRE va en primer lugar, seguido de `- Lorena Torbellino (Videoclip Oficial)`).*
> - En Plataformas / DSPs:  
>   `{Título de la Canción}` (estrictamente el nombre limpio de la pista, sin sufijos de artista ni número de pista).
> - **PROHIBIDO:** NUNCA colocar "Lorena Torbellino" antes del título de la pista en los vídeos de YouTube.

---

## 8. REGLAS ESTRICTAS DE PUBLICACIÓN Y SUBIDA A YOUTUBE

> [!CAUTION]
> **REGLAS PERMANENTES DE SUBIDA A YOUTUBE:**
> 1. **PROHIBICIÓN TOTAL DE SUBIDA AUTÓNOMA:**
>    - NUNCA subir vídeos de forma automática ni autónoma tras su renderizado.
>    - El usuario DEBE revisarlos previamente de forma manual en local.
>    - Solo se sube a YouTube bajo orden expresa y manual del usuario.
> 2. **POLÍTICA DE PROPIEDAD INTELECTUAL Y CERO MENCIONES A IA / HERRAMIENTAS:**
>    - La letra de todas las canciones es **propiedad intelectual exclusiva del autor/creador**.
>    - **PROHIBIDO:** No debe aparecer "IA" o "AI" por ningún sitio en metadatos, descripciones, etiquetas ni títulos (salvo el título cómico de la canción ficticia "La IA Se Ha Comido a Mi Perro").
>    - **PROHIBIDO:** Jamás hacer referencia a software o herramientas de inteligencia artificial (Suno, Midjourney, Kling, Whisper, etc.) ni de edición de vídeo.
> 3. **FORMATO OBLIGATORIO DE TÍTULO:**
>    - Siempre `{Título de la Canción} - Lorena Torbellino (Videoclip Oficial)` (longitud < 100 caracteres).
> 4. **DOBLE ASOCIACIÓN OBLIGATORIA A LISTAS DE REPRODUCCIÓN:**
>    - Al subir cualquier canción, debe añadirse de forma obligatoria a **DOS listas**:
>      1. **La lista oficial del álbum:**
>         - *Cosas de la vida real*: `PLPwZENVaGzdg`
>         - *Me pasa de todo*: `PLaL95oSelBkw`
>         - *Que locura*: Lista del disco correspondiente.
>         - *Problemas de viejoven*: Lista del disco correspondiente.
>      2. **La lista global que une todos los discos:**
>         - *Lorena Torbellino - Discografía Completa (Todos los Videoclips)*: `PLIBYuJ5Rb82M`.
> 5. **SINCRONIZACIÓN INMEDIATA DE METADATOS:**
>    - Cada vez que se sube un vídeo, se actualiza automáticamente su archivo JSON en `metadata/` (`cdX_<disco>.json`) y `historial_subidas_youtube.json`, registrando `youtube_id`, `youtube_url`, `has_video: true` y la fecha de publicación.
> 6. **DECLARACIÓN DE CONTENIDO MODIFICADO EN YOUTUBE STUDIO:**
>    - La API pública v3 de Google no expone aún el campo de contenido sintético en `videos.insert`. Por tanto, al revisar el vídeo subido (en estado privado), debe verificarse y marcarse en YouTube Studio la casilla "Contenido alterado o sintético".
> 7. **ESTADO DE PRIVACIDAD OBLIGATORIO: SIEMPRE EN PRIVADO (`private`):**
>    - **NUNCA EN OCULTO (`unlisted`) NI EN PÚBLICO.**
>    - Todas las subidas a YouTube se realizan de forma obligatoria y estricta en estado **PRIVADO (`private`)**.
>    - Queda terminantemente prohibido usar el estado "oculto" o "no listado" (`unlisted`). El creador es el único que revisa el vídeo en privado en YouTube Studio y decide cuándo y cómo publicarlo.

