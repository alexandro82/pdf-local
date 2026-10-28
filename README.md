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

## Acceso desde otros equipos en la red

Para que otros dispositivos de la red accedan a PDF Local, configura **Nginx** como reverse proxy en el puerto 80.

### 1. Instalar Nginx

```bash
sudo apt install nginx
```

### 2. Configurar el reverse proxy

```bash
sudo cp nginx/pdf-local.conf /etc/nginx/sites-available/pdf-local
sudo ln -s /etc/nginx/sites-available/pdf-local /etc/nginx/sites-enabled/
sudo nginx -t                          # Verificar configuración
sudo systemctl restart nginx
```

Ajusta la IP en `server_name` del archivo de configuración si tu equipo tiene otra dirección.

### 3. Configurar el servicio systemd (opcional)

```bash
sudo cp nginx/pdf-local.service /etc/systemd/system/
# Edita las rutas en el servicio según tu instalación
sudo systemctl daemon-reload
sudo systemctl enable --now pdf-local
```

### 4. Abrir el puerto en el firewall

```bash
sudo ufw allow 80/tcp
```

### 5. Acceder desde otro equipo

Abre el navegador en cualquier dispositivo de la red y navega a:

```
http://192.168.0.6
```

> **Nota de seguridad:** La aplicación escucha en `0.0.0.0`, lo que permite acceso desde la red local. Si necesitas acceso externo, configura autenticación en Nginx o usa HTTPS con Let's Encrypt.

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
├── nginx/
│   ├── pdf-local.conf  # Configuración de Nginx como reverse proxy
│   └── pdf-local.service # Servicio systemd para ejecutar en segundo plano
├── requirements.txt    # Dependencias Python
├── docs/               # Prototipos y guía de diseño
└── README.md           # Este archivo
```

### Agregar una nueva herramienta

1. **Backend:** Crea una función en `app.py` que reciba `(files, form)` y devuelva un archivo.
2. **Frontend:** Agrega una entrada en el objeto `TOOLS` de `static/index.html` con `label`, `desc`, `accept`, `fields`, `category`, `icon`, `badge` y `keywords`.

## Licencia

Distribuido bajo la licencia **GNU GPL v3**. Ver [LICENSE](LICENSE) para más detalles.
