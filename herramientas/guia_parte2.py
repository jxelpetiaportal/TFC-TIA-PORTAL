# -*- coding: utf-8 -*-
"""
Guía paso a paso · Parte 2: FC2 · Modos y seguridad.
Genera docs/03_Guia_Parte2.html   (y, si se pasa una ruta, la versión para publicar).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import datos_variables as D  # noqa: E402
from guia_comun import (EMG, FIFO, FLA, MOD, NIV, Guia, e, escribir, fuente, interfaz,  # noqa: E402,F401
                        leer_fuente, lista, m, ojo, ruta, seg, tabla, tip)
from kop import bobina, caja, comparar, contacto, segmento  # noqa: E402

G = Guia()
paso = G.paso

# ---------------------------------------------------------------------------
# PARTE A · Antes de empezar
# ---------------------------------------------------------------------------
A = []

estados = tabla(["Estado de la línea", "Cómo lo ve el programa", "Piloto (lo hará FC10)", "Cómo se sale"], [
    ("<b>Parada de seguridad</b>", m("Hay_Causa = 1"), "REARME fijo · baliza si no es MANUAL", "Quitar la causa"),
    ("<b>Rearme pendiente</b>", m("Hay_Causa = 0 y Rearme_Pendiente = 1"), "REARME parpadeando", "Pulsar REARME"),
    ("<b>Lista, esperando MARCHA</b>", m("Parada_Seguridad = 0 y Ciclo_Marcha = 0"), "PARO fijo", "Pulsar MARCHA"),
    ("<b>En marcha</b>", m("Ciclo_Marcha = 1 y Fin_Ciclo = 0"), "MARCHA fijo", "PARO → terminando"),
    ("<b>Terminando</b> (fin de ciclo)", m("Ciclo_Marcha = 1 y Fin_Ciclo = 1"), "PARO parpadeando",
     "Al vaciarse la línea → Lista. MARCHA → vuelve a En marcha"),
])
causas = tabla(["Causa", "Bit en DB_Linea", "Quién lo escribe", "Sirena y baliza", "Para poder rearmar"], [
    ("Seta pulsada", m("Emergencia.Seta"), "FC2", "Sí", "Desenclavar la seta"),
    ("Tanque al 99 %", m("Emergencia.Nivel_99"), "FC2 (con el nivel de FC1)", "Sí", "Que el nivel baje del 99 %"),
    ("Botella más de 40 s", m("Emergencia.Tiempo_40s"), "FC9 (más adelante)", "Sí", "Se definirá en FC9"),
    ("Selector en MANUAL", m("Emergencia.Manual"), "FC2", "<b>No</b>", "Volver a AUTO"),
    ("Fallo rojo de una fase", m("Emergencia.Fallo_Equipo"), "FC10 (más adelante)", "Sí", "Corregir el fallo"),
])
A.append(paso("p-idea", "Cómo funciona la seguridad (léelo antes de programar)", (
    "<p>Toda la seguridad de la línea se apoya en una sola idea:</p>"
    + lista(
        "Cada <b>causa</b> de emergencia es un bit que vale 1 <b>solo mientras la causa existe</b> "
        "(la seta está pulsada, el nivel está al 99 %…). No se memoriza.",
        f"La memoria está en un único bit: {m('Modo.Rearme_Pendiente')}. Se activa con cualquier causa "
        "y <b>solo se borra al pulsar REARME cuando ya no queda ninguna causa</b>.",
        f"{m('Modo.Parada_Seguridad')} = hay causa <b>o</b> falta el rearme. Todas las FC de la línea lo miran: "
        "si vale 1, no mueven nada.",
    )
    + "<p>Así, aunque sueltes la seta, la línea no arranca sola: siempre hace falta REARME y luego MARCHA.</p>"
    + "<h4>Estados de la línea</h4>" + estados
    + "<h4>Las 5 causas</h4>" + causas
    + tip("Las causas de 40 s y de fallo rojo las escribirán FC9 y FC10. Hasta entonces valen 0 y no molestan: "
          "puedes programar y probar FC2 completo ya.")
), "A"))

nuevas = [(g, n, t, x) for g, n, t, _v, _r, x in D.DB_LINEA
          if g == "Flancos" or (g == "Emergencia" and n in ("Hay_Causa", "Memo_Sirena", "Memo_Baliza"))]
A.append(paso("p-db", "Añadir variables nuevas a DB_Linea", (
    "<p>FC2 necesita 3 variables nuevas en el Struct <span class='mono'>Emergencia</span> y un Struct nuevo, "
    "<span class='mono'>Flancos</span>. Tienes dos caminos:</p>"
    "<h4>Camino A · A mano</h4>"
    + lista(
        "Abre <span class='mono'>DB_Linea</span>.",
        "Despliega <span class='mono'>Emergencia</span>. Debajo de <span class='mono'>Fallo_Equipo</span> añade "
        "<span class='mono'>Hay_Causa</span>, <span class='mono'>Memo_Sirena</span> y <span class='mono'>Memo_Baliza</span>, todas Bool.",
        "Justo debajo del Struct <span class='mono'>Emergencia</span> (al mismo nivel) crea el Struct "
        "<span class='mono'>Flancos</span> con sus 8 Bool.",
    )
    + tabla(["Struct", "Nombre", "Tipo", "Para qué"],
            [(f"<span class='mono'>{g}</span>", f"<span class='nm'>{n}</span>", f"<span class='ty'>{t}</span>", e(x))
             for g, n, t, x in nuevas])
    + "<h4>Camino B · Fuente externa actualizada</h4>"
    + lista(
        "En Fuentes externas, borra el <span class='mono'>02_DB_Linea.db</span> antiguo y añade el nuevo (texto abajo).",
        "Clic derecho › <b>Generar bloques a partir de la fuente</b> › acepta sobrescribir DB_Linea.",
    )
    + fuente("02_DB_Linea.db", leer_fuente("02_DB_Linea.db"))
    + ojo("Si regeneras DB_Linea desde la fuente, los parámetros vuelven a sus valores iniciales. "
          "Ahora mismo da igual porque aún no has cambiado ninguno.")
), "A"))

# ---------------------------------------------------------------------------
# PARTE B · FC2 segmento a segmento
# ---------------------------------------------------------------------------
B = []

B.append(paso("p-crear", "Crear FC2", lista(
    "Agregar nuevo bloque › <b>Función (FC)</b>. Nombre <span class='mono'>FC_Modos_Seguridad</span>, "
    "lenguaje KOP, número manual <span class='mono'>2</span>.",
    "Esta FC no necesita variables en la interfaz: todo lo que usa está en DB_Linea y en la tabla de variables.",
    "Vas a hacer 20 segmentos. Están agrupados en 6 pasos; pon a cada segmento el título que indica la guía.",
), "B"))

g1 = (
    seg(1, "Modo AUTO", segmento(serie=[contacto('"SEL_Auto"')], salida=[bobina(MOD + "Auto")]),
        "Copia el selector a DB_Linea. El resto del programa mira siempre la variable del DB, nunca la entrada directa.")
    + seg(2, "Causa: seta pulsada", segmento(serie=[contacto('"SETA_Emergencia"', "|/|")], salida=[bobina(EMG + "Seta")]),
          "La seta es NC: en reposo la entrada vale 1 y al pulsarla vale 0. Por eso el contacto es cerrado "
          "<span class='mono'>|/|</span>: da 1 justo cuando la seta está pulsada, o si se corta el cable.")
    + seg(3, "Causa: tanque al 99 %", segmento(serie=[contacto(NIV + "Nivel_99")], salida=[bobina(EMG + "Nivel_99")]),
          "El sensor lo calcula FC1 (real o simulado).")
    + seg(4, "Causa: modo MANUAL", segmento(serie=[contacto('"SEL_Auto"', "|/|")], salida=[bobina(EMG + "Manual")]), "")
    + seg(5, "Resumen de causas", segmento(
        paralelo=[[contacto(EMG + "Seta")], [contacto(EMG + "Nivel_99")], [contacto(EMG + "Tiempo_40s")],
                  [contacto(EMG + "Manual")], [contacto(EMG + "Fallo_Equipo")]],
        salida=[bobina(EMG + "Hay_Causa")]),
        "Cinco ramas en paralelo (OR). Si cualquiera vale 1, hay causa. Para hacerlo: pon el primer contacto, "
        "abre rama debajo, pon el segundo, cierra la rama, y repite.")
)
B.append(paso("p-g1", "Segmentos 1 a 5 · Modo y causas", g1, "B"))

g2 = (
    seg(6, "Pulso de MARCHA", segmento(
        serie=[contacto('"PB_Marcha"', "|P|", FLA + "Marcha_FM")], salida=[bobina(FLA + "Marcha_Pulso")]),
        "El contacto <span class='mono'>|P|</span> da 1 durante un solo ciclo cuando la entrada pasa de 0 a 1. "
        "Debajo lleva un bit de memoria (<span class='mono'>Marcha_FM</span>) donde TIA guarda cómo estaba la entrada "
        "en el ciclo anterior.")
    + seg(7, "Pulso de REARME", segmento(
        serie=[contacto('"PB_Rearme"', "|P|", FLA + "Rearme_FM")], salida=[bobina(FLA + "Rearme_Pulso")]), "")
    + ojo("Cada <span class='mono'>|P|</span> necesita su propio bit de memoria y ese bit no se usa en ningún otro sitio. "
          "Si repites un bit de memoria en dos flancos, los dos fallan.")
    + tip("Por eso sacamos el pulso a una variable (<span class='mono'>Marcha_Pulso</span>): la podemos usar en "
          "todos los segmentos que queramos sin repetir el flanco.")
)
B.append(paso("p-g2", "Segmentos 6 y 7 · Pulsos de MARCHA y REARME", g2, "B"))

g3 = (
    seg(8, "Rearme pendiente: se activa con cualquier causa", segmento(
        serie=[contacto(EMG + "Hay_Causa")], salida=[bobina(MOD + "Rearme_Pendiente", "(S)")]),
        "Bobina <span class='mono'>(S)</span>: una vez activada se queda a 1 aunque la causa desaparezca.")
    + seg(9, "Rearme pendiente: se borra con REARME si no queda ninguna causa", segmento(
        serie=[contacto(FLA + "Rearme_Pulso"), contacto(EMG + "Hay_Causa", "|/|")],
        salida=[bobina(MOD + "Rearme_Pendiente", "(R)")]),
        "Si pulsas REARME con la seta todavía pulsada, no pasa nada: el contacto cerrado de "
        "<span class='mono'>Hay_Causa</span> lo impide.")
    + seg(10, "Parada de seguridad", segmento(
        paralelo=[[contacto(EMG + "Hay_Causa")], [contacto(MOD + "Rearme_Pendiente")]],
        salida=[bobina(MOD + "Parada_Seguridad")]),
        "Esta es la variable que mirarán todas las FC: si vale 1, nada se mueve.")
)
B.append(paso("p-g3", "Segmentos 8 a 10 · Rearme y parada de seguridad", g3, "B"))

g4 = (
    seg(11, "Sirena: REARME la silencia", segmento(
        serie=[contacto(FLA + "Rearme_Pulso")], salida=[bobina(EMG + "Memo_Sirena", "(R)")]),
        "Tal como acordamos: REARME silencia la sirena aunque la causa siga activa.")
    + seg(12, "Emergencia nueva: sirena y baliza", segmento(
        paralelo=[[contacto(EMG + "Seta", "|P|", FLA + "Seta_FM")],
                  [contacto(EMG + "Nivel_99", "|P|", FLA + "Nivel99_FM")],
                  [contacto(EMG + "Tiempo_40s", "|P|", FLA + "T40_FM")],
                  [contacto(EMG + "Fallo_Equipo", "|P|", FLA + "Fallo_FM")]],
        salida=[bobina(EMG + "Memo_Sirena", "(S)"), bobina(EMG + "Memo_Baliza", "(S)")]),
        "<p>Cuatro flancos en paralelo: la sirena y la baliza se disparan <b>cuando aparece</b> una causa, no mientras dura. "
        "Así, si silencias con REARME y luego aparece otra causa distinta, la sirena vuelve a sonar.</p>"
        "<p>MANUAL no está aquí a propósito: pasar a MANUAL no hace sonar la sirena.</p>")
    + ojo("El segmento 11 va <b>antes</b> que el 12. Si en el mismo ciclo se pulsa REARME y aparece una emergencia nueva, "
          "gana la emergencia y la sirena suena.")
    + seg(13, "Baliza: se apaga al completar el rearme", segmento(
        serie=[contacto(MOD + "Rearme_Pendiente", "|/|")], salida=[bobina(EMG + "Memo_Baliza", "(R)")]),
        "La baliza sigue avisando mientras la causa exista o falte el rearme.")
    + seg(14, "Salida: sirena", segmento(serie=[contacto(EMG + "Memo_Sirena")], salida=[bobina('"Sirena"')]), "")
    + seg(15, "Salida: baliza intermitente y prueba de lámparas", segmento(
        paralelo=[[contacto(EMG + "Memo_Baliza"), contacto('"Clock_2Hz"')], [contacto('"PB_Prueba_Lamparas"')]],
        salida=[bobina('"Baliza_Naranja"')]),
        "La marca de ciclo <span class='mono'>Clock_2Hz</span> hace el parpadeo. Con el pulsador de prueba se enciende fija.")
)
B.append(paso("p-g4", "Segmentos 11 a 15 · Sirena y baliza", g4, "B"))

g5 = (
    seg(16, "Línea vacía", segmento(
        serie=[comparar(FIFO + "N_Botellas", "==", "0", "Int")], salida=[bobina(MOD + "Linea_Vacia")]),
        "Comparador de igualdad, tipo Int. De momento siempre vale 1 porque todavía no hay botellas en el FIFO.")
    + seg(17, "MARCHA: arrancar el ciclo", segmento(
        serie=[contacto(FLA + "Marcha_Pulso"), contacto(MOD + "Auto"), contacto(MOD + "Parada_Seguridad", "|/|"),
               contacto('"PB_Paro"')],
        salida=[bobina(MOD + "Ciclo_Marcha", "(S)"), bobina(MOD + "Fin_Ciclo", "(R)")]),
        "<p>Arranca solo en AUTO, sin parada de seguridad y con PARO sin pulsar. PARO es NC, por eso aquí el contacto es "
        "abierto: vale 1 cuando <b>no</b> está pulsado.</p>"
        "<p>Si pulsas MARCHA mientras la línea está terminando, se anula el fin de ciclo y sigue produciendo.</p>")
    + seg(18, "PARO: pedir fin de ciclo", segmento(
        serie=[contacto('"PB_Paro"', "|/|"), contacto(MOD + "Ciclo_Marcha")],
        salida=[bobina(MOD + "Fin_Ciclo", "(S)")]),
        "PARO no para en seco: solo deja de pedir botellas nuevas (lo hará FC4) y espera a que salgan las que hay.")
    + seg(19, "Parar el ciclo: fin de ciclo terminado o emergencia", segmento(
        paralelo=[[contacto(MOD + "Fin_Ciclo"), contacto(MOD + "Linea_Vacia")], [contacto(MOD + "Parada_Seguridad")]],
        salida=[bobina(MOD + "Ciclo_Marcha", "(R)"), bobina(MOD + "Fin_Ciclo", "(R)")]),
        "Rama de arriba: se pidió PARO y ya no queda ninguna botella. Rama de abajo: cualquier emergencia corta el ciclo al momento.")
)
B.append(paso("p-g5", "Segmentos 16 a 19 · Ciclo: MARCHA y PARO de fin de ciclo", g5, "B"))

g6 = seg(20, "Válvula de seguridad del tanque", segmento(
    serie=[contacto(MOD + "Auto"), contacto(MOD + "Parada_Seguridad", "|/|")],
    salida=[bobina('"VS_Valvula_Seguridad"')]),
    "<p>La válvula se abre en AUTO y sin parada de seguridad, <b>aunque el ciclo esté parado</b>. Así el tanque "
    "mantiene su nivel y está listo cuando pulses MARCHA.</p>"
    "<p>Con cualquier emergencia, con MANUAL o mientras falte el rearme, se cierra.</p>")
B.append(paso("p-g6", "Segmento 20 · Válvula de seguridad", g6, "B"))

B.append(paso("p-ob1", "Llamar a FC2 desde el OB1", lista(
    "Abre <span class='mono'>Main [OB1]</span>. Añade un segmento debajo del de FC1.",
    "Arrastra <span class='mono'>FC_Modos_Seguridad</span> al segmento 2. Título: <span class='mono'>FC2 · Modos y seguridad</span>.",
) + "<div class='kopw'><pre class='kop'>" + e(segmento(salida=caja("\"FC_Modos_Seguridad\"", "", [], []))) + "</pre></div>"
  + "<p>El orden importa: FC1 prepara los sensores y FC2 decide si la línea puede funcionar. "
    "Todas las FC que vengan después usarán lo que FC2 ha decidido en este mismo ciclo.</p>", "B"))

# ---------------------------------------------------------------------------
# PARTE C · Probar
# ---------------------------------------------------------------------------
C = []
obs = ["Modo.Auto", "Modo.Ciclo_Marcha", "Modo.Fin_Ciclo", "Modo.Rearme_Pendiente", "Modo.Parada_Seguridad",
       "Emergencia.Hay_Causa", "Emergencia.Memo_Sirena", "Emergencia.Memo_Baliza"]
C.append(paso("p-tablas", "Preparar las tablas de prueba", (
    "<h4>En TIA: tabla de observación</h4>"
    + lista(
        f"En el árbol: {ruta('PLC_Linea', 'Tablas de observación y forzado permanente')} › <b>Agregar tabla de observación</b>. "
        "Nombre: <span class='mono'>Obs_FC2</span>.",
        "Escribe estas variables, una por fila: "
        + ", ".join(m('"DB_Linea".' + x) for x in obs)
        + ", " + m('"VS_Valvula_Seguridad"') + ", " + m('"Sirena"') + " y " + m('"Baliza_Naranja"') + ".",
        "Pulsa <b>Observar todo</b> (las gafas) cuando el PLC esté en RUN.",
    )
    + "<h4>En PLCSIM: tabla SIM</h4>"
    + lista(
        "Compila y carga como en la Parte 1.",
        "En la tabla SIM añade " + ", ".join(m(x) for x in ('"SETA_Emergencia"', '"PB_Paro"', '"SEL_Auto"',
                                                             '"PB_Marcha"', '"PB_Rearme"', '"AI_Nivel_Tanque"')) + ".",
    )
    + ojo("PLCSIM arranca con todas las entradas a 0. Para el PLC eso es <b>seta pulsada, PARO pulsado y MANUAL</b>, "
          "porque la seta y el PARO son NC. Así que lo primero que verás es la sirena sonando: es lo correcto.")
    + tip("Para simular que pulsas un botón en la tabla SIM, pon su valor a 1 y enseguida otra vez a 0. "
          "En PARO es al revés, porque es NC: de 1 a 0 y otra vez a 1.")
), "C"))

pruebas = [
    ("0", "Nada: acabas de cargar", "Sirena = 1 · Baliza parpadea · Rearme_Pendiente = 1 · VS = 0"),
    ("1", "SETA = 1 · PARO = 1 · SEL_Auto = 1 · AI_Nivel_Tanque = 13824",
     "Hay_Causa = 0 · Rearme_Pendiente = 1 · la sirena sigue sonando · VS = 0"),
    ("2", "Pulsa REARME", "Rearme_Pendiente = 0 · Parada = 0 · Sirena = 0 · Baliza = 0 · <b>VS = 1</b>"),
    ("3", "Pulsa MARCHA", "Ciclo_Marcha = 1"),
    ("4", "Pulsa PARO (1 → 0 → 1)", "Ciclo_Marcha = 0 enseguida, porque no hay botellas en la línea"),
    ("5", "Pulsa MARCHA y luego pon SETA = 0", "Sirena = 1 · Baliza parpadea · Ciclo_Marcha = 0 · VS = 0"),
    ("6", "Con la seta aún a 0, pulsa REARME", "Sirena = 0 · la baliza <b>sigue</b> · Rearme_Pendiente = 1"),
    ("7", "SETA = 1 y pulsa REARME", "Todo limpio · VS = 1 · Baliza = 0"),
    ("8", "SEL_Auto = 0", "Parada = 1 · VS = 0 · <b>sin</b> sirena ni baliza"),
    ("9", "SEL_Auto = 1 y pulsa MARCHA sin rearmar", "No arranca: Rearme_Pendiente = 1. Pulsa REARME y ya puedes"),
    ("10", "AI_Nivel_Tanque = 27400", "Sirena = 1 · Baliza parpadea · VS = 0"),
    ("11", "AI_Nivel_Tanque = 13824 y pulsa REARME", "Todo limpio · VS = 1"),
    ("12", "PB_Prueba_Lamparas = 1", "Baliza_Naranja = 1 fija mientras lo mantengas"),
]
C.append(paso("p-pruebas", "Las 13 pruebas de FC2", (
    "<p>Hazlas en orden. Cada fila parte de cómo quedó la anterior.</p>"
    + tabla(["#", "Qué haces", "Qué debes ver"], pruebas)
    + tip("Si una prueba falla, abre FC2 y pulsa <b>Activar/desactivar observación</b> (las gafas del editor). "
          "Verás en verde por dónde pasa la corriente en cada segmento y encontrarás el fallo enseguida.")
), "C"))

PARTES = [
    ("A", "Antes de empezar", A),
    ("B", "FC2 segmento a segmento", B),
    ("C", "Probar en PLCSIM", C),
]


def construir():
    return G.pagina(2, "FC2 · Modos y seguridad", PARTES, (
        "Siguiente: Parte 3",
        "<p>FC3 · Tanque: la bomba arranca por debajo del 25 % y para al 90 %, el interruptor de prueba del 99 % "
        "y las alarmas A101 a A104.</p>"),
        "guia_parte2.py")


if __name__ == "__main__":
    escribir(construir(), "03_Guia_Parte2.html")
