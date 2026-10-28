# PDF Local

> Herramientas tipo iLovePDF que corren **100 % en tu equipo**. Nada se sube a internet.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-GPL--3.0-green.svg)](LICENSE)
[![Flask](https://img.shields.io/badge/Flask-3.x-maroon.svg)](https://flask.palletsprojects.com/)

## Herramientas (23)

| Categoría | Herramientas |
|---|---|
| **Organizar** | Unir PDFs · Dividir/Extraer · Rotar Páginas · Marca de Agua · Numerar Páginas |
| **Optimizar** | Comprimir |
| **Seguridad** | Proteger con Contraseña · Desbloquear · Cambiar Contraseña · Eliminar Metadatos · Censurar PDF |
| **Convertir** | Imágenes → PDF · PDF → Imágenes · PDF → Word · PDF → TXT · PDF → HTML · Word → PDF · Excel → PDF · PowerPoint → PDF |
| **Editar** | Recortar PDF · Eliminar Páginas · Ordenar Páginas |
| **Utilidades** | Reparar PDF |

## Instalación

### Dependencias del sistema

| Sistema | Comando |
|---|---|
| **Arch Linux** | `sudo pacman -S ghostscript` |
| **Debian/Ubuntu** | `sudo apt install ghostscript` |
| **Fedora** | `sudo dnf install ghostscript` |
| **macOS** | `brew install ghostscript` |
| **Windows** | [Descargar Ghostscript](https://www.ghostscript.com/releases/gsdnld.html) |

> **Opcional:** Para convertir Word/Excel/PowerPoint a PDF, instala también **LibreOffice**.

### Python

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Abre **[http://127.0.0.1:5000](http://127.0.0.1:5000)** en tu navegador.

## Uso

1. Elige una herramienta desde la pantalla principal.
2. Arrastra uno o más archivos al área de carga.
3. Configura las opciones (si aplica) y presiona **Procesar**.
4. El resultado se descarga automáticamente.

Todo el procesamiento ocurre en memoria RAM; no se crean archivos temporales en disco.

## Estructura del proyecto

```
├── app.py              # Backend Flask: rutas API y lógica de cada herramienta
├── static/
│   └── index.html      # Interfaz: CSS + JS con las 23 herramientas
├── requirements.txt    # Dependencias Python
├── docs/               # Prototipos y guía de diseño
└── README.md           # Este archivo
```

### Agregar una nueva herramienta

1. **Backend:** Crea una función en `app.py` que reciba `(files, form)` y devuelva un archivo.
2. **Frontend:** Agrega una entrada en el objeto `TOOLS` de `static/index.html` con `label`, `desc`, `accept`, `fields`, `category`, `icon`, `badge` y `keywords`.

## Licencia

Distribuido bajo la licencia **GNU GPL v3**. Ver [LICENSE](LICENSE) para más detalles.
