# Historial de cambios / Changelog

Lo más nuevo va arriba. / Newest first.

## v1.0.0 (2026-11)

**Español** · [English](#english)

### Español

Primera versión pública. Probada con un iCON Platform Nano Air real y FL Studio 2025 en Windows (API de scripts de FL versión 40), por cable USB y con el receptor inalámbrico.

Base: el script «Mackie Control Universal» de FL Studio (`device_MackieCU.py`, versión 2026.1, © Image-Line Software). En FL aparece como **iCON Platform Nano Air (custom)**.

#### El fader sigue a la pista seleccionada

- El fader motorizado, los botones Mute, Solo y Rec y la pantalla trabajan sobre la pista del Mixer que tengas seleccionada en FL. Vale en las páginas Pan, Stereo, Sends y Effects; con Flip o en las páginas EQ y Free todo funciona como en el script original.
- Las luces de Mute, Solo y Rec muestran cómo está la pista seleccionada.
- Botón Master: el fader mueve el volumen principal de FL y la pantalla dice `MASTER` y el porcentaje.

#### Fader más estable

- Un dedo apoyado en el fader ya no cambia el volumen: se ignoran los movimientos chiquitos.
- Toma suave: si la pista seleccionada cambia mientras tienes el dedo en el fader, la pista nueva no se toca hasta que el fader llega a su nivel o hasta que lo sueltas.

#### Botones de modo de la rueda

- Pattern, Mixer, Channel, Tempo, Free 1–4, Window, Move y Mark se quedan prendidos: un toque prende el modo y otro toque lo apaga.
- Si mantienes el botón apretado mientras giras la rueda, el modo es momentáneo: se apaga al soltar (como en FL).
- La luz del modo activo, ZOOM incluido, se queda prendida.

#### Zoom

- ZOOM también se prende con un toque y se apaga con otro.
- Con ZOOM prendido: flechas arriba/abajo = zoom vertical (alto de las pistas); izquierda/derecha = zoom horizontal; la rueda hace zoom horizontal (con Shift, vertical).

#### Undo

- Tecla amarilla 7 «Undo»: un toque deshace un paso; mantenerla apretada y girar la rueda recorre el historial de deshacer.
- Tecla amarilla 8 «Un/Redo»: igual que Ctrl+Z en FL (deshace o rehace el último paso).

#### Transporte

- LOOP prende y apaga la grabación en loop (*loop recording*), y su luz muestra ese estado.
- Shift + LOOP prende y apaga el snap (el imán a la cuadrícula). En el script original, LOOP era el snap.

#### La pantallita del Nano (2 renglones de 7 letras)

- Vista normal: arriba la pista seleccionada y abajo su volumen real en dB (por ejemplo `Ins 12` / `-5.2dB`).
- Los nombres se acortan para caber en 7 letras (`Insert 12` → `Ins 12`, `Kick Drum` → `KickDrm`) y se quitan los acentos, porque la pantalla no los muestra.
- Cuando tocas un botón sale un mensaje corto y completo durante 1.5 s (arriba la función, abajo el estado): `METRO ON`, `LOOPREC OFF`, `SNAP ON`, `3..2..1 ON`, `MODO SONG`, `MUTE ON`, `SOLO ON`, `REC ARM ON`, `SAVE OK`, `UNDO 3/10`, `FLIP ON`, `SCRUB ON`, `TIEMPO MIN:SEG`, `PAN PAGINA`… Lo último que tocas reemplaza al mensaje anterior.
- Con un modo de la rueda prendido: arriba el modo y abajo lo que vas cambiando (`MIXER` + pista, `CHANNEL` + canal, `PATTERN` + pattern, `TEMPO` + BPM, `WINDOW` + ventana, `MARKER` + último salto).
- En modo Tempo, los dígitos LED muestran el BPM (por ejemplo `130.00`).
- Cuando el script arranca dice `FL` / `LISTO` unos 2 segundos; al cerrar FL dice `FL` / `CERRADO`.
- La pantalla se dibuja solo desde el ciclo de espera de FL, así no parpadea, ni siquiera mientras mueves el fader.
- Algunas palabras de la pantalla están en español: `LISTO`, `PAGINA`, `MODO`, `TIEMPO`, `COMPAS`, `CERRADO`.

#### Pantalla externa Platform D3 (opcional, 8 cuadros)

- Cada cuadro muestra un canal del banco: arriba su nombre y abajo lo que hace su perilla en la página actual (por ejemplo `Snare` / `10%L`).
- El cuadro del canal donde está el fader (el mismo que ves en la pantallita del Nano) muestra la pista seleccionada y su volumen, o el modo de la rueda.
- Los mensajes de los botones llenan los 8 cuadros; al girar una perilla solo cambia su cuadro.
- Después de abrir FL, toca el fader una vez: así el script aprende en qué canal está. Mientras tanto, los 8 cuadros repiten lo mismo.

#### Errores del script original que se corrigieron

- Shift + Solo ya no da error (`NameError`).
- Shift + tecla amarilla (F1–F8): si sueltas Shift antes que la tecla, FL recibe igual que soltaste esa tecla F, y ya no se dispara la función normal de la tecla (por ejemplo, deshacer con la 7).
- Mantener Undo y girar la rueda ya no da error (decía `ui.GetHintMsg` en lugar de `ui.getHintMsg`).
- Página Free: el texto con el valor del fader ahora sale bien (usaba una escala equivocada).

#### Opciones para usuarios avanzados

Al principio del script hay interruptores (`True` / `False`) por si prefieres algo como en el script original:

- `NanoFollowSelected`: el fader sigue a la pista seleccionada.
- `NanoLatchJogSources`: los modos de la rueda se quedan prendidos (`False` = hay que mantenerlos apretados, como en FL).
- `NanoScreen`: textos cortos para la pantallita (`False` = los textos del script original).
- `NanoStrips`: un canal por cuadro en la Platform D3 (`False` = los 8 cuadros repiten la pantallita del Nano).
- `NanoFaderKick`: un empujoncito extra del motor para movimientos muy chicos (apagado de fábrica).
- `NanoDebug`: escribe diagnósticos en VIEW > Script output.

#### Lo que no cambió

- Los 40 botones de colores (5 capas) mandan lo mismo que dice el overlay oficial de iCON para FL Studio; lo que cambia es cómo responde el script.
- Todo lo demás funciona como el script Mackie Control Universal de FL.

#### Documentación y herramientas

- README con un manual de instalación paso a paso.
- Tutorial interactivo en español: <https://noisybeats03-eng.github.io/icon-platform-nano-air-fl-studio/>. Tocas cualquier tecla del controlador dibujado y te dice qué hace; las pantallas dibujadas muestran lo que deben mostrar las de verdad. Incluye la lista de los 69 controles, los modos de la rueda, las combinaciones con Shift, las páginas de las perillas, recetas y solución de problemas.
- Carpeta `dev/`: un simulador de FL con 112 pruebas y las herramientas que generan las pantallas del tutorial.

#### Bueno saber

- Mientras navegas los menús de FL, sus textos (por ejemplo `Menu` / `View`) también salen en la pantallita. Es normal.
- En VIEW > Script output puede salir el aviso `Invalid mixer track nr 501`. Viene del script original de FL y no afecta.
- FL guarda la configuración MIDI por nombre de dispositivo, y el Nano se llama distinto por cable que con el receptor inalámbrico (por ejemplo `PlatformNano(A) V2.05` y `PlatformNano Air V1.02`). Si usas los dos, configura los dos nombres una vez.
- No se probó en Mac (el script es Python normal y debería funcionar).

### English

First public release. Tested with a real iCON Platform Nano Air and FL Studio 2025 on Windows (FL scripting API version 40), over the USB cable and through the wireless receiver.

Based on FL Studio's "Mackie Control Universal" script (`device_MackieCU.py`, version 2026.1, © Image-Line Software). It shows up in FL as **iCON Platform Nano Air (custom)**.

#### The fader follows the selected track

- The motorized fader, the Mute, Solo and Rec buttons and the screen work on the mixer track selected in FL. This applies on the Pan, Stereo, Sends and Effects pages; with Flip or on the EQ and Free pages everything works as in the original script.
- The Mute, Solo and Rec lights show the state of the selected track.
- Master button: the fader controls FL's main volume and the screen shows `MASTER` and the percentage.

#### Steadier fader

- A finger resting on the fader no longer changes the volume: tiny movements are ignored.
- Soft take-over: if the selected track changes while your finger is on the fader, the new track is not touched until the fader reaches its level or you let go.

#### Wheel-mode buttons

- Pattern, Mixer, Channel, Tempo, Free 1–4, Window, Move and Mark latch: one tap turns the mode on, another tap turns it off.
- Holding the button while turning the wheel makes the mode momentary: it turns off when you let go (as in FL).
- The light of the active mode, ZOOM included, stays on.

#### Zoom

- ZOOM also turns on with one tap and off with another.
- With ZOOM on: up/down arrows = vertical zoom (track height); left/right = horizontal zoom; the wheel zooms horizontally (vertically with Shift).

#### Undo

- Yellow key 7 "Undo": one tap undoes one step; holding it and turning the wheel walks through the undo history.
- Yellow key 8 "Un/Redo": the same as Ctrl+Z in FL (undoes or redoes the last step).

#### Transport

- LOOP turns loop recording on and off, and its light shows that state.
- Shift + LOOP turns snap to grid on and off. In the original script, LOOP was snap.

#### The Nano's small screen (2 lines of 7 characters)

- Normal view: the selected track on top and its real volume in dB below (for example `Ins 12` / `-5.2dB`).
- Names are squeezed into 7 characters (`Insert 12` → `Ins 12`, `Kick Drum` → `KickDrm`) and accents are removed, because the screen cannot show them.
- When you press a button, a short whole message stays up for 1.5 s (function on top, state below): `METRO ON`, `LOOPREC OFF`, `SNAP ON`, `3..2..1 ON`, `MODO SONG`, `MUTE ON`, `SOLO ON`, `REC ARM ON`, `SAVE OK`, `UNDO 3/10`, `FLIP ON`, `SCRUB ON`, `TIEMPO MIN:SEG`, `PAN PAGINA`… The newest press replaces the previous message.
- With a wheel mode on: the mode on top and what you are changing below (`MIXER` + track, `CHANNEL` + channel, `PATTERN` + pattern, `TEMPO` + BPM, `WINDOW` + window, `MARKER` + last jump).
- In Tempo mode, the LED digits show the BPM (for example `130.00`).
- When the script starts it shows `FL` / `LISTO` for about 2 seconds; when FL closes it shows `FL` / `CERRADO`.
- The screen is drawn only from FL's idle loop, so it does not flicker, not even while you move the fader.
- Some screen words are Spanish: `LISTO` (ready), `PAGINA` (page), `MODO` (mode), `TIEMPO` (time), `COMPAS` (bars), `CERRADO` (closed).

#### Platform D3 external display (optional, 8 squares)

- Each square shows one bank channel: its name on top and what its knob does on the current page below (for example `Snare` / `10%L`).
- The square of the strip the fader is on (the same one you see on the Nano's small screen) shows the selected track and its volume, or the wheel mode.
- Button messages fill all 8 squares; turning a knob changes only its own square.
- After opening FL, touch the fader once: that is how the script learns which strip it is on. Until then, all 8 squares repeat the same view.

#### Bugs of the original script that were fixed

- Shift + Solo no longer raises an error (`NameError`).
- Shift + yellow key (F1–F8): if you let go of Shift before the key, FL still gets the release of that F key, and the key's normal function is no longer triggered (for example, undo on key 7).
- Holding Undo and turning the wheel no longer raises an error (it said `ui.GetHintMsg` instead of `ui.getHintMsg`).
- Free page: the fader's value text is now right (it used the wrong scale).

#### Options for advanced users

At the top of the script there are switches (`True` / `False`) in case you prefer something as in the original script:

- `NanoFollowSelected`: the fader follows the selected track.
- `NanoLatchJogSources`: wheel modes latch (`False` = hold them down, as in FL).
- `NanoScreen`: short texts for the small screen (`False` = the original script's texts).
- `NanoStrips`: one channel per square on the Platform D3 (`False` = all 8 squares repeat the Nano's small screen).
- `NanoFaderKick`: a small extra push of the motor for very small moves (off by default).
- `NanoDebug`: prints diagnostics in VIEW > Script output.

#### What did not change

- The 40 coloured buttons (5 layers) send exactly what iCON's official FL Studio overlay says; what changes is how the script responds.
- Everything else works like FL's Mackie Control Universal script.

#### Documentation and tools

- README with a step-by-step installation manual.
- Interactive tutorial in Spanish: <https://noisybeats03-eng.github.io/icon-platform-nano-air-fl-studio/>. Click any key of the drawn controller to read what it does; the drawn screens show what the real ones should show. It includes the list of all 69 controls, the wheel modes, the Shift combinations, the knob pages, recipes and troubleshooting.
- `dev/` folder: an FL simulator with 112 checks and the tools that generate the tutorial's screens.

#### Good to know

- While you browse FL's menus, their texts (for example `Menu` / `View`) also appear on the small screen. This is normal.
- The warning `Invalid mixer track nr 501` may appear in VIEW > Script output. It comes from FL's original script and is harmless.
- FL keeps MIDI settings per device name, and the Nano has a different name over the cable than through the wireless receiver (for example `PlatformNano(A) V2.05` and `PlatformNano Air V1.02`). If you use both, set up both names once.
- Not tested on a Mac (the script is plain Python and should work).
