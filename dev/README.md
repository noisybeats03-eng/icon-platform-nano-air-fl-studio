# Herramientas de desarrollo · iCON Platform Nano Air para FL Studio / Developer tools · iCON Platform Nano Air for FL Studio

> **No necesitas esta carpeta para usar el script.** Es para quien quiera cambiarlo o comprobar que sigue funcionando. Para instalarlo, ve al [README principal](../README.md).
>
> **You do not need this folder to use the script.** It is for people who want to change it or check that it still works. To install it, see the [main README](../README.md).

**Español** · [English](#english)

## Español

### Qué hay aquí

| Archivo | Para qué sirve |
|---|---|
| `flsim.py` | Un simulador pequeño de FL Studio: corre el script fuera de FL y hace 112 pruebas (fader, botones, las dos pantallas). |
| `gen_screen_data.py` | Corre el script en el simulador y graba qué muestran la pantallita del Nano y la Platform D3 con cada uno de los 69 controles. Escribe un archivo JSON. |
| `embed_screen_data.py` | Mete ese JSON dentro del tutorial (`docs/index.html`), para que las pantallas dibujadas muestren exactamente lo que dibuja el script. |
| `flicker_probe.py` | Imprime la línea de tiempo de la pantallita (qué texto sale, cuándo y cuánto dura) en varias escenas, para ver si algo parpadea. |

### Lo que necesitas

- **Python 3** (se probó con Python 3.14 en Windows). No hace falta instalar paquetes.
- **FL Studio instalado.** El simulador usa `midi.py` y `utils.py` de FL (las constantes y funciones reales de FL). No vienen en este repositorio: se leen de tu instalación, en

  ```
  C:\Program Files\Image-Line\FL Studio 2025\Shared\Python\Lib
  ```

  Esa ruta está escrita en la línea `FL_LIB = ...` al principio de `flsim.py`. Si tu FL está en otra carpeta o es otra versión, cambia esa línea. En Mac busca la carpeta de FL Studio que tiene `midi.py` y pon esa ruta (no se probó en Mac).

### Cómo correrlas

Abre una terminal (PowerShell o Símbolo del sistema) **en la carpeta `dev`** y copia los comandos tal cual. Si `python` no funciona en Windows, prueba con `py`.

Usa siempre `python -I -B`:

- `-I` (modo aislado): Python no usa variables de entorno ni paquetes del usuario y no busca módulos en la carpeta actual, así ningún `midi.py` suelto reemplaza al de FL.
- `-B`: no crea la carpeta `__pycache__` junto al script. Sin `-B` aparece `iCON Platform Nano Air FL Studio\__pycache__`, que no debe subirse al repositorio ni ir en el ZIP.

**1. Probar el script (112 pruebas)**

```
python -I -B flsim.py "..\iCON Platform Nano Air FL Studio\device_iCON_PlatformNanoAir_FLStudio.py"
```

Escribe una línea `PASS` o `FAIL` por cada prueba y al final `ALL PASS` (o `N FAILED`). Si todo pasó, termina con código 0; si algo falló, con código 1. Las líneas `OnInit ready`, `OnDeInit ready` y `Nano Air screen: ...` que salen en medio son normales: son mensajes del propio script.

**2. Actualizar las pantallas del tutorial** (cada vez que cambies lo que muestra la pantalla)

```
python -I -B gen_screen_data.py flsim.py "..\iCON Platform Nano Air FL Studio\device_iCON_PlatformNanoAir_FLStudio.py" screen_data.json
python -I -B embed_screen_data.py ..\docs\index.html screen_data.json
```

- El primero corre las 69 escenas con un proyecto de ejemplo (nombres genéricos como Kick, Snare, HiHat) y escribe `screen_data.json`. Dice `ok 69 scenes, ... bytes` y luego un resumen de una línea por control.
- El segundo reemplaza lo que hay entre las marcas `/*SCR*/` y `/*SCR-END*/` de `docs/index.html` y guarda la página en UTF-8 con finales de línea LF. Dice `embedded ... bytes of screen data; page ... bytes`.
- Después puedes borrar `screen_data.json`: es un archivo de paso y no hace falta subirlo.

**3. Ver la línea de tiempo de la pantallita** (opcional)

```
python -I -B flicker_probe.py flsim.py "..\iCON Platform Nano Air FL Studio\device_iCON_PlatformNanoAir_FLStudio.py"
```

Primero repite las pruebas A y B de `flsim.py`. Luego, para cada escena (mover el fader, Metronome, prender el modo Mixer, girar la rueda, mover el fader en modo Mixer, apagar el modo Mixer, Undo, Mute), imprime cada texto que sale en la pantallita, cuándo sale y cuánto se ve, y cuenta cuántos cambios duran menos de 0.3 s. No dice PASS o FAIL: es para mirarlo.

En Mac o Linux los comandos son los mismos, con `/` en lugar de `\` (y `python3` si tu sistema lo llama así).

### Cómo funciona el simulador

- Reemplaza los módulos de FL (`mixer`, `device`, `transport`, `ui`, `general`, `playlist`, `channels`, `patterns`, `arrangement`, `launchMapPages`) por imitaciones que anotan cada llamada. Lo único real de FL son `midi.py` y `utils.py`.
- Tiene un mixer de juguete: 30 pistas con volúmenes distintos, más Mute, Solo y Rec.
- Copia lo que el script manda a la pantalla tipo Mackie (2 renglones de 56 caracteres, o sea 8 cuadros de 7) y a los 10 dígitos del contador.
- Usa un reloj falso que avanza a mano, en pasos de 20 ms como el `OnIdle` de FL. Así las pruebas de «el mensaje dura 1.5 s» no tienen que esperar de verdad.
- Las pruebas van por secciones:
  - **A** El fader sigue a la pista seleccionada; Mute, Solo y Rec actúan sobre ella; el fader Master no cambia.
  - **B** Modos de la rueda (un toque = se queda prendido; mantener y girar = momentáneo), Undo, Loop y Zoom.
  - **C** La pantallita del Nano: vista normal, mensajes, modos de la rueda, el BPM en los dígitos y cómo se acortan los textos de FL.
  - **D** Sin parpadeo, con el suavizado de controles de FL simulado.
  - **E** La pantalla externa de 8 cuadros (Platform D3).
  - **F** Dedo apoyado en el fader, toma suave después de cambiar de pista, Shift + teclas amarillas, Shift + Solo, Undo rápido, modos Marker y Free, menús de FL, reloj de la PC que se atrasa y el texto del fader en la página Free.
- Es una simulación: revisa la lógica del script, no el aparato. La prueba final siempre es con el Nano de verdad en FL Studio.

### Probar un cambio en FL

1. Edita `iCON Platform Nano Air FL Studio\device_iCON_PlatformNanoAir_FLStudio.py`. El archivo usa finales de línea de Windows (CRLF); `.gitattributes` hace que Git no los cambie.
2. Corre `flsim.py` hasta que diga `ALL PASS`.
3. Copia la carpeta `iCON Platform Nano Air FL Studio` a `Documentos\Image-Line\FL Studio\Settings\Hardware` (o a la carpeta de datos que dice FL en OPTIONS > File settings > User data folder).
4. En FL: **VIEW > Script output > Reload script** si el script ya estaba elegido, o reinicia FL si copiaste la carpeta por primera vez. En la pestaña con el nombre del Nano debe decir `OnInit ready`.
5. Si cambiaste textos de la pantalla, actualiza el tutorial (paso 2 de arriba).

Para ver más detalle mientras pruebas, pon `NanoDebug = True` al principio del script: en VIEW > Script output se escribe cada posición del fader que entra y que sale, y las notas de Select, de banco y de toque del fader. Vuelve a ponerlo en `False` al terminar.

### Armar el ZIP de una versión nueva

Desde la carpeta principal del repositorio (no desde `dev`), cambiando `v1.1.0` por la versión nueva:

```
python -I -B -c "import zipfile; z = zipfile.ZipFile('../iCON-Platform-Nano-Air-FL-Studio-v1.1.0.zip', 'w', zipfile.ZIP_DEFLATED); z.write('iCON Platform Nano Air FL Studio'); z.write('iCON Platform Nano Air FL Studio/device_iCON_PlatformNanoAir_FLStudio.py'); z.write('docs/index.html', 'Tutorial iCON Platform Nano Air FL Studio (ES-EN).html'); z.close()"
```

Deja el ZIP en la carpeta de arriba (fuera del repositorio). Debe traer la carpeta `iCON Platform Nano Air FL Studio`, con solo el script adentro (byte por byte igual al del repositorio), y `Tutorial iCON Platform Nano Air FL Studio (ES-EN).html`, que es una copia de `docs/index.html`. Sube ese ZIP al release; no lo subas al repositorio.

El tutorial es bilingüe: los textos en español tienen su traducción en el bloque `/*EN*/ ... /*EN-END*/` de `docs/index.html`. Si cambias textos de la página o etiquetas de pasos en `gen_screen_data.py`, abre la página, escribe `i18nMissing()` en la consola del navegador y agrega lo que falte hasta que regrese `[]`.

Antes de publicar, cambia la versión y el nombre del ZIP en `README.md`, `docs/index.html` (también en el JSON-LD: `version`, `softwareVersion` y `dateModified`), `docs/llms.txt`, el encabezado del script (`release 1.1.0`) y la fecha `<lastmod>` de `docs/sitemap.xml` (búscalos con `git grep -n 1.1.0`), y agrega la versión nueva a `CHANGELOG.md`.

## English

### What is here

| File | What it is for |
|---|---|
| `flsim.py` | A small FL Studio simulator: runs the script outside FL and makes 112 checks (fader, buttons, both screens). |
| `gen_screen_data.py` | Runs the script in the simulator and records what the Nano's small screen and the Platform D3 show for each of the 69 controls. Writes a JSON file. |
| `embed_screen_data.py` | Puts that JSON inside the tutorial (`docs/index.html`), so the drawn screens show exactly what the script draws. |
| `flicker_probe.py` | Prints the small screen's timeline (which text appears, when and for how long) for a few scenes, to spot flicker. |

### What you need

- **Python 3** (tested with Python 3.14 on Windows). No packages to install.
- **FL Studio installed.** The simulator uses FL's own `midi.py` and `utils.py` (FL's real constants and helpers). They are not in this repository: they are read from your installation, in

  ```
  C:\Program Files\Image-Line\FL Studio 2025\Shared\Python\Lib
  ```

  That path is written in the `FL_LIB = ...` line at the top of `flsim.py`. If your FL is in another folder or is another version, change that line. On a Mac, look for the FL Studio folder that contains `midi.py` and use that path (not tested on a Mac).

### How to run them

Open a terminal (PowerShell or Command Prompt) **in the `dev` folder** and copy the commands as they are. If `python` does not work on Windows, try `py`.

Always use `python -I -B`:

- `-I` (isolated mode): Python ignores environment variables and user packages and does not look for modules in the current folder, so no stray `midi.py` can replace FL's.
- `-B`: does not create a `__pycache__` folder next to the script. Without `-B`, an `iCON Platform Nano Air FL Studio\__pycache__` folder appears; it must not go into the repository or the ZIP.

**1. Check the script (112 checks)**

```
python -I -B flsim.py "..\iCON Platform Nano Air FL Studio\device_iCON_PlatformNanoAir_FLStudio.py"
```

It prints one `PASS` or `FAIL` line per check and finally `ALL PASS` (or `N FAILED`). It exits with code 0 when everything passed and 1 when something failed. The `OnInit ready`, `OnDeInit ready` and `Nano Air screen: ...` lines in between are normal: they are the script's own messages.

**2. Update the tutorial's screens** (whenever you change what the screen shows)

```
python -I -B gen_screen_data.py flsim.py "..\iCON Platform Nano Air FL Studio\device_iCON_PlatformNanoAir_FLStudio.py" screen_data.json
python -I -B embed_screen_data.py ..\docs\index.html screen_data.json
```

- The first one runs the 69 scenes with an example project (generic names such as Kick, Snare, HiHat) and writes `screen_data.json`. It prints `ok 69 scenes, ... bytes` and then a one-line summary per control.
- The second one replaces what is between the `/*SCR*/` and `/*SCR-END*/` markers in `docs/index.html` and saves the page as UTF-8 with LF line endings. It prints `embedded ... bytes of screen data; page ... bytes`.
- Afterwards you can delete `screen_data.json`: it is an intermediate file and does not need to be committed.

**3. See the small screen's timeline** (optional)

```
python -I -B flicker_probe.py flsim.py "..\iCON Platform Nano Air FL Studio\device_iCON_PlatformNanoAir_FLStudio.py"
```

It first repeats sections A and B of `flsim.py`. Then, for each scene (moving the fader, Metronome, Mixer mode on, turning the wheel, moving the fader in Mixer mode, Mixer mode off, Undo, Mute), it prints every text the small screen shows, when it appears and how long it stays, and counts the changes that last less than 0.3 s. It does not say PASS or FAIL: it is for looking at.

On a Mac or Linux the commands are the same, with `/` instead of `\` (and `python3` if that is what your system calls it).

### How the simulator works

- It replaces FL's modules (`mixer`, `device`, `transport`, `ui`, `general`, `playlist`, `channels`, `patterns`, `arrangement`, `launchMapPages`) with stand-ins that record every call. The only real FL parts are `midi.py` and `utils.py`.
- It has a toy mixer: 30 tracks with different volumes, plus Mute, Solo and Rec.
- It copies what the script sends to the Mackie-style screen (2 rows of 56 characters, that is 8 squares of 7) and to the 10-digit counter.
- It uses a fake clock moved by hand, in 20 ms steps like FL's `OnIdle`, so checks such as "the message stays 1.5 s" do not have to wait for real.
- The checks come in sections:
  - **A** The fader follows the selected track; Mute, Solo and Rec act on it; the Master fader is unchanged.
  - **B** Wheel modes (tap = stays on; hold and turn = momentary), Undo, Loop and Zoom.
  - **C** The Nano's small screen: normal view, messages, wheel modes, the BPM on the digits and how FL's texts are squeezed.
  - **D** No flicker, with FL's control smoothing simulated.
  - **E** The 8-square external display (Platform D3).
  - **F** Resting finger on the fader, soft take-over after a track change, Shift + yellow keys, Shift + Solo, quick Undo, Marker and Free modes, FL's menus, the PC clock going back, and the fader text on the Free page.
- It is a simulation: it checks the script's logic, not the hardware. The final test is always with the real Nano in FL Studio.

### Trying a change in FL

1. Edit `iCON Platform Nano Air FL Studio\device_iCON_PlatformNanoAir_FLStudio.py`. The file uses Windows (CRLF) line endings; `.gitattributes` keeps Git from changing them.
2. Run `flsim.py` until it says `ALL PASS`.
3. Copy the `iCON Platform Nano Air FL Studio` folder to `Documents\Image-Line\FL Studio\Settings\Hardware` (or to the data folder FL shows in OPTIONS > File settings > User data folder).
4. In FL: **VIEW > Script output > Reload script** if the script was already selected, or restart FL if you copied the folder for the first time. On the tab with the Nano's name it must say `OnInit ready`.
5. If you changed screen texts, update the tutorial (step 2 above).

For more detail while testing, set `NanoDebug = True` at the top of the script: VIEW > Script output then shows every fader position coming in and going out, and the Select, bank and fader-touch notes. Set it back to `False` when you are done.

### Building the ZIP for a new version

From the repository's main folder (not from `dev`), replacing `v1.1.0` with the new version:

```
python -I -B -c "import zipfile; z = zipfile.ZipFile('../iCON-Platform-Nano-Air-FL-Studio-v1.1.0.zip', 'w', zipfile.ZIP_DEFLATED); z.write('iCON Platform Nano Air FL Studio'); z.write('iCON Platform Nano Air FL Studio/device_iCON_PlatformNanoAir_FLStudio.py'); z.write('docs/index.html', 'Tutorial iCON Platform Nano Air FL Studio (ES-EN).html'); z.close()"
```

The ZIP lands in the folder above (outside the repository). It must hold the `iCON Platform Nano Air FL Studio` folder, with only the script inside (byte for byte the same as in the repository), and `Tutorial iCON Platform Nano Air FL Studio (ES-EN).html`, a copy of `docs/index.html`. Upload that ZIP to the release; do not commit it.

The tutorial is bilingual: the Spanish texts have their translation in the `/*EN*/ ... /*EN-END*/` block of `docs/index.html`. If you change page texts or step labels in `gen_screen_data.py`, open the page, type `i18nMissing()` in the browser console and add what is missing until it returns `[]`.

Before publishing, update the version and the ZIP name in `README.md`, `docs/index.html` (including the JSON-LD `version`, `softwareVersion` and `dateModified`), `docs/llms.txt`, the script header (`release 1.1.0`) and the `<lastmod>` date in `docs/sitemap.xml` (find them with `git grep -n 1.1.0`), and add the new version to `CHANGELOG.md`.
