# Workshido — Instrucciones para Claude

## Quién soy
Juan David, dueño y único desarrollador de Workshido (workshido.com). Stack: HTML/CSS/JS puro, Netlify, Supabase, Cloudinary, Render. Respóndeme siempre en **español**.

→ Detalles completos: [memory/user_juan.md](../../../.claude/projects/C--Users-juand-OneDrive-Desktop-Workshido/memory/user_juan.md)

---

## Reglas de comportamiento

### Costos
Siempre ofrecer primero la opción gratuita o más económica. Si existe una opción gratis viable, implementarla por defecto sin preguntar.
→ [memory/feedback_costos.md](../../../.claude/projects/C--Users-juand-OneDrive-Desktop-Workshido/memory/feedback_costos.md)

### Deploys a Netlify
**Un solo deploy por sesión.** Acumular todos los cambios antes de hacer `netlify deploy --prod`. Quedan ~249 créditos (límite 1000).
→ [memory/feedback_netlify.md](../../../.claude/projects/C--Users-juand-OneDrive-Desktop-Workshido/memory/feedback_netlify.md)

### Google Auth
Usar **GIS + signInWithIdToken**. Nunca usar `signInWithOAuth` de Supabase. Client ID: `402662121573-hjto2nl434h1qdgvtl21n58du49kl2bd.apps.googleusercontent.com`
→ [memory/feedback_google_auth.md](../../../.claude/projects/C--Users-juand-OneDrive-Desktop-Workshido/memory/feedback_google_auth.md)

---

## Proyecto — Estado actual

### Worksheets
Flujo: HTML + CSS (Nunito, Caveat) → PDF via Chrome headless. Tags SEO: `worksheet` siempre primero. Script de subida: `upload_worksheet.py`.
→ [memory/project_worksheets.md](../../../.claude/projects/C--Users-juand-OneDrive-Desktop-Workshido/memory/project_worksheets.md)

### Pipeline de subida de worksheets PNG (herramientas en `tools/`)
Cuando Juan diga "sube los worksheets que descargué hoy", usar este pipeline (no reescribir scripts ad-hoc):

1. **Localizar**: PNGs del día en `C:\Users\juand\Downloads` (los genera con ChatGPT).
2. **Leer los PNGs COMPLETOS** con la herramienta Read (+crops con zoom si algo no se lee) — regla dura: texto ilegible/corrupto = NO se sube; listar literalmente todas las secciones antes de escribir la TE.
   - **Puzzles/cuadrículas (word search, crucigramas)**: hacer zoom letra por letra — es el punto más común donde ChatGPT genera glifos rotados/espejados ilegibles. Si está corrupta, reconstruirla (nunca subir tal cual): detectar el bounding box de la caja, redibujar la cuadrícula completa con las palabras reales del checklist (fuente bold sans tipo Arial Bold, mismo color de borde) y pegarla sobre el PNG original.
   - **Consistencia numérica entre actividades**: si un dato (precio, cantidad, hora) aparece en más de un ejercicio del mismo worksheet, verificar que coincida en todos (ej. precio de un ítem en "Match" vs. en "Look and Write").
   - **Ejercicios de matching/opuestos**: verificar que cada opción de la derecha tenga exactamente una pareja correcta a la izquierda (sin dos ítems compitiendo por la misma respuesta ni opciones sobrantes sin pareja real).
   - **Una sola respuesta en ítems cerrados** (elegir opción, completar con banco, relacionar, completar con la forma correcta): revisar ítem por ítem que solo UNA opción sea correcta. Causas típicas de ambigüedad accidental: falta el sujeto (*¿Qué ___ a hacer?* → vas/va/van), falta la hora o el dato que decide, dos opciones del menú que concuerdan igual. Si pasa, **se reescribe el ítem en la ficha antes de subir** (agregar sujeto/dato); la TE nunca dice "también es válida" para tapar eso. Excepción legítima: tipos abiertos por naturaleza (ordenar palabras, reescribir/transformar, escribir oraciones, clasificar con criterio, respuestas personales) sí admiten varias respuestas y la TE las lista como variantes aceptadas.
   - **Error encontrado en cualquier momento** (aunque sea en una ficha ya publicada, leyendo para otra tarea): corregir la ficha → rehacer su TE → revisar el quiz del set. Vale para Workshido y Spanishido.
3. **Manifiesto**: crear `manifest.json` temporal (schema documentado en `tools/upload_batch.py`): slug, png, pdf, thumb, te_html, te_pdf, title, level, category, tags (`worksheet` primero), description.
4. **Convertir worksheets**: `python tools/png_to_pdf.py manifest.json`
5. **Teacher Editions** (PREMIUM: cero huecos): escribir un JSON de contenido por worksheet (schema en `tools/build_te.py`; `p1_reference` con 10-14 filas es OBLIGATORIO — el conversor recorta/estira para llenar la pág. 1; si imprime `⚠⚠`, no se sube) → `python tools/build_te.py contenido.json te_xxx.html` → `python tools/html_to_pdf_cdp.py manifest.json`
6. **Verificar visualmente** (obligatorio): `python tools/render_pdf_pages.py <dir> *.pdf` y leer los PNGs renderizados (worksheets 1 página, TEs 2 páginas exactas).
7. **Subir**: `python tools/upload_batch.py manifest.json` (is_free siempre True, forzado por el script).
8. **Verificar subida**: `python tools/verify_uploads.py N` (ficha y miniatura se re-descargan desde sus URLs públicas; la TE se baja con `get_object` del bucket privado `workshido-premium`, porque ya no es pública; correr con `PYTHONIOENCODING=utf-8`). Las TE, quizzes y claves (`teacher-editions/`, `quizzes/`, con o sin `es/`) se suben solas a `workshido-premium`; la URL guardada en Supabase sigue siendo `https://files.workshido.com/<key>` y las funciones `get-teacher-edition-url` / `get-quiz-url` la firman por 5 minutos.
8b. **Pinterest (automático, no preguntar)**: `node tools/gen_pinterest_csv.js 1` (o `--site spanishido 1`) y `python tools/pinterest/render_pins.py --out <scratch> [--site spanishido]` → pinta y sube la imagen de pin de las fichas nuevas (se salta las ya subidas). El feed `/pinterest/feed/<tablero>.xml` (netlify/functions/pin-feed.js) publica cada ficha nueva solo, al día siguiente de subirla; si falta la imagen usa la vista previa real.
9. **Reportar a Juan** cualquier error pedagógico encontrado en los PNGs (se documentan con ⚠ en la TE; él decide si regenera).

No requiere deploy a Netlify (los worksheets cargan dinámicamente desde Supabase).

### Teacher Edition
PDF premium separado por worksheet. Template aprobado en `teacher-edition-template.html`. Aplica solo a worksheets nuevos.
→ [memory/project_teacher_edition.md](../../../.claude/projects/C--Users-juand-OneDrive-Desktop-Workshido/memory/project_teacher_edition.md)

### Upload bloqueado
Solo Juan David puede subir worksheets. Implementar verificación por email `juanda.5790@hotmail.com` cuando dé la orden.
→ [memory/project_upload_lock.md](../../../.claude/projects/C--Users-juand-OneDrive-Desktop-Workshido/memory/project_upload_lock.md)
