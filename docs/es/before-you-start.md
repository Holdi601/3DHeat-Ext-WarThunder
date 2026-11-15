---
title: Antes de empezar
nav_order: 2
lang: es
source: before-you-start.md
source_hash: "99034fb56b0d"
nav_exclude: true
search_exclude: true
---
# Antes de empezar {#before-you-start}

¿Es tu primera vez con la línea de comandos? Esta página te lleva de cero a un
`heat3d-wt-replay` en funcionamiento en unos diez minutos. Si ya usas Python, ve
directamente a [Instalación](installing.md).

## 1. Instala Python {#install-python}

1. Descarga Python **3.10 o posterior** desde
   [python.org/downloads](https://www.python.org/downloads/).
2. En Windows, marca **Add python.exe to PATH** en la primera ventana del
   instalador y luego haz clic en **Install Now**.
3. En macOS y Linux, Python 3 suele estar ya instalado. Escribe `python3`
   donde estas páginas dicen `python`, y `pip3` en lugar de `pip`.

## 2. Abre una terminal {#open-a-terminal}

Una terminal es una ventana donde escribes comandos.

- **Windows:** abre la carpeta en el Explorador de archivos, haz clic en la barra
  de direcciones, escribe `cmd` y pulsa Intro. Se abre una ventana ya en esa carpeta.
- **macOS:** abre la aplicación **Terminal**. **Linux:** haz clic derecho en la
  carpeta y elige **Abrir en una terminal**.

Para ir a otra carpeta, escribe `cd` y la carpeta:

```bash
cd "C:\Users\tu\Downloads\3DHeat-Ext-WarThunder-main"
```

## 3. Comprueba que Python funciona {#check-that-python-works}

```bash
python --version
```

Deberías ver `Python 3.` y un número 10 o superior, por ejemplo
`Python 3.12.4`.

## 4. Consigue la herramienta e instálala {#get-the-tool-and-install-it}

1. En [la página de GitHub de la herramienta](https://github.com/Holdi601/3DHeat-Ext-WarThunder), haz clic en
   el botón verde **Code** y luego en **Download ZIP**, y descomprime el zip.
2. Abre una terminal en la carpeta descomprimida (la que tiene `README.md`).
3. Escribe:

   ```bash
   pip install -e .
   ```

   Al final deberías ver: `Successfully installed heat3d-ext-warthunder-0.2.0`
   (puede que con más nombres).
4. Compruébalo:

   ```bash
   heat3d-wt-replay --version
   ```

   Deberías ver: `heat3d-wt-replay 0.2.0`

## Cómo leer los comandos de estas páginas {#how-to-read-the-commands-on-these-pages}

- Las palabras entre corchetes angulares, como `<repeticiones>`, son marcadores:
  escribe ahí tu propio archivo o carpeta, sin los corchetes.
- Una ruta con espacios necesita comillas: `"C:\Program Files (x86)\Steam"`.
- El texto después de `#` es un comentario: no lo escribes.
- `-o out` escribe en una carpeta llamada `out` dentro de la carpeta donde esté
  tu terminal. Se crea si no existe.

## Cómo es un resultado correcto {#what-success-looks-like}

El comando muestra una línea por repetición, por ejemplo:

```text
ok out/<mapa>/<partida>.3dheat
```

y termina con el estado de salida `0`. Los archivos nuevos están en la carpeta `out`.

## Errores comunes {#common-errors}

| Lo que ves | Qué hacer |
|---|---|
| `'python' is not recognized ...` o `command not found` | Python no está en el PATH: instálalo de nuevo con **Add python.exe to PATH** marcado, o escribe `py` en lugar de `python` (Windows) |
| `'pip' is not recognized ...` | escribe `python -m pip install -e .` en su lugar |
| `'heat3d-wt-replay' is not recognized ...` | escribe `python -m heat3d_ext_warthunder` en lugar de `heat3d-wt-replay`; hace lo mismo |
| `No module named heat3d_ext_warthunder` | no estás en la carpeta de la herramienta, o no está instalada: entra con `cd` y ejecuta `pip install -e .` |
| `the following arguments are required: -o/--out` | añade `-o out` al comando |

Siguiente: [Convertir repeticiones](converting.md).
