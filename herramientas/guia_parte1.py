# -*- coding: utf-8 -*-
"""
Guía paso a paso · Parte 1: proyecto, hardware, variables, datos y primeros bloques KOP.
Genera docs/02_Guia_Parte1.html   (y, si se pasa una ruta, la versión para publicar).
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import datos_variables as D  # noqa: E402
from kop import bobina, caja, comparar, contacto, segmento  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
e = html.escape

# ---------------------------------------------------------------------------
# Piezas de maquetación
# ---------------------------------------------------------------------------
_pasos = []


def paso(id_, titulo, cuerpo, parte):
    _pasos.append((id_, titulo, parte))
    n = len(_pasos)
    return (f'<section class="paso" id="{id_}"><div class="pnum">{n}</div>'
            f'<div class="pbody"><h3>{titulo}</h3>{cuerpo}</div></section>')


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


# Nombres largos que se repiten
NIV = '"DB_Linea".Tanque.'
LLE = '"DB_Linea".Llenado.'
PAR = '"DB_Linea".Param.'
FIFO = '"DB_FIFO".'

# ---------------------------------------------------------------------------
# PARTE A · Proyecto y hardware
# ---------------------------------------------------------------------------
A = []
A.append(paso("p-proyecto", "Crear el proyecto", lista(
    f"Abre TIA Portal V15. En la vista del portal pulsa {ruta('Crear proyecto')}.",
    "Nombre del proyecto: <span class='mono'>Linea_Llenado_TFC</span>. Elige la carpeta y escribe tu nombre en Autor.",
    "Pulsa <b>Crear</b>.",
    "Abajo a la izquierda pulsa <b>Vista del proyecto</b>. Toda la guía se hace desde esta vista.",
), "A"))

A.append(paso("p-cpu", "Añadir la CPU", lista(
    f"En el árbol del proyecto (izquierda), doble clic en {ruta('Agregar dispositivo')}.",
    f"Elige {ruta('Controladores', 'SIMATIC S7-1200', 'CPU', 'CPU 1214C DC/DC/DC', '6ES7 214-1AG40-0XB0')}.",
    "Abajo, en <b>Versión</b>, elige <span class='mono'>V4.2</span> y pulsa <b>Aceptar</b>.",
    f"Con la CPU seleccionada, ve a {ruta('Propiedades', 'General', 'Información del proyecto')} "
    "y en <b>Nombre</b> escribe <span class='mono'>PLC_Linea</span>.",
) + tip("La ventana de <b>Propiedades</b> es la de abajo (ventana de inspección). "
        "Si no la ves, haz doble clic sobre la CPU."), "A"))

filas_hw = [
    ("1", "CPU 1214C DC/DC/DC", "—", "Integrada: I0.0–I1.5 · Q0.0–Q1.1 · IW64/IW66"),
    ("2", "DI 16x24VDC · 6ES7 221-1BH32-0XB0", "<b>2</b>", "I2.0–I3.7"),
    ("3", "DQ 16x24VDC · 6ES7 222-1BH32-0XB0", "<b>2</b>", "Q2.0–Q3.7"),
    ("4", "DQ 16x24VDC · 6ES7 222-1BH32-0XB0", "<b>4</b>", "Q4.0–Q5.7"),
    ("5", "AQ 2x14BIT · 6ES7 232-4HB32-0XB0", "<b>64</b>", "QW64, QW66"),
]
A.append(paso("p-modulos", "Añadir los módulos y cambiar sus direcciones", lista(
    "Abre la <b>Vista de dispositivos</b> de la CPU (doble clic sobre <span class='mono'>PLC_Linea</span> › Configuración de dispositivos).",
    "A la derecha abre el <b>Catálogo de hardware</b>. Arrastra cada módulo al slot que indica la tabla.",
    f"Haz clic en cada módulo y ve a {ruta('Propiedades', 'General', 'Direcciones E/S')}. "
    "En <b>Dirección inicial</b> escribe el valor de la tabla.",
) + tabla(["Slot", "Módulo del catálogo", "Dirección inicial", "Resultado"],
          [(f"<span class='mono'>{a}</span>", b, f"<span class='mono'>{c}</span>", f"<span class='mono'>{d}</span>")
           for a, b, c, d in filas_hw])
    + tip("Para revisarlo todo de un vistazo, abre la <b>Vista general de dispositivos</b> "
          "(la flecha pequeña a la derecha del dibujo de la CPU). Las columnas <b>Dirección I</b> y "
          "<b>Dirección Q</b> deben coincidir con la tabla.")
    + ojo("Si TIA dice que una dirección está ocupada, revisa que no hayas puesto dos módulos con la misma dirección inicial."), "A"))

A.append(paso("p-marcas", "Activar las marcas de sistema y de ciclo", lista(
    f"Selecciona la CPU y ve a {ruta('Propiedades', 'General', 'Marcas de sistema y de ciclo')}.",
    "Marca <b>Activar la utilización del byte de marcas de sistema</b> y pon la dirección <span class='mono'>1</span> (MB1).",
    "Marca <b>Activar la utilización del byte de marcas de ciclo</b> y pon la dirección <span class='mono'>0</span> (MB0).",
) + "<p>TIA crea solo estas variables. Las usaremos para los parpadeos y para el arranque:</p>"
    + tabla(["Variable", "Dirección", "Uso en el programa"],
            [(f"<span class='nm'>{n}</span>", f"<span class='mono'>{a}</span>", x) for a, n, _t, _c, x in D.MARCAS]), "A"))

A.append(paso("p-sim", "Permitir la simulación", lista(
    "En el árbol, clic derecho sobre el nombre del proyecto (la primera línea, <span class='mono'>Linea_Llenado_TFC</span>) › <b>Propiedades</b>.",
    "Pestaña <b>Protección</b>.",
    "Marca la casilla <b>Soportar simulación durante la compilación de bloques</b> y pulsa <b>Aceptar</b>.",
) + ojo("Sin esta casilla, PLCSIM no deja cargar el programa. Es el fallo más típico al empezar."), "A"))

A.append(paso("p-variables", "Importar la tabla de variables", lista(
    "Descarga <span class='mono'>tia/Variables_PLC.xlsx</span> de tu repositorio de GitHub "
    "(rama <span class='mono'>claude/bottle-filling-line-kop-javw6f</span>).",
    f"En el árbol abre {ruta('PLC_Linea', 'Variables PLC')} y haz doble clic en <b>Mostrar todas las variables</b>.",
    "En la barra de herramientas del editor pulsa el botón <b>Importar</b> (icono de tabla con una flecha que entra).",
    "Elige el Excel, deja marcada la opción <b>Variables</b> y acepta.",
    "Debe aparecer una tabla nueva, <span class='mono'>Linea_Llenado</span>, con 73 variables.",
) + tip("Si TIA da error al importar: pulsa <b>Exportar</b> con la tabla vacía para que genere su propio Excel, "
        "copia nuestras filas en ese fichero respetando sus columnas y vuelve a importar.")
    + "<p>Comprueba después:</p>" + lista(
        "Ninguna fila en rojo.",
        "<span class='mono'>SETA_Emergencia</span> está en <span class='mono'>%I0.2</span> y "
        "<span class='mono'>L7_General_Rojo</span> en <span class='mono'>%Q5.7</span>.",
        "Las marcas de sistema (<span class='mono'>FirstScan</span>, <span class='mono'>Clock_1Hz</span>…) "
        "están en la tabla estándar y no repetidas.", ordenada=False), "A"))

# ---------------------------------------------------------------------------
# PARTE B · Datos
# ---------------------------------------------------------------------------
B = []
udt_filas = [(f"<span class='nm'>{n}</span>", f"<span class='ty'>{t}</span>", f"<span class='mono'>{v}</span>", x)
             for n, t, v, x in D.UDT_BOTELLA]
B.append(paso("p-udt", "Crear el tipo de datos UDT_Botella", lista(
    f"En el árbol: {ruta('PLC_Linea', 'Tipos de datos PLC')} › doble clic en <b>Agregar nuevo tipo de datos</b>.",
    "Clic derecho sobre el tipo nuevo › <b>Cambiar nombre</b> (o F2): <span class='mono'>UDT_Botella</span>.",
    "Rellena una fila por campo: <b>Nombre</b>, <b>Tipo de datos</b>, <b>Valor predeterminado</b> y <b>Comentario</b>.",
) + tabla(["Nombre", "Tipo", "Valor", "Comentario"], udt_filas)
    + tip("Un UDT es un molde. Lo creamos una vez y luego el FIFO tiene 4 botellas con ese mismo molde."), "B"))

fifo_filas = [(f"<span class='nm'>{n}</span>", f"<span class='ty'>{e(t)}</span>", f"<span class='mono'>{v}</span>", x)
              for n, t, v, x in D.DB_FIFO]
B.append(paso("p-fifo", "Crear DB_FIFO a mano", lista(
    f"{ruta('PLC_Linea', 'Bloques de programa')} › doble clic en <b>Agregar nuevo bloque</b>.",
    "Elige <b>Bloque de datos (DB)</b>. Nombre: <span class='mono'>DB_FIFO</span>. Tipo: <b>DB global</b>.",
    "Marca <b>Manual</b> en Número y pon <span class='mono'>2</span>. Pulsa <b>Aceptar</b>.",
    "Primera fila: nombre <span class='mono'>Botella</span>, y en tipo escribe exactamente "
    "<span class='mono'>Array[0..3] of \"UDT_Botella\"</span>. Pulsa Intro.",
    "Despliega la flecha de <span class='mono'>Botella</span>: verás <span class='mono'>Botella[0]</span> a "
    "<span class='mono'>Botella[3]</span>, cada una con los 8 campos del UDT.",
    "Añade el resto de filas de la tabla.",
) + tabla(["Nombre", "Tipo", "Inicial", "Qué es"], fifo_filas), "B"))

B.append(paso("p-dblinea", "Crear DB_Linea y DB_Tiempos", (
    "<p>DB_Linea tiene más de 50 variables, así que te propongo dos caminos. "
    "Haz el <b>A</b> con el primer Struct para aprender y el <b>B</b> para el resto.</p>"
    "<h4>Camino A · A mano (para aprender cómo se hace un Struct)</h4>"
    + lista(
        "Agregar nuevo bloque › Bloque de datos. Nombre <span class='mono'>DB_Linea</span>, número manual <span class='mono'>1</span>.",
        "Primera fila: nombre <span class='mono'>Modo</span>, tipo <span class='mono'>Struct</span>. Intro.",
        "TIA abre una fila metida hacia dentro: ahí van los campos del Struct "
        "(<span class='mono'>Auto</span>, <span class='mono'>Ciclo_Marcha</span>…).",
        "Para cerrar el Struct y crear el siguiente, escribe en la primera fila vacía de abajo, al nivel de <span class='mono'>Modo</span>.",
        "En los Struct <span class='mono'>Produccion</span> y <span class='mono'>Param</span> marca la casilla "
        "<b>Remanencia</b>. En un DB optimizado se marca en el Struct entero, no campo por campo.",
    )
    + "<h4>Camino B · Desde fuente externa (rápido)</h4>"
    + lista(
        f"En el árbol: {ruta('PLC_Linea', 'Fuentes externas')} › doble clic en <b>Agregar nuevo archivo externo</b>.",
        "Elige <span class='mono'>02_DB_Linea.db</span> de la carpeta <span class='mono'>tia/fuentes</span> del repositorio. "
        "Si no tienes el fichero, copia el texto de abajo en el Bloc de notas y guárdalo con ese nombre.",
        "Clic derecho sobre el archivo › <b>Generar bloques a partir de la fuente</b>.",
        "Repite con <span class='mono'>04_DB_Tiempos.db</span>.",
        "Abre cada DB generado y, en Propiedades › General, pon el número: DB_Linea = 1 y DB_Tiempos = 3.",
    )
    + ojo("Si ya creaste DB_Linea a mano, TIA pregunta si quieres sobrescribirlo. Di que sí: la fuente trae el DB completo.")
    + tip("En DB_Tiempos los temporizadores son del tipo <span class='mono'>TON_TIME</span> y los contadores "
          "<span class='mono'>CTU_INT</span>. Tenerlos en un DB global permite usarlos desde cualquier FC sin crear un DB de instancia por cada uno.")
    + "<h4>Textos de las fuentes</h4>"
    + fuente("01_UDT_Botella.udt", leer_fuente("01_UDT_Botella.udt"))
    + fuente("02_DB_Linea.db", leer_fuente("02_DB_Linea.db"))
    + fuente("03_DB_FIFO.db", leer_fuente("03_DB_FIFO.db"))
    + fuente("04_DB_Tiempos.db", leer_fuente("04_DB_Tiempos.db"))
    + "<p class='note'>Las fuentes 01 y 03 son por si prefieres no hacer a mano el UDT y el FIFO. "
      "Se generan en orden: primero el UDT y luego los DB.</p>"
), "B"))

B.append(paso("p-compilar1", "Primera compilación", lista(
    "Clic derecho sobre <span class='mono'>PLC_Linea</span> › <b>Compilar</b> › <b>Hardware y software (solo cambios)</b>.",
    "Abajo, en la pestaña <b>Compilar</b>, debe salir <b>0 errores</b>. Los avisos (warnings) de que un DB no se usa son normales por ahora.",
) + ojo("Si sale un error en DB_FIFO del tipo <i>UDT_Botella no existe</i>, compila primero el UDT "
        "(clic derecho sobre él › Compilar) y luego el DB."), "B"))

# ---------------------------------------------------------------------------
# PARTE C · Cómo se dibuja en KOP
# ---------------------------------------------------------------------------
leyenda_kop = tabla(["Dibujo", "Instrucción en TIA", "Dónde está"], [
    ("<span class='mono'>──| |──</span>", "Contacto normalmente abierto", "Barra de favoritos · Instrucciones básicas › Operaciones lógicas con bits"),
    ("<span class='mono'>──|/|──</span>", "Contacto normalmente cerrado", "Igual"),
    ("<span class='mono'>──|P|──</span>", "Detectar flanco positivo del operando", "Operaciones lógicas con bits"),
    ("<span class='mono'>──( )</span>", "Asignación (bobina)", "Favoritos"),
    ("<span class='mono'>──(S)</span> / <span class='mono'>──(R)</span>", "Activar / desactivar salida (memoriza)", "Operaciones lógicas con bits"),
    ("<span class='mono'>──| &gt;= |──</span>", "Comparador. Arriba el valor 1, abajo el valor 2 y el tipo entre corchetes", "Instrucciones básicas › Comparación"),
    ("Caja con EN/ENO", "MOVE, ADD, DIV, NORM_X, SCALE_X, TON…", "Transferencia, Matemáticas, Conversión, Temporizadores"),
])
C = []
C.append(paso("p-kop", "Cómo se dibuja en KOP (léelo una vez)", (
    "<p>En todos los segmentos de la guía, la barra gruesa <span class='mono'>┃</span> de la izquierda es la "
    "alimentación. Lo que va entre comillas es una variable global "
    "(<span class='mono'>\"PB_Marcha\"</span>, <span class='mono'>\"DB_Linea\".Modo.Auto</span>) y lo que empieza por "
    "<span class='mono'>#</span> es una variable local del bloque (se declara en su interfaz).</p>"
    + leyenda_kop
    + "<h4>Las 5 maniobras que vas a repetir</h4>"
    + lista(
        "<b>Poner un contacto o bobina</b>: arrástralo desde la barra de favoritos (encima del editor) hasta la línea del segmento.",
        "<b>Poner el operando</b>: doble clic en <span class='mono'>&lt;??.?&gt;</span> y escribe el nombre. "
        "Al escribir <span class='mono'>\"DB_Linea\".</span> TIA te ofrece la lista de campos.",
        "<b>Hacer una rama OR</b>: selecciona el punto donde empieza, pulsa <b>Abrir rama</b> (flecha hacia abajo en favoritos), "
        "pon los contactos y arrastra el final de la rama hasta la línea principal.",
        "<b>Poner una caja</b>: búscala en el panel <b>Instrucciones</b> (derecha). Después haz clic en "
        "<span class='mono'>???</span> debajo del nombre para elegir el tipo (Int, Real, DInt…).",
        "<b>Añadir salidas a un MOVE</b>: haz clic en la estrella amarilla junto a <span class='mono'>OUT1</span> "
        "o clic derecho › <b>Insertar salida</b>.",
    )
    + tip("Escribe siempre el <b>título del segmento</b> (la línea gris de arriba). Pon el mismo que en la guía: "
          "el tribunal lo agradecerá y a ti te servirá para encontrar las cosas.")
), "C"))

# ---------------------------------------------------------------------------
# PARTE D · Primeros bloques
# ---------------------------------------------------------------------------
Dp = []

ob30 = (
    lista(
        "Agregar nuevo bloque › <b>Bloque de organización (OB)</b> › <b>Cyclic interrupt</b>.",
        "Nombre: <span class='mono'>OB30_Ciclo_100ms</span>. Lenguaje: <b>KOP</b>. Número: <span class='mono'>30</span>.",
        "En <b>Tiempo de ciclo</b> escribe <span class='mono'>100000</span> µs (100 ms) y acepta.",
        "Arriba del editor está la <b>interfaz</b> del bloque. En <b>Temp</b> añade la variable de la tabla.",
    )
    + interfaz([("Temp", "Litros_100ms", "Real", "Litros que entran en 100 ms.")])
    + "<p>Por qué un OB cíclico: el OB1 no tarda siempre lo mismo. El OB30 se ejecuta exactamente cada 100 ms, "
      "así que sirve de reloj para contar los 40 s de cada botella y para sumar los litros.</p>"
    + seg(1, "Reloj base de 100 ms", segmento(
        salida=caja("ADD", "DInt", [('"DB_Linea".Reloj.Base_100ms', "IN1"), ("1", "IN2")],
                    [("OUT", '"DB_Linea".Reloj.Base_100ms')])),
        "Cada 100 ms suma 1. Así <span class='mono'>Base_100ms</span> cuenta décimas de segundo desde que arranca la CPU. "
        "40 s son 400 décimas. La caja va pegada a la barra: se ejecuta siempre.")
    + seg(2, "Litros que entran en 100 ms", segmento(
        serie=[contacto(LLE + "En_Curso")],
        salida=caja("DIV", "Real", [(LLE + "Caudal_Lmin", "IN1"), ("600.0", "IN2")],
                    [("OUT", "#Litros_100ms")])),
        "El caudal viene en litros por minuto. Un minuto tiene 600 trozos de 100 ms, "
        "así que en cada trozo entran <span class='mono'>Caudal_Lmin / 600</span> litros. Solo se calcula mientras se llena.")
    + seg(3, "Acumular el volumen de la botella", segmento(
        serie=[contacto(LLE + "En_Curso")],
        salida=caja("ADD", "Real", [(LLE + "Volumen_L", "IN1"), ("#Litros_100ms", "IN2")],
                    [("OUT", LLE + "Volumen_L")])),
        "Va sumando los litros de cada trozo. Quien pone <span class='mono'>Volumen_L</span> a 0 al empezar cada botella "
        "será la FC5 de llenado.")
)
Dp.append(paso("p-ob30", "OB30 · Reloj de 100 ms y litros", ob30, "D"))

ob100 = (
    lista(
        "Agregar nuevo bloque › Bloque de organización › <b>Startup</b>. Nombre <span class='mono'>OB100_Arranque</span>, KOP.",
    )
    + "<p>El S7-1200 ya pone a su valor inicial los datos no remanentes al arrancar. Aun así hacemos el OB100 "
      "para que se vea claro, en el propio programa, cómo queda la línea al encender: parada, con la válvula "
      "cerrada, el FIFO vacío y esperando REARME.</p>"
    + seg(1, "Arranque seguro: rearme pendiente", segmento(
        salida=caja("MOVE", "Bool", [("TRUE", "IN")],
                    [("OUT1", '"DB_Linea".Modo.Rearme_Pendiente'), ("OUT2", '"DB_Linea".Modo.Parada_Seguridad')])),
        "Con un MOVE de tipo Bool se pueden escribir varios bits a la vez. Pegado a la barra se ejecuta siempre.")
    + seg(2, "Arranque seguro: válvula cerrada y llenado parado", segmento(
        salida=caja("MOVE", "Bool", [("FALSE", "IN")],
                    [("OUT1", '"VS_Valvula_Seguridad"'), ("OUT2", LLE + "En_Curso"),
                     ("OUT3", '"DB_Linea".Modo.Ciclo_Marcha')])),
        "La válvula de seguridad empieza siempre cerrada.")
    + seg(3, "FIFO vacío: punteros a 0", segmento(
        salida=caja("MOVE", "Int", [("0", "IN")],
                    [("OUT1", FIFO + "Ptr_Entrada"), ("OUT2", FIFO + "Ptr_Deteccion"),
                     ("OUT3", FIFO + "Ptr_Llenado"), ("OUT4", FIFO + "Ptr_Rechazo"),
                     ("OUT5", FIFO + "Idx_Transversal"), ("OUT6", FIFO + "N_Botellas")])),
        "Añade las salidas OUT2…OUT6 con la estrella amarilla.")
    + seg(4, "FIFO vacío: primera botella con ID 1", segmento(
        salida=caja("MOVE", "Int", [("1", "IN")], [("OUT1", FIFO + "Siguiente_ID")])), "")
    + seg(5, "FIFO vacío: las 4 posiciones libres", segmento(
        salida=caja("MOVE", "Bool", [("FALSE", "IN")],
                    [("OUT1", FIFO + "Botella[0].Activa"), ("OUT2", FIFO + "Botella[1].Activa"),
                     ("OUT3", FIFO + "Botella[2].Activa"), ("OUT4", FIFO + "Botella[3].Activa")])),
        "Así se escribe un campo de un elemento del array: <span class='mono'>Botella[2].Activa</span>.")
)
Dp.append(paso("p-ob100", "OB100 · Arranque seguro", ob100, "D"))


def seg_nivel(n, pct, sensor, num):
    return seg(num, f"Sensor de nivel {pct} %", segmento(
        paralelo=[[contacto(PAR + "Simulacion_FIO"), comparar(NIV + "Nivel_Pct", ">=", f"{pct}.0", "Real")],
                  [contacto(PAR + "Simulacion_FIO", "|/|"), contacto(f'"{sensor}"')]],
        salida=[bobina(NIV + f"Nivel_{pct}")]),
        n)


fc1 = (
    lista(
        "Agregar nuevo bloque › <b>Función (FC)</b>. Nombre <span class='mono'>FC_Entradas</span>, KOP, número manual <span class='mono'>1</span>.",
        "En la interfaz, sección <b>Temp</b>, añade estas dos variables:",
    )
    + interfaz([("Temp", "Nivel_Norm", "Real", "Nivel en tanto por uno (0.0 a 1.0)."),
                ("Temp", "Caudal_Norm", "Real", "Caudal en tanto por uno (0.0 a 1.0).")])
    + "<p>La entrada analógica da un número de 0 a 27648. <b>NORM_X</b> lo pasa a un valor de 0.0 a 1.0 y "
      "<b>SCALE_X</b> lo pasa a la unidad que queremos (% o l/min). Las dos están en "
      f"{ruta('Instrucciones básicas', 'Conversión')}.</p>"
    + seg(1, "Nivel del tanque: normalizar", segmento(
        salida=caja("NORM_X", "Int to Real", [("0", "MIN"), ('"AI_Nivel_Tanque"', "VALUE"), ("27648", "MAX")],
                    [("OUT", "#Nivel_Norm")])),
        "Elige los tipos haciendo clic en <span class='mono'>???</span>: primero Int (lo que entra) y luego Real (lo que sale).")
    + seg(2, "Nivel del tanque: escalar a %", segmento(
        salida=caja("SCALE_X", "Real to Real", [("0.0", "MIN"), ("#Nivel_Norm", "VALUE"), ("100.0", "MAX")],
                    [("OUT", NIV + "Nivel_Pct")])),
        "Si IW64 vale 13824 (la mitad), <span class='mono'>Nivel_Pct</span> vale 50.0.")
    + seg(3, "Caudalímetro: normalizar", segmento(
        salida=caja("NORM_X", "Int to Real", [("0", "MIN"), ('"AI_Caudalimetro"', "VALUE"), ("27648", "MAX")],
                    [("OUT", "#Caudal_Norm")])), "")
    + seg(4, "Caudalímetro: escalar a l/min", segmento(
        salida=caja("SCALE_X", "Real to Real",
                    [("0.0", "MIN"), ("#Caudal_Norm", "VALUE"), (PAR + "Caudal_Max_Lmin", "MAX")],
                    [("OUT", LLE + "Caudal_Lmin")])),
        "El máximo no es un número fijo: es un parámetro, porque lo calibraremos cuando montemos Factory I/O.")
    + seg_nivel("<p>Dos ramas en paralelo (OR):</p>" + lista(
        "<b>Arriba</b>: si estamos en simulación, el sensor se calcula comparando el nivel con 25.0.",
        "<b>Abajo</b>: si no estamos en simulación, se copia el sensor real I3.3.", ordenada=False)
        + "<p>Así el resto del programa usa siempre <span class='mono'>\"DB_Linea\".Tanque.Nivel_25</span> "
          "y no le importa de dónde venga.</p>", "25", "S_Tanque_25", 5)
    + seg_nivel("Igual que el anterior, con 90.0 e I3.4.", "90", "S_Tanque_90", 6)
    + seg_nivel("Igual, con 99.0 e I3.5. Este es el que dispara la emergencia del 99 %.", "99", "S_Tanque_99", 7)
    + tip("Haz el segmento 5 completo, cópialo (Ctrl+C sobre el segmento, Ctrl+V) y en la copia cambia solo el 25 por el 90. "
          "Tardas la mitad.")
)
Dp.append(paso("p-fc1", "FC1 · FC_Entradas", fc1, "D"))

Dp.append(paso("p-ob1", "Llamar a FC1 desde el OB1", lista(
    "Abre <span class='mono'>Main [OB1]</span>.",
    "Arrastra <span class='mono'>FC_Entradas</span> desde el árbol del proyecto al segmento 1.",
    "Título del segmento: <span class='mono'>FC1 · Entradas y escalados</span>.",
) + "<div class='kopw'><pre class='kop'>" + e(segmento(salida=caja("\"FC_Entradas\"", "", [], []))) + "</pre></div>"
  + "<p>El resto de FC se irán llamando en los segmentos siguientes, en orden (FC2, FC3…).</p>", "D"))

Dp.append(paso("p-prueba", "Compilar, cargar y probar en PLCSIM", (
    "<h4>Cargar</h4>" + lista(
        "Compila: clic derecho en <span class='mono'>PLC_Linea</span> › Compilar › Hardware y software (solo cambios). Debe dar 0 errores.",
        "Selecciona <span class='mono'>PLC_Linea</span> y pulsa el botón <b>Iniciar simulación</b> de la barra de herramientas.",
        "Se abre PLCSIM y la ventana <b>Carga avanzada</b>. Tipo de interfaz PG/PC: <b>PN/IE</b>. Pulsa <b>Iniciar búsqueda</b>, "
        "elige la CPU que aparece y pulsa <b>Cargar</b>.",
        "En el resumen pulsa <b>Cargar</b>, marca <b>Arrancar todos</b> y <b>Finalizar</b>. La CPU de PLCSIM pasa a RUN (verde).",
    )
    + "<h4>Probar (tabla SIM)</h4>" + lista(
        "En PLCSIM cambia a la <b>vista del proyecto</b> (icono arriba a la derecha). Abre <b>Tablas SIM › Tabla SIM_1</b>.",
        "Añade <span class='mono'>AI_Nivel_Tanque</span>, <span class='mono'>AI_Caudalimetro</span> y <span class='mono'>S_Tanque_25</span>.",
        "En TIA abre <span class='mono'>DB_Linea</span> y pulsa <b>Observar todo</b> (las gafas).",
    )
    + tabla(["Prueba", "Pon en la tabla SIM", "Debes ver en DB_Linea"], [
        ("1", "AI_Nivel_Tanque = 13824", "Nivel_Pct = 50.0 · Nivel_25 = TRUE · Nivel_90 = FALSE"),
        ("2", "AI_Nivel_Tanque = 27000", "Nivel_Pct ≈ 97.66 · Nivel_90 = TRUE · Nivel_99 = FALSE"),
        ("3", "AI_Nivel_Tanque = 27400", "Nivel_99 = TRUE"),
        ("4", "AI_Nivel_Tanque = 5000", "Nivel_Pct ≈ 18.1 · Nivel_25 = FALSE"),
        ("5", "AI_Caudalimetro = 27648", "Caudal_Lmin = 10.0"),
        ("6", "Además, en TIA fuerza Llenado.En_Curso = TRUE (clic derecho en el valor › Modificar)",
         "Volumen_L sube 1 L cada 6 s. Reloj.Base_100ms sube 10 por segundo."),
        ("7", "En TIA pon Param.Simulacion_FIO = FALSE y en la tabla SIM S_Tanque_25 = 1",
         "Nivel_25 sigue al sensor I3.3, no al nivel. Vuelve a poner Simulacion_FIO = TRUE al terminar."),
    ])
    + ojo("Al acabar la prueba 6 vuelve a poner <span class='mono'>En_Curso = FALSE</span>. Si no, el volumen sigue subiendo.")
), "D"))

# ---------------------------------------------------------------------------
PARTES = [
    ("A", "Proyecto y hardware", A),
    ("B", "Datos: UDT y DB", B),
    ("C", "Cómo se dibuja en KOP", C),
    ("D", "Primeros bloques", Dp),
]


def construir():
    cuerpo = ""
    for letra, titulo, pasos in PARTES:
        cuerpo += f'<h2 class="parte" id="parte-{letra}"><span>Parte {letra}</span> {titulo}</h2>' + "".join(pasos)

    indice = ""
    n = 0
    for letra, titulo, _ in PARTES:
        items = ""
        for id_, t, p in _pasos:
            if p == letra:
                n += 1
                items += f"<li><a href='#{id_}'><span>{n}</span>{t}</a></li>"
        indice += f"<div><h4>{letra} · {titulo}</h4><ol>{items}</ol></div>"

    with open(os.path.join(os.path.dirname(__file__), "estilo.css"), encoding="utf-8") as fh:
        css = fh.read()
    with open(os.path.join(os.path.dirname(__file__), "estilo_guia.css"), encoding="utf-8") as fh:
        css += fh.read()
    return f"""<title>Guía TIA Parte 1</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>
{css}
</style>
<div class="wrap">
  <header class="top">
    <div class="eyebrow">TFC · Línea de llenado · Guía paso a paso</div>
    <h1>Parte 1 <span>/ Del proyecto vacío a los primeros bloques KOP</span></h1>
    <div class="meta">
      <span>TIA Portal <b>V15</b></span><span>S7-PLCSIM <b>V15</b></span>
      <span><b>{len(_pasos)}</b> pasos</span><span>Tabla de variables <b>{e(D.REVISION)}</b></span>
    </div>
  </header>
  <nav class="indice" aria-label="Índice">{indice}</nav>
  {cuerpo}
  <section class="sig">
    <h2>Siguiente: Parte 2</h2>
    <p>FC2 · Modos y seguridad: AUTO/MANUAL, MARCHA, PARO de fin de ciclo, SETA, REARME, emergencias,
    válvula de seguridad, baliza y sirena. Es el corazón de la línea y lo haremos con calma.</p>
  </section>
  <footer>Generado desde herramientas/guia_parte1.py · Los dibujos KOP salen de herramientas/kop.py</footer>
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


if __name__ == "__main__":
    pagina = construir()
    ruta_html = os.path.join(RAIZ, "docs", "02_Guia_Parte1.html")
    with open(ruta_html, "w", encoding="utf-8") as fh:
        fh.write('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
                 '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
                 '</head>\n<body>\n' + pagina + '\n</body>\n</html>\n')
    print("HTML ->", ruta_html)
    if len(sys.argv) > 1:
        with open(sys.argv[1], "w", encoding="utf-8") as fh:
            fh.write(pagina)
        print("Web  ->", sys.argv[1])
