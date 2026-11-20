# ROM hack de Pokémon Esmeralda (en español)

&nbsp;[Read in English](README.md)

Un hack de Pokémon Esmeralda centrado en la dificultad, en español, compilado desde el código fuente sobre [pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion) (la decompilación del juego hecha por la comunidad, ampliada con mecánicas modernas). Está en desarrollo y se distribuye como parche.

<!-- Capturas: añade 2-4 imágenes en docs/ y enlázalas aquí, p. ej. ![Combate de gimnasio](docs/gym.png) -->

## Características

- **Combates más difíciles y planificados.** Entrenadores y gimnasios rehechos, con los equipos documentados para que puedas prepararte (ver Documentación).
- **Tope de nivel estricto y nivelado sin farmeo.** Los Pokémon no pueden pasar del tope actual, y las tiendas venden Caramelos Raros: el tiempo se va en armar el equipo, no en entrenar.
- **Herramientas en el PokéNav.** Un menú nuevo: MAPA (mapa de la región), LUZ (ilumina cuevas sin necesitar Destello), CURAR (una cura completa del equipo, que se recarga en cualquier Centro Pokémon), NIVEL (gasta Caramelos Raros para subir al equipo hasta el tope, deteniéndose en movimientos nuevos y evoluciones) y TELÉFONO.
- **Un combate extra después del Campeón.** Un combate doble contra dos entrenadores en la sala del Campeón.
- **Mecánicas modernas** de pokeemerald-expansion: movimientos, habilidades y Pokémon nuevos, división física/especial y reglas de combate actualizadas.
- **En español.** El diálogo se está traduciendo al español de España zona por zona; los términos de menús y combate siguen en inglés por ahora.
- Pensado para Nuzlocke: estilo de combate Fijo por defecto, y nada del diseño depende de curarse con objetos en combate.

## Documentación

Guías en PDF con los cambios de estadísticas de los Pokémon, los encuentros salvajes y el equipo de cada entrenador importante:

> 📁 **[Documentación en Google Drive](https://drive.google.com/drive/folders/1X7U3qSoCkZmtn9oEiggJ291KKCRRhj-f)** (solo lectura)

## Cómo jugar

Necesitas tu propia copia limpia de **Pokémon Emerald (USA, Europe)**. Su SHA-1 debe ser `f3ae088181bf583e55daf962a92bb46f4f1d07b7`.

1. Descarga el parche `.bps` desde [Releases](../../releases).
2. Abre [Rom Patcher JS](https://www.marcrobledo.com/RomPatcher.js/) en el navegador (o usa Floating IPS en Windows).
3. Elige tu ROM de Esmeralda y el parche, y pulsa **Apply patch**. El parche comprueba la ROM: rechaza una incorrecta o modificada.
4. Juega el resultado en un emulador de GBA como [mGBA](https://mgba.io).

Este repositorio no contiene ninguna ROM. Pokémon es © Nintendo / Game Freak / Creatures; este es un proyecto de fans sin ánimo de lucro.

## Por dentro

El juego está escrito en C y se compila con `arm-none-eabi-gcc`. Junto al hack construí una herramienta de desarrollo que analiza cómo combate el jugador, describe su estilo con un LLM y lo devuelve al juego: [llm-fight-tracker](https://github.com/alvarollopezgarcia-cpu/llm-fight-tracker). Está desactivada en las versiones publicadas aquí.

`tools/make_bps_patch.py` es el script que genera el parche de cada versión. Escribe el formato BPS directamente y se niega a guardar un parche que no reconstruya el hack byte a byte.

## Créditos

- [pret](https://github.com/pret/pokeemerald), por la decompilación de Pokémon Esmeralda.
- [Rom Hacking Hideout](https://github.com/rh-hideout/pokeemerald-expansion) y todos los colaboradores de pokeemerald-expansion.
- [Porymap](https://github.com/huderlem/porymap), por la edición de mapas.
