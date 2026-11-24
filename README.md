# iCON Platform Nano Air · FL Studio script (Mackie Control / MIDI)

**Script de FL Studio para el controlador iCON Platform Nano Air** en modo Mackie Control (MCP). Se usa en lugar del script genérico Mackie Control Universal (MCU) que trae FL: el fader motorizado sigue al canal seleccionado del Mixer, la pantallita muestra ese canal y su volumen en dB, los modos de la rueda se prenden con un toque y la pantalla externa Platform D3 (opcional) muestra un canal por cuadro. Incluye un [manual de instalación](#manual-de-instalación) paso a paso.

**FL Studio MIDI script for the iCON Platform Nano Air controller** in Mackie Control (MCP) mode. Use it instead of the generic Mackie Control Universal (MCU) script that comes with FL: the motorized fader follows the selected mixer track, the small screen shows that track and its volume in dB, wheel modes latch with one tap and the optional Platform D3 external display shows one track per square. Includes a step-by-step [installation manual](#installation-manual).

- **Tutorial interactivo / Interactive tutorial** (en español / in Spanish): [https://noisybeats03-eng.github.io/icon-platform-nano-air-fl-studio/](https://noisybeats03-eng.github.io/icon-platform-nano-air-fl-studio/)
- **Descarga / Download:** [última versión / latest release](https://github.com/noisybeats03-eng/icon-platform-nano-air-fl-studio/releases/latest), archivo / file `iCON-Platform-Nano-Air-FL-Studio-v1.0.0.zip`
- **Versión / Version:** 1.0.0, noviembre de 2026 / November 2026. Probado con FL Studio 2025 en Windows / Tested with FL Studio 2025 on Windows.

**[Español](#español)** · **[English](#english)**

Proyecto independiente y no oficial: no está afiliado a iCON Pro Audio ni a Image-Line. · Independent, unofficial project: not affiliated with iCON Pro Audio or Image-Line.

---

## Español

Manual completo para instalar y usar el script paso a paso. No necesitas saber programar.

### Contenido

1. [Qué es y qué mejora](#qué-es-y-qué-mejora)
2. [Manual de instalación](#manual-de-instalación)
    - [Qué necesitas](#qué-necesitas)
    - [Descargar](#descargar)
    - [Instalar el script](#instalar-el-script)
    - [Conectar el Nano](#conectar-el-nano)
    - [Poner el Nano en modo MCP](#poner-el-nano-en-modo-mcp)
    - [Configurar FL Studio](#configurar-fl-studio)
    - [Comprobar que funciona](#comprobar-que-funciona)
    - [Primer uso: toca el fader](#primer-uso-toca-el-fader)
3. [Cómo se usa](#cómo-se-usa)
    - [Las partes del Nano](#las-partes-del-nano)
    - [Los 8 botones de colores](#los-8-botones-de-colores)
    - [Modos de la rueda](#modos-de-la-rueda)
    - [Combinaciones con Shift](#combinaciones-con-shift)
    - [Páginas de las perillas](#páginas-de-las-perillas)
    - [Lo que muestran las pantallas](#lo-que-muestran-las-pantallas)
    - [Pantalla externa Platform D3](#pantalla-externa-platform-d3)
    - [Recetas](#recetas)
4. [Preguntas frecuentes](#preguntas-frecuentes)
5. [Si algo no funciona](#si-algo-no-funciona)
6. [Actualizar a una versión nueva](#actualizar-a-una-versión-nueva)
7. [Volver al script original de FL](#volver-al-script-original-de-fl)
8. [Desinstalar](#desinstalar)
9. [Créditos y aviso legal](#créditos-y-aviso-legal)
10. [Licencia](#licencia)
11. [Para desarrolladores](#para-desarrolladores)

### Qué es y qué mejora

El **iCON Platform Nano Air** es un controlador con un fader motorizado, una rueda (jog), 5 perillas y 8 botones de colores que, con sus 5 capas, dan 40 funciones. Tiene una pantallita de 2 líneas de 7 letras y un reloj de números rojos. Funciona por cable USB o inalámbrico, con batería.

Se comunica con FL Studio en el "idioma" **Mackie Control**. FL ya trae un script para ese idioma (**Mackie Control Universal**), pero está hecho para consolas grandes de 8 faders con una pantalla larga, y con el Nano varias cosas no funcionan bien.

Este proyecto es un **script de FL Studio** (un archivo de Python que FL carga solo) basado en el de FL y adaptado al Nano. No es un programa: se instala copiando una carpeta.

Qué mejora:

- **El fader motorizado sigue al canal seleccionado.** Eliges un canal en el Mixer de FL (con el mouse, con la rueda o con `|<` `>|`) y el fader se va a su volumen. Mute, Solo, Rec y la pantalla también trabajan sobre ese canal. Esto pasa en las páginas Pan, Stereo, Sends y Effects (no con Flip ni en EQ o Free). Con **Master**, el fader controla el volumen principal de FL. (Con el script de FL, el fader se quedaba fijo en un canal del banco.)
- **Pantalla clara.** Arriba el canal seleccionado (los nombres largos se acortan a 7 letras: "Insert 12" sale `Ins 12`) y abajo su volumen real en dB. Al tocar un botón sale un mensaje corto y completo durante 1.5 segundos: `METRO ON`, `LOOPREC OFF`, `SNAP ON`, `MUTE ON`, `SAVE OK`… No parpadea.
- **Modos de la rueda con un toque.** Pattern, Mixer, Channel, Tempo, Free 1–4, Window, Move y Mark: un toque los prende y otro toque los apaga. Si mantienes el botón mientras giras la rueda, se apaga solo al soltar. (Con el de FL había que mantenerlos apretados.)
- **Zoom en dos ejes.** Zoom ↕ cambia la altura de los tracks y Zoom ↔ el zoom horizontal. Se queda prendido hasta que lo apagas. (Con el de FL, los dos hacían zoom horizontal.)
- **Undo de un toque.** La tecla amarilla 7 deshace un paso; si la mantienes y giras la rueda, recorres el historial.
- **LOOP graba en loop.** El botón LOOP prende o apaga la grabación en loop; Shift + LOOP prende o apaga el Snap. (Con el de FL, LOOP era el Snap.)
- **BPM en los números rojos.** En modo Tempo, el reloj muestra el tempo (por ejemplo `130.00`).
- **Pantalla externa Platform D3 (opcional):** un canal del banco en cada cuadro.
- **Fader más estable.** Ignora el temblor de un dedo apoyado. Si cambias de canal con el dedo en el fader, el canal nuevo no cambia hasta que el fader llega a su nivel o lo sueltas.
- **Errores corregidos** del script de FL: Shift + Solo daba error; soltar Shift antes que una tecla F hacía otra cosa (Undo); mantener Undo y girar la rueda daba error; el valor del fader en la página Free salía mal.

Los 40 botones de colores hacen lo que dice la plantilla (overlay) de FL Studio que iCON incluye con el Nano.

### Manual de instalación

Cómo instalar y configurar el script del iCON Platform Nano Air en FL Studio, paso a paso.

**En resumen** (si ya sabes cómo va):

1. Descarga el ZIP de la [última versión](https://github.com/noisybeats03-eng/icon-platform-nano-air-fl-studio/releases/latest) y descomprímelo.
2. Copia la carpeta `iCON Platform Nano Air` en `Documentos\Image-Line\FL Studio\Settings\Hardware`.
3. Pon el Nano en modo **MCP**.
4. En FL, **OPTIONS > MIDI settings**: en **Input** elige el Nano, **Controller type** = **iCON Platform Nano Air (custom)** y **Port** = 1; en **Output**, el mismo Nano con **Port** = 1.
5. **VIEW > Script output** debe decir **OnInit ready**. Toca el fader una vez.

Abajo está cada paso con detalle.

#### Qué necesitas

- Un **iCON Platform Nano Air** con su cable USB o con su receptor inalámbrico USB.
- **FL Studio.** Probado con **FL Studio 2025 en Windows** (API de scripts de FL versión 40). Otras versiones de FL Studio y macOS no están probadas (el script es Python normal, así que en Mac debería funcionar).
- Opcional: la pantalla externa **iCON Platform D3**.
- Recomendado: la **plantilla (overlay) de FL Studio** que viene con el Nano, para ver el nombre de cada botón de colores.
- **No** necesitas instalar Python (FL ya lo trae), ni drivers (el Nano funciona sin drivers), ni el programa iMap de iCON.

#### Descargar

**Opción A (recomendada): el ZIP de la versión**

1. Abre la página de la [última versión](https://github.com/noisybeats03-eng/icon-platform-nano-air-fl-studio/releases/latest).
2. Baja hasta **Assets** y haz clic en `iCON-Platform-Nano-Air-FL-Studio-v1.0.0.zip` (en versiones nuevas cambia el número). No uses los archivos "Source code".
3. El ZIP queda en tu carpeta **Descargas**.
4. Haz clic derecho en el ZIP → **Extraer todo…** (en Windows en inglés: **Extract All…**) → **Extraer**.
5. Se abre una carpeta nueva. Adentro está la carpeta `iCON Platform Nano Air`, y dentro de ella el archivo `device_iCON_PlatformNanoAir.py`. Esa carpeta es lo único que vas a instalar.

**Opción B: todo el repositorio**

1. En la página principal del repositorio, haz clic en el botón verde **Code** → **Download ZIP**.
2. Descomprímelo igual (clic derecho → **Extraer todo…**).
3. Abre la carpeta `icon-platform-nano-air-fl-studio-main`: adentro está la carpeta `iCON Platform Nano Air`.

> Windows a veces esconde la terminación `.py`: el archivo puede verse como `device_iCON_PlatformNanoAir`, de tipo "Python File" o "Archivo PY". Es el mismo. No hace falta abrirlo.

#### Instalar el script

No hay instalador: solo copias una carpeta dentro de la carpeta de scripts de FL.

**Paso 1. Encuentra tu carpeta de datos de FL**

1. Abre FL Studio.
2. Ve al menú **OPTIONS > File settings**.
3. Mira el campo **User data folder**. Esa es tu carpeta de datos de FL. Si nunca la cambiaste, es `Documentos\Image-Line` (en el disco se llama `Documents\Image-Line`).

**Paso 2. Abre la carpeta Hardware**

Los scripts van en `FL Studio\Settings\Hardware`, dentro de tu carpeta de datos. Con la carpeta de datos normal, la ruta completa es:

```text
C:\Users\<tu usuario>\Documents\Image-Line\FL Studio\Settings\Hardware
```

Forma fácil en Windows:

1. Abre el **Explorador de archivos**.
2. Haz clic en la barra de dirección (arriba), pega esto y presiona **Enter**:
   ```text
   %USERPROFILE%\Documents\Image-Line\FL Studio\Settings\Hardware
   ```
3. Si Windows dice que no existe, usa la ruta que te mostró FL en **User data folder** y entra a `FL Studio` → `Settings` → `Hardware`. Eso pasa si cambiaste la carpeta de datos (por ejemplo a otro disco) o si tu carpeta Documentos está en OneDrive.
4. Si dentro de `Settings` no hay una carpeta `Hardware`, créala: clic derecho → **Nuevo** → **Carpeta**, con el nombre exacto `Hardware`.

En macOS (no probado): en Finder, menú **Ir > Ir a la carpeta…**, pega `~/Documents/Image-Line/FL Studio/Settings/Hardware` y presiona Enter.

**Paso 3. Copia la carpeta**

1. Copia la carpeta `iCON Platform Nano Air` completa (no solo el archivo) dentro de `Hardware`.
2. Debe quedar así:
   ```text
   ...\FL Studio\Settings\Hardware\iCON Platform Nano Air\device_iCON_PlatformNanoAir.py
   ```
3. Revisa que no haya una carpeta de más en medio, por ejemplo `Hardware\iCON-Platform-Nano-Air-FL-Studio-v1.0.0\iCON Platform Nano Air\...`. Si queda así, FL no lo encuentra.

**Paso 4. Haz que FL lo vea**

- Cierra FL Studio y vuelve a abrirlo, **o**
- en **OPTIONS > MIDI settings**, haz clic en **Update MIDI scripts**.

#### Conectar el Nano

El Nano funciona con batería. Su switch de encendido está **atrás**: es el interruptor del extremo izquierdo cuando miras la parte de atrás. El lado con la rayita (**–**) es prendido y el lado con la **O** es apagado.

**Por cable USB**

1. Conecta el cable USB que viene con el Nano a la computadora y al puerto USB azul de atrás del Nano. Mejor directo a la computadora, sin hub ni extensión.
2. Prende el Nano con el switch de atrás.
3. La computadora lo reconoce sola. Por cable, la batería se carga mientras lo usas.

**Inalámbrico (con el receptor USB)**

1. Conecta el receptor inalámbrico de iCON (el pequeño receptor USB, o dongle, que viene con el Nano) a un puerto USB de la computadora.
2. Prende el Nano con el switch de atrás.
3. Espera unos segundos: el Nano y el receptor se conectan solos. Cuando la pantallita del Nano dice **Paired**, ya están conectados. La luz **Paired** del receptor se queda fija; si parpadea, todavía no se conectan.

**La batería**

- Los 4 LEDs de batería del Nano muestran la carga: verde (76–100 %), verde (51–75 %), naranja (26–50 %) y rojo (menos de 25 %). Si el rojo parpadea, queda menos de 5 %: cárgalo ya.
- Para cargarlo, conéctalo por cable USB a la computadora (se carga mientras lo usas), o conecta un cargador USB de celular o una batería externa al puerto mini USB de atrás.
- Según iCON, con la batería llena dura unas 5 a 6 horas.
- Si se acaba la batería, conéctalo por cable: funciona igual. Lee el aviso sobre los dos nombres en [Configurar FL Studio](#configurar-fl-studio).

#### Poner el Nano en modo MCP

El Nano tiene varios modos, uno por tipo de programa. FL Studio usa el modo **MCP** (Mackie Control). Solo se hace una vez: el Nano recuerda el último modo que elegiste.

1. Apaga el Nano con el switch de atrás y vuelve a prenderlo.
2. Al prenderse, el Nano te deja elegir el modo durante unos segundos. La pantallita muestra el modo actual, por ejemplo **(1) MCP**. En ese momento, los botones **1, 2 y 3 de la fila de arriba** de los 8 botones de colores funcionan como **<<**, **>>** y **DAW Mode**. (Con la plantilla de FL puesta, en la capa roja se llaman Flip, Browser y Main.)
3. Toca **<<** o **>>** hasta que la pantallita diga **MCP**. Los modos son: (1) MCP, (2) LogicPro, (3) HUI y (4) User-Def.
4. Toca **DAW Mode** para elegirlo.
5. Listo. Las próximas veces no toques nada al prenderlo: después de unos segundos entra solo al último modo que elegiste.

- Si entra solo a otro modo antes de que alcances a elegir, apágalo y vuelve a intentarlo.
- iCON pone FL Studio en la lista del modo MCP. No uses LogicPro, HUI ni User-Def con este script.
- El modo también se puede elegir con el programa iMap de iCON (**Control Mode** → **1) MCP** → **Send Data**), pero no hace falta.
- Consejo de iCON: lo más estable es prender el Nano y elegir el modo **antes** de abrir FL.

#### Configurar FL Studio

Esto se hace una vez para cada nombre del Nano (lee el aviso al final de esta sección).

1. Prende y conecta el Nano, y abre FL Studio.
2. Abre **OPTIONS > MIDI settings** (o presiona **F10**).
3. En la lista **Input**, haz clic en el nombre del Nano:
   - inalámbrico (receptor): **PlatformNano Air V1.02**
   - por cable: **PlatformNano(A) V2.05**

   Con otro firmware el nombre puede ser un poco distinto: busca el que empieza con **PlatformNano**.
4. En **Controller type**, elige **iCON Platform Nano Air (custom)**.
5. Mira la luz de **Enable**: debe estar prendida.

   **Ojo:** al elegir el Controller type, FL prende Enable solo. Si después haces clic en Enable, lo **apagas**. Haz clic en Enable solo si su luz está apagada.
6. Pon **Port** en **1**. Sirve cualquier número que no use otro controlador, pero la entrada y la salida del Nano deben tener el mismo.
7. En la lista **Output**, haz clic en el mismo nombre del Nano y pon **Port** en el mismo número (**1**).
8. Cierra la ventana.

Si **iCON Platform Nano Air (custom)** no aparece en la lista, ve a [Si algo no funciona](#si-algo-no-funciona).

> **¿Usas cable e inalámbrico?** FL guarda la configuración por *nombre* de dispositivo, y el Nano tiene un nombre por cable y otro por inalámbrico. Configura los dos una vez: conéctalo de una forma y haz los pasos 3 a 7; luego conéctalo de la otra forma y repítelos. Si no, el día que se acabe la batería y conectes el cable, va a parecer que se perdió la configuración.

#### Comprobar que funciona

1. En FL, abre **VIEW > Script output**.
2. Haz clic en la pestaña con el nombre del Nano. Debe decir **OnInit ready**.
3. Mira la pantallita del Nano. Cuando el script arranca (al abrir FL o al elegir el Controller type) dice **FL** / **LISTO** unos 2 segundos. Después muestra arriba el canal del Mixer seleccionado y abajo su volumen en dB, por ejemplo **Kick** / **-5.2dB**.
4. En el Mixer de FL, haz clic en otro canal: el fader se mueve solo a su volumen y la pantallita cambia de nombre.
5. Mueve el fader: cambia el volumen de ese canal en FL.

Si algo de esto no pasa, ve a [Si algo no funciona](#si-algo-no-funciona).

#### Primer uso: toca el fader

Cada vez que abras FL, **toca el fader una vez**. Basta con tocarlo; no hace falta moverlo.

- Así el script aprende en qué lugar del banco de 8 canales está el fader del Nano.
- Importa sobre todo con la pantalla externa Platform D3: hasta que tocas el fader, sus 8 cuadros repiten lo mismo; después, cada cuadro muestra su canal.
- En **VIEW > Script output** aparece una línea que empieza con `Nano Air screen: fader on strip`.

**Prueba rápida:** toca el botón redondo azul (capa azul) y luego el botón 4 de la fila de arriba, **Metronome**. La pantallita dice **METRO** / **ON** y se prende el metrónomo de FL. Tócalo otra vez: **METRO** / **OFF**.

### Cómo se usa

Aquí está el resumen. Para verlo con dibujos, abre el [tutorial interactivo](https://noisybeats03-eng.github.io/icon-platform-nano-air-fl-studio/): tocas cualquier botón del Nano dibujado y te dice qué hace, y la pantallita y la Platform D3 dibujadas muestran lo que deberían decir. Su sección "Lo que dicen las pantallas" lista los 69 controles, y también tiene los modos de la rueda, las combinaciones con Shift, las páginas de las perillas, recetas y ayuda si algo falla.

Tres palabras que se usan mucho:

- **Canal seleccionado:** el canal del Mixer que está seleccionado en FL.
- **Banco:** el grupo de 8 canales del Mixer que controlan las perillas. Cambias de banco con `<<8` y `8>>`.
- **Capa:** el color que eliges con los 5 botones redondos. Cambia lo que hacen los 8 botones de colores.

#### Las partes del Nano

| Parte | Qué hace |
|---|---|
| **Fader** (motorizado y sensible al tacto) | Volumen del canal seleccionado. Se mueve solo cuando cambias de canal. Mientras lo tocas, FL no lo mueve. |
| **Master** | El fader pasa al volumen principal de FL (la pantallita dice `MASTER` y el %). Tócalo otra vez para regresar al canal. |
| **`\|<`** y **`>\|`** (columna izquierda) | Pasan el fader al canal anterior o siguiente del banco. FL selecciona ese canal y muestra el Mixer. |
| **`<<8`** y **`8>>`** (columna izquierda) | Banco anterior o siguiente: las perillas saltan 8 canales. |
| **5-8** (arriba en la columna izquierda) | Las 4 perillas pequeñas pasan de los canales 1–4 del banco a los 5–8, y de regreso. |
| **Candado** (abajo en la columna izquierda) | Función propia del Nano; no manda nada a FL. |
| **Mute**, **Solo** y **Rec** (el botón redondo con punto rojo, abajo de Solo) | Silenciar, dejar solo y armar para grabar el canal seleccionado. |
| **Perilla grande y 4 perillas pequeñas** | Hacen lo que diga la página elegida en la columna derecha (paneo, envíos, efectos…). Apretar una perilla regresa su valor (en Sends y Effects, prende o apaga). La perilla grande funciona como la del canal 1 del banco. |
| **Columna derecha:** Pan, Stereo, Sends, Effects, EQ, Free | Eligen qué hacen las perillas. Ver [Páginas de las perillas](#páginas-de-las-perillas). |
| **«** y **»** (transporte) | Retroceden o adelantan mientras los mantienes. |
| **Stop**, **Play** y **Rec** (transporte) | Parar, reproducir y prender la grabación de FL, como su botón de grabar (luego Play). |
| **LOOP** (transporte) | Prende o apaga la grabación en loop de FL; su luz lo indica. |
| **Rueda (jog)** | Sin modo, se mueve por la ventana activa de FL (en la Playlist, la posición de la canción). Con un modo prendido, hace lo de ese modo. **Apretarla** prende o apaga Scrub: la rueda usa su modo alterno. |
| **Zoom ↕** y **Zoom ↔** (a la derecha de la rueda) | Un toque prende el zoom (con luz) y giras la rueda: ↕ cambia la altura de los tracks y ↔ el zoom horizontal. Otro toque lo apaga. |
| **↕** y **↔** (a la izquierda de la rueda) | La rueda manda flechas, como las del teclado (sirve en menús y listas). Otro toque para salir. |
| **5 botones redondos de color** | Eligen la capa: roja, verde, azul, morada o amarilla. |
| **8 botones de colores** | Cambian según la capa. Ver [Los 8 botones de colores](#los-8-botones-de-colores). |
| **Pantallita** y **números rojos** | Ver [Lo que muestran las pantallas](#lo-que-muestran-las-pantallas). |

#### Los 8 botones de colores

Los botones 1 a 4 son la fila de arriba (de izquierda a derecha) y los 5 a 8 la de abajo. Los nombres son los de la plantilla de FL Studio de iCON. **↻** = modo de la rueda.

| Botón | Capa roja | Capa verde | Capa azul | Capa morada | Capa amarilla |
|---|---|---|---|---|---|
| 1 | Flip | Pattern ↻ | Display Mode | Save | Cut |
| 2 | Browser | Mixer ↻ | Shift | Menu | Copy |
| 3 | Main | Channel ↻ | Edison | Esc | Paste |
| 4 | Window ↻ | Tempo ↻ | Metronome | Enter | Insert |
| 5 | Smooth | Free 1 ↻ | TimeFormat | Move ↻ | Del |
| 6 | In | Free 2 ↻ | 3..2..1 | Link Ch | ItemMenu |
| 7 | Out | Free 3 ↻ | Mode | Mark ↻ | Undo |
| 8 | Select | Free 4 ↻ | Pattern Song | +Mark | Un/Redo |

**Capa roja**

- **Flip:** intercambia el fader y las perillas: el fader controla lo que hacían las perillas (por ejemplo el paneo). Mientras está prendido, la pantallita dice `FLIP` / `ON` y el fader no sigue al canal seleccionado.
- **Browser:** abre el Browser de FL.
- **Main:** abre el Channel Rack.
- **Window ↻:** la rueda pasa de una ventana de FL a otra.
- **Smooth:** prende o apaga el suavizado: lo que mueves llega a FL con una pequeña rampa en vez de saltar. Viene prendido, así que el primer toque lo apaga (`SMOOTH` / `OFF`).
- **In** y **Out:** mandan los comandos Punch In y Punch Out de FL.
- **Select:** mantenlo apretado mientras suena para hacer una selección en vivo.

**Capa verde**

- **Pattern ↻, Mixer ↻, Channel ↻ y Tempo ↻:** modos de la rueda (ver [Modos de la rueda](#modos-de-la-rueda)).
- **Free 1–4 ↻:** la rueda se vuelve un control libre que puedes ligar a cualquier perilla de FL con Link to controller.

**Capa azul**

- **Display Mode:** cambia cómo dibuja el controlador sus medidores (`METERS` / `HORIZ`, `VERT` u `OFF`). No cambia nada en FL.
- **Shift:** mantenlo apretado y toca otro botón (ver [Combinaciones con Shift](#combinaciones-con-shift)).
- **Edison:** abre Edison, el grabador y editor de audio de FL, en el canal seleccionado.
- **Metronome:** prende o apaga el metrónomo de FL.
- **TimeFormat:** el reloj de FL y los números rojos del Nano cambian entre compases y minutos:segundos.
- **3..2..1:** prende o apaga la cuenta antes de grabar.
- **Mode:** manda el comando Mode de FL.
- **Pattern Song:** cambia entre modo Pattern (repite el pattern) y modo Song (toca la Playlist).

**Capa morada**

- **Save:** guarda el proyecto. Con Shift: guarda una versión nueva con otro número, sin tocar la anterior.
- **Menu:** abre el menú de la ventana activa. Muévete con las flechas (↕ o ↔ a la izquierda de la rueda, y giras), confirma con **Enter** y cierra con **Esc**.
- **Esc** y **Enter:** cancelar y aceptar. Con Shift: responder "No" y "Sí" en los diálogos de FL.
- **Move ↻:** la rueda mueve lo seleccionado (clips o notas).
- **Link Ch:** manda los canales seleccionados del Channel Rack al canal seleccionado del Mixer (como Ctrl+L). Con Shift: uno por canal del Mixer, a partir del seleccionado.
- **Mark ↻:** la rueda salta al marcador anterior o siguiente. Con Shift: selecciona el tramo entre marcadores.
- **+Mark:** agrega un marcador en la Playlist (como Alt+T). Con Shift: un marcador alterno.

**Capa amarilla**

- **Cut, Copy, Paste, Insert y Del:** como esas teclas, en la ventana activa. Ojo en la Playlist: Insert corta el clip donde está el cursor y Del borra lo seleccionado.
- **ItemMenu:** abre el menú del elemento seleccionado.
- **Undo:** un toque deshace un paso (`UNDO` / `2/10`). Mantenlo y gira la rueda para recorrer el historial.
- **Un/Redo:** como Ctrl+Z en FL: deshace y, si lo tocas otra vez, rehace.
- Con Shift, las teclas amarillas son las teclas F de FL (ver [Combinaciones con Shift](#combinaciones-con-shift)).

#### Modos de la rueda

La rueda hace una cosa a la vez; estos botones eligen cuál.

- **Un toque** prende el modo: su botón se ilumina y la pantallita muestra el modo arriba y lo que vas cambiando abajo. Gira la rueda.
- **Otro toque** lo apaga. La pantallita dice el modo y `OFF` un momento.
- Si **mantienes** el botón mientras giras, el modo se apaga solo al soltar.
- Sin ningún modo, la rueda se mueve por la ventana activa de FL.

| Modo | Botón | Qué hace la rueda | Pantallita |
|---|---|---|---|
| Mixer | verde 2 | Va de canal en canal del Mixer; el fader lo sigue | `MIXER` / canal |
| Pattern | verde 1 | Pattern anterior o siguiente | `PATTERN` / pattern |
| Channel | verde 3 | Canal anterior o siguiente del Channel Rack | `CHANNEL` / canal |
| Tempo | verde 4 | Sube o baja el BPM (cambia tu canción) | `TEMPO` / BPM; el reloj de números rojos también muestra el BPM, por ejemplo `130.00` |
| Free 1–4 | verde 5 a 8 | Un control libre para Link to controller | `FREE 1` / `ON` |
| Window | roja 4 | Pasa de una ventana de FL a otra | `WINDOW` / ventana |
| Move | morada 5 | Mueve lo seleccionado | `MOVE` / `ON` |
| Mark | morada 7 | Salta entre marcadores (con Shift, selecciona) | `MARKER` / último salto |
| Undo | amarilla 7 (mantener) | Recorre el historial de deshacer | `UNDO` / paso |
| Zoom ↕ y ↔ | a la derecha de la rueda | Altura de los tracks / zoom horizontal | `ZOOM` / `ON` |
| Flechas ↕ y ↔ | a la izquierda de la rueda | Flechas, como el teclado | no cambia |
| Sin modo | — | Se mueve por la ventana activa: en la Playlist, la posición de la canción | vista normal |

#### Combinaciones con Shift

**Shift** es el botón 2 de la capa azul. Mantenlo apretado y toca el otro botón. Funciona directo con los botones que no cambian de capa (transporte, rueda, Mute, Solo…) y con los de la capa azul. Para usarlo con otra capa: mantén Shift, toca el botón redondo de esa capa y luego el botón.

| Combinación | Qué hace |
|---|---|
| Shift + Save (morada 1) | Guarda una versión nueva del proyecto (`NEW VER` / `OK`) |
| Shift + « o » | Reproduce a media velocidad o al doble mientras lo mantienes |
| Shift + LOOP | Prende o apaga el Snap, el imán de la cuadrícula (`SNAP` / `ON`) |
| Shift + Enter o Esc (morada 4 o 3) | Responde "Sí" o "No" en los diálogos de FL |
| Shift + Link Ch (morada 6) | Manda los canales seleccionados uno por canal del Mixer, a partir del seleccionado |
| Shift + +Mark (morada 8) | Agrega un marcador alterno |
| Shift + Solo | Solo que incluye también los canales que le mandan audio |
| Shift + rueda (modo Mark) | Selecciona el tramo entre marcadores |
| Shift + rueda (modo Zoom) | Zoom vertical con la rueda |
| Shift + rueda (sin modo) | El modo alterno de la rueda (como Scrub) |
| Shift + amarillas 1 a 8 | Las teclas F1 a F8 de FL (por ejemplo F5 Playlist, F6 Channel Rack, F7 Piano roll, F8 Plugin picker). F2 no se puede: es el mismo botón que Shift. |
| Mantener Undo (amarilla 7) + rueda | Recorre el historial de deshacer |
| Mantener un modo de la rueda + girar | Modo momentáneo: se apaga al soltar |

#### Páginas de las perillas

La columna derecha elige qué hacen las perillas. Las 4 perillas pequeñas controlan los canales 1 a 4 del banco (5 a 8 si prendes **5-8**); cambias de banco con `<<8` y `8>>`. Al elegir una página, la pantallita dice su nombre y `PAGINA` (por ejemplo `PAN` / `PAGINA`).

| Página | Cada perilla | Apretar la perilla | El fader |
|---|---|---|---|
| **Pan** | Paneo de su canal | Lo centra | Volumen del canal seleccionado |
| **Stereo** | Separación estéreo de su canal | La regresa a normal | Volumen del canal seleccionado |
| **Sends** | Perilla N: cuánto manda el canal seleccionado al canal N del banco | Prende o apaga ese envío | Volumen del canal seleccionado |
| **Effects** | Perilla N: mezcla del efecto en el slot N del canal seleccionado | Prende o apaga ese efecto | Volumen del canal seleccionado |
| **EQ** | El ecualizador del canal seleccionado (frecuencias y ancho de banda) | Regresa el valor | Ganancia de una banda del EQ |
| **Free** | Controles libres para ligar con Link to controller | Control libre | Control libre |

En **EQ** y **Free**, el fader no sigue al canal seleccionado.

#### Lo que muestran las pantallas

La pantallita del Nano tiene 2 líneas de 7 letras.

- **Vista normal:** arriba el canal seleccionado y abajo su volumen real en dB, por ejemplo `Kick` / `-5.2dB` (o `0.0dB`, `-INF dB`). Los nombres largos se acortan: "Insert 12" sale `Ins 12` y "Kick Drum" sale `KickDrm`. Mientras mueves el fader, el nombre se queda fijo y solo cambia el número.
- **Al tocar un botón:** un mensaje corto y completo durante unos 1.5 segundos; luego vuelve la vista normal.
- **Con un modo de la rueda:** arriba el modo y abajo lo que vas cambiando (ver [Modos de la rueda](#modos-de-la-rueda)).
- **Números rojos:** la posición de la canción, en compases o en minutos:segundos (se cambia con TimeFormat). En modo Tempo, el BPM (por ejemplo `130.00`).

| Pantallita (arriba / abajo) | Cuándo sale |
|---|---|
| `FL` / `LISTO` | Al arrancar el script (unos 2 segundos) |
| `FL` / `CERRADO` | Al cerrar FL |
| `MASTER` / `73%` | Mueves el fader con Master prendido |
| `METRO` / `ON` u `OFF` | Metronome (azul 4) |
| `3..2..1` / `ON` u `OFF` | Cuenta antes de grabar (azul 6) |
| `MODO` / `PATTERN` o `SONG` | Pattern Song (azul 8) |
| `TIEMPO` / `COMPAS` o `MIN:SEG` | TimeFormat (azul 5) |
| `LOOPREC` / `ON` u `OFF` | LOOP |
| `SNAP` / `ON` u `OFF` | Shift + LOOP |
| `MUTE`, `SOLO` o `REC ARM` / `ON` u `OFF` | Mute, Solo o Rec |
| `SAVE` / `OK` | Save (morada 1) |
| `NEW VER` / `OK` | Shift + Save |
| `UNDO` / `2/10` | Undo (amarilla 7): paso del historial / total |
| `UN/REDO` / `3/10` | Un/Redo (amarilla 8) |
| `FLIP` / `ON` | Flip prendido (se queda mientras esté prendido) |
| `SCRUB` / `ON` u `OFF` | Apretar la rueda |
| `SMOOTH` / `ON` u `OFF` | Smooth (roja 5) |
| `METERS` / `HORIZ`, `VERT` u `OFF` | Display Mode (azul 1) |
| `EDISON` / `LISTO` | Edison (azul 3) |
| `PAN` / `PAGINA` (o `STEREO`, `SENDS`, `EFFECTS`, `EQ`, `FREE`) | Eliges una página |
| `EQ` / canal | Mientras estás en la página EQ |
| `FREE` / `CTRL` | Mientras estás en la página Free |
| `Cut`, `Copy`, `Paste`, `Insert`, `Delete`, `Menu`, `Tools` | Botones de edición y de menús |
| `NO SEND` | En Sends, apretaste la perilla de un canal al que no se puede enviar |
| `Menu` / `View` (por ejemplo) | Recorres los menús de FL: FL manda su ayuda a la pantalla. Es normal y se quita sola. |

#### Pantalla externa Platform D3

- Es opcional. Se conecta con su cable al conector para pantalla que está atrás del Nano.
- Tiene 8 cuadros de 2 líneas de 7 letras: uno por canal del banco.
- Cada cuadro muestra arriba el nombre de su canal y abajo lo que hace su perilla en la página actual. En Pan: `C` es centro, `10%L` es 10 % a la izquierda y `25%R` es 25 % a la derecha. Un `-` quiere decir que no hay nada que controlar (por ejemplo un envío apagado o un slot de efecto vacío).
- En la página Effects, arriba sale el slot (`FX 1` a `FX 8`); en EQ, el nombre del parámetro; en Free, `Knob 1` a `Knob 8`.
- El cuadro donde está el fader muestra lo mismo que la pantallita del Nano: el canal seleccionado y su volumen, o el modo de la rueda.
- Los mensajes de los botones (`METRO ON`, `MUTE ON`…) salen en los 8 cuadros.
- Al girar una perilla, solo cambia su cuadro.
- Al abrir FL, los 8 cuadros repiten lo mismo hasta que [tocas el fader una vez](#primer-uso-toca-el-fader).
- **Sin la D3:** la pantallita del Nano muestra el cuadro del fader (el canal seleccionado y su volumen). El valor de las otras perillas lo ves en FL. Si prefieres verlo en la pantallita, lee la opción `NanoStrips` en [Para desarrolladores](#para-desarrolladores).

#### Recetas

**Mezclar canal por canal**

1. Toca el botón redondo verde (capa verde) y luego **Mixer** (botón 2).
2. Gira la rueda hasta el canal que quieres: el fader se va a su volumen y la pantallita dice su nombre.
3. Ajusta con el fader; usa Mute, Solo y Rec para ese canal.
4. Toca **Mixer** otra vez para que la rueda regrese a lo normal.

**Controlar la perilla de un plugin (Link to controller)**

1. Toca **Free** en la columna derecha, para que las perillas del Nano no estén haciendo otra cosa. (O prende **Free 1** de la capa verde para usar la rueda.)
2. En FL, haz clic derecho en la perilla del plugin → **Link to controller…**
3. Mueve la perilla del Nano (o gira la rueda): FL la detecta sola. Haz clic en **Accept**.

Más recetas en el [tutorial interactivo](https://noisybeats03-eng.github.io/icon-platform-nano-air-fl-studio/): grabar automatización con el fader, grabar en loop, grabar solo una parte con marcadores y grabar con Edison.

### Preguntas frecuentes

#### ¿El iCON Platform Nano Air funciona con FL Studio?

Sí. En modo Mackie Control (MCP), FL lo puede manejar con su script Mackie Control Universal, pero ese script está hecho para consolas de 8 faders con una pantalla larga. Este script lo adapta al Nano: un solo fader que sigue al canal seleccionado y una pantallita de 2 líneas de 7 letras que sí se entiende.

#### Mi iCON Platform Nano Air no funciona en FL Studio, ¿qué reviso?

Casi siempre es una de estas cosas:

- El Nano no está en modo MCP (ver [Poner el Nano en modo MCP](#poner-el-nano-en-modo-mcp)).
- Falta la salida: en **Output**, el Nano debe tener el mismo **Port** que en **Input**.
- Hiciste clic en **Enable** después de elegir el Controller type y lo apagaste.
- Cambiaste de inalámbrico a cable (o al revés): el Nano tiene otro nombre en cada forma y hay que configurar cada nombre una vez.

Todo está explicado en [Si algo no funciona](#si-algo-no-funciona).

#### ¿Cómo configuro el controlador iCON Platform Nano Air en FL Studio?

Instala el script y luego, en **OPTIONS > MIDI settings** (F10): en **Input** elige el Nano, **Controller type** = **iCON Platform Nano Air (custom)** y **Port** = 1; en **Output**, el mismo Nano con **Port** = 1. Paso a paso en el [manual de instalación](#manual-de-instalación).

#### ¿El fader motorizado puede seguir al canal seleccionado?

Sí, es lo principal de este script: eliges un canal en el Mixer de FL y el fader se va a su volumen; Mute, Solo y Rec también trabajan sobre ese canal. Con el script Mackie Control Universal de FL, el fader se queda fijo en un canal del banco.

#### ¿Funciona con la pantalla iCON Platform D3?

Sí, es opcional: cada uno de sus 8 cuadros muestra un canal del banco. Ver [Pantalla externa Platform D3](#pantalla-externa-platform-d3).

#### ¿Funciona en Mac? ¿Con qué versión de FL Studio?

Se probó con FL Studio 2025 en Windows. En macOS no se ha probado; el script es Python normal y debería funcionar igual (la carpeta va en `~/Documents/Image-Line/FL Studio/Settings/Hardware`).

#### ¿Sirve para otros controladores Mackie Control?

Está hecho y probado solo para el Platform Nano Air (un fader y una pantallita de 2 líneas de 7 letras). Para consolas de 8 faders, usa el script Mackie Control Universal de FL.

#### ¿Es gratis? ¿Es oficial?

Es gratis, con licencia MIT para el trabajo propio de este repositorio (ver [Licencia](#licencia)). No es oficial: no tiene relación con iCON Pro Audio ni con Image-Line.

#### ¿Cómo regreso al script original de FL?

En **OPTIONS > MIDI settings**, cambia el **Controller type** del Nano a **Mackie Control Universal**. Ver [Volver al script original de FL](#volver-al-script-original-de-fl).

### Si algo no funciona

**No aparece "iCON Platform Nano Air (custom)" en Controller type**

- La carpeta no está en el lugar correcto. Debe quedar `...\FL Studio\Settings\Hardware\iCON Platform Nano Air\device_iCON_PlatformNanoAir.py`.
- Errores típicos: copiaste el ZIP sin descomprimir; quedó una carpeta de más en medio; la pusiste en otra carpeta de datos (revisa **OPTIONS > File settings** → **User data folder**).
- Después, cierra y abre FL, o haz clic en **Update MIDI scripts** en **OPTIONS > MIDI settings**.

**El Nano no aparece en las listas de MIDI settings**

- Revisa que esté prendido y conectado. Por inalámbrico, la pantallita debe decir **Paired**.
- Cierra FL, prende y conecta el Nano, y abre FL otra vez.
- Prueba otro puerto USB, directo a la computadora (sin hub ni extensión).

**FL no le hace caso al Nano**

- En **OPTIONS > MIDI settings**, en **Input**: el nombre del Nano con Controller type **iCON Platform Nano Air (custom)**, la luz de **Enable** prendida y **Port** 1. En **Output**: el mismo nombre con **Port** 1.
- Si hiciste clic en Enable después de elegir el Controller type, lo apagaste: haz clic otra vez para que se prenda la luz.

**Funcionaba y de repente parece que se perdió la configuración**

- Seguramente cambiaste de inalámbrico a cable (por ejemplo, se acabó la batería) o al revés. El Nano tiene otro nombre en cada forma, y FL guarda la configuración por nombre. Configura el otro nombre una vez (ver [Configurar FL Studio](#configurar-fl-studio)).

**Los botones hacen cosas raras o no coinciden con la plantilla**

- El Nano no está en modo MCP. Apágalo, préndelo y elige MCP (ver [Poner el Nano en modo MCP](#poner-el-nano-en-modo-mcp)).
- Revisa qué capa de color está elegida.

**La pantallita no muestra nada de FL, o el fader no se mueve solo**

- Falta la salida: en **OPTIONS > MIDI settings**, en **Output**, el nombre del Nano debe tener el mismo **Port** que en Input.
- ¿Está prendido **Flip** (roja 1)? La pantallita dice `FLIP` / `ON`. Tócalo para apagarlo.
- ¿Está prendido **Master**? Tócalo para regresar al canal.
- ¿Estás en la página **EQ** o **Free**? Ahí el fader no sigue al canal seleccionado: elige Pan, Stereo, Sends o Effects.

**La pantalla del Nano no prende**

- Revisa el switch de atrás (el del extremo izquierdo cuando miras la parte de atrás): **–** es prendido y **O** apagado.
- Si se acabó la batería, conéctalo por cable USB: funciona igual y se va cargando.

**Por inalámbrico no se conecta**

- Conecta el receptor antes de prender el Nano y espera a que diga **Paired**. La luz Paired del receptor debe quedarse fija; si parpadea, no se han conectado.
- Apaga y prende el Nano, o prueba otro puerto USB.

**Los 8 cuadros de la Platform D3 muestran lo mismo**

- Es normal al abrir FL. Toca el fader una vez.

**La pantalla muestra nombres de menús de FL (por ejemplo `Menu` / `View`)**

- Es normal: mientras recorres los menús de FL, FL manda su ayuda a la pantalla. Se quita sola.

**En Script output dice "Invalid mixer track nr 501"**

- Es un aviso sin importancia que viene del script original de FL. Puedes ignorarlo.

**Moví el fader y el canal nuevo no cambió de volumen**

- Es a propósito: si cambias de canal con el dedo en el fader, el canal nuevo no se toca hasta que el fader llega a su nivel o sueltas el fader. Suelta y vuelve a tocar. Además, los movimientos muy pequeños de un dedo apoyado se ignoran.

**La rueda no hace lo que espero, o el tempo cambió solo**

- Hay un modo de la rueda prendido: su botón tiene luz y la pantallita dice el modo. Tócalo otra vez para apagarlo.
- Si cambiaste algo sin querer (por ejemplo el tempo), usa Undo (amarilla 7).

**Un botón hizo algo inesperado**

- Muchos botones actúan sobre la ventana activa de FL. Mira el mensaje de ayuda de FL, arriba a la izquierda: dice qué acaba de pasar. Para deshacerlo, usa Undo (amarilla 7).

**En Script output sale un error (un texto que dice Traceback o Error)**

- Copia el texto completo y repórtalo en [Issues](https://github.com/noisybeats03-eng/icon-platform-nano-air-fl-studio/issues). Mientras tanto, puedes [volver al script original de FL](#volver-al-script-original-de-fl).

### Actualizar a una versión nueva

1. Descarga el ZIP nuevo de la página de la [última versión](https://github.com/noisybeats03-eng/icon-platform-nano-air-fl-studio/releases/latest) y descomprímelo.
2. Cierra FL Studio.
3. Copia la carpeta nueva `iCON Platform Nano Air` en `...\FL Studio\Settings\Hardware`, en el mismo lugar que la anterior. Cuando Windows pregunte, elige **Reemplazar el archivo en el destino** (en inglés: **Replace the file in the destination**).
4. Abre FL Studio. No tienes que configurar nada otra vez: el Controller type se llama igual.
5. Revisa que **VIEW > Script output** diga **OnInit ready**.

Para saber si hay una versión nueva, revisa la página de versiones (Releases). Si tienes cuenta de GitHub, puedes usar **Watch > Custom > Releases** en este repositorio para que te avise. Lo que cambió en cada versión está en [CHANGELOG.md](CHANGELOG.md).

### Volver al script original de FL

Puedes cambiar entre este script y el de FL cuando quieras, sin borrar nada.

1. Abre **OPTIONS > MIDI settings**.
2. En **Input**, haz clic en el nombre del Nano.
3. En **Controller type**, elige **Mackie Control Universal**.
4. Revisa la luz de **Enable** y el **Port**, como en [Configurar FL Studio](#configurar-fl-studio).
5. Si usas cable e inalámbrico, repite con el otro nombre.

Para regresar a este script, elige otra vez **iCON Platform Nano Air (custom)**.

### Desinstalar

1. En **OPTIONS > MIDI settings**, para cada nombre del Nano, cambia el **Controller type** a otro (por ejemplo **Mackie Control Universal**).
2. Cierra FL Studio.
3. Borra la carpeta `iCON Platform Nano Air` de `...\FL Studio\Settings\Hardware`.
4. Abre FL Studio otra vez.

### Créditos y aviso legal

- Basado en el script **Mackie Control Universal** que trae FL Studio (`device_MackieCU.py`, versión 2026.1), © Image-Line Software. Los cambios para el Nano Air están anotados al principio del archivo del script y explicados en [CHANGELOG.md](CHANGELOG.md).
- Proyecto independiente y no oficial: no está afiliado a iCON Pro Audio ni a Image-Line, y ellos no lo patrocinan ni lo revisan. Si algo falla con este script, no le escribas al soporte de iCON ni al de Image-Line: abre un [issue](https://github.com/noisybeats03-eng/icon-platform-nano-air-fl-studio/issues) aquí.
- iCON, Platform Nano Air, Platform D3, FL Studio, Edison, Image-Line y Mackie Control son marcas de sus respectivos dueños. Se mencionan solo para decir con qué funciona este script.
- Los nombres de los botones de colores son los de la plantilla de FL Studio de iCON. Este proyecto no copia el manual de iCON ni usa sus logos.
- Se ofrece tal cual, sin garantía. Guarda tu proyecto seguido.

### Licencia

Licencia MIT ([LICENSE](LICENSE)) para el trabajo propio de este repositorio: los cambios al script, la documentación, el tutorial y las herramientas de `dev/`. Las partes que vienen del script de Image-Line siguen siendo de Image-Line y no están cubiertas por esa licencia. Los detalles y avisos están en [NOTICE.md](NOTICE.md).

### Para desarrolladores

**Qué hay en el repositorio**

| Ruta | Qué es |
|---|---|
| `iCON Platform Nano Air/device_iCON_PlatformNanoAir.py` | El script (lo único que se instala) |
| `docs/index.html` | El tutorial interactivo en español (GitHub Pages) |
| `dev/` | Herramientas para probar el script fuera de FL ([dev/README.md](dev/README.md)) |
| `CHANGELOG.md` | Lo que cambió en cada versión |
| `LICENSE`, `NOTICE.md` | Licencia y avisos |

**Opciones del script.** Al principio del archivo hay opciones que puedes cambiar. Ábrelo con el Bloc de notas (clic derecho → **Abrir con** → **Bloc de notas**), cambia el valor después del `=`, guarda y reinicia FL. Al actualizar, el archivo nuevo trae otra vez los valores normales.

| Opción | Normal | Qué hace |
|---|---|---|
| `NanoLatchJogSources` | `True` | Modos de la rueda con un toque. `False` = como FL: hay que mantenerlos apretados. |
| `NanoFollowSelected` | `True` | El fader, Mute, Solo, Rec y la pantalla siguen al canal seleccionado. `False` = fijos en su canal del banco, como FL. |
| `NanoScreen` | `True` | La pantallita la dibuja este script. `False` = los textos originales de FL. |
| `NanoStrips` | `True` | Platform D3: un canal por cuadro. `False` = los 8 cuadros repiten la pantallita del Nano (útil sin D3: el valor de cualquier perilla sale en la pantallita). |
| `NanoFaderDeadband` | `48` | Cuánto movimiento de un dedo apoyado se ignora (en una escala de 0 a 16383). |
| `NanoFaderPickup` | `150` | Qué tan cerca debe llegar el fader al nivel del canal nuevo para tomarlo. |
| `NanoFaderKick` | `False` | Empujón al motor del fader en movimientos pequeños. |
| `NanoDebug` | `False` | Mensajes de diagnóstico en **VIEW > Script output**. |

**Herramientas en `dev/`.** Necesitan Python 3 y FL Studio instalados: usan los archivos `midi.py` y `utils.py` de tu FL (la ruta está en la línea `FL_LIB` al principio de `dev/flsim.py`). Abre una terminal en la carpeta `dev` y usa siempre `python -I -B` (`-B` evita que se cree una carpeta `__pycache__` junto al script).

- `flsim.py`: un simulador de la API de scripts de FL que corre 112 pruebas del script. Debe terminar con `ALL PASS`.
  ```text
  python -I -B flsim.py "..\iCON Platform Nano Air\device_iCON_PlatformNanoAir.py"
  ```
- `gen_screen_data.py` y `embed_screen_data.py`: graban lo que muestran las dos pantallas con cada uno de los 69 controles (corriendo el script en el simulador) y lo meten en el tutorial.
  ```text
  python -I -B gen_screen_data.py flsim.py "..\iCON Platform Nano Air\device_iCON_PlatformNanoAir.py" screen_data.json
  python -I -B embed_screen_data.py ..\docs\index.html screen_data.json
  ```
- `flicker_probe.py`: imprime la línea de tiempo de la pantallita para revisar parpadeos.
  ```text
  python -I -B flicker_probe.py flsim.py "..\iCON Platform Nano Air\device_iCON_PlatformNanoAir.py"
  ```

Todos los detalles (cómo funciona el simulador, cómo probar un cambio en FL y cómo armar el ZIP de una versión) están en [dev/README.md](dev/README.md). Probado con la API de scripts de FL versión 40 (FL Studio 2025). Para reportar un problema o proponer un cambio, abre un [issue](https://github.com/noisybeats03-eng/icon-platform-nano-air-fl-studio/issues).

---

## English

A complete step-by-step manual to install and use the script. No programming needed.

### Contents

1. [What it is and what it improves](#what-it-is-and-what-it-improves)
2. [Installation manual](#installation-manual)
    - [What you need](#what-you-need)
    - [Download](#download)
    - [Install the script](#install-the-script)
    - [Connect the Nano](#connect-the-nano)
    - [Put the Nano in MCP mode](#put-the-nano-in-mcp-mode)
    - [Set up FL Studio](#set-up-fl-studio)
    - [Check that it works](#check-that-it-works)
    - [First use: touch the fader](#first-use-touch-the-fader)
3. [How to use it](#how-to-use-it)
    - [The parts of the Nano](#the-parts-of-the-nano)
    - [The 8 colored keys](#the-8-colored-keys)
    - [Wheel modes](#wheel-modes)
    - [Shift combinations](#shift-combinations)
    - [Knob pages](#knob-pages)
    - [What the screens show](#what-the-screens-show)
    - [Platform D3 external display](#platform-d3-external-display)
    - [Recipes](#recipes)
4. [FAQ](#faq)
5. [Troubleshooting](#troubleshooting)
6. [Update to a new version](#update-to-a-new-version)
7. [Go back to FL's original script](#go-back-to-fls-original-script)
8. [Uninstall](#uninstall)
9. [Credits and disclaimer](#credits-and-disclaimer)
10. [License](#license)
11. [For developers](#for-developers)

### What it is and what it improves

The **iCON Platform Nano Air** is a controller with one motorized fader, a jog wheel, 5 knobs and 8 colored keys that, with their 5 layers, give 40 functions. It has a small screen of 2 lines of 7 characters and a red LED digit display. It works by USB cable or wirelessly, on battery.

It talks to FL Studio in the **Mackie Control** "language". FL already comes with a script for that language (**Mackie Control Universal**), but it was made for big 8-fader consoles with a long display, and several things don't work well on the Nano.

This project is an **FL Studio script** (a Python file that FL loads by itself), based on FL's own script and adapted to the Nano. It is not a program: you install it by copying a folder.

What it improves:

- **The motorized fader follows the selected track.** Pick a track in FL's Mixer (with the mouse, the wheel or `|<` `>|`) and the fader moves to its volume. Mute, Solo, Rec and the screen work on that track too. This happens on the Pan, Stereo, Sends and Effects pages (not with Flip, nor on EQ or Free). With **Master**, the fader controls FL's main volume. (With FL's script, the fader stayed on one fixed track of the bank.)
- **A readable screen.** The top line shows the selected track (long names are squeezed to 7 characters: "Insert 12" becomes `Ins 12`) and the bottom line its real volume in dB. Pressing a key shows a short, whole message for 1.5 seconds: `METRO ON`, `LOOPREC OFF`, `SNAP ON`, `MUTE ON`, `SAVE OK`… No flicker.
- **One-tap wheel modes.** Pattern, Mixer, Channel, Tempo, Free 1–4, Window, Move and Mark: one tap turns the mode on and another tap turns it off. If you hold the key while turning the wheel, the mode turns off when you let go. (With FL's script you had to keep them held.)
- **Zoom on both axes.** Zoom ↕ changes the track height and Zoom ↔ the horizontal zoom. It stays on until you turn it off. (With FL's script, both did horizontal zoom.)
- **One-tap Undo.** Yellow key 7 undoes one step; hold it and turn the wheel to walk through the undo history.
- **LOOP records in a loop.** The LOOP key turns loop recording on or off; Shift + LOOP turns Snap on or off. (With FL's script, LOOP was Snap.)
- **BPM on the red digits.** In Tempo mode, the digit display shows the tempo (for example `130.00`).
- **Platform D3 external display (optional):** one track of the bank in each square.
- **A steadier fader.** It ignores the tiny movements of a resting finger. If you change track with your finger on the fader, the new track isn't changed until the fader reaches its level or you let go.
- **Bugs of FL's script fixed:** Shift + Solo gave an error; releasing Shift before an F key triggered something else (Undo); holding Undo and turning the wheel gave an error; the fader value on the Free page was wrong.

The 40 colored-key functions match iCON's FL Studio overlay that comes with the Nano.

### Installation manual

How to install and set up the iCON Platform Nano Air script in FL Studio, step by step.

**In short** (if you know the drill):

1. Download the ZIP from the [latest release](https://github.com/noisybeats03-eng/icon-platform-nano-air-fl-studio/releases/latest) and unzip it.
2. Copy the `iCON Platform Nano Air` folder into `Documents\Image-Line\FL Studio\Settings\Hardware`.
3. Put the Nano in **MCP** mode.
4. In FL, **OPTIONS > MIDI settings**: in **Input** pick the Nano, **Controller type** = **iCON Platform Nano Air (custom)** and **Port** = 1; in **Output**, the same Nano with **Port** = 1.
5. **VIEW > Script output** must say **OnInit ready**. Touch the fader once.

Every step is explained below.

#### What you need

- An **iCON Platform Nano Air** with its USB cable or its wireless USB receiver.
- **FL Studio.** Tested with **FL Studio 2025 on Windows** (FL scripting API version 40). Other FL Studio versions and macOS are not tested (the script is plain Python, so it should work on a Mac).
- Optional: the **iCON Platform D3** external display.
- Recommended: the **FL Studio overlay** that comes with the Nano, so you can read the name of each colored key.
- You do **not** need to install Python (FL already includes it), drivers (the Nano works without drivers) or iCON's iMap software.

#### Download

**Option A (recommended): the release ZIP**

1. Open the [latest release](https://github.com/noisybeats03-eng/icon-platform-nano-air-fl-studio/releases/latest) page.
2. Scroll down to **Assets** and click `iCON-Platform-Nano-Air-FL-Studio-v1.0.0.zip` (newer versions have a different number). Don't use the "Source code" files.
3. The ZIP goes to your **Downloads** folder.
4. Right-click the ZIP → **Extract All…** → **Extract**.
5. A new folder opens. Inside it is the `iCON Platform Nano Air` folder, which contains the file `device_iCON_PlatformNanoAir.py`. That folder is the only thing you install.

**Option B: the whole repository**

1. On the repository's main page, click the green **Code** button → **Download ZIP**.
2. Unzip it the same way (right-click → **Extract All…**).
3. Open the `icon-platform-nano-air-fl-studio-main` folder: the `iCON Platform Nano Air` folder is inside.

> Windows sometimes hides the `.py` ending: the file may show as `device_iCON_PlatformNanoAir`, of type "Python File" or "PY File". It's the same file. You don't need to open it.

#### Install the script

There is no installer: you just copy one folder into FL's script folder.

**Step 1. Find your FL user data folder**

1. Open FL Studio.
2. Go to **OPTIONS > File settings**.
3. Look at the **User data folder** field. That is your FL data folder. If you never changed it, it is `Documents\Image-Line`.

**Step 2. Open the Hardware folder**

Scripts go in `FL Studio\Settings\Hardware`, inside your data folder. With the default data folder, the full path is:

```text
C:\Users\<your user name>\Documents\Image-Line\FL Studio\Settings\Hardware
```

The easy way on Windows:

1. Open **File Explorer**.
2. Click the address bar (at the top), paste this and press **Enter**:
   ```text
   %USERPROFILE%\Documents\Image-Line\FL Studio\Settings\Hardware
   ```
3. If Windows says it doesn't exist, use the path FL showed you in **User data folder** and go into `FL Studio` → `Settings` → `Hardware`. This happens if you changed the data folder (for example to another drive) or if your Documents folder is in OneDrive.
4. If there is no `Hardware` folder inside `Settings`, create it: right-click → **New** → **Folder**, named exactly `Hardware`.

On macOS (not tested): in Finder, use **Go > Go to Folder…**, paste `~/Documents/Image-Line/FL Studio/Settings/Hardware` and press Enter.

**Step 3. Copy the folder**

1. Copy the whole `iCON Platform Nano Air` folder (not just the file) into `Hardware`.
2. It must end up like this:
   ```text
   ...\FL Studio\Settings\Hardware\iCON Platform Nano Air\device_iCON_PlatformNanoAir.py
   ```
3. Make sure there is no extra folder in between, such as `Hardware\iCON-Platform-Nano-Air-FL-Studio-v1.0.0\iCON Platform Nano Air\...`. FL won't find it that way.

**Step 4. Make FL see it**

- Close FL Studio and open it again, **or**
- in **OPTIONS > MIDI settings**, click **Update MIDI scripts**.

#### Connect the Nano

The Nano runs on battery. Its power switch is on the **back**: it's the switch at the far left when you look at the back panel. The side with the dash (**–**) is on and the side with the **O** is off.

**By USB cable**

1. Connect the USB cable that comes with the Nano to the computer and to the blue USB port on the back of the Nano. Plug it straight into the computer, without a hub or extension cable.
2. Switch the Nano on with the switch on the back.
3. The computer finds it by itself. While it's on the cable, the battery charges as you use it.

**Wireless (with the USB receiver)**

1. Plug iCON's wireless receiver (the USB dongle that comes with the Nano) into a USB port of the computer.
2. Switch the Nano on with the switch on the back.
3. Wait a few seconds: the Nano and the receiver pair by themselves. When the Nano's screen says **Paired**, they are connected. The receiver's **Paired** light stays on; if it blinks, they are not connected yet.

**The battery**

- The Nano's 4 battery LEDs show the charge: green (76–100 %), green (51–75 %), orange (26–50 %) and red (under 25 %). If the red one blinks, less than 5 % is left: charge it now.
- To charge it, connect it by USB cable to the computer (it charges while you use it), or plug a phone USB charger or a power bank into the mini USB port on the back.
- According to iCON, a full battery lasts about 5 to 6 hours.
- If the battery runs out, connect it by cable: it works the same. Read the note about the two names in [Set up FL Studio](#set-up-fl-studio).

#### Put the Nano in MCP mode

The Nano has several modes, one per kind of music software. FL Studio uses **MCP** mode (Mackie Control). You only do this once: the Nano remembers the last mode you chose.

1. Switch the Nano off with the switch on the back, and switch it on again.
2. When it starts, the Nano lets you choose the mode for a few seconds. The screen shows the current mode, for example **(1) MCP**. At that moment, keys **1, 2 and 3 of the top row** of the 8 colored keys work as **<<**, **>>** and **DAW Mode**. (With the FL overlay on, on the red layer they are labeled Flip, Browser and Main.)
3. Press **<<** or **>>** until the screen says **MCP**. The modes are: (1) MCP, (2) LogicPro, (3) HUI and (4) User-Def.
4. Press **DAW Mode** to choose it.
5. Done. From now on, don't touch anything when you switch it on: after a few seconds it goes into the last mode you chose.

- If it goes into another mode before you can choose, switch it off and try again.
- iCON lists FL Studio under MCP mode. Don't use LogicPro, HUI or User-Def with this script.
- The mode can also be set with iCON's iMap software (**Control Mode** → **1) MCP** → **Send Data**), but you don't need it.
- iCON's tip: for the most stable start, switch the Nano on and choose the mode **before** you open FL.

#### Set up FL Studio

You do this once for each name of the Nano (read the note at the end of this section).

1. Switch on and connect the Nano, then open FL Studio.
2. Open **OPTIONS > MIDI settings** (or press **F10**).
3. In the **Input** list, click the Nano's name:
   - wireless (receiver): **PlatformNano Air V1.02**
   - USB cable: **PlatformNano(A) V2.05**

   With other firmware the name may be a little different: look for the one that starts with **PlatformNano**.
4. In **Controller type**, choose **iCON Platform Nano Air (custom)**.
5. Look at the **Enable** light: it must be on.

   **Careful:** choosing the Controller type already switches Enable on. If you click Enable after that, you switch it **off**. Click Enable only if its light is off.
6. Set **Port** to **1**. Any number that no other controller uses will work, but the Nano's input and output must use the same number.
7. In the **Output** list, click the same Nano name and set **Port** to the same number (**1**).
8. Close the window.

If **iCON Platform Nano Air (custom)** is not in the list, see [Troubleshooting](#troubleshooting).

> **Do you use both cable and wireless?** FL keeps MIDI settings per device *name*, and the Nano has one name on the cable and another one wirelessly. Set up both once: connect it one way and do steps 3 to 7, then connect it the other way and repeat them. Otherwise, the day the battery dies and you plug in the cable, it will look as if your setup was lost.

#### Check that it works

1. In FL, open **VIEW > Script output**.
2. Click the tab with the Nano's name. It must say **OnInit ready**.
3. Look at the Nano's screen. When the script starts (when FL opens or when you choose the Controller type) it says **FL** / **LISTO** ("ready") for about 2 seconds. Then the top line shows the selected mixer track and the bottom line its volume in dB, for example **Kick** / **-5.2dB**.
4. In FL's Mixer, click another track: the fader moves by itself to its volume and the screen shows the new name.
5. Move the fader: that track's volume changes in FL.

If any of this doesn't happen, see [Troubleshooting](#troubleshooting).

#### First use: touch the fader

Every time you open FL, **touch the fader once**. Just touch it; you don't have to move it.

- This way the script learns where in the bank of 8 tracks the Nano's fader is.
- It matters most with the Platform D3 external display: until you touch the fader, its 8 squares repeat the same view; after that, each square shows its own track.
- In **VIEW > Script output**, a line that starts with `Nano Air screen: fader on strip` appears.

**Quick test:** press the round blue key (blue layer), then key 4 of the top row, **Metronome**. The screen says **METRO** / **ON** and FL's metronome turns on. Press it again: **METRO** / **OFF**.

### How to use it

Here is the summary. To see it with drawings, open the [interactive tutorial](https://noisybeats03-eng.github.io/icon-platform-nano-air-fl-studio/) (in Spanish): click any key of the drawn Nano to read what it does, and the drawn small screen and Platform D3 play what they should show. Its section "Lo que dicen las pantallas" ("what the screens say") lists all 69 controls, and it also covers the wheel modes, Shift combinations, knob pages, recipes and troubleshooting.

Three words used a lot:

- **Selected track:** the mixer track that is selected in FL.
- **Bank:** the group of 8 mixer tracks that the knobs control. You change bank with `<<8` and `8>>`.
- **Layer:** the color you choose with the 5 round keys. It changes what the 8 colored keys do.

The screen uses a few Spanish words: `LISTO` = ready, `CERRADO` = closed, `MODO` = mode, `TIEMPO` = time format, `COMPAS` = bars, `MIN:SEG` = min:sec, `PAGINA` = page.

#### The parts of the Nano

| Part | What it does |
|---|---|
| **Fader** (motorized, touch-sensitive) | Volume of the selected track. It moves by itself when you change track. While you touch it, FL doesn't move it. |
| **Master** | The fader switches to FL's main volume (the screen shows `MASTER` and the %). Press it again to go back to the track. |
| **`\|<`** and **`>\|`** (left column) | Move the fader to the previous or next track of the bank. FL selects that track and shows the Mixer. |
| **`<<8`** and **`8>>`** (left column) | Previous or next bank: the knobs jump 8 tracks. |
| **5-8** (top of the left column) | Switches the 4 small knobs from tracks 1–4 of the bank to 5–8, and back. |
| **Lock** (padlock, bottom of the left column) | A function of the Nano itself; it sends nothing to FL. |
| **Mute**, **Solo** and **Rec** (the round key with a red dot, below Solo) | Mute, solo and arm for recording the selected track. |
| **Big knob and 4 small knobs** | Do what the page chosen in the right-hand column says (pan, sends, effects…). Pressing a knob resets its value (on Sends and Effects, it switches on or off). The big knob works like the knob of track 1 of the bank. |
| **Right-hand column:** Pan, Stereo, Sends, Effects, EQ, Free | Choose what the knobs do. See [Knob pages](#knob-pages). |
| **«** and **»** (transport) | Rewind or fast-forward while you hold them. |
| **Stop**, **Play** and **Rec** (transport) | Stop, play, and switch on FL's recording, like FL's record button (then Play). |
| **LOOP** (transport) | Turns FL's loop recording on or off; its light shows the state. |
| **Jog wheel** | With no mode, it moves through FL's focused window (in the Playlist, the song position). With a mode on, it does what that mode says. **Pressing it** turns Scrub on or off: the wheel uses its alternate mode. |
| **Zoom ↕** and **Zoom ↔** (right of the wheel) | One tap turns zoom on (lit) and you turn the wheel: ↕ changes the track height and ↔ the horizontal zoom. Another tap turns it off. |
| **↕** and **↔** (left of the wheel) | The wheel sends arrow keys, like the keyboard (useful in menus and lists). Tap again to leave. |
| **5 round colored keys** | Choose the layer: red, green, blue, purple or yellow. |
| **8 colored keys** | Change with the layer. See [The 8 colored keys](#the-8-colored-keys). |
| **Small screen** and **red digits** | See [What the screens show](#what-the-screens-show). |

#### The 8 colored keys

Keys 1 to 4 are the top row (left to right) and 5 to 8 the bottom row. The names are those of iCON's FL Studio overlay. **↻** = wheel mode.

| Key | Red layer | Green layer | Blue layer | Purple layer | Yellow layer |
|---|---|---|---|---|---|
| 1 | Flip | Pattern ↻ | Display Mode | Save | Cut |
| 2 | Browser | Mixer ↻ | Shift | Menu | Copy |
| 3 | Main | Channel ↻ | Edison | Esc | Paste |
| 4 | Window ↻ | Tempo ↻ | Metronome | Enter | Insert |
| 5 | Smooth | Free 1 ↻ | TimeFormat | Move ↻ | Del |
| 6 | In | Free 2 ↻ | 3..2..1 | Link Ch | ItemMenu |
| 7 | Out | Free 3 ↻ | Mode | Mark ↻ | Undo |
| 8 | Select | Free 4 ↻ | Pattern Song | +Mark | Un/Redo |

**Red layer**

- **Flip:** swaps the fader and the knobs: the fader controls what the knobs did (for example pan). While it's on, the screen says `FLIP` / `ON` and the fader doesn't follow the selected track.
- **Browser:** opens FL's Browser.
- **Main:** opens the Channel Rack.
- **Window ↻:** the wheel goes from one FL window to the next.
- **Smooth:** turns control smoothing on or off: what you move reaches FL with a short ramp instead of jumping. It starts on, so the first tap turns it off (`SMOOTH` / `OFF`).
- **In** and **Out:** send FL's Punch In and Punch Out commands.
- **Select:** hold it while the song plays to make a live selection.

**Green layer**

- **Pattern ↻, Mixer ↻, Channel ↻ and Tempo ↻:** wheel modes (see [Wheel modes](#wheel-modes)).
- **Free 1–4 ↻:** the wheel becomes a free control that you can link to any FL knob with Link to controller.

**Blue layer**

- **Display Mode:** changes how the controller draws its meters (`METERS` / `HORIZ`, `VERT` or `OFF`). It changes nothing in FL.
- **Shift:** hold it and press another key (see [Shift combinations](#shift-combinations)).
- **Edison:** opens Edison, FL's audio recorder and editor, on the selected track.
- **Metronome:** turns FL's metronome on or off.
- **TimeFormat:** FL's clock and the Nano's red digits switch between bars and minutes:seconds.
- **3..2..1:** turns the recording count-in on or off.
- **Mode:** sends FL's Mode command.
- **Pattern Song:** switches between Pattern mode (loops the pattern) and Song mode (plays the Playlist).

**Purple layer**

- **Save:** saves the project. With Shift: saves a new version with a new number, without touching the previous one.
- **Menu:** opens the menu of the focused window. Move with the arrows (↕ or ↔ left of the wheel, then turn it), confirm with **Enter** and close with **Esc**.
- **Esc** and **Enter:** cancel and accept. With Shift: answer "No" and "Yes" in FL's dialogs.
- **Move ↻:** the wheel moves the selection (clips or notes).
- **Link Ch:** routes the selected Channel Rack channels to the selected mixer track (like Ctrl+L). With Shift: one per mixer track, starting from the selected one.
- **Mark ↻:** the wheel jumps to the previous or next marker. With Shift: selects the part between markers.
- **+Mark:** adds a marker in the Playlist (like Alt+T). With Shift: an alternate marker.

**Yellow layer**

- **Cut, Copy, Paste, Insert and Del:** like those keyboard keys, in the focused window. Careful in the Playlist: Insert splits the clip at the cursor and Del deletes the selection.
- **ItemMenu:** opens the menu of the selected item.
- **Undo:** one tap undoes one step (`UNDO` / `2/10`). Hold it and turn the wheel to walk through the history.
- **Un/Redo:** like Ctrl+Z in FL: undoes, and if you press it again, redoes.
- With Shift, the yellow keys are FL's F keys (see [Shift combinations](#shift-combinations)).

#### Wheel modes

The wheel does one thing at a time; these keys choose which.

- **One tap** turns the mode on: its key lights up and the screen shows the mode on top and what you are changing below. Turn the wheel.
- **Another tap** turns it off. The screen shows the mode and `OFF` for a moment.
- If you **hold** the key while turning the wheel, the mode turns off when you let go.
- With no mode, the wheel moves through FL's focused window.

| Mode | Key | What the wheel does | Screen |
|---|---|---|---|
| Mixer | green 2 | Goes from track to track in the Mixer; the fader follows | `MIXER` / track |
| Pattern | green 1 | Previous or next pattern | `PATTERN` / pattern |
| Channel | green 3 | Previous or next Channel Rack channel | `CHANNEL` / channel |
| Tempo | green 4 | Raises or lowers the BPM (it changes your song) | `TEMPO` / BPM; the red digits also show the BPM, for example `130.00` |
| Free 1–4 | green 5 to 8 | A free control for Link to controller | `FREE 1` / `ON` |
| Window | red 4 | Goes from one FL window to the next | `WINDOW` / window |
| Move | purple 5 | Moves the selection | `MOVE` / `ON` |
| Mark | purple 7 | Jumps between markers (with Shift, selects) | `MARKER` / last jump |
| Undo | yellow 7 (hold) | Walks through the undo history | `UNDO` / step |
| Zoom ↕ and ↔ | right of the wheel | Track height / horizontal zoom | `ZOOM` / `ON` |
| Arrows ↕ and ↔ | left of the wheel | Arrow keys, like the keyboard | no change |
| No mode | — | Moves through the focused window: in the Playlist, the song position | normal view |

#### Shift combinations

**Shift** is key 2 of the blue layer. Hold it and press the other key. It works directly with the keys that don't change with the layer (transport, wheel, Mute, Solo…) and with the blue-layer keys. To use it with another layer: hold Shift, press that layer's round key, then the key.

| Combination | What it does |
|---|---|
| Shift + Save (purple 1) | Saves a new version of the project (`NEW VER` / `OK`) |
| Shift + « or » | Plays at half or double speed while you hold it |
| Shift + LOOP | Turns Snap (the grid magnet) on or off (`SNAP` / `ON`) |
| Shift + Enter or Esc (purple 4 or 3) | Answers "Yes" or "No" in FL's dialogs |
| Shift + Link Ch (purple 6) | Routes the selected channels one per mixer track, starting from the selected one |
| Shift + +Mark (purple 8) | Adds an alternate marker |
| Shift + Solo | Solo that also includes the tracks that send audio to it |
| Shift + wheel (Mark mode) | Selects the part between markers |
| Shift + wheel (Zoom mode) | Vertical zoom with the wheel |
| Shift + wheel (no mode) | The wheel's alternate mode (like Scrub) |
| Shift + yellow 1 to 8 | FL's F1 to F8 keys (for example F5 Playlist, F6 Channel Rack, F7 Piano roll, F8 Plugin picker). F2 is not possible: it's the same key as Shift. |
| Hold Undo (yellow 7) + wheel | Walks through the undo history |
| Hold a wheel-mode key + turn | Momentary mode: it turns off when you let go |

#### Knob pages

The right-hand column chooses what the knobs do. The 4 small knobs control tracks 1 to 4 of the bank (5 to 8 if you switch on **5-8**); you change bank with `<<8` and `8>>`. When you choose a page, the screen shows its name and `PAGINA` ("page"), for example `PAN` / `PAGINA`.

| Page | Each knob | Pressing the knob | The fader |
|---|---|---|---|
| **Pan** | Pan of its track | Centers it | Volume of the selected track |
| **Stereo** | Stereo separation of its track | Resets it | Volume of the selected track |
| **Sends** | Knob N: how much the selected track sends to track N of the bank | Switches that send on or off | Volume of the selected track |
| **Effects** | Knob N: mix level of the effect in slot N of the selected track | Switches that effect on or off | Volume of the selected track |
| **EQ** | The selected track's EQ (frequencies and bandwidth) | Resets the value | Gain of one EQ band |
| **Free** | Free controls to link with Link to controller | Free control | Free control |

On **EQ** and **Free**, the fader doesn't follow the selected track.

#### What the screens show

The Nano's small screen has 2 lines of 7 characters.

- **Normal view:** the selected track on top and its real volume in dB below, for example `Kick` / `-5.2dB` (or `0.0dB`, `-INF dB`). Long names are squeezed: "Insert 12" becomes `Ins 12` and "Kick Drum" becomes `KickDrm`. While you move the fader, the name stays and only the number changes.
- **When you press a key:** a short, whole message for about 1.5 seconds; then the normal view comes back.
- **With a wheel mode on:** the mode on top and what you are changing below (see [Wheel modes](#wheel-modes)).
- **Red digits:** the song position, in bars or in minutes:seconds (switch with TimeFormat). In Tempo mode, the BPM (for example `130.00`).

| Screen (top / bottom) | When it appears |
|---|---|
| `FL` / `LISTO` | When the script starts (about 2 seconds) |
| `FL` / `CERRADO` | When FL closes |
| `MASTER` / `73%` | You move the fader with Master on |
| `METRO` / `ON` or `OFF` | Metronome (blue 4) |
| `3..2..1` / `ON` or `OFF` | Recording count-in (blue 6) |
| `MODO` / `PATTERN` or `SONG` | Pattern Song (blue 8) |
| `TIEMPO` / `COMPAS` or `MIN:SEG` | TimeFormat (blue 5) |
| `LOOPREC` / `ON` or `OFF` | LOOP |
| `SNAP` / `ON` or `OFF` | Shift + LOOP |
| `MUTE`, `SOLO` or `REC ARM` / `ON` or `OFF` | Mute, Solo or Rec |
| `SAVE` / `OK` | Save (purple 1) |
| `NEW VER` / `OK` | Shift + Save |
| `UNDO` / `2/10` | Undo (yellow 7): step in the history / total |
| `UN/REDO` / `3/10` | Un/Redo (yellow 8) |
| `FLIP` / `ON` | Flip is on (stays while it's on) |
| `SCRUB` / `ON` or `OFF` | Pressing the wheel |
| `SMOOTH` / `ON` or `OFF` | Smooth (red 5) |
| `METERS` / `HORIZ`, `VERT` or `OFF` | Display Mode (blue 1) |
| `EDISON` / `LISTO` | Edison (blue 3) |
| `PAN` / `PAGINA` (or `STEREO`, `SENDS`, `EFFECTS`, `EQ`, `FREE`) | You choose a page |
| `EQ` / track | While you are on the EQ page |
| `FREE` / `CTRL` | While you are on the Free page |
| `Cut`, `Copy`, `Paste`, `Insert`, `Delete`, `Menu`, `Tools` | Editing and menu keys |
| `NO SEND` | On Sends, you pressed the knob of a track that can't receive a send |
| `Menu` / `View` (for example) | You browse FL's menus: FL sends its hints to the screen. This is normal and goes away by itself. |

#### Platform D3 external display

- It's optional. It plugs with its cable into the display connector on the back of the Nano.
- It has 8 squares of 2 lines of 7 characters: one per track of the bank.
- Each square shows its track's name on top and, below, what its knob does on the current page. On Pan: `C` is center, `10%L` is 10 % left and `25%R` is 25 % right. A `-` means there's nothing to control (for example a send that is off or an empty effect slot).
- On the Effects page, the top line shows the slot (`FX 1` to `FX 8`); on EQ, the parameter name; on Free, `Knob 1` to `Knob 8`.
- The square where the fader is shows the same as the Nano's small screen: the selected track and its volume, or the wheel mode.
- Key messages (`METRO ON`, `MUTE ON`…) appear on all 8 squares.
- Turning a knob changes only its own square.
- When FL opens, the 8 squares repeat the same view until you [touch the fader once](#first-use-touch-the-fader).
- **Without the D3:** the Nano's small screen shows the fader's square (the selected track and its volume). You see the value of the other knobs in FL. If you'd rather see it on the small screen, read about the `NanoStrips` option in [For developers](#for-developers).

#### Recipes

**Mix track by track**

1. Press the round green key (green layer), then **Mixer** (key 2).
2. Turn the wheel to the track you want: the fader moves to its volume and the screen shows its name.
3. Adjust with the fader; use Mute, Solo and Rec for that track.
4. Press **Mixer** again so the wheel goes back to normal.

**Control a plugin knob (Link to controller)**

1. Press **Free** in the right-hand column, so the Nano's knobs aren't doing something else. (Or switch on **Free 1** on the green layer to use the wheel.)
2. In FL, right-click the plugin knob → **Link to controller…**
3. Move the Nano's knob (or turn the wheel): FL detects it by itself. Click **Accept**.

More recipes in the [interactive tutorial](https://noisybeats03-eng.github.io/icon-platform-nano-air-fl-studio/) (in Spanish): recording automation with the fader, loop recording, recording only one part with markers, and recording with Edison.

### FAQ

#### Does the iCON Platform Nano Air work with FL Studio?

Yes. In Mackie Control (MCP) mode, FL can drive it with its own Mackie Control Universal script, but that script is made for 8-fader consoles with a long display. This script adapts it to the Nano: a single fader that follows the selected track and a small screen of 2 lines of 7 characters that you can actually read.

#### My iCON Platform Nano Air is not working in FL Studio. What should I check?

It's almost always one of these:

- The Nano is not in MCP mode (see [Put the Nano in MCP mode](#put-the-nano-in-mcp-mode)).
- The output is missing: in **Output**, the Nano must have the same **Port** as in **Input**.
- You clicked **Enable** after choosing the Controller type and switched it off.
- You switched from wireless to cable (or the other way around): the Nano has a different name each way, and each name must be set up once.

Everything is explained in [Troubleshooting](#troubleshooting).

#### How do I set up the iCON Platform Nano Air in FL Studio?

Install the script, then open **OPTIONS > MIDI settings** (F10): in **Input** pick the Nano, **Controller type** = **iCON Platform Nano Air (custom)** and **Port** = 1; in **Output**, the same Nano with **Port** = 1. Step by step in the [installation manual](#installation-manual).

#### Can the motorized fader follow the selected track?

Yes, that's the main thing this script does: pick a track in FL's Mixer and the fader moves to its volume; Mute, Solo and Rec work on that track too. With FL's Mackie Control Universal script, the fader stays on one fixed track of the bank.

#### Does it work with the iCON Platform D3 display?

Yes, it's optional: each of its 8 squares shows one track of the bank. See [Platform D3 external display](#platform-d3-external-display).

#### Does it work on a Mac? Which FL Studio version?

It was tested with FL Studio 2025 on Windows. It hasn't been tested on macOS; the script is plain Python and should work the same (the folder goes in `~/Documents/Image-Line/FL Studio/Settings/Hardware`).

#### Does it work with other Mackie Control controllers?

It is made and tested only for the Platform Nano Air (one fader and a small screen of 2 lines of 7 characters). For 8-fader consoles, use FL's Mackie Control Universal script.

#### Is it free? Is it official?

It's free, with an MIT license for this repository's own work (see [License](#license)). It's unofficial: it has nothing to do with iCON Pro Audio or Image-Line.

#### How do I go back to FL's original script?

In **OPTIONS > MIDI settings**, change the Nano's **Controller type** to **Mackie Control Universal**. See [Go back to FL's original script](#go-back-to-fls-original-script).

### Troubleshooting

**"iCON Platform Nano Air (custom)" is not in the Controller type list**

- The folder is not in the right place. It must end up as `...\FL Studio\Settings\Hardware\iCON Platform Nano Air\device_iCON_PlatformNanoAir.py`.
- Common mistakes: you copied the ZIP without unzipping it; there is an extra folder in between; you put it in another data folder (check **OPTIONS > File settings** → **User data folder**).
- Then close and reopen FL, or click **Update MIDI scripts** in **OPTIONS > MIDI settings**.

**The Nano is not in the MIDI settings lists**

- Check that it is switched on and connected. Wirelessly, the screen must say **Paired**.
- Close FL, switch on and connect the Nano, then open FL again.
- Try another USB port, straight into the computer (no hub or extension cable).

**FL ignores the Nano**

- In **OPTIONS > MIDI settings**, in **Input**: the Nano's name with Controller type **iCON Platform Nano Air (custom)**, the **Enable** light on and **Port** 1. In **Output**: the same name with **Port** 1.
- If you clicked Enable after choosing the Controller type, you switched it off: click it again so the light comes on.

**It worked, and now the setup seems lost**

- You probably switched from wireless to cable (for example, the battery died) or the other way around. The Nano has a different name each way, and FL keeps the settings per name. Set up the other name once (see [Set up FL Studio](#set-up-fl-studio)).

**The keys do strange things or don't match the overlay**

- The Nano is not in MCP mode. Switch it off and on and choose MCP (see [Put the Nano in MCP mode](#put-the-nano-in-mcp-mode)).
- Check which color layer is selected.

**The screen shows nothing from FL, or the fader doesn't move by itself**

- The output is missing: in **OPTIONS > MIDI settings**, in **Output**, the Nano's name must have the same **Port** as in Input.
- Is **Flip** (red 1) on? The screen says `FLIP` / `ON`. Press it to turn it off.
- Is **Master** on? Press it to go back to the track.
- Are you on the **EQ** or **Free** page? There the fader doesn't follow the selected track: choose Pan, Stereo, Sends or Effects.

**The Nano's screen doesn't light up**

- Check the switch on the back (the one at the far left when you look at the back panel): **–** is on and **O** is off.
- If the battery is empty, connect it by USB cable: it works the same and charges.

**Wireless doesn't connect**

- Plug in the receiver before switching on the Nano, and wait for **Paired**. The receiver's Paired light must stay on; if it blinks, they haven't paired.
- Switch the Nano off and on, or try another USB port.

**All 8 squares of the Platform D3 show the same thing**

- That's normal right after FL opens. Touch the fader once.

**The screen shows FL menu names (for example `Menu` / `View`)**

- That's normal: while you browse FL's menus, FL sends its hints to the screen. It goes away by itself.

**Script output says "Invalid mixer track nr 501"**

- It's a harmless warning that comes from FL's original script. You can ignore it.

**I moved the fader and the new track's volume didn't change**

- That's on purpose: if you change track with your finger on the fader, the new track isn't touched until the fader reaches its level or you let go. Let go and touch it again. Also, the tiny movements of a resting finger are ignored.

**The wheel doesn't do what I expect, or the tempo changed by itself**

- A wheel mode is on: its key is lit and the screen shows the mode. Press it again to turn it off.
- If you changed something by accident (for example the tempo), use Undo (yellow 7).

**A key did something unexpected**

- Many keys act on FL's focused window. Look at FL's hint bar at the top left: it says what just happened. To undo it, use Undo (yellow 7).

**Script output shows an error (text that says Traceback or Error)**

- Copy the whole text and report it in [Issues](https://github.com/noisybeats03-eng/icon-platform-nano-air-fl-studio/issues). Meanwhile, you can [go back to FL's original script](#go-back-to-fls-original-script).

### Update to a new version

1. Download the new ZIP from the [latest release](https://github.com/noisybeats03-eng/icon-platform-nano-air-fl-studio/releases/latest) page and unzip it.
2. Close FL Studio.
3. Copy the new `iCON Platform Nano Air` folder into `...\FL Studio\Settings\Hardware`, in the same place as the old one. When Windows asks, choose **Replace the file in the destination**.
4. Open FL Studio. You don't have to set anything up again: the Controller type has the same name.
5. Check that **VIEW > Script output** says **OnInit ready**.

To know whether there's a new version, check the Releases page. If you have a GitHub account, you can use **Watch > Custom > Releases** on this repository to get notified. What changed in each version is in [CHANGELOG.md](CHANGELOG.md).

### Go back to FL's original script

You can switch between this script and FL's whenever you want, without deleting anything.

1. Open **OPTIONS > MIDI settings**.
2. In **Input**, click the Nano's name.
3. In **Controller type**, choose **Mackie Control Universal**.
4. Check the **Enable** light and the **Port**, as in [Set up FL Studio](#set-up-fl-studio).
5. If you use both cable and wireless, repeat for the other name.

To come back to this script, choose **iCON Platform Nano Air (custom)** again.

### Uninstall

1. In **OPTIONS > MIDI settings**, for each name of the Nano, change the **Controller type** to another one (for example **Mackie Control Universal**).
2. Close FL Studio.
3. Delete the `iCON Platform Nano Air` folder from `...\FL Studio\Settings\Hardware`.
4. Open FL Studio again.

### Credits and disclaimer

- Based on the **Mackie Control Universal** script that comes with FL Studio (`device_MackieCU.py`, version 2026.1), © Image-Line Software. The changes for the Nano Air are listed at the top of the script file and explained in [CHANGELOG.md](CHANGELOG.md).
- Independent, unofficial project: not affiliated with, sponsored or reviewed by iCON Pro Audio or Image-Line. If something goes wrong with this script, don't contact iCON's or Image-Line's support: open an [issue](https://github.com/noisybeats03-eng/icon-platform-nano-air-fl-studio/issues) here.
- iCON, Platform Nano Air, Platform D3, FL Studio, Edison, Image-Line and Mackie Control are trademarks of their respective owners. They are mentioned only to say what this script works with.
- The colored-key names are those of iCON's FL Studio overlay. This project doesn't copy iCON's manual or use its logos.
- Provided as is, without warranty. Save your project often.

### License

MIT license ([LICENSE](LICENSE)) for this repository's own work: the changes to the script, the documentation, the tutorial and the tools in `dev/`. The parts that come from Image-Line's script still belong to Image-Line and are not covered by that license. Details and notices are in [NOTICE.md](NOTICE.md).

### For developers

**What's in the repository**

| Path | What it is |
|---|---|
| `iCON Platform Nano Air/device_iCON_PlatformNanoAir.py` | The script (the only thing you install) |
| `docs/index.html` | The interactive tutorial, in Spanish (GitHub Pages) |
| `dev/` | Tools to test the script outside FL ([dev/README.md](dev/README.md)) |
| `CHANGELOG.md` | What changed in each version |
| `LICENSE`, `NOTICE.md` | License and notices |

**Script options.** At the top of the file there are options you can change. Open it with Notepad (right-click → **Open with** → **Notepad**), change the value after the `=`, save and restart FL. When you update, the new file comes with the default values again.

| Option | Default | What it does |
|---|---|---|
| `NanoLatchJogSources` | `True` | One-tap wheel modes. `False` = like FL: you have to keep them held. |
| `NanoFollowSelected` | `True` | The fader, Mute, Solo, Rec and the screen follow the selected track. `False` = fixed on their bank track, like FL. |
| `NanoScreen` | `True` | This script draws the small screen. `False` = FL's original texts. |
| `NanoStrips` | `True` | Platform D3: one track per square. `False` = all 8 squares repeat the Nano's small screen (useful without a D3: the value of any knob shows on the small screen). |
| `NanoFaderDeadband` | `48` | How much movement of a resting finger is ignored (on a 0 to 16383 scale). |
| `NanoFaderPickup` | `150` | How close the fader must get to the new track's level to take it over. |
| `NanoFaderKick` | `False` | A push to the fader motor on small moves. |
| `NanoDebug` | `False` | Diagnostic messages in **VIEW > Script output**. |

**Tools in `dev/`.** They need Python 3 and FL Studio installed: they use your FL's own `midi.py` and `utils.py` (the path is in the `FL_LIB` line at the top of `dev/flsim.py`). Open a terminal in the `dev` folder and always use `python -I -B` (`-B` stops a `__pycache__` folder from appearing next to the script).

- `flsim.py`: a simulator of FL's scripting API that runs 112 checks on the script. It must end with `ALL PASS`.
  ```text
  python -I -B flsim.py "..\iCON Platform Nano Air\device_iCON_PlatformNanoAir.py"
  ```
- `gen_screen_data.py` and `embed_screen_data.py`: record what both screens show for each of the 69 controls (running the script in the simulator) and embed it in the tutorial.
  ```text
  python -I -B gen_screen_data.py flsim.py "..\iCON Platform Nano Air\device_iCON_PlatformNanoAir.py" screen_data.json
  python -I -B embed_screen_data.py ..\docs\index.html screen_data.json
  ```
- `flicker_probe.py`: prints a timeline of the small screen to look for flicker.
  ```text
  python -I -B flicker_probe.py flsim.py "..\iCON Platform Nano Air\device_iCON_PlatformNanoAir.py"
  ```

All the details (how the simulator works, how to try a change in FL and how to build a release ZIP) are in [dev/README.md](dev/README.md). Tested with FL scripting API version 40 (FL Studio 2025). To report a problem or suggest a change, open an [issue](https://github.com/noisybeats03-eng/icon-platform-nano-air-fl-studio/issues).
