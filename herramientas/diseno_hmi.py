# -*- coding: utf-8 -*-
"""
Diseño de la pantalla HMI (KTP700 Basic, 800 × 480): boceto de cada imagen y tabla de objetos
con posición, tamaño, colores, variable y animación, para reproducirlo en WinCC (TIA Portal V15).

Genera docs/03_Diseno_HMI.html   (y, si se pasa una ruta, la versión para publicar).
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import datos_variables as D  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
e = html.escape

# ---------------------------------------------------------------------------
# Paleta (estilo "HMI de alto rendimiento": gris neutro y color solo para estados)
# ---------------------------------------------------------------------------
PAL = {
    "fondo":      ("#E6E8EB", "230, 232, 235", "Fondo de todas las imágenes"),
    "panel":      ("#F5F6F7", "245, 246, 247", "Fondo de los paneles"),
    "borde":      ("#C4C8CE", "196, 200, 206", "Borde de paneles y campos"),
    "cabecera":   ("#263238", "38, 50, 56", "Cabecera y barra de navegación"),
    "boton":      ("#37474F", "55, 71, 79", "Botones de navegación y manuales"),
    "titulo":     ("#455A64", "69, 90, 100", "Títulos de panel"),
    "texto":      ("#212121", "33, 33, 33", "Texto normal"),
    "tenue":      ("#607D8B", "96, 125, 139", "Texto secundario y etiquetas"),
    "apagado":    ("#CFD8DC", "207, 216, 220", "Lámpara apagada / equipo parado"),
    "marcha":     ("#2EA043", "46, 160, 67", "En marcha / verde"),
    "aviso":      ("#F59E0B", "245, 158, 11", "Aviso / naranja"),
    "fallo":      ("#D32F2F", "211, 47, 47", "Fallo / rojo"),
    "agua":       ("#409CD6", "64, 156, 214", "Agua del tanque"),
    "acento":     ("#1976D2", "25, 118, 210", "Valores y botón activo"),
    "blanco":     ("#FFFFFF", "255, 255, 255", "Campos E/S y texto sobre oscuro"),
}
C = {k: v[0] for k, v in PAL.items()}

ESTADOS = [(0, "LISTA", "boton"), (1, "EN MARCHA", "marcha"), (2, "TERMINANDO", "aviso"),
           (3, "REARME PENDIENTE", "aviso"), (4, "PARADA DE SEGURIDAD", "fallo"), (5, "MODO MANUAL", "acento")]

# ---------------------------------------------------------------------------
# Objetos
# Cada objeto: dict(t=tipo, x, y, w, h, ...) — tipos:
#   rect, text, circle, button, io, bar, tank, pump, valve, belt, bottle, sym, time
# Campos de la tabla: obj (objeto de TIA), src (dónde está), var, anim, nota
# ---------------------------------------------------------------------------
OBJ_RECT = ("Rectángulo", "Herramientas › Objetos básicos")
OBJ_TEXT = ("Campo de texto", "Herramientas › Objetos básicos")
OBJ_CIRC = ("Círculo", "Herramientas › Objetos básicos")
OBJ_BTN = ("Botón", "Herramientas › Elementos")
OBJ_IO = ("Campo E/S", "Herramientas › Elementos")
OBJ_BAR = ("Barra", "Herramientas › Elementos")
OBJ_SYM = ("Campo E/S simbólico", "Herramientas › Elementos")
OBJ_TIME = ("Campo de fecha/hora", "Herramientas › Elementos")
OBJ_GRAF = ("Visor de gráficos", "Herramientas › Gráficos › Carpetas de gráficos de WinCC")


NOMBRE_COLOR = {"apagado": "gris claro", "marcha": "verde", "aviso": "naranja", "fallo": "rojo", "agua": "azul agua",
                "acento": "azul", "boton": "gris oscuro", "cabecera": "gris muy oscuro", "blanco": "blanco",
                "tenue": "gris azulado", "borde": "gris borde", "panel": "gris panel", "titulo": "gris título",
                "texto": "negro", "fondo": "gris fondo"}


def rgb(k):
    """Nombre del color y sus números RGB, tal y como se escriben en WinCC."""
    return f"{NOMBRE_COLOR[k]} (RGB {PAL[k][1]} · código {PAL[k][0]})"


def anim_color(var, on="marcha", borde=None):
    pp = f"primer plano {rgb(borde)}" if borde else "primer plano el mismo color que el fondo"
    return (f"Receta B · variable {var} · Rango 0 → fondo {rgb('apagado')} · Rango 1 → fondo {rgb(on)} · "
            f"en las dos filas {pp} y parpadeo No")


def plantilla():
    """Cabecera y barra de navegación comunes (plantilla)."""
    o = [
        dict(t="rect", x=0, y=0, w=800, h=48, fill="cabecera", obj=OBJ_RECT, nota="Cabecera, sin borde"),
        dict(t="text", x=16, y=12, w=240, h=24, txt="LÍNEA DE LLENADO", size=16, bold=True, color="blanco", obj=OBJ_TEXT),
        dict(t="sym", x=500, y=10, w=196, h=28, var="DB_Linea.Modo.Estado", demo=1, obj=OBJ_SYM,
             anim="Receta E (modo Salida, lista de textos «Estados») + Receta B con 6 filas: "
                  + " · ".join(f"Rango {n} → fondo {rgb(c)}" for n, _, c in ESTADOS)
                  + " · en todas primer plano blanco (255, 255, 255) · parpadeo Sí solo en el 4"),
        dict(t="time", x=708, y=12, w=80, h=24, obj=OBJ_TIME, nota="Modo: hora del sistema, texto blanco"),
        dict(t="rect", x=0, y=424, w=800, h=56, fill="cabecera", obj=OBJ_RECT, nota="Barra de navegación"),
    ]
    for i, (nom, img) in enumerate([("INICIO", "Inicio"), ("MANUAL", "Manual"), ("ALARMAS", "Alarmas"), ("PRODUCCIÓN", "Produccion")]):
        o.append(dict(t="button", x=12 + i * 198, y=430, w=184, h=44, txt=nom, fill="boton", color="blanco", size=14,
                      obj=OBJ_BTN, anim=f"Receta D · evento Hacer clic › ActivarImagen › {img}"))
    return o


def panel(x, y, w, h, titulo):
    return [dict(t="rect", x=x, y=y, w=w, h=h, fill="panel", stroke="borde", r=4, obj=OBJ_RECT, nota="Panel: borde 1 px"),
            dict(t="text", x=x + 12, y=y + 8, w=w - 24, h=18, txt=titulo, size=12, bold=True, color="titulo", obj=OBJ_TEXT)]


def lamp(x, y, d, var, color_on, demo=0, nota=""):
    return dict(t="circle", x=x, y=y, w=d, h=d, fill=color_on if demo else "apagado", obj=OBJ_CIRC,
                var=var, anim=anim_color(var, color_on), b=color_on, nota=nota)


def io(x, y, w, h, var, fmt, demo, size=14, modo="Salida", color="acento", bold=True):
    return dict(t="io", x=x, y=y, w=w, h=h, var=var, demo=demo, size=size, color=color, bold=bold, obj=OBJ_IO,
                anim=f"Receta E · modo {modo} · formato {fmt}")


# --- INICIO -----------------------------------------------------------------
def imagen_inicio():
    o = panel(8, 56, 180, 360, "TANQUE")
    o += [
        dict(t="pump", x=28, y=84, w=40, h=40, on=True, obj=("Círculo + Campo de texto", "Herramientas › Objetos básicos"),
             var="DB_Linea.Tanque.Bomba_Marcha", b="marcha",
             anim="En el círculo: " + anim_color("DB_Linea.Tanque.Bomba_Marcha", borde="cabecera"),
             nota="Círculo 40 × 40 con borde 2 px gris oscuro. Encima, un Campo de texto en (28, 92), 40 × 24, con el "
                  "símbolo ▲ (cópialo de aquí), Tahoma 18 negrita, blanco, centrado y fondo transparente. "
                  "Si en la pantalla sale un cuadrado, escribe una P"),
        dict(t="text", x=76, y=94, w=100, h=18, txt="Bomba", size=12, color="tenue", obj=OBJ_TEXT),
        dict(t="valve", x=36, y=138, w=24, h=24, on=True, obj=("Rectángulo + 2 Líneas", "Herramientas › Objetos básicos"),
             var="VS_Valvula_Seguridad", b="marcha",
             anim="En el rectángulo: " + anim_color("VS_Valvula_Seguridad", borde="cabecera"),
             nota="Rectángulo 24 × 24 con borde 1 px gris oscuro. Encima, dos Líneas gris oscuro de 2 px que forman una X: "
                  "de (36, 138) a (60, 162) y de (60, 138) a (36, 162)"),
        dict(t="text", x=76, y=142, w=104, h=18, txt="Válv. seguridad", size=12, color="tenue", obj=OBJ_TEXT),
        dict(t="tank", x=40, y=184, w=100, h=170, obj=OBJ_RECT,
             nota="El contorno del tanque. Fondo: estilo transparente. Borde: 2 px, color tenue (96, 125, 139). "
                  "Esquinas redondeadas: radio X 8 y radio Y 8"),
        dict(t="bar", x=44, y=188, w=92, h=162, var="DB_Linea.Tanque.Nivel_Pct", demo=62, fill="agua", obj=OBJ_BAR,
             anim="Receta F · mín 0 · máx 100 · color de barra agua (64, 156, 214) · fondo blanco · sin borde · "
                  "sin escala ni etiquetas · crece de abajo arriba",
             nota="Va dentro del contorno, 4 px más pequeña por cada lado"),
        dict(t="line", x=140, y=204, w=6, h=0, color="tenue", obj=("Línea", "Herramientas › Objetos básicos"),
             nota="Marca del 90 %: de (140, 204) a (146, 204), 1 px, color tenue"),
        dict(t="line", x=140, y=309, w=6, h=0, color="tenue", obj=("Línea", "Herramientas › Objetos básicos"),
             nota="Marca del 25 %: de (140, 309) a (146, 309), 1 px, color tenue"),
        dict(t="text", x=144, y=198, w=40, h=14, txt="90 %", size=10, color="tenue", obj=OBJ_TEXT),
        dict(t="text", x=144, y=303, w=40, h=14, txt="25 %", size=10, color="tenue", obj=OBJ_TEXT),
        io(40, 364, 100, 30, "DB_Linea.Tanque.Nivel_Pct", "999.9 (y el texto % en Unidad, o en un campo de texto al lado)",
           "62.0 %", size=16),
    ]
    o += panel(196, 56, 596, 214, "LÍNEA")
    cintas = [("C1", 212, 150, "Cinta_C1_Entrada", True), ("C2", 366, 96, "Cinta_C2_Llenado", False),
              ("C3", 466, 96, "Cinta_C3_Taponado", True), ("C4", 566, 124, "Cinta_C4_Rechazo", False)]
    for nom, x, w, var, on in cintas:
        o.append(dict(t="belt", x=x, y=176, w=w, h=18, on=on, var=var, obj=OBJ_RECT, anim=anim_color(var), b="marcha"))
        o.append(dict(t="text", x=x, y=198, w=w, h=14, txt=nom, size=11, color="tenue", align="c", obj=OBJ_TEXT))
    o += [
        dict(t="belt", x=702, y=92, w=18, h=172, on=True, vertical=True, var="Cinta_C5_Hacia_05L / Cinta_C5_Hacia_2L",
             obj=("2 Rectángulos", "Herramientas › Objetos básicos"), b="marcha",
             anim="Mitad de arriba: " + anim_color("Cinta_C5_Hacia_05L") + ". Mitad de abajo: lo mismo con Cinta_C5_Hacia_2L",
             nota="La C5 se dibuja en dos mitades para que se vea hacia qué caja va: rectángulo de arriba (702, 92), "
                  "18 × 84, hacia la caja de 0,5 L; rectángulo de abajo (702, 176), 18 × 88, hacia la caja de 2 L. "
                  "Haz el de arriba, cópialo y en la copia cambia posición, alto y variable"),
        dict(t="text", x=682, y=270 - 20, w=16, h=14, txt="C5", size=11, color="tenue", obj=OBJ_TEXT),
        dict(t="text", x=212, y=154, w=80, h=16, txt="Entrada →", size=11, color="tenue", obj=OBJ_TEXT),
        # llenado
        dict(t="rect", x=402, y=128, w=24, h=40, fill="boton", r=3, obj=OBJ_RECT, nota="Boquilla de llenado"),
        lamp(406, 110, 16, "DB_Linea.Llenado.Valvula", "agua", demo=1, nota="Válvula de llenado"),
        dict(t="text", x=378, y=84, w=80, h=16, txt="LLENADO", size=11, bold=True, color="titulo", obj=OBJ_TEXT),
        io(432, 132, 64, 22, "DB_Linea.Llenado.Volumen_L", "9.99 L", "1.21 L", size=12),
        # TAP-01
        dict(t="rect", x=496, y=126, w=36, h=30, fill="marcha", r=3, var="TAP01_Bajar", obj=OBJ_RECT, b="marcha",
             anim=anim_color("TAP01_Bajar")),
        dict(t="text", x=490, y=84, w=60, h=16, txt="TAP-01", size=11, bold=True, color="titulo", obj=OBJ_TEXT),
        # empujador
        dict(t="rect", x=612, y=148, w=28, h=24, fill="apagado", r=3, var="Empujador_Avanzar", obj=OBJ_RECT,
             b="aviso", anim=anim_color("Empujador_Avanzar", "aviso")),
        dict(t="text", x=596, y=84, w=80, h=16, txt="RECHAZO", size=11, bold=True, color="titulo", obj=OBJ_TEXT),
        dict(t="rect", x=596, y=214, w=64, h=34, fill="blanco", stroke="borde", r=3, obj=OBJ_RECT, nota="Caja de malas"),
        dict(t="text", x=596, y=224, w=64, h=16, txt="MALAS", size=11, color="tenue", align="c", obj=OBJ_TEXT),
        # cajas buenas
        dict(t="rect", x=728, y=92, w=56, h=34, fill="blanco", stroke="borde", r=3, obj=OBJ_RECT, nota="Caja 0,5 L"),
        dict(t="text", x=728, y=102, w=56, h=16, txt="0,5 L", size=11, color="tenue", align="c", obj=OBJ_TEXT),
        dict(t="rect", x=728, y=230, w=56, h=34, fill="blanco", stroke="borde", r=3, obj=OBJ_RECT, nota="Caja 2 L"),
        dict(t="text", x=728, y=240, w=56, h=16, txt="2 L", size=11, color="tenue", align="c", obj=OBJ_TEXT),
        # botellas por zona
        dict(t="bottle", x=406, y=152, w=16, h=24, on=True, var="DB_Linea.Zonas.Z1", obj=OBJ_RECT,
             anim="Receta C · variable DB_Linea.Zonas.Z1 · visible con 1"),
        dict(t="bottle", x=506, y=152, w=16, h=24, on=True, var="DB_Linea.Zonas.Z2", obj=OBJ_RECT,
             anim="Receta C · variable DB_Linea.Zonas.Z2 · visible con 1"),
        dict(t="bottle", x=618, y=152 + 2, w=16, h=22, on=False, var="DB_Linea.Zonas.Z3", obj=OBJ_RECT,
             anim="Receta C · variable DB_Linea.Zonas.Z3 · visible con 1"),
        dict(t="bottle", x=703, y=150, w=16, h=24, on=False, var="DB_Linea.Zonas.Z4", obj=OBJ_RECT,
             anim="Receta C · variable DB_Linea.Zonas.Z4 · visible con 1"),
        dict(t="text", x=212, y=240, w=124, h=18, txt="Botellas en línea", size=12, color="tenue", obj=OBJ_TEXT),
        io(338, 236, 40, 24, "DB_FIFO.N_Botellas", "9", "2", size=14),
    ]
    o += panel(196, 278, 404, 138, "FASES")
    nombres = ["Tanque", "Detec.", "Llenado", "Tapón", "Rechazo", "Clasif.", "General"]
    largos = {1: "Tanque", 2: "Deteccion", 3: "Llenado", 4: "Taponado", 5: "Rechazo", 6: "Clasif", 7: "General"}
    demo = {1: "V", 2: "V", 3: "V", 4: "V", 5: "-", 6: "-", 7: "V"}
    for i, nom in enumerate(nombres):
        f = i + 1
        x = 206 + i * 56
        o.append(dict(t="rect", x=x, y=304, w=52, h=104, fill="blanco", stroke="borde", r=4, obj=OBJ_RECT, nota=f"Fase {f}"))
        o.append(dict(t="text", x=x, y=310, w=52, h=14, txt=nom, size=10, bold=True, color="titulo", align="c", obj=OBJ_TEXT))
        for j, (col, sufijo) in enumerate([("fallo", "Rojo"), ("aviso", "Naranja"), ("marcha", "Verde")]):
            var = f"L{f}_{largos[f]}_{sufijo}"
            on = (demo[f] == "V" and sufijo == "Verde")
            o.append(lamp(x + 16, 330 + j * 24, 20, var, col, demo=on))
    o += panel(608, 278, 184, 138, "CAJAS")
    for j, (lab, cnt, cap, val) in enumerate([("Malas", "Cnt_Malas", 20, 7), ("0,5 L", "Cnt_05L", 6, 4), ("2 L", "Cnt_2L", 6, 2)]):
        y = 308 + j * 34
        o.append(dict(t="text", x=620, y=y + 2, w=48, h=16, txt=lab, size=12, color="tenue", obj=OBJ_TEXT))
        o.append(dict(t="bar", x=670, y=y + 2, w=78, h=16, var=f"DB_Linea.Cajas.{cnt}", demo=100 * val / cap, fill="acento",
                      obj=OBJ_BAR, anim=f"Receta F · mín 0 · máx {cap} · color de barra acento"))
        o.append(io(754, y, 30, 22, f"DB_Linea.Cajas.{cnt}", "99", str(val), size=13))
    return o


# --- MANUAL -----------------------------------------------------------------
def imagen_manual():
    o = panel(8, 56, 200, 360, "MODO MANUAL")
    o += [
        lamp(20, 92, 22, "DB_Linea.Modo.Manual_OK", "marcha", demo=1),
        dict(t="text", x=50, y=94, w=150, h=18, txt="Manual permitido", size=13, bold=True, color="texto", obj=OBJ_TEXT),
        dict(t="text", x=20, y=130, w=176, h=60, txt="Selector en MANUAL|y seta sin pulsar.", size=12, color="tenue",
             obj=OBJ_TEXT, nota="Texto en dos líneas"),
        dict(t="text", x=20, y=200, w=176, h=60, txt="Mantén pulsado el|botón para mover.", size=12, color="tenue",
             obj=OBJ_TEXT),
        dict(t="rect", x=20, y=300, w=176, h=100, fill="aviso", r=4, demo_hide=True, var="DB_Linea.Modo.Manual_OK",
             anim="Receta C · variable DB_Linea.Modo.Manual_OK · visible con 0", obj=OBJ_RECT,
             nota="Aviso naranja (en el boceto, transparente: con Manual_OK = 1 no se ve)"),
        dict(t="text", x=20, y=330, w=176, h=40, txt="PON EL SELECTOR|EN MANUAL", size=14, bold=True, color="blanco",
             align="c", demo_hide=True, var="DB_Linea.Modo.Manual_OK", anim="Receta C · variable DB_Linea.Modo.Manual_OK · visible con 0",
             obj=OBJ_TEXT),
    ]
    o += panel(216, 56, 576, 116, "CINTAS")
    bot = [("C1 + C2", "C12", "Cinta_C1_Entrada"), ("C3", "C3", "Cinta_C3_Taponado"), ("C4", "C4", "Cinta_C4_Rechazo"),
           ("C5 ← 0,5 L", "C5_05L", "Cinta_C5_Hacia_05L"), ("C5 → 2 L", "C5_2L", "Cinta_C5_Hacia_2L")]
    for i, (txt, v, sal) in enumerate(bot):
        x = 228 + i * 112
        o.append(dict(t="button", x=x, y=92, w=104, h=64, txt=txt, fill="boton", color="blanco", size=13, obj=OBJ_BTN,
                      var=f"DB_HMI.Manual.{v}", anim="Receta D (Pulsar › ActivarBit · Soltar › DesactivarBit) + Receta C (DB_Linea.Modo.Manual_OK visible con 1)"))
        o.append(lamp(x + 84, 98, 14, sal, "marcha", demo=(i == 1), nota="Piloto encima del botón (traer al frente)"))
    o += panel(216, 180, 576, 100, "MÁQUINAS")
    for i, (txt, v, sal) in enumerate([("BAJAR TAP-01", "TAP01_Bajar", "TAP01_Bajar"),
                                       ("EMPUJADOR", "Empujador", "Empujador_Avanzar")]):
        x = 228 + i * 176
        o.append(dict(t="button", x=x, y=212, w=164, h=56, txt=txt, fill="boton", color="blanco", size=13, obj=OBJ_BTN,
                      var=f"DB_HMI.Manual.{v}", anim="Receta D (Pulsar › ActivarBit · Soltar › DesactivarBit) + Receta C (DB_Linea.Modo.Manual_OK visible con 1)"))
        o.append(lamp(x + 144, 218, 14, sal, "marcha"))
    o += [
        lamp(596, 214, 16, "DB_Linea.Taponado.Arriba", "marcha", demo=1),
        dict(t="text", x=618, y=214, w=160, h=16, txt="TAP-01 arriba", size=12, color="tenue", obj=OBJ_TEXT),
        lamp(596, 242, 16, "S_Empujador_Atras", "marcha", demo=1),
        dict(t="text", x=618, y=242, w=160, h=16, txt="Empujador atrás", size=12, color="tenue", obj=OBJ_TEXT),
    ]
    o += panel(216, 288, 576, 128, "CAJAS")
    for i, (lab, suf) in enumerate([("Malas", "Malas"), ("0,5 L", "05L"), ("2 L", "2L")]):
        x = 228 + i * 188
        o.append(dict(t="text", x=x, y=312, w=176, h=16, txt=lab, size=12, bold=True, color="titulo", obj=OBJ_TEXT))
        for j, (txt, v) in enumerate([("RETIRAR", f"Retirar_{suf}"), ("PONER", f"Reponer_{suf}")]):
            o.append(dict(t="button", x=x + j * 90, y=334, w=84, h=52, txt=txt, fill="boton", color="blanco", size=12,
                          obj=OBJ_BTN, var=f"DB_HMI.Manual.{v}",
                          anim="Receta D (Pulsar › ActivarBit · Soltar › DesactivarBit) + Receta C (DB_Linea.Modo.Manual_OK visible con 1)"))
    return o


# --- ALARMAS ----------------------------------------------------------------
def imagen_alarmas():
    o = panel(8, 56, 388, 360, "ALARMAS · FASES 1 A 4")
    o += panel(404, 56, 388, 360, "ALARMAS · FASES 5 A 7")
    demo_on = {"A101": 0, "A301": 1}
    izq = [a for a in D.ALARMAS if a[1] in "1234"]
    der = [a for a in D.ALARMAS if a[1] in "567"]
    for col, lista_al in ((0, izq), (1, der)):
        for k, (aid, _f, color, texto, *_r) in enumerate(lista_al):
            x0 = 8 + col * 396
            y = 82 + k * 28
            o.append(lamp(x0 + 12, y + 4, 16, f"DB_Linea.Alarmas.{aid}", "fallo" if color == "R" else "aviso",
                          demo=demo_on.get(aid, 0)))
            o.append(dict(t="text", x=x0 + 36, y=y + 4, w=44, h=16, txt=aid, size=12, bold=True, color="texto", obj=OBJ_TEXT))
            o.append(dict(t="text", x=x0 + 84, y=y + 4, w=296, h=16, txt=texto, size=11, color="tenue", obj=OBJ_TEXT,
                          clip=True))
    return o


# --- PRODUCCIÓN -------------------------------------------------------------
def imagen_produccion():
    o = panel(8, 56, 388, 360, "PRODUCCIÓN")
    tiles = [("Buenas 0,5 L", "Total_Buenas_05L", "128"), ("Buenas 2 L", "Total_Buenas_2L", "96"),
             ("Malas", "Total_Malas", "9"), ("Cajas 0,5 L", "Total_Cajas_05L", "21"),
             ("Cajas 2 L", "Total_Cajas_2L", "16"), ("Cajas malas", "Total_Cajas_Malas", "0")]
    for i, (lab, var, demo) in enumerate(tiles):
        x = 20 + (i % 2) * 188
        y = 84 + (i // 2) * 90
        o.append(dict(t="rect", x=x, y=y, w=176, h=80, fill="blanco", stroke="borde", r=4, obj=OBJ_RECT))
        o.append(dict(t="text", x=x + 12, y=y + 8, w=152, h=16, txt=lab, size=12, color="tenue", obj=OBJ_TEXT))
        o.append(io(x + 12, y + 30, 152, 40, f"DB_Linea.Produccion.{var}", "9999999", demo, size=26))
    o.append(dict(t="button", x=20, y=360, w=364, h=46, txt="PONER A 0 LA PRODUCCIÓN", fill="fallo", color="blanco", size=14,
                  obj=OBJ_BTN, var="DB_HMI.Ordenes.Reset_Produccion", anim="Receta D (Pulsar › ActivarBit · Soltar › DesactivarBit)"))
    o += panel(404, 56, 388, 360, "PARÁMETROS")
    params = [("Botellas a la vez", "Max_Botellas", "9", "3", "botellas"),
              ("Llenado objetivo", "Pct_Llenado", "999.9", "90.0", "%"),
              ("Caudal máximo", "Caudal_Max_Lmin", "999.9", "10.0", "l/min"),
              ("Capacidad caja buenas", "Cap_Caja_Buenas", "99", "6", "botellas"),
              ("Capacidad caja malas", "Cap_Caja_Malas", "99", "20", "botellas")]
    for i, (lab, var, fmt, demo, unidad) in enumerate(params):
        y = 88 + i * 62
        o.append(dict(t="text", x=420, y=y + 10, w=200, h=18, txt=lab, size=13, color="texto", obj=OBJ_TEXT))
        o.append(io(624, y, 96, 40, f"DB_Linea.Param.{var}", fmt, demo, size=18, modo="Entrada/salida", color="texto"))
        o.append(dict(t="text", x=726, y=y + 12, w=60, h=16, txt=unidad, size=12, color="tenue", obj=OBJ_TEXT))
    return o


IMAGENES = [
    ("inicio", "Inicio", "Sinóptico de la línea: tanque, cintas, estaciones, botellas, lámparas por fase y cajas.", imagen_inicio),
    ("manual", "Manual", "Botones de mantener pulsado, con un piloto que muestra si la salida se ha activado.", imagen_manual),
    ("alarmas", "Alarmas", "Las 23 alarmas en dos columnas. El círculo se enciende rojo o naranja.", imagen_alarmas),
    ("produccion", "Produccion", "Contadores grandes y parámetros que el operario puede cambiar.", imagen_produccion),
]


# ---------------------------------------------------------------------------
# Dibujo SVG del boceto
# ---------------------------------------------------------------------------
def _txt_svg(o):
    size = o.get("size", 12)
    peso = "700" if o.get("bold") else "400"
    color = C[o.get("color", "texto")]
    lineas = o["txt"].split("|")
    if o.get("align") == "c":
        x, anchor = o["x"] + o["w"] / 2, "middle"
    else:
        x, anchor = o["x"], "start"
    out = ""
    for k, ln in enumerate(lineas):
        y = o["y"] + size + k * (size + 4) - 2
        out += (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{peso}" fill="{color}" '
                f'text-anchor="{anchor}">{e(ln)}</text>')
    return out


def svg_objeto(o):
    t, x, y, w, h = o["t"], o["x"], o["y"], o["w"], o["h"]
    if t == "rect":
        if o.get("demo_hide"):
            return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{C["aviso"]}" opacity=".3"/>'
        st = f' stroke="{C[o["stroke"]]}"' if o.get("stroke") else ""
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{o.get("r", 0)}" fill="{C[o["fill"]]}"{st}/>'
    if t == "text":
        if o.get("demo_hide"):
            return f'<g opacity=".45">{_txt_svg(o)}</g>'
        return _txt_svg(o)
    if t == "circle":
        r = w / 2
        return (f'<circle cx="{x + r}" cy="{y + r}" r="{r}" fill="{C[o["fill"]]}" stroke="#90A4AE" stroke-width="1"/>')
    if t == "button":
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{C[o["fill"]]}"/>'
                f'<rect x="{x}" y="{y + h - 4}" width="{w}" height="4" rx="2" fill="#000" opacity=".18"/>'
                + _txt_svg(dict(x=x, y=y + h / 2 - o.get("size", 13) / 2 - 2, w=w, txt=o["txt"], size=o.get("size", 13),
                                bold=True, color=o.get("color", "blanco"), align="c")))
    if t == "io":
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{C["blanco"]}" stroke="{C["borde"]}"/>'
                f'<text x="{x + w - 8}" y="{y + h / 2 + o["size"] * 0.36}" font-size="{o["size"]}" '
                f'font-weight="{"700" if o.get("bold") else "400"}" fill="{C[o["color"]]}" text-anchor="end" '
                f'font-family="IBM Plex Mono, Consolas, monospace">{e(str(o["demo"]))}</text>')
    if t == "bar":
        frac = max(0, min(100, o["demo"])) / 100
        hh = h * frac
        if h > w:
            return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{C["blanco"]}"/>'
                    f'<rect x="{x}" y="{y + h - hh}" width="{w}" height="{hh}" fill="{C[o["fill"]]}"/>')
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="{C["blanco"]}" stroke="{C["borde"]}"/>'
                f'<rect x="{x}" y="{y}" width="{w * frac}" height="{h}" rx="2" fill="{C[o["fill"]]}"/>')
    if t == "tank":
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="none" stroke="{C["tenue"]}" stroke-width="2"/>'
    if t == "line":
        return f'<line x1="{x}" y1="{y}" x2="{x + w}" y2="{y + h}" stroke="{C[o.get("color", "tenue")]}" stroke-width="1"/>'
    if t == "pump":
        col = C["marcha"] if o.get("on") else C["apagado"]
        r = w / 2
        return (f'<circle cx="{x + r}" cy="{y + r}" r="{r}" fill="{col}" stroke="{C["cabecera"]}" stroke-width="2"/>'
                f'<path d="M{x + r - 9} {y + r + 9} L{x + r} {y + 6} L{x + r + 9} {y + r + 9} Z" fill="{C["blanco"]}"/>')
    if t == "valve":
        col = C["marcha"] if o.get("on") else C["apagado"]
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{col}" stroke="{C["cabecera"]}"/>'
                f'<line x1="{x}" y1="{y}" x2="{x + w}" y2="{y + h}" stroke="{C["cabecera"]}" stroke-width="2"/>'
                f'<line x1="{x + w}" y1="{y}" x2="{x}" y2="{y + h}" stroke="{C["cabecera"]}" stroke-width="2"/>')
    if t == "belt" and o.get("vertical"):
        # C5: mitad de arriba (hacia 0,5 L) en marcha en el boceto, mitad de abajo parada
        return (svg_objeto(dict(o, h=84, vertical=False, rot=True))
                + svg_objeto(dict(o, y=y + 84, h=h - 84, on=False, vertical=False, rot=True)))
    if t == "belt":
        col = C["marcha"] if o.get("on") else C["apagado"]
        out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{col}"/>'
        if o.get("rot"):
            for yy in range(int(y) + 8, int(y + h), 12):
                out += f'<line x1="{x + 3}" y1="{yy}" x2="{x + w - 3}" y2="{yy}" stroke="#fff" opacity=".35"/>'
        else:
            for xx in range(int(x) + 8, int(x + w), 12):
                out += f'<line x1="{xx}" y1="{y + 3}" x2="{xx}" y2="{y + h - 3}" stroke="#fff" opacity=".35"/>'
        return out
    if t == "bottle":
        if not o.get("on"):
            return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="none" stroke="{C["tenue"]}" '
                    f'stroke-dasharray="3 3" opacity=".6"/>')
        return (f'<rect x="{x + w / 2 - 3}" y="{y}" width="6" height="5" fill="{C["acento"]}"/>'
                f'<rect x="{x}" y="{y + 5}" width="{w}" height="{h - 5}" rx="4" fill="{C["acento"]}"/>')
    if t == "sym":
        n, txt, col = ESTADOS[o["demo"]]
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{C[col]}"/>'
                + _txt_svg(dict(x=x, y=y + 6, w=w, txt=txt, size=13, bold=True, color="blanco", align="c")))
    if t == "time":
        return _txt_svg(dict(x=x, y=y + 3, w=w, txt="12:34:56", size=15, color="blanco", align="c"))
    return ""


def svg_imagen(objs, ident, fondo=()):
    """fondo: objetos que se dibujan sin número (la plantilla, en las imágenes)."""
    cuerpo = "".join(svg_objeto(o) for o in list(fondo) + list(objs))
    nums = ""
    for i, o in enumerate(objs, 1):
        cx, cy = o["x"] + 2, o["y"] + 2
        nums += (f'<g class="num"><circle cx="{cx + 7}" cy="{cy + 7}" r="8" fill="#6A1B9A"/>'
                 f'<text x="{cx + 7}" y="{cy + 10.5}" font-size="9" font-weight="700" fill="#fff" text-anchor="middle">{i}</text></g>')
    return (f'<svg viewBox="0 0 800 480" role="img" aria-label="Boceto de la imagen {ident}" '
            f'font-family="Tahoma, Segoe UI, Arial, sans-serif">'
            f'<rect width="800" height="480" fill="{C["fondo"]}"/>{cuerpo}<g class="nums">{nums}</g></svg>')


# ---------------------------------------------------------------------------
# Página
# ---------------------------------------------------------------------------
def colores(o):
    """Lista (qué, color) para la columna Colores. Color None = sin color (transparente)."""
    t = o["t"]
    if o.get("b"):                       # receta B: el color fijo es el de apagado
        base = {"pump": [("Círculo, fondo:", "apagado"), ("Círculo, borde 2 px:", "cabecera"), ("Texto ▲:", "blanco")],
                "valve": [("Rectángulo, fondo:", "apagado"), ("Borde y las 2 líneas:", "cabecera")]}.get(
                    t, [("Fondo:", "apagado")] + ([("Borde:", "apagado")] if t in ("circle", "rect", "belt") else []))
        return base + [("Animación, con 1:", o["b"])]
    if t == "sym":
        return [("Fondo:", "boton"), ("Texto:", "blanco"), ("Animación: tabla de estados", None)]
    if t == "rect":
        if o.get("demo_hide"):
            return [("Fondo:", o["fill"]), ("Borde: sin línea", None)]
        return [("Fondo:", o["fill"])] + ([("Borde 1 px:", o["stroke"])] if o.get("stroke") else [("Borde: sin línea", None)])
    if t == "text":
        return [("Texto:", o.get("color", "texto")), ("Fondo: transparente", None)]
    if t == "button":
        return [("Fondo:", o["fill"]), ("Texto:", o.get("color", "blanco"))]
    if t == "io":
        return [("Fondo:", "blanco"), ("Borde 1 px:", "borde"), ("Texto:", o["color"])]
    if t == "bar":
        return [("Barra:", o["fill"]), ("Fondo:", "blanco")] + ([("Borde: sin línea", None)] if o["h"] > o["w"] else [("Borde 1 px:", "borde")])
    if t == "tank":
        return [("Fondo: transparente", None), ("Borde 2 px:", "tenue")]
    if t == "line":
        return [("Línea 1 px:", o.get("color", "tenue"))]
    if t == "bottle":
        return [("Fondo:", "acento"), ("Borde:", "acento")]
    if t == "time":
        return [("Texto:", "blanco"), ("Fondo: transparente", None)]
    return []


def tabla_objetos(objs):
    filas = []
    for i, o in enumerate(objs, 1):
        nombre, donde = o["obj"]
        col = "<br>".join(f'<span class="sw" style="background:{C[k]}"></span>{e(que)} {e(rgb(k))}'
                          if k else e(que) for que, k in colores(o))
        detalle = []
        if o.get("txt"):
            detalle.append(f"Texto «{e(o['txt'].replace('|', ' '))}»" + (f" · {o['size']} px" if o.get("size") else "")
                           + (" negrita" if o.get("bold") else ""))
        if o.get("var"):
            detalle.append(f"<span class='mono'>{e(o['var'])}</span>")
        if o.get("anim"):
            detalle.append(e(o["anim"]))
        if o.get("nota"):
            detalle.append(f"<i>{e(o['nota'])}</i>")
        filas.append(
            f"<tr><td class='n'>{i}</td><td><b>{e(nombre)}</b><br><span class='src'>{e(donde)}</span></td>"
            f"<td class='mono'>{o['x']}, {o['y']}</td><td class='mono'>{o['w']} × {o['h']}</td>"
            f"<td>{col}</td><td>{'<br>'.join(detalle)}</td></tr>")
    return ("<div class='tw'><table class='vt'><thead><tr><th>Nº</th><th>Objeto</th><th>X, Y</th><th>Ancho × alto</th>"
            "<th>Colores</th><th>Texto · variable · cómo (receta)</th></tr></thead><tbody>" + "".join(filas) + "</tbody></table></div>")


def construir():
    pal = "".join(f"<tr><td><span class='sw big' style='background:{v[0]}'></span></td><td><b>{k}</b></td>"
                  f"<td class='mono'>{v[1]}</td><td class='mono'>{v[0]}</td><td>{e(v[2])}</td></tr>"
                  for k, v in PAL.items())
    est = "".join(f"<tr><td class='mono'>{n}</td><td><b>{e(t)}</b></td><td><span class='sw' style='background:{C[c]}'></span>"
                  f"{c} · <span class='mono'>{PAL[c][1]}</span></td></tr>" for n, t, c in ESTADOS)
    pl = plantilla()
    secciones = (
        f"<section id='plantilla'><h2>Plantilla común</h2><p class='lead'>Cabecera y barra de navegación. Se hacen "
        f"una sola vez en una plantilla y se asignan a las 4 imágenes.</p>"
        f"<div class='scr'>{svg_imagen(pl, 'plantilla')}</div>{tabla_objetos(pl)}</section>")
    for ident, nombre, desc, fn in IMAGENES:
        objs = fn()
        secciones += (f"<section id='{ident}'><h2>Imagen {e(nombre)}</h2><p class='lead'>{e(desc)} La cabecera y la barra "
                      f"de abajo vienen de la plantilla.</p>"
                      f"<div class='scr'>{svg_imagen(objs, ident, fondo=pl)}</div>"
                      f"<p class='note'>Los números del boceto son los de la tabla. La cabecera y la barra de abajo no llevan "
                      f"número porque son de la plantilla (tabla «Plantilla común»).</p>"
                      f"{tabla_objetos(objs)}</section>")

    pasos = """
<ol class='acc'>
<li><b>Colores de la imagen</b>: selecciona la imagen (clic en un hueco vacío) › Propiedades › <b>General</b> › Color de fondo:
 <span class='mono'>230, 232, 235</span>. Para escribir el color en RGB: desplegable de color › <b>Más colores</b>.</li>
<li><b>Plantilla</b>: en el árbol, HMI_1 › Administración de imágenes › <b>Plantillas</b> › Agregar nueva plantilla. Llámala
 <span class='mono'>Base</span> y dibuja en ella la cabecera y la barra de navegación (tabla «Plantilla común»).</li>
<li>En cada imagen: Propiedades › General › <b>Plantilla</b>: <span class='mono'>Base</span>. Ya no hace falta copiar los botones.</li>
<li><b>Lista de textos «Estados»</b>: HMI_1 › <b>Listas de textos y gráficos</b> › pestaña Listas de textos › Agregar.
 Nombre <span class='mono'>Estados</span>, selección <b>Valor/Rango</b>, y una entrada por estado (tabla de abajo).</li>
<li><b>Posición y tamaño exactos</b>: selecciona el objeto › Propiedades › <b>Diseño</b> (o «Posición y tamaño»): escribe X, Y,
 ancho y alto de la tabla. Mucho más rápido y preciso que arrastrar.</li>
<li><b>Fuente</b>: Tahoma en todo. Propiedades › <b>Formato de texto</b> › Fuente, con el tamaño de la tabla.</li>
<li><b>Lámparas y equipos que cambian de color</b>: Propiedades › Animaciones › <b>Visualización › Apariencia</b>. Variable de la
 tabla, tipo <b>Rango</b>: valor 0 color «apagado», valor 1 su color (marcha, aviso o fallo).</li>
<li><b>Botellas por zona</b>: animación <b>Visibilidad</b> con la variable de la zona, visible con 1.</li>
<li><b>Bomba y válvula</b>: en el KTP700 Basic los objetos básicos son Línea, Elipse, Círculo, Rectángulo, Campo de texto y
 Visor de gráficos (no hay polígonos). La bomba es un círculo con el símbolo ▲ en un campo de texto encima, y la válvula un
 rectángulo con dos líneas en X. Las medidas exactas están en la tabla de la imagen Inicio (objetos 3 y 5).</li>
<li><b>Un objeto, varios iguales</b>: haz el primero completo (posición, colores, animación), cópialo y pégalo; en la copia
 solo cambias X, Y y la variable.</li>
</ol>"""

    css = ""
    for nombre in ("estilo.css", "estilo_guia.css"):
        with open(os.path.join(os.path.dirname(__file__), nombre), encoding="utf-8") as fh:
            css += fh.read()
    css += """
.scr{background:#0f1519;border-radius:10px;padding:14px;margin:12px 0;max-width:860px}
.scr svg{display:block;width:100%;height:auto;border-radius:4px}
.ocultar-num .num{display:none}
.sw{display:inline-block;width:12px;height:12px;border-radius:3px;border:1px solid rgba(0,0,0,.25);vertical-align:-2px;margin-right:4px}
.sw.big{width:26px;height:18px}
td.n{font:700 12px var(--f-mono);color:#6A1B9A}
.src{font-size:11.5px;color:var(--muted)}
.tog{display:inline-flex;gap:8px;align-items:center;font-size:14px;margin:6px 0 0}
"""
    nav = "".join(f"<a href='#{i}'>{t}</a>" for i, t in [("principios", "Principios"), ("paleta", "Colores"), ("pasos", "Cómo"), ("recetas", "Recetas"),
                                                        ("plantilla", "Plantilla"), ("inicio", "Inicio"), ("manual", "Manual"),
                                                        ("alarmas", "Alarmas"), ("produccion", "Producción")])
    return f"""<title>Diseño HMI Llenado</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>
{css}
</style>
<div class="wrap">
  <header class="top">
    <div class="eyebrow">TFC · Línea de llenado · Pantalla KTP700 Basic</div>
    <h1>Diseño de la HMI <span>/ 800 × 480 px, objeto a objeto</span></h1>
    <div class="meta"><span>WinCC Basic <b>V15</b></span><span>Fuente <b>Tahoma</b></span><span><b>4</b> imágenes + plantilla</span></div>
    <label class="tog"><input type="checkbox" id="vernum" checked> Mostrar los números de objeto en los bocetos</label>
  </header>
  <nav class="bar" aria-label="Secciones"><div class="links">{nav}</div></nav>

  <section id="principios"><h2>La idea</h2>
  <p class="lead">El estilo que se usa hoy en la industria para pantallas de operador (HMI «de alto rendimiento»):</p>
  <ul class="acc">
   <li><b>Fondo gris neutro</b> y paneles claros con borde fino. Nada de fondos de colores ni fotos.</li>
   <li><b>El color solo significa algo</b>: verde = en marcha, naranja = aviso, rojo = fallo, azul = valores y agua. Lo parado es gris.
    Así el operario ve de un vistazo dónde hay un problema.</li>
   <li><b>Todo alineado a una rejilla</b> de 8 px, con los mismos márgenes en todas las imágenes.</li>
   <li><b>Una sola fuente</b> (Tahoma) en 3 tamaños: 11–12 px etiquetas, 13–16 px textos, 18–26 px números importantes.</li>
  </ul>
  <p>No hace falta buscar imágenes en Google: con los objetos de WinCC y estos colores queda limpio y profesional. Además, las
  imágenes de Internet suelen tener derechos de autor y en la pantalla se ven pixeladas.</p></section>

  <section id="paleta"><h2>Colores</h2><p class="lead">Escríbelos en WinCC en RGB (desplegable de color › Más colores).</p>
  <div class="tw"><table class="vt"><thead><tr><th></th><th>Nombre</th><th>RGB</th><th>Hex</th><th>Uso</th></tr></thead>
  <tbody>{pal}</tbody></table></div>
  <h3>Lista de textos «Estados» (rótulo de la cabecera)</h3>
  <p class="note">La variable <span class="mono">DB_Linea.Modo.Estado</span> la calcula FC10 (segmentos 38 a 43 de la guía).
  En el Campo E/S simbólico: lista <span class="mono">Estados</span> y animación Apariencia por valor con estos colores de fondo y
  texto blanco.</p>
  <div class="tw"><table class="vt"><thead><tr><th>Valor</th><th>Texto</th><th>Fondo</th></tr></thead><tbody>{est}</tbody></table></div>
  <h3>Cómo hacer el rótulo de estado paso a paso</h3>
  <ol class="acc">
   <li><b>Lista de textos</b>: HMI_1 › <b>Listas de textos y gráficos</b> › pestaña Listas de textos › doble clic en Agregar.
    Nombre <span class="mono">Estados</span>, Selección <b>Valor/Rango</b>. Abajo, una entrada por fila: valor 0 texto LISTA,
    valor 1 EN MARCHA… hasta 5 MODO MANUAL.</li>
   <li>Arrastra un <b>Campo E/S simbólico</b> a la plantilla y escribe su posición y tamaño (500, 10 · 196 × 28).</li>
   <li>Propiedades › <b>General</b>: Variable <span class="mono">DB_Linea.Modo.Estado</span>, <b>Modo: Salida</b> y Lista de
    textos <span class="mono">Estados</span>. Al poner el modo en <b>Salida</b> desaparece la flecha del desplegable: el operario
    no puede cambiar el estado, solo verlo.</li>
   <li>Propiedades › <b>Apariencia</b>: fondo 55, 71, 79 (gris), texto blanco, borde sin línea. Formato de texto: Tahoma 13
    negrita, centrado.</li>
   <li>Animaciones › Visualización › <b>Apariencia</b>: variable <span class="mono">DB_Linea.Modo.Estado</span>, tipo
    <b>Rango</b>. Añade una fila por valor (0 a 5) con el color de fondo de la tabla y el color de primer plano (las letras)
    blanco. Parpadeo: <b>No</b> en todas menos en la 4 (PARADA DE SEGURIDAD), que va con parpadeo <b>Sí</b>.</li>
  </ol>
  <p class="note">En el editor de TIA el campo se ve blanco o gris y con el primer texto de la lista: es normal. El texto y el
  color cambian cuando la pantalla está funcionando (simulación o panel real). El boceto lo dibuja como se vería con la
  línea en marcha (Estado = 1).</p>
  </section>

  <section id="pasos"><h2>Cómo pasarlo a WinCC</h2>{pasos}</section>

  <section id="recetas"><h2>Recetas: cómo se hace cada cosa</h2>
  <p class="lead">Todo lo que pide el diseño se hace con estas 6 recetas. En las tablas, la columna de la derecha dice qué receta
  usar en cada objeto. Primero selecciona el objeto con un clic; todo se hace abajo, en la ventana de inspección.</p>

  <h3>A · Posición, tamaño y color fijo</h3>
  <ol class="acc">
   <li>Selecciona el objeto. Abajo: <b>Propiedades</b> › pestaña <b>Propiedades</b>.</li>
   <li><b>Diseño</b> (o «Posición y tamaño»): escribe X, Y, Ancho y Alto de la tabla.</li>
   <li><b>Apariencia</b>: <b>Fondo › Color</b> es el relleno. <b>Borde › Color</b> y <b>Ancho</b> son el contorno.
    En un campo de texto, el color de las letras es el <b>Color de texto</b> o primer plano.</li>
   <li>Para escribir un color exacto: despliega el color › <b>Más colores…</b> › escribe Rojo, Verde y Azul (los números RGB
    de la tabla de colores) › Aceptar.</li>
   <li>Si no quieres relleno (por ejemplo, el texto encima de la bomba): Fondo › Estilo <b>Transparente</b>.</li>
   <li><b>Formato de texto</b>: fuente Tahoma, tamaño y negrita. <b>Alineación</b> horizontal y vertical: centrado si la tabla lo dice.</li>
  </ol>

  <h3>B · Color que cambia con una variable (lámparas, bomba, cintas…)</h3>
  <ol class="acc">
   <li>Ponle primero el color de «apagado» con la receta A (gris 207, 216, 220). Es el que verás en el editor.</li>
   <li>Abajo: <b>Propiedades</b> › pestaña <b>Animaciones</b>.</li>
   <li>En el árbol de la izquierda, <b>Visualización</b> › doble clic en <b>Agregar nueva animación</b> › elige <b>Apariencia</b>.</li>
   <li><b>Variable</b>: pulsa <b>…</b> y busca la variable de la tabla. Las del DB están en PLC_Linea › Bloques de programa ›
    DB_Linea; las salidas, como <span class="mono">Cinta_C1_Entrada</span>, en Variables PLC.</li>
   <li><b>Tipo</b>: <b>Rango</b>.</li>
   <li>En la tabla de debajo añade dos filas:
    <br>Fila 1 · Rango <b>0</b> · Color de fondo gris claro (207, 216, 220) · Color de primer plano el mismo · Parpadeo No.
    <br>Fila 2 · Rango <b>1</b> · Color de fondo el que diga la columna <b>Colores</b> de la tabla del objeto, en la línea
    «Animación, con 1» (verde 46, 160, 67; naranja 245, 158, 11; rojo 211, 47, 47; azul agua 64, 156, 214) ·
    Color de primer plano el mismo · Parpadeo No.</li>
   <li><b>Color de primer plano</b>: en un círculo o un rectángulo es el color del <b>borde</b>. Por eso se pone igual que el
    fondo y el objeto se ve de un solo color. Solo en la bomba y la válvula va gris muy oscuro (38, 50, 56), para que se les
    vea el contorno; la tabla lo dice en esos dos.</li>
   <li>Copia y pega el objeto: la animación se copia también. En la copia solo cambias la variable y, si hace falta, el color.</li>
  </ol>

  <h3>C · Que algo aparezca o desaparezca (botellas, botones de manual, aviso)</h3>
  <ol class="acc">
   <li>Propiedades › <b>Animaciones</b> › <b>Visualización</b> › Agregar nueva animación › <b>Visibilidad</b>.</li>
   <li><b>Variable</b>: la de la tabla.</li>
   <li><b>Rango</b>: de 1 a 1 si la tabla dice «visible con 1», o de 0 a 0 si dice «visible con 0». Marca <b>Visible</b>.</li>
   <li>Se pueden seleccionar varios objetos a la vez (Ctrl + clic) y ponerles la misma visibilidad de una vez.</li>
  </ol>

  <h3>D · Lo que hace un botón (eventos)</h3>
  <ol class="acc">
   <li>Selecciona el botón › Propiedades › pestaña <b>Eventos</b>.</li>
   <li>Navegación: evento <b>Hacer clic</b> › &lt;Agregar función&gt; › <b>ActivarImagen</b> › nombre de la imagen.</li>
   <li>Botones de mantener pulsado: evento <b>Pulsar</b> › <b>ActivarBit</b> con la variable; evento <b>Soltar</b> ›
    <b>DesactivarBit</b> con la misma variable. Están en Procesamiento de bits.</li>
   <li>El texto del botón se escribe en Propiedades › <b>General</b> › Texto.</li>
  </ol>

  <h3>E · Campos que muestran o piden un número (Campo E/S)</h3>
  <ol class="acc">
   <li>Propiedades › <b>General</b>: <b>Variable</b> la de la tabla.</li>
   <li><b>Modo</b>: <b>Salida</b> si solo se muestra; <b>Entrada/salida</b> si el operario lo puede cambiar (parámetros).</li>
   <li><b>Formato de representación</b>: Decimal. <b>Patrón de formato</b>: el de la tabla, con un 9 por cada cifra y el punto
    para los decimales (por ejemplo <span class="mono">999.9</span>). La unidad (%, L…) va en un campo de texto al lado o en
    «Unidad» si tu versión la tiene.</li>
   <li>Apariencia: fondo blanco, borde 1 px gris (196, 200, 206), texto azul (25, 118, 210) o negro en los parámetros.
    Alineación a la derecha.</li>
   <li>El <b>Campo E/S simbólico</b> es igual, pero en vez de un número muestra un texto de una lista (ver el rótulo de estado).</li>
  </ol>

  <h3>G · Poner un objeto encima de otro (texto sobre un círculo, pilotos sobre botones)</h3>
  <ol class="acc">
   <li>Son <b>dos objetos separados</b>: el círculo no tiene texto. Arrastra el segundo objeto (por ejemplo un <b>Campo de texto</b>
    de Objetos básicos) y colócalo encima con la receta A (posición y tamaño de la tabla).</li>
   <li>En el campo de texto: Propiedades › <b>General</b> › Texto. Fondo <b>transparente</b> para que se vea el círculo de debajo.</li>
   <li>Si queda escondido detrás: clic derecho sobre él › <b>Orden</b> › <b>Traer al primer plano</b>.</li>
   <li>Para moverlos juntos: selecciona los dos (Ctrl + clic) › clic derecho › <b>Agrupar</b>. La animación de color sigue en el círculo.</li>
  </ol>

  <h3>F · Barras (nivel del tanque y llenado de cajas)</h3>
  <ol class="acc">
   <li>Herramientas › Elementos › <b>Barra</b>. Posición y tamaño con la receta A.</li>
   <li>Propiedades › <b>General</b>: <b>Variable de proceso</b> la de la tabla. <b>Máximo</b> y <b>Mínimo</b> los de la tabla.</li>
   <li><b>Apariencia</b>: Color de la barra (agua 64, 156, 214 o acento 25, 118, 210), fondo blanco.</li>
   <li>En <b>Escalas</b> (o «Representación») desactiva la escala y las marcas si las muestra: queda más limpio.</li>
   <li>Si la barra es horizontal (cajas), cambia la <b>Dirección</b> a «de izquierda a derecha».</li>
  </ol>
  </section>

  {secciones}
  <footer>Generado desde herramientas/diseno_hmi.py</footer>
</div>
<script>
(function(){{
  var cb=document.getElementById('vernum');
  function upd(){{document.body.classList.toggle('ocultar-num',!cb.checked);}}
  cb.addEventListener('change',upd);upd();
}})();
</script>
"""


if __name__ == "__main__":
    pagina = construir()
    ruta = os.path.join(RAIZ, "docs", "03_Diseno_HMI.html")
    with open(ruta, "w", encoding="utf-8") as fh:
        fh.write('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
                 '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
                 '</head>\n<body>\n' + pagina + '\n</body>\n</html>\n')
    print("HTML ->", ruta)
    if len(sys.argv) > 1:
        with open(sys.argv[1], "w", encoding="utf-8") as fh:
            fh.write(pagina)
        print("Web  ->", sys.argv[1])
