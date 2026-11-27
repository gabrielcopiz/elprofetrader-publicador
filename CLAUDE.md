# Memoria de trabajo: El Profe Trader

Este archivo se carga solo en cada sesión que abre este repo, en cualquier computadora o en la nube.
**Regla:** al terminar cada tanda de trabajo, actualizar este archivo y subirlo. Lo que no está acá, la próxima sesión no lo sabe.
**Ojo:** el repo es público. Acá no van mails, contraseñas, llaves, datos de cuenta de fondeo ni nombres de estrategia.

## Quién y qué
- Marca: El Profe Trader, usuario `@elprofetrader` en Instagram, Threads, TikTok y YouTube.
- El fundador es ex profe de educación física y trader de futuros (S&P 500 y Nasdaq en CME) a tiempo completo. Me llama "Claudito".
- Objetivo actual: conseguir seguidores. Al 27/11 la cuenta casi no tiene (se sumó una persona).
- Tono con él: directo, corto, sin vueltas. Quiere que yo haga todo lo que pueda sin preguntarle.

## Cómo sale cada cosa
- **Instagram:** robot de este repo (`publicar.py`, `.github/workflows/publicar.yml`). Reel desde 12:30 y carrusel desde 19:00, hora Argentina, según `agenda.json`. Lo publicado queda en `publicado.json`.
- **Threads:** robot (`publicar_threads.py`, `threads/posteos.json`). Cada posteo tiene su fecha y hora. Registro en `threads/publicado.json`. Desde las 19:00 puede salir además la operativa del día si hay trades en el diario.
- **TikTok:** se programa a mano en TikTok Studio desde un navegador logueado, a las 12:30. TikTok Studio publica como "Solo yo": después hay que cambiar a "Todo el mundo". Se entra con código QR desde el celular.
- **YouTube Shorts:** se programa en YouTube, 12:30, el mismo día que Instagram.
- **Control:** una tarea revisa cada hora y dispara el robot si algo falta. Informe en `control/informe.md`.
- GitHub atrasa los horarios, por eso el robot corre muchas veces y decide por la hora real.

## Reglas que ya fijó el fundador
- **Música:** cada video usa un sonido en tendencia de la propia red, preferentemente electrónica, elegido de la biblioteca de esa red. Nada de música de banco ni armada por mí. A Instagram y TikTok el archivo se sube mudo (una pista propia ya saturó una vez y lo pueden silenciar). En Instagram el sonido va por `audio_id` en `agenda.json`.
- **Prohibido mostrar o nombrar:** nombres de estrategia, número de cuenta, nombre de la firma de fondeo, saldo, usuario, señales, operaciones reconstruidas.
- **Control de calidad antes de publicar un video:** textos sin faltas y fuera de la zona que tapan los botones, números que coincidan con los del fundador, audio medido.
- No decir "en vivo" si el video no es en vivo.
- Verificar lo que se afirma y decir qué quedó sin verificar.

## Reglas para comentar en otras cuentas
- Nunca comentar ni responder en `@watsontradingacademy`.
- Cada comentario suma algo concreto (dato propio, experiencia, matiz o pregunta), 1 a 3 oraciones, respetuoso, sin enlaces, sin "seguime", sin señales.
- Solo datos del fundador ya publicados en este repo (captions y `threads/posteos.json`). No inventar.
- 5 a 10 por día por red, espaciados. Videos recién subidos y con pocos comentarios.
- Ya comentados el 26/11: un reel de Chelo Psicotrading y uno de Alekay.
- Las reglas completas de Threads (pregunta final, un tema, horarios, sin links) están en `threads/posteos.json`, campo `reglas`.

## Estrategia para crecer (acordada 26/11)
1. Videos con su cara: cara, gancho y prueba real. De sus grabaciones salen 5 cortos y 5 clases.
2. Comentar desde `@elprofetrader` en reels recién subidos de cuentas grandes de trading (ser el primer comentario), en Instagram, Threads y YouTube. Necesita un navegador logueado.
3. Libro gratuito de futuros como regalo ("comentá LIBRO y te lo mando"). Falta su sí.

## Material hecho (páginas en su cuenta de Claude)
- Libro: "Trading de futuros desde cero", "El libro de las 200", "La media de 200".
- PDF: "Guía en PDF", "Cuaderno de trabajo".
- Guiones: "Guiones para grabar", "Plan de grabación", "Los cinco videos, parte de abajo", "Serie gratuita de futuros", "Guiones YouTube".
- Video "16 días" (historia animada, evaluación de fondeo aprobada en 16 días operados).
- Se encuentran con la lista de artifacts de la cuenta.

## Dónde está lo que no está en este repo
- Carpeta de trabajo de la compu de escritorio: `OneDrive\Escritorio\Claudito\el-profe-trader` (videos sin cara, notas, compromisos, diario). Los videos de "16 días" están en `videos-sin-cara\out`.
- Las sesiones en la nube no ven esa carpeta ni tienen navegador con las cuentas abiertas.

## Pendientes al 27/11
- "16 días": terminado y corregido. Falta que diga qué día sale (propuesta: lunes 30/11, 12:30, las 4 redes; YouTube con música B, Instagram con "Right Round", TikTok con sonido de su biblioteca).
- Sí o no al libro gratuito como regalo en los cortos.
- Grabar los videos con su cara.
- Cargar posteos de Threads del 3 al 9 de diciembre.
- Sin reels en la agenda desde el 30/11. Sin carrusel los viernes 4, 11 y 18/12. `s3-1-lunes` tiene láminas pero no está en la agenda.
- Encontrar el mail con el que se crearon las cuentas (no está en su Gmail principal ni en Drive) y guardarlo en un lugar privado, no acá.

## Bitácora
- 27/11: compu de escritorio sin luz, trabajó desde la notebook en una sesión en la nube. Se creó este archivo porque la memoria anterior vivía solo en la compu de escritorio.
