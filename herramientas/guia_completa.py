# -*- coding: utf-8 -*-
"""
Guía completa, paso a paso y todo a mano (sin importar nada): de un proyecto vacío a la línea funcionando.
Genera docs/02_Guia_Completa.html   (y, si se pasa una ruta, la versión para publicar).

Uso:  python3 herramientas/guia_completa.py [ruta_para_publicar]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import guia_c1  # noqa: E402
import guia_c2  # noqa: E402
import guia_c3  # noqa: E402
import guia_c4  # noqa: E402
from guia_comun import Guia, escribir  # noqa: E402


def construir():
    G = Guia()
    partes = guia_c1.partes(G) + guia_c2.partes(G) + guia_c3.partes(G) + guia_c4.partes(G)
    final = ("<p>Con las 18 partes hechas tienes la línea completa: tanque con bomba y válvula de seguridad, botellas de 0,5 L y "
             "2 L con seguimiento FIFO, llenado con caudalímetro, TAP-01, rechazo de malas, clasificación en cajas, vigilancia "
             "de 40 s, alarmas por fase con lámparas verde/naranja/roja y pantalla HMI.</p>"
             "<p>La tabla de variables (página aparte) resume todas las variables, alarmas y decisiones del proyecto.</p>")
    return G.pagina(0, "", partes, ("Resultado final", final), "guia_completa.py",
                    titulo_tag="Guía Completa TIA",
                    cabecera="Guía completa <span>/ Línea de llenado en KOP, paso a paso</span>")


if __name__ == "__main__":
    escribir(construir(), "02_Guia_Completa.html")
