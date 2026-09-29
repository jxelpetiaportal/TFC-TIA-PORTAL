# -*- coding: utf-8 -*-
"""Piezas compartidas por todas las partes de la guía paso a paso."""
import html
import os
import sys

import datos_variables as D

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
e = html.escape

# Nombres largos que se repiten en los segmentos
MOD = '"DB_Linea".Modo.'
EMG = '"DB_Linea".Emergencia.'
FLA = '"DB_Linea".Flancos.'
NIV = '"DB_Linea".Tanque.'
LLE = '"DB_Linea".Llenado.'
PAR = '"DB_Linea".Param.'
FIFO = '"DB_FIFO".'


class Guia:
    def __init__(self):
        self.pasos = []   # (id, título, parte)

    def paso(self, id_, titulo, cuerpo, parte):
        self.pasos.append((id_, titulo, parte))
        n = len(self.pasos)
        return (f'<section class="paso" id="{id_}"><div class="pnum">{n}</div>'
                f'<div class="pbody"><h3>{titulo}</h3>{cuerpo}</div></section>')

    def pagina(self, num, subtitulo, partes, siguiente, fichero_py):
        """partes: [(letra, título, [html de pasos])]; siguiente: (título, html)."""
        cuerpo = ""
        for letra, titulo, pasos in partes:
            cuerpo += (f'<h2 class="parte" id="parte-{letra}"><span>Parte {letra}</span> {titulo}</h2>'
                       + "".join(pasos))
        indice, n = "", 0
        for letra, titulo, _ in partes:
            items = ""
            for id_, t, p in self.pasos:
                if p == letra:
                    n += 1
                    items += f"<li><a href='#{id_}'><span>{n}</span>{t}</a></li>"
            indice += f"<div><h4>{letra} · {titulo}</h4><ol>{items}</ol></div>"
        css = ""
        for nombre in ("estilo.css", "estilo_guia.css"):
            with open(os.path.join(os.path.dirname(__file__), nombre), encoding="utf-8") as fh:
                css += fh.read()
        sig_t, sig_html = siguiente
        return f"""<title>Guía TIA Parte {num}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>
{css}
</style>
<div class="wrap">
  <header class="top">
    <div class="eyebrow">TFC · Línea de llenado · Guía paso a paso</div>
    <h1>Parte {num} <span>/ {subtitulo}</span></h1>
    <div class="meta">
      <span>TIA Portal <b>V15</b></span><span>S7-PLCSIM <b>V15</b></span>
      <span><b>{len(self.pasos)}</b> pasos</span><span>Tabla de variables <b>{e(D.REVISION)}</b></span>
    </div>
  </header>
  <nav class="indice" aria-label="Índice">{indice}</nav>
  {cuerpo}
  <section class="sig">
    <h2>{sig_t}</h2>
    {sig_html}
  </section>
  <footer>Generado desde herramientas/{fichero_py} · Los dibujos KOP salen de herramientas/kop.py</footer>
</div>
<script>
document.querySelectorAll('button.copiar').forEach(function(b){{
  b.addEventListener('click',function(ev){{
    ev.preventDefault();
    var pre=document.getElementById(b.dataset.copiar);
    var ok=function(){{b.textContent='Copiado';setTimeout(function(){{b.textContent='Copiar';}},1500);}};
    var fallo=function(){{var r=document.createRange();r.selectNodeContents(pre);var s=getSelection();s.removeAllRanges();s.addRange(r);b.textContent='Seleccionado: Ctrl+C';}};
    try{{navigator.clipboard.writeText(pre.textContent).then(ok,fallo);}}catch(err){{fallo();}}
  }});
}});
</script>
"""


def escribir(pagina, nombre_docs):
    """Guarda docs/<nombre_docs> completo y, si se pasa una ruta por argumento, la versión para publicar."""
    ruta_html = os.path.join(RAIZ, "docs", nombre_docs)
    with open(ruta_html, "w", encoding="utf-8") as fh:
        fh.write('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
                 '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
                 '</head>\n<body>\n' + pagina + '\n</body>\n</html>\n')
    print("HTML ->", ruta_html)
    if len(sys.argv) > 1:
        with open(sys.argv[1], "w", encoding="utf-8") as fh:
            fh.write(pagina)
        print("Web  ->", sys.argv[1])


def ruta(*partes):
    return '<span class="ruta">' + ' <b>›</b> '.join(e(p) for p in partes) + '</span>'


def tip(txt):
    return f'<div class="tip"><b>Truco</b> {txt}</div>'


def ojo(txt):
    return f'<div class="ojo"><b>Ojo</b> {txt}</div>'


def lista(*items, ordenada=True):
    tag = "ol" if ordenada else "ul"
    return f"<{tag} class='acc'>" + "".join(f"<li>{i}</li>" for i in items) + f"</{tag}>"


def tabla(cab, filas):
    th = "".join(f"<th>{c}</th>" for c in cab)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in f) + "</tr>" for f in filas)
    return f'<div class="tw"><table class="vt"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


def seg(num, titulo, dibujo, explicacion):
    return (f'<figure class="seg"><figcaption><span>Segmento {num}</span> {e(titulo)}</figcaption>'
            f'<div class="kopw"><pre class="kop">{e(dibujo)}</pre></div>'
            f'<div class="segtxt">{explicacion}</div></figure>')


def interfaz(filas):
    return tabla(["Sección", "Nombre", "Tipo", "Para qué"],
                 [(f"<span class='mono'>{a}</span>", f"<span class='nm'>{b}</span>",
                   f"<span class='ty'>{c}</span>", d) for a, b, c, d in filas])


def fuente(nombre, texto):
    id_ = "src-" + nombre.split(".")[0]
    return (f'<details class="src"><summary><span class="mono">{e(nombre)}</span>'
            f'<button type="button" class="copiar" data-copiar="{id_}">Copiar</button></summary>'
            f'<pre id="{id_}">{e(texto)}</pre></details>')


def leer_fuente(nombre):
    with open(os.path.join(RAIZ, "tia", "fuentes", nombre), encoding="ascii") as fh:
        return fh.read().replace("\r\n", "\n")


def m(txt):
    """Texto en monoespaciado (nombres de variables dentro de un párrafo)."""
    return f"<span class='mono'>{e(txt)}</span>"
