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
3. **Manifiesto**: crear `manifest.json` temporal (schema documentado en `tools/upload_batch.py`): slug, png, pdf, thumb, te_html, te_pdf, title, level, category, tags (`worksheet` primero), description.
4. **Convertir worksheets**: `python tools/png_to_pdf.py manifest.json`
5. **Teacher Editions**: escribir un JSON de contenido por worksheet (schema en `tools/build_te.py`) → `python tools/build_te.py contenido.json te_xxx.html` → `python tools/html_to_pdf_cdp.py manifest.json`
6. **Verificar visualmente** (obligatorio): `python tools/render_pdf_pages.py <dir> *.pdf` y leer los PNGs renderizados (worksheets 1 página, TEs 2 páginas exactas).
7. **Subir**: `python tools/upload_batch.py manifest.json` (is_free siempre True, forzado por el script).
8. **Verificar subida**: `python tools/verify_uploads.py N` (re-descarga desde URLs públicas; correr con `PYTHONIOENCODING=utf-8`).
9. **Reportar a Juan** cualquier error pedagógico encontrado en los PNGs (se documentan con ⚠ en la TE; él decide si regenera).

No requiere deploy a Netlify (los worksheets cargan dinámicamente desde Supabase).

### Teacher Edition
PDF premium separado por worksheet. Template aprobado en `teacher-edition-template.html`. Aplica solo a worksheets nuevos.
→ [memory/project_teacher_edition.md](../../../.claude/projects/C--Users-juand-OneDrive-Desktop-Workshido/memory/project_teacher_edition.md)

### Upload bloqueado
Solo Juan David puede subir worksheets. Implementar verificación por email `juanda.5790@hotmail.com` cuando dé la orden.
→ [memory/project_upload_lock.md](../../../.claude/projects/C--Users-juand-OneDrive-Desktop-Workshido/memory/project_upload_lock.md)
