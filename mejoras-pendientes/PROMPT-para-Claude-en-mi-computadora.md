Necesito aplicar mejoras ya probadas a mis dos sitios y publicarlos. Respóndeme en español.
Sigue mis reglas de CLAUDE.md (en especial: UN solo deploy por sitio).

## Carpetas (se publican con la CLI de Netlify)
- Workshido:  C:\Users\juand\OneDrive\Desktop\Workshido
- Spanishido: C:\Users\juand\OneDrive\Desktop\Spanishido   (corrígela si es otra)

## Archivos en C:\Users\juand\Downloads\mejoras
- analytics-workshido.js
- workshido-seo.patch
- workshido-premium-security.patch
- (para Spanishido, solo si no se puede usar git merge:) spanishido-todo.patch

======================================================================
## PARTE A — SPANISHIDO
======================================================================
Todos los cambios de Spanishido están en GitHub, repo juannh18/spanishido, rama
`claude/bold-hopper-xjrlf1` (PR #1). Son 5 commits: analytics, SEO, seguridad
Premium, UX, catálogo compacto y redes sociales en el pie de página.

A1. En la carpeta de Spanishido, revisa `git status`. Si hay cambios locales sin
    commit (lo que está publicado y no está en GitHub), haz commit primero
    ("Snapshot de lo publicado antes de las mejoras").
A2. `git fetch origin claude/bold-hopper-xjrlf1` y `git merge origin/claude/bold-hopper-xjrlf1`.
    Si hay conflictos, resuélvelos conservando AMBAS cosas: lo que ya está
    publicado y las mejoras. Explícame cada conflicto antes de resolverlo.
    (Si la carpeta no es un repo git: `git apply --3way spanishido-todo.patch`,
    que trae los 5 commits juntos. Si una parte no aplica, hazla a mano con la
    misma intención y dímelo.)
    - Redes sociales: el pie de página de cada página debe quedar con UN solo
      bloque <div class="footer-social"> con Instagram, Pinterest, TikTok y
      YouTube, todas de Spanishido: instagram.com/spanishido,
      pinterest.com/spanishido, tiktok.com/@spanishido y youtube.com/@spanishido.
      Mi versión publicada ya tenía un enlace a Instagram: si aparece dos veces,
      deja uno solo.
A3. Verifica:
    - `node --check` en: js/analytics.js, js/spanishido-worksheet.js,
      js/spanishido-index.js, js/spanishido-login.js,
      netlify/functions/worksheet-page.js, netlify/functions/category-page.js,
      netlify/functions/sitemap.js
    - Que NINGÚN archivo del navegador (js/*.js, *.html) haga select('*') sobre
      worksheets o quizzes, ni pida teacher_edition_url / quiz_pdf_url / key_pdf_url.
    - Que existan worksheets/practice/index-app.html y worksheets/levels/b1/index-app.html
      y sus rutas en netlify.toml.

======================================================================
## PARTE B — WORKSHIDO (el GitHub de Workshido está desactualizado: trabaja
## SIEMPRE sobre la carpeta local, que es lo publicado)
======================================================================
B1. Analytics: reemplaza js/analytics.js por analytics-workshido.js. Antes compara:
    los únicos cambios esperados son esperar hasta 1,5 s a /api/geo antes de
    enviar eventos (con envío en pagehide), ignorar navigator.webdriver, contar
    page_view solo con la página visible y web vitals sin { once: true }. Si el
    actual tiene OTRAS diferencias, avísame. Debe conservar la URL de Supabase
    mhbgxdsdaalvtgobnvbh y su clave.
B2. `git apply workshido-seo.patch` y `git apply workshido-premium-security.patch`.
    Si algo no aplica porque el código local es distinto, haz el cambio a mano
    con la misma intención:
    - category-page.js: traer TODAS las fichas con fetchAllRows (no .limit(60)),
      agrupadas por nivel (páginas de categoría) o por categoría (páginas de nivel).
    - worksheet-page.js: 503 + Retry-After: 60 si Supabase falla (también en el
      catch); 404 solo si la ficha no existe (PGRST116). El <script id="wsData">
      NO debe contener teacher_edition_url (usar has_teacher_edition).
    - workshido-worksheet.js: select con columnas explícitas (nunca '*'),
      quizzes solo 'id,topic_key,level,title,skills', y el botón de Teacher
      Edition depende de data.has_teacher_edition.
B3. En TODOS los worksheets/**/index-app.html cambia
    sb2.from('worksheets').select('*') por
    sb2.from('worksheets').select('id,slug,title,level,category,tags,description,file_url,file_type,is_free,downloads,uploaded_by,uploader_name,thumbnail_url,created_at,rating,ratings_count,topic_key,piece_type,description_long,has_teacher_edition')
    y busca cualquier otro select('*') de worksheets/quizzes en js/ y *.html.
B4. Porta a Workshido las mejoras de UX que ya están en Spanishido (míralas en el
    commit "UX from the site audit" de juannh18/spanishido, rama
    claude/bold-hopper-xjrlf1, y replica la MISMA intención en los archivos de
    Workshido):
    - Página de ficha: barra fija "Download free" abajo en celular mientras el
      botón real no se ve (IntersectionObserver); Print y Save en una sola fila;
      botones bloqueados de Teacher Edition / Full Quiz con borde (no degradado
      sólido); "More on this topic" sin repetir las fichas del panel "Complete
      the set"; evento download_gate_shown al abrir el modal de "Sign in to download".
    - Búsqueda (workshido-index.js): raíz inversa solo si la palabra del
      catálogo tiene 4+ letras y >= 60% de la buscada; 'vs','versus','y','o',
      'and','or' como stopwords; sinónimos de nivel beginner/beginners→a1,
      elementary/pre-intermediate→a2, intermediate→b1, upper-intermediate→b2,
      y sumar w.level al texto donde se busca; registrar search_submitted solo
      cuando la búsqueda queda quieta 1,5 s y tiene 3+ letras.
    - Login (workshido-login.js): login_failure con { reason }, y botón "Send
      me a new confirmation email" (sb.auth.resend type 'signup') cuando el
      email no está confirmado.
    - Catálogo (workshido-index.html): encabezado compacto (título "Browse free
      English worksheets" + buscador + filtros), sin la barra de cifras, y la
      sección "What makes Workshido different" DEBAJO del catálogo, para que las
      fichas se vean en la primera pantalla. En celular: botón de búsqueda solo
      con la lupa y filtros en una fila deslizable.
    - Textos: Workshido tiene Teacher Edition en 864 de 874 fichas. Cambia
      "some / most / almost every worksheet" por "860+ worksheets" o "every new
      worksheet" (que sea verdad). Revisa que los rangos de nivel y los
      "coming soon" del pie coincidan con lo que existe (hay fichas A1, A2, B1, B2).
B5. node --check en todos los .js que cambiaste.

======================================================================
## PARTE C — PUBLICAR (un solo deploy por sitio)
======================================================================
C1. Muéstrame un resumen corto de los cambios de cada sitio y ESPERA mi "sí".
C2. `netlify deploy --prod` en la carpeta de Spanishido y luego en la de Workshido.
C3. Comprueba en el navegador:
    - https://spanishido.com/worksheets/practice/ y /worksheets/levels/b1/ cargan.
    - https://spanishido.com/worksheets/levels/a1/ lista TODAS las fichas A1 agrupadas.
    - https://workshido.com/worksheets/grammar/ lista TODAS las fichas de gramática.
    - En una ficha de cada sitio, "Ver código fuente": NO debe aparecer
      "teacher_edition_url" ni "teacher-editions/".
    - En el celular (o vista móvil), la barra "Download free" aparece abajo.
    - Buscar "beginner" en el catálogo devuelve fichas A1.
C4. NO ejecutes SQL en Supabase (los permisos de quizzes y funciones ya los
    corrigió la sesión de Claude en la nube). El bloqueo de columnas lo hace la sesión de
    Claude en la nube DESPUÉS del deploy (si se hace antes, se rompen las páginas).

======================================================================
## PARTE D — DEJAR GITHUB IGUAL QUE LO PUBLICADO
======================================================================
D1. Sube a GitHub lo que quedó publicado: juannh18/spanishido y juannh18/workshido,
    rama principal (master/main según el repo).
D2. Cierra el PR #1 de juannh18/spanishido indicando que quedó incluido en la rama principal.

Al final dime: qué se publicó, qué no, y cualquier problema. Recuérdame avisarle
a la sesión de Claude en la nube que ya está publicado para que bloquee las
columnas Premium en Supabase.
