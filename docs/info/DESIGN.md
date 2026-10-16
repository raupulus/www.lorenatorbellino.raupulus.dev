# DESIGN.md — Sistema de Diseño e Identidad Visual

Sitio web oficial: **Lorena Torbellino** (`www.lorenatorbellino.raupulus.dev`)  
Canal oficial: `@LorenaTorbellino`  
Contacto oficial: `public@raupulus.dev`

---

## 1. Filosofía y Personalidad de Marca

Lorena Torbellino es un proyecto musical de comedia absurda, pop costumbrista y sátira de la vida cotidiana moderna protagonizado por un avatar 2D: una joven española de 20 años, carismática, alegre, descarada y con voz dulce e infantil, con un talento casi sobrenatural para que todo le salga al revés.

El diseño web debe transmitir:
- **Frescura y vitalidad pop:** Colores alegres, cálidos y vibrantes pero armoniosos (no estridentes ni infantiles de párvulos).
- **Estética Cómic / Y2K Moderno:** Bordes redondeados generosos (`rounded-2xl`, `rounded-3xl`), sombreados suaves y definidos con volumen, tarjetas tipo sticker o viñeta de cómic.
- **Claridad e inmediatez:** Estructura limpia, intuitiva y responsive, adaptada tanto a smartphones como a monitores ultra-panorámicos.
- **Autonomía 100% estática:** Cero dependencias externas en tiempo de ejecución (CDN externos prohibidos). Todo el CSS y JS corre en local.

---

## 2. Paleta de Colores Oficial (Extraída del Logotipo y Assets Oficiales)

La paleta se extrae directamente de las letras del logotipo tridimensional de **Lorena Torbellino** (en el banner oficial y marca de agua troquelada), complementada con los tonos cálidos de su piel, pecas, cabello castaño caramelo y sus inseparables zapatillas Converse rojas:

### 2.1. Colores Principales (Brand Primary & Accents)

| Nombre del Color | Hex | Muestra / Uso en Diseño |
| :--- | :--- | :--- |
| **Coral Torbellino (Primario)** | `#F87157` | Botones de acción principal (CTA), bordes de foco, acentos de títulos |
| **Melocotón Cálido (Primario Light)** | `#FCD499` | Degradados de cabecera, brillos de logotipo, badges de alerta cómicos |
| **Ciruela / Mora Profundo (Contraste Primario)** | `#3F173B` | Contorno de letras del logo, texto sobre fondos pastel, badges oscuros |
| **Vino Berenjena (Acento Sombras)** | `#78364D` | Sombras proyectadas, bordes de viñetas, pie de página |
| **Rojo Converse (Firma Lorena)** | `#DC2626` | Iconos de corazón, etiquetas de atención, zapatillas icónicas |
| **Azul Denim Vaquero (Chaqueta)** | `#4A7499` | Secciones secundarias, etiquetas de disco, botones alternativos |
| **Menta Pastel (Letras Logo)** | `#B1CAB2` | Badges de estado, fondos de tarjetas alternadas, frescura pop |
| **Lila / Lavanda Dulce (Degradado Banner)** | `#CAA5D9` | Fondos de degradados ambientales, brillos decorativos |

### 2.2. Neutros y Fondos

| Nombre | Hex | Propósito |
| :--- | :--- | :--- |
| **Fondo Base Claro** | `#FFF9F5` | Fondo principal de la web (blanco cálido crema / vainilla suave) |
| **Superficie Tarjetas** | `#FFFFFF` | Fondos de módulos y tarjetas con sombra suave cálida |
| **Borde / Separadores** | `#F3E2D8` | Líneas divisorias sutiles y bordes de tarjetas |
| **Texto Principal** | `#291C22` | Tipografía para títulos y lecturas principales (alto contraste sin ser negro puro) |
| **Texto Secundario** | `#6B5660` | Metadatos, subtítulos y descripciones |
| **Superficie Oscura (Header / Footer)** | `#241424` | Modo oscuro en footer o barra superior con degradado cálido |

---

## 3. Escala Tipográfica y Jerarquía

La tipografía debe sentirse cercana, moderna y legible con buena dosis de personalidad:
- **Fuente de Interfaz:** `Inter`, `system-ui`, `-apple-system`, `sans-serif` con pesos `font-bold` (700) y `font-extrabold` (800) para titulares, y `font-normal` (400) / `font-medium` (500) para lectura.
- **Titulares Cómicos:** Acompañados de sutiles degradados (`bg-gradient-to-r from-torbellino-coral via-torbellino-peach to-torbellino-plum bg-clip-text text-transparent`) o sombreados de texto suaves.

---

## 4. Componentes UI Estandarizados

### 4.1. Tarjetas ("Sticker Cards")
- Bordes redondeados amplios (`rounded-3xl` o `rounded-2xl`).
- Borde fino de delimitación (`border-2 border-torbellino-sand` o `border-torbellino-coral/20`).
- Sombra sutil cálida (`shadow-lg shadow-torbellino-coral/5` o `shadow-xl`).
- Efecto hover con micro-interacción (`hover:-translate-y-1 transition duration-200`).

### 4.2. Botones de Acción (Pills & Badges)
- Forma de píldora redondeada completa (`rounded-full`).
- Botón primario: Fondo degradado Coral a Fresa (`bg-gradient-to-r from-[#F87157] to-[#DC2626] text-white shadow-md shadow-red-500/25`).
- Botón secundario: Fondo blanco con borde denim o coral (`border-2 border-[#4A7499] text-[#4A7499] hover:bg-[#4A7499]/10`).

---

## 5. Estructura de Secciones de la Página Principal

1. **Top Banner & Navegación:**
   - Logo con avatar de Lorena guiñando el ojo.
   - Enlaces rápidos (Discos, Videoclips, Sobre Lorena, Redes).
   - Acceso directo a YouTube oficial.
2. **Hero Section:**
   - Presentación de Lorena Torbellino: "Canciones, desastres cotidianos y risas garantizadas".
   - Botón CTA principal: "Ver videoclips en YouTube".
   - Tarjeta destacada con el avatar y sello de zapatillas rojas.
3. **Catálogo de Discos (Estructura de 4 Álbumes):**
   - Álbum 1: *Cosas de la vida real*
   - Álbum 2: *Me pasa de todo*
   - Álbum 3: *Que locura*
   - Álbum 4: *Problemas de viejoven*
4. **Zona de Videoclips Populares (Layout de Pruebas):**
   - Rejilla responsiva con tarjetas de prueba para mostrar miniaturas y gags.
5. **Sobre Lorena Torbellino:**
   - Ficha cómica: 20 años, zapatillas Converse rojas, moño con pinza y enemiga declarada de las tareas del hogar.
6. **Footer Oficial:**
   - Identidad canónica, aviso legal, canal oficial `@LorenaTorbellino`, contacto oficial `public@raupulus.dev` y copyright.

---

## 6. Arquitectura Técnica

- **Estructura Estática Local:**
  ```text
  www.lorenatorbellino.raupulus.dev/
  ├── index.html
  ├── assets/
  │   ├── css/
  │   │   └── tailwind.css         # CSS compilado local (cero CDN)
  │   ├── js/
  │   │   └── alpine.min.js        # Micro-framework local para reactividad
  │   └── images/
  │       ├── lorena_logo_oficial.png
  │       ├── lorena_sticker_guiño.png
  │       ├── lorena_avatar.jpg
  │       └── lorena_banner.jpg
  └── docs/
      └── info/
          └── DESIGN.md
  ```
- **Sin recursos externos:** No se permite cargar fuentes de Google Fonts, scripts de CDNs (cdnjs, unpkg) ni imágenes externas en tiempo de ejecución.
