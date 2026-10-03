# Key Word Speaking · B2 First

Primera versión del ejercicio oral de Key Word Transformations del Hub de Adrián.

- 120 transformaciones completas reutilizadas del banco de `adaptive-exam`.
- Sesiones de 15 preguntas.
- Temporizador configurable: 90 / 120 / 180 segundos, sin límite o tiempo personalizado por transformación.
- Entrada por micrófono propio o por Gboard.
- Se puede decir solo el hueco o la segunda frase completa; si se dicta la frase completa, la app reconoce las partes impresas y extrae automáticamente el contenido del hueco.
- Las partes impresas reconocidas reciben un flash azul como confirmación visual.
- La transcripción se muestra antes de corregir y puede repetirse o editarse con teclado.
- Gboard queda libre de reescrituras durante la composición: la extracción de frase completa se aplica al comprobar, no mientras el IME está componiendo.
- Puntuación Cambridge-style 0/1/2 por transformación; 15 preguntas = 30 puntos.
- Maquetación Part 4 tipo libro/examen: número, frase original, keyword y segunda frase partida alrededor del hueco.
- Estadísticas persistentes en `localStorage`.
- Priorización ligera de preguntas poco vistas o con más fallos.
- Puntuación de práctica 0/1/2 inspirada en Cambridge Part 4: 2/2 por coincidencia completa; 1/2 conservador cuando se conserva la keyword, el límite de 2–5 palabras y una parte sustancial de la estructura. El 1/2 es una estimación porque el banco no incluye los cortes oficiales del mark scheme.
- Sistema común de medallas, escalado proporcionalmente a 30 puntos por sesión: azul 26/30, violeta 28/30, oro 30/30.
- PWA instalable y navegación común de vuelta al Hub.

## Principio de corrección

La voz nunca corrige automáticamente. Primero rellena el hueco con lo que el navegador ha entendido; el usuario confirma con **COMPROBAR**. Esto separa los errores de reconocimiento de los errores reales de inglés.

## Privacidad / arquitectura

Esta versión no incluye ninguna clave de OpenAI en el frontend. Usa el reconocimiento de voz disponible en el navegador y permite también el dictado del teclado del sistema.
