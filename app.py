"""PDF Local: herramientas tipo iLovePDF que corren 100 % en tu equipo.
Uso: python app.py  ->  http://127.0.0.1:5000
"""
import io, os, shutil, subprocess, tempfile, zipfile
from flask import Flask, request, send_file, jsonify, send_from_directory
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image
import pypdfium2 as pdfium
import pdfplumber
from docx import Document
from docx.shared import Pt, Inches

BASE = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024 * 1024  # 1 GB


def open_pdf(f, password=""):
    r = PdfReader(io.BytesIO(f.read()))
    if r.is_encrypted and r.decrypt(password) == 0:
        raise ValueError(f"'{f.filename}' está protegido: contraseña incorrecta o faltante.")
    return r


def parse_pages(spec, n):
    groups = []
    for part in spec.replace(" ", "").split(","):
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            a, b = int(a) if a else 1, int(b) if b else n
        else:
            a = b = int(part)
        if a < 1 or b > n or a > b:
            raise ValueError(f"Rango inválido '{part}' (el PDF tiene {n} páginas).")
        groups.append(list(range(a - 1, b)))
    if not groups:
        raise ValueError("Indica las páginas.")
    return groups


def pdf_bytes(writer):
    buf = io.BytesIO()
    writer.write(buf)
    return buf.getvalue()


def out(data, name, mime="application/pdf"):
    return send_file(io.BytesIO(data), download_name=name, mimetype=mime, as_attachment=True)


def zip_out(items, name):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for n, d in items:
            z.writestr(n, d)
    return out(buf.getvalue(), name, "application/zip")


def one_pdf(files):
    if len(files) != 1:
        raise ValueError("Sube exactamente un PDF.")
    return files[0]


def overlay(w, h, draw):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(w, h))
    draw(c)
    c.save()
    buf.seek(0)
    return PdfReader(buf).pages[0]


# ---------- herramientas ----------
def merge(files, form):
    if len(files) < 2:
        raise ValueError("Sube al menos 2 PDF.")
    w = PdfWriter()
    for f in files:
        for p in open_pdf(f, form.get("password", "")).pages:
            w.add_page(p)
    return out(pdf_bytes(w), "unido.pdf")


def split(files, form):
    r = open_pdf(one_pdf(files), form.get("password", ""))
    n, mode = len(r.pages), form.get("mode", "each")
    groups = [[i] for i in range(n)] if mode == "each" else parse_pages(form.get("pages", ""), n)
    if mode == "extract":
        groups = [[i for g in groups for i in g]]
    parts = []
    for k, g in enumerate(groups, 1):
        w = PdfWriter()
        for i in g:
            w.add_page(r.pages[i])
        parts.append((f"parte_{k:03d}.pdf", pdf_bytes(w)))
    return out(parts[0][1], "extraido.pdf") if len(parts) == 1 else zip_out(parts, "dividido.zip")


def rotate(files, form):
    r = open_pdf(one_pdf(files), form.get("password", ""))
    n = len(r.pages)
    sel = {i for g in parse_pages(form["pages"], n) for i in g} if form.get("pages", "").strip() else set(range(n))
    angle = int(form.get("angle", 90))
    w = PdfWriter()
    for i, p in enumerate(r.pages):
        if i in sel:
            p.rotate(angle)
        w.add_page(p)
    return out(pdf_bytes(w), "rotado.pdf")


def compress(files, form):
    if not shutil.which("gs"):
        raise ValueError("Falta Ghostscript. Instálalo (en Arch: sudo pacman -S ghostscript).")
    level = {"screen": "/screen", "ebook": "/ebook", "printer": "/printer"}.get(form.get("level"), "/ebook")
    f = one_pdf(files)
    with tempfile.TemporaryDirectory() as d:
        src, dst = os.path.join(d, "in.pdf"), os.path.join(d, "out.pdf")
        f.save(src)
        subprocess.run(["gs", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4", f"-dPDFSETTINGS={level}",
                        "-dNOPAUSE", "-dQUIET", "-dBATCH", f"-sOutputFile={dst}", src], check=True)
        a, b = os.path.getsize(src), os.path.getsize(dst)
        with open(dst if b < a else src, "rb") as fh:  # si no mejora, devuelve el original
            return out(fh.read(), "comprimido.pdf")


def watermark(files, form):
    text = form.get("text", "").strip()
    if not text:
        raise ValueError("Escribe el texto de la marca de agua.")
    size, op = int(form.get("size", 60)), float(form.get("opacity", 0.25))
    r = open_pdf(one_pdf(files), form.get("password", ""))
    w = PdfWriter()
    for p in r.pages:
        W, H = float(p.mediabox.width), float(p.mediabox.height)

        def draw(c):
            c.setFillColorRGB(0.4, 0.4, 0.4)
            c.setFillAlpha(op)
            c.setFont("Helvetica-Bold", size)
            c.translate(W / 2, H / 2)
            c.rotate(45)
            c.drawCentredString(0, 0, text)
        p.merge_page(overlay(W, H, draw))
        w.add_page(p)
    return out(pdf_bytes(w), "marca_de_agua.pdf")


def numbers(files, form):
    r = open_pdf(one_pdf(files), form.get("password", ""))
    n, w = len(r.pages), PdfWriter()
    for i, p in enumerate(r.pages):
        W, H = float(p.mediabox.width), float(p.mediabox.height)

        def draw(c):
            c.setFont("Helvetica", 10)
            c.drawCentredString(W / 2, 20, f"{i + 1} / {n}")
        p.merge_page(overlay(W, H, draw))
        w.add_page(p)
    return out(pdf_bytes(w), "numerado.pdf")


def protect(files, form):
    pw = form.get("newpassword", "")
    if not pw:
        raise ValueError("Escribe una contraseña.")
    r = open_pdf(one_pdf(files), form.get("password", ""))
    w = PdfWriter()
    for p in r.pages:
        w.add_page(p)
    w.encrypt(pw)
    return out(pdf_bytes(w), "protegido.pdf")


def unlock(files, form):
    r = open_pdf(one_pdf(files), form.get("password", ""))
    w = PdfWriter()
    for p in r.pages:
        w.add_page(p)
    return out(pdf_bytes(w), "desbloqueado.pdf")


def images2pdf(files, form):
    imgs = [Image.open(f).convert("RGB") for f in files]
    if not imgs:
        raise ValueError("Sube al menos una imagen.")
    buf = io.BytesIO()
    imgs[0].save(buf, "PDF", save_all=True, append_images=imgs[1:])
    return out(buf.getvalue(), "imagenes.pdf")


def pdf2images(files, form):
    fmt = "JPEG" if form.get("format") == "jpg" else "PNG"
    ext = "jpg" if fmt == "JPEG" else "png"
    dpi = int(form.get("dpi", 150))
    doc = pdfium.PdfDocument(one_pdf(files).read())
    items = []
    for i in range(len(doc)):
        img = doc[i].render(scale=dpi / 72).to_pil().convert("RGB")
        b = io.BytesIO()
        img.save(b, fmt)
        items.append((f"pagina_{i + 1:03d}.{ext}", b.getvalue()))
    return zip_out(items, "paginas.zip")


# ---------- PDF extraction tools ----------
def pdf2word(files, form):
    f = one_pdf(files)
    doc = Document()
    with pdfplumber.open(io.BytesIO(f.read())) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                if i > 0:
                    doc.add_paragraph("")
                for para in text.split("\n"):
                    doc.add_paragraph(para)
    buf = io.BytesIO()
    doc.save(buf)
    return out(buf.getvalue(), "documento.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")


def pdf2txt(files, form):
    f = one_pdf(files)
    parts = []
    with pdfplumber.open(io.BytesIO(f.read())) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                parts.append(text)
    if not parts:
        raise ValueError("No se encontró texto en el PDF.")
    return out("\n".join(parts).encode("utf-8"), "texto.txt", "text/plain")


def pdf2html(files, form):
    f = one_pdf(files)
    body_parts = []
    with pdfplumber.open(io.BytesIO(f.read())) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            lines = text.split("\n")
            body_parts.append(f"<h2>Página {i+1}</h2>\n" + "".join(f"<p>{line}</p>" for line in lines if line.strip()))
    html = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8"><title>Documento</title>
<style>body{{font-family:sans-serif;max-width:800px;margin:2rem auto;padding:0 1rem}}
h2{{border-bottom:1px solid #ccc;padding-bottom:0.25rem}}</style></head>
<body>{"".join(body_parts)}</body></html>"""
    return out(html.encode("utf-8"), "documento.html", "text/html")


# ---------- Office → PDF tools ----------
def _office2pdf(files, form, extensions):
    if len(files) != 1:
        raise ValueError("Sube exactamente un archivo.")
    f = files[0]
    if not any(f.filename.lower().endswith(ext) for ext in extensions):
        raise ValueError(f"Formato no soportado. Acepta: {', '.join(extensions)}")
    if not shutil.which("soffice"):
        raise ValueError("Falta LibreOffice. Instálalo (en Arch: sudo pacman -S libreoffice).")
    with tempfile.TemporaryDirectory() as d:
        src = os.path.join(d, f.filename)
        f.save(src)
        dst_dir = os.path.join(d, "out")
        os.makedirs(dst_dir)
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", dst_dir, src],
                       check=True, capture_output=True, timeout=120)
        pdf_file = os.path.join(dst_dir, os.path.splitext(f.filename)[0] + ".pdf")
        if not os.path.exists(pdf_file):
            raise ValueError("La conversión falló. Verifica que el archivo no esté dañado.")
        with open(pdf_file, "rb") as fh:
            return out(fh.read(), os.path.basename(pdf_file))


def docx2pdf(files, form):
    return _office2pdf(files, form, [".docx", ".doc"])


def xlsx2pdf(files, form):
    return _office2pdf(files, form, [".xlsx", ".xls"])


def pptx2pdf(files, form):
    return _office2pdf(files, form, [".pptx", ".ppt"])


# ---------- Editing tools ----------
def crop(files, form):
    f = one_pdf(files)
    r = open_pdf(f, form.get("password", ""))
    top = float(form.get("top", 0))
    bottom = float(form.get("bottom", 0))
    left = float(form.get("left", 0))
    right = float(form.get("right", 0))
    w = PdfWriter()
    for p in r.pages:
        mb = p.mediabox
        llx = float(mb.left) + left
        lly = float(mb.bottom) + bottom
        urx = float(mb.right) - right
        ury = float(mb.top) - top
        if llx >= urx or lly >= ury:
            raise ValueError("Los márgenes de recorte son mayores que el tamaño de la página.")
        p.mediabox.lower_left = (llx, lly)
        p.mediabox.upper_right = (urx, ury)
        w.add_page(p)
    return out(pdf_bytes(w), "recortado.pdf")


def delete_pages(files, form):
    r = open_pdf(one_pdf(files), form.get("password", ""))
    n = len(r.pages)
    pages_str = form.get("pages", "").strip()
    if not pages_str:
        raise ValueError("Indica las páginas a eliminar.")
    to_delete = set()
    for part in pages_str.replace(" ", "").split(","):
        if "-" in part:
            a, b = part.split("-", 1)
            a, b = int(a) if a else 1, int(b) if b else n
            if a < 1 or b > n or a > b:
                raise ValueError(f"Rango inválido '{part}' (el PDF tiene {n} páginas).")
            to_delete.update(range(a - 1, b))
        else:
            p = int(part)
            if p < 1 or p > n:
                raise ValueError(f"Página {p} fuera de rango (el PDF tiene {n} páginas).")
            to_delete.add(p - 1)
    if len(to_delete) == n:
        raise ValueError("No puedes eliminar todas las páginas.")
    w = PdfWriter()
    for i in range(n):
        if i not in to_delete:
            w.add_page(r.pages[i])
    return out(pdf_bytes(w), "paginas_eliminadas.pdf")


def reorder(files, form):
    if len(files) < 1:
        raise ValueError("Sube al menos un PDF.")
    w = PdfWriter()
    for f in files:
        r = open_pdf(f, form.get("password", ""))
        for p in r.pages:
            w.add_page(p)
    return out(pdf_bytes(w), "reordenado.pdf")


def redact(files, form):
    f = one_pdf(files)
    r = open_pdf(f, form.get("password", ""))
    n = len(r.pages)
    pages_str = form.get("pages", "").strip()
    if not pages_str:
        raise ValueError("Indica las páginas a censurar.")
    sel = set()
    for part in pages_str.replace(" ", "").split(","):
        if "-" in part:
            a, b = part.split("-", 1)
            a, b = int(a) if a else 1, int(b) if b else n
            sel.update(range(a - 1, b))
        else:
            p = int(part)
            sel.add(p - 1)
    # Draw black rectangles covering the entire page content
    w = PdfWriter()
    for i, p in enumerate(r.pages):
        W, H = float(p.mediabox.width), float(p.mediabox.height)
        # Draw a semi-transparent black overlay to redact
        def draw(c):
            c.setFillColorRGB(0, 0, 0)
            c.setFillAlpha(1.0)
            c.rect(0, 0, W, H, fill=1, stroke=0)
        p.merge_page(overlay(W, H, draw))
        w.add_page(p)
    return out(pdf_bytes(w), "censurado.pdf")


# ---------- Security tools ----------
def change_password(files, form):
    old_pw = form.get("password", "")
    new_pw = form.get("newpassword", "")
    if not new_pw:
        raise ValueError("Escribe una nueva contraseña.")
    r = open_pdf(one_pdf(files), old_pw)
    w = PdfWriter()
    for p in r.pages:
        w.add_page(p)
    w.encrypt(new_pw)
    return out(pdf_bytes(w), "contrasena_cambiada.pdf")


def strip_metadata(files, form):
    r = open_pdf(one_pdf(files), form.get("password", ""))
    w = PdfWriter()
    for p in r.pages:
        w.add_page(p)
    w.metadata = {}
    return out(pdf_bytes(w), "sin_metadatos.pdf")


# ---------- Utility tools ----------
def repair(files, form):
    f = one_pdf(files)
    try:
        r = PdfReader(io.BytesIO(f.read()))
        w = PdfWriter()
        for p in r.pages:
            w.add_page(p)
        return out(pdf_bytes(w), "reparado.pdf")
    except Exception as e:
        # Try pdfium as fallback
        try:
            doc = pdfium.PdfDocument(f.read())
            buf = io.BytesIO()
            doc.save(buf)
            return out(buf.getvalue(), "reparado.pdf")
        except Exception:
            raise ValueError(f"No se pudo reparar el PDF: {e}")


TOOLS = dict(merge=merge, split=split, rotate=rotate, compress=compress, watermark=watermark,
             numbers=numbers, protect=protect, unlock=unlock, images2pdf=images2pdf, pdf2images=pdf2images,
             pdf2word=pdf2word, pdf2txt=pdf2txt, pdf2html=pdf2html,
             docx2pdf=docx2pdf, xlsx2pdf=xlsx2pdf, pptx2pdf=pptx2pdf,
             crop=crop, delete_pages=delete_pages, reorder=reorder, redact=redact,
             change_password=change_password, strip_metadata=strip_metadata, repair=repair)


@app.post("/api/<tool>")
def api(tool):
    fn = TOOLS.get(tool)
    if not fn:
        return jsonify(error="Herramienta desconocida"), 404
    try:
        return fn(request.files.getlist("files"), request.form)
    except (ValueError, KeyError) as e:
        return jsonify(error=str(e)), 400
    except Exception as e:
        return jsonify(error=f"Error: {e}"), 500


@app.get("/")
def index():
    return send_from_directory(os.path.join(BASE, "static"), "index.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
