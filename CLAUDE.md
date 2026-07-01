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

### Teacher Edition
PDF premium separado por worksheet. Template aprobado en `teacher-edition-template.html`. Aplica solo a worksheets nuevos.
→ [memory/project_teacher_edition.md](../../../.claude/projects/C--Users-juand-OneDrive-Desktop-Workshido/memory/project_teacher_edition.md)

### Upload bloqueado
Solo Juan David puede subir worksheets. Implementar verificación por email `juanda.5790@hotmail.com` cuando dé la orden.
→ [memory/project_upload_lock.md](../../../.claude/projects/C--Users-juand-OneDrive-Desktop-Workshido/memory/project_upload_lock.md)
