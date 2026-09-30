# -*- coding: utf-8 -*-
"""Guía completa · Partes 1 a 5: proyecto, variables, datos, KOP, OB100 y OB30 (todo a mano)."""
import datos_variables as D
from guia_comun import (FIFO, FLA, LLE, MOD, PAR, R, S, Segmentos, b, c, crear_bloque, e, g, interfaz,  # noqa: F401
                        kop, lista, m, mat, mv, ojo, ruta, tabla, tip)


def _tabla_vars(filas):
    return tabla(["Nombre", "Tipo de datos", "Dirección", "Comentario"],
                 [(f"<span class='nm'>{e(n)}</span>", f"<span class='ty'>{t}</span>",
                   f"<span class='mono'>{a}</span>", e(cm)) for a, n, t, cm, _x, _f in filas if n])


def _tabla_db(filas, con_rem=False):
    cab = ["Nombre", "Tipo de datos", "Valor de arranque", "Comentario"]
    return tabla(cab, [(f"<span class='nm'>{e(n)}</span>", f"<span class='ty'>{e(t)}</span>",
                        f"<span class='mono'>{e(v)}</span>", e(x)) for n, t, v, x in filas])


def partes(G):
    paso = G.paso
    P = []

    # =====================================================================
    # PARTE 1 · Proyecto y hardware
    # =====================================================================
    p1 = []
    p1.append(paso("p-proyecto", "Crear el proyecto", lista(
        f"Abre TIA Portal V15. En la vista del portal pulsa {ruta('Crear proyecto')}.",
        "Nombre del proyecto: <span class='mono'>Linea_Llenado_TFC</span>. Elige la carpeta y escribe tu nombre en Autor.",
        "Pulsa <b>Crear</b>.",
        "Abajo a la izquierda pulsa <b>Vista del proyecto</b>. Toda la guía se hace desde esta vista.",
    ), 1))

    p1.append(paso("p-cpu", "Añadir la CPU", lista(
        f"En el árbol del proyecto (izquierda), doble clic en {ruta('Agregar dispositivo')}.",
        f"Elige {ruta('Controladores', 'SIMATIC S7-1200', 'CPU', 'CPU 1214C DC/DC/DC', '6ES7 214-1AG40-0XB0')}.",
        "Abajo, en <b>Versión</b>, elige <span class='mono'>V4.2</span> y pulsa <b>Aceptar</b>.",
        f"Con la CPU seleccionada, ve a {ruta('Propiedades', 'General', 'Información del proyecto')} "
        "y en <b>Nombre</b> escribe <span class='mono'>PLC_Linea</span>.",
    ) + tip("La ventana de <b>Propiedades</b> es la de abajo (ventana de inspección). "
            "Si no la ves, haz doble clic sobre la CPU."), 1))

    filas_hw = [
        ("1", "CPU 1214C DC/DC/DC", "—", "Integrada: I0.0–I1.5 · Q0.0–Q1.1 · IW64/IW66"),
        ("2", "DI 16x24VDC · 6ES7 221-1BH32-0XB0", "<b>2</b>", "I2.0–I3.7"),
        ("3", "DQ 16x24VDC · 6ES7 222-1BH32-0XB0", "<b>2</b>", "Q2.0–Q3.7"),
        ("4", "DQ 16x24VDC · 6ES7 222-1BH32-0XB0", "<b>4</b>", "Q4.0–Q5.7"),
        ("5", "AQ 2x14BIT · 6ES7 232-4HB32-0XB0", "<b>64</b>", "QW64, QW66"),
    ]
    p1.append(paso("p-modulos", "Añadir los módulos y cambiar sus direcciones", lista(
        "Abre la <b>Vista de dispositivos</b> de la CPU (doble clic en <span class='mono'>PLC_Linea</span> › Configuración de dispositivos).",
        "A la derecha abre el <b>Catálogo de hardware</b>. Arrastra cada módulo al slot que indica la tabla.",
        f"Haz clic en cada módulo y ve a {ruta('Propiedades', 'General', 'Direcciones E/S')}. "
        "En <b>Dirección inicial</b> escribe el valor de la tabla.",
    ) + tabla(["Slot", "Módulo del catálogo", "Dirección inicial", "Resultado"],
              [(f"<span class='mono'>{a}</span>", bb, f"<span class='mono'>{cc}</span>", f"<span class='mono'>{d}</span>")
               for a, bb, cc, d in filas_hw])
        + tip("Para revisarlo todo de un vistazo, abre la <b>Vista general de dispositivos</b> "
              "(la flecha pequeña a la derecha del dibujo de la CPU). Las columnas <b>Dirección I</b> y "
              "<b>Dirección Q</b> deben coincidir con la tabla."), 1))

    p1.append(paso("p-marcas", "Activar las marcas de sistema y de ciclo", lista(
        f"Selecciona la CPU y ve a {ruta('Propiedades', 'General', 'Marcas de sistema y de ciclo')}.",
        "Marca <b>Activar la utilización del byte de marcas de sistema</b> y pon la dirección <span class='mono'>1</span> (MB1).",
        "Marca <b>Activar la utilización del byte de marcas de ciclo</b> y pon la dirección <span class='mono'>0</span> (MB0).",
    ) + "<p>TIA crea solo estas variables en la tabla estándar. Las usaremos para los parpadeos:</p>"
        + tabla(["Variable", "Dirección", "Uso en el programa"],
                [(f"<span class='nm'>{n}</span>", f"<span class='mono'>{a}</span>", x) for a, n, _t, _c, x in D.MARCAS]), 1))

    p1.append(paso("p-sim", "Permitir la simulación", lista(
        "En el árbol, clic derecho sobre el nombre del proyecto (la primera línea) › <b>Propiedades</b>.",
        "Pestaña <b>Protección</b>.",
        "Marca <b>Soportar simulación durante la compilación de bloques</b> y pulsa <b>Aceptar</b>.",
    ) + ojo("Sin esta casilla PLCSIM no deja cargar el programa. Es el fallo más típico al empezar."), 1))

    p1.append(paso("p-comp-hw", "Compilar el hardware", lista(
        "Clic derecho en <span class='mono'>PLC_Linea</span> › <b>Compilar</b> › <b>Configuración hardware</b>.",
        "Abajo, en la pestaña <b>Compilar</b>, debe salir 0 errores.",
    ), 1))
    P.append((1, "Proyecto y hardware", p1,
              "Creamos el proyecto, la CPU y los módulos, con las direcciones que usa todo el programa."))

    # =====================================================================
    # PARTE 2 · Tabla de variables
    # =====================================================================
    p2 = []
    di = D.ENTRADAS_DIGITALES
    dq = [x for x in D.SALIDAS_DIGITALES if not x[1].startswith("L")]
    lam = [x for x in D.SALIDAS_DIGITALES if x[1].startswith("L")]
    p2.append(paso("p-tabla", "Crear la tabla de variables y aprender a rellenarla rápido", lista(
        f"En el árbol: {ruta('PLC_Linea', 'Variables PLC')} › doble clic en <b>Agregar tabla de variables</b>.",
        "Clic derecho sobre la tabla nueva › <b>Cambiar nombre</b>: <span class='mono'>Linea_Llenado</span>. Ábrela.",
        "En la primera fila vacía escribe el <b>Nombre</b>, pulsa Tab, el <b>Tipo de datos</b> (Bool, Int…), Tab, la "
        "<b>Dirección</b> y Tab, el <b>Comentario</b>.",
    ) + tip("En la dirección puedes escribir <span class='mono'>I0.0</span> sin el <span class='mono'>%</span>: TIA lo añade solo.")
        + tip("Para las lámparas, escribe la primera fila, selecciónala, y arrastra hacia abajo el cuadradito de la esquina "
              "inferior derecha de la celda: TIA crea las siguientes subiendo la dirección. Después solo corriges los nombres.")
        + ojo("Las direcciones tienen que ser exactamente las de esta guía: Factory I/O se conectará a ellas.")
        + ojo("En cada fila nueva TIA copia el tipo de la fila de arriba. Las analógicas son <span class='mono'>Int</span> y "
              "todo lo demás <span class='mono'>Bool</span>: revísalo."), 2))

    p2.append(paso("p-var-di", f"Entradas digitales ({sum(1 for x in di if x[1])})",
                   "<p>Cuadro de mando (I0), sensores de la cinta (I1) y módulo DI16 (I2 e I3). Las reservas no se escriben.</p>"
                   + _tabla_vars(di)
                   + ojo("<span class='mono'>PB_Paro</span> y <span class='mono'>SETA_Emergencia</span> son NC: en reposo valen 1. "
                         "Lo tendremos en cuenta al programar."), 2))
    p2.append(paso("p-var-dq", f"Salidas digitales ({len(dq)})", _tabla_vars(dq), 2))
    p2.append(paso("p-var-lam", f"Lámparas de fase ({len(lam)})",
                   "<p>Tres por fase: verde, naranja y roja. Van seguidas de Q3.3 a Q5.7.</p>" + _tabla_vars(lam), 2))
    p2.append(paso("p-var-an", "Entradas y salidas analógicas (4)", _tabla_vars(D.ANALOGICAS)
                   + "<p>Tipo <span class='mono'>Int</span>: el valor va de 0 a 27648 (0 a 10 V).</p>", 2))
    p2.append(paso("p-var-comp", "Comprobar la tabla", lista(
        f"Debe haber {sum(1 for x in di if x[1]) + len(dq) + len(lam) + len(D.ANALOGICAS)} variables en <span class='mono'>Linea_Llenado</span>.",
        "Ninguna fila en rojo (si hay una, suele ser una dirección repetida o mal escrita).",
        "Compila: clic derecho en <span class='mono'>PLC_Linea</span> › Compilar › Software.",
    ), 2))
    P.append((2, "Tabla de variables", p2,
              "Escribimos a mano todas las entradas y salidas físicas. El resto de datos va en bloques de datos (parte 3)."))

    # =====================================================================
    # PARTE 3 · Datos
    # =====================================================================
    p3 = []
    p3.append(paso("p-udt", "Crear el tipo de datos UDT_Botella", lista(
        f"En el árbol: {ruta('PLC_Linea', 'Tipos de datos PLC')} › doble clic en <b>Agregar nuevo tipo de datos</b>.",
        "Cámbiale el nombre (F2) a <span class='mono'>UDT_Botella</span>.",
        "Rellena una fila por campo.",
    ) + _tabla_db(D.UDT_BOTELLA)
        + tip("Un UDT es un molde: los datos que lleva cada botella. El FIFO tendrá 4 botellas con este molde."), 3))

    p3.append(paso("p-dbfifo", "Crear DB_FIFO (DB2)", lista(
        f"{ruta('Bloques de programa')} › <b>Agregar nuevo bloque</b> › <b>Bloque de datos (DB)</b>.",
        "Nombre <span class='mono'>DB_FIFO</span>, tipo <b>DB global</b>, número manual <span class='mono'>2</span>.",
        "Primera fila: nombre <span class='mono'>Botella</span> y en tipo escribe "
        "<span class='mono'>Array[0..3] of \"UDT_Botella\"</span>. Intro.",
        "Despliega la flecha de <span class='mono'>Botella</span>: verás <span class='mono'>Botella[0]</span> a "
        "<span class='mono'>Botella[3]</span>, cada una con los 8 campos del UDT.",
        "Añade el resto de filas.",
    ) + _tabla_db(D.DB_FIFO), 3))

    p3.append(paso("p-dbtiempos", "Crear DB_Tiempos (DB3)", lista(
        "Agregar nuevo bloque › Bloque de datos. Nombre <span class='mono'>DB_Tiempos</span>, número <span class='mono'>3</span>.",
        "Una fila por temporizador o contador. En <b>Tipo de datos</b> escribe exactamente "
        "<span class='mono'>TON_TIME</span>, <span class='mono'>TP_TIME</span> o <span class='mono'>CTU_INT</span>.",
    ) + tabla(["Nombre", "Tipo de datos", "Se usa en", "Para qué"],
              [(f"<span class='nm'>{n}</span>", f"<span class='ty'>{t}</span>", f, e(x))
               for n, t, _p, f, x in D.TEMPORIZADORES])
        + tip("Tener los temporizadores en un DB global evita que TIA cree un DB de instancia por cada uno."), 3))

    hmi_filas = [(f"<span class='mono'>{gg}</span>", f"<span class='nm'>{n}</span>", f"<span class='ty'>{t}</span>", e(x))
                 for gg, n, t, x in D.DB_HMI]
    p3.append(paso("p-dbhmi", "Crear DB_HMI (DB4)", lista(
        "Agregar nuevo bloque › Bloque de datos. Nombre <span class='mono'>DB_HMI</span>, número <span class='mono'>4</span>.",
        "Crea el Struct <span class='mono'>Manual</span> (fila con tipo <span class='mono'>Struct</span>) y dentro sus campos. "
        "Después, al mismo nivel que <span class='mono'>Manual</span>, el Struct <span class='mono'>Ordenes</span>.",
    ) + tabla(["Struct", "Nombre", "Tipo", "Para qué"], hmi_filas)
        + "<p>Son las órdenes que dará la pantalla. Hasta que la hagamos (parte 18) puedes probarlas desde una tabla de observación.</p>", 3))

    grupos = []
    for fila in D.DB_LINEA:
        if not grupos or grupos[-1][0] != fila[0]:
            grupos.append((fila[0], []))
        grupos[-1][1].append(fila)
    cuerpo_db = lista(
        "Agregar nuevo bloque › Bloque de datos. Nombre <span class='mono'>DB_Linea</span>, número <span class='mono'>1</span>.",
        "Cada grupo de abajo es un <b>Struct</b>: escribe su nombre en una fila con tipo <span class='mono'>Struct</span>, "
        "pulsa Intro y rellena sus campos (quedan metidos hacia dentro).",
        "Para empezar el siguiente Struct, escribe en la primera fila vacía de abajo, al nivel de los Struct.",
        "En los Struct <span class='mono'>Produccion</span> y <span class='mono'>Param</span> marca la casilla "
        "<b>Remanencia</b>. En un DB optimizado se marca en el Struct entero.",
    ) + ojo("Al crear una fila nueva, TIA copia el <b>tipo de datos de la fila de arriba</b>. Por ejemplo, debajo de "
            "<span class='mono'>Nivel_Pct</span> (Real) las filas <span class='mono'>Nivel_25</span>, <span class='mono'>Nivel_90</span> "
            "y <span class='mono'>Nivel_99</span> salen como Real y deben ser Bool. Revisa la columna <b>Tipo de datos</b> de cada fila "
            "con la tabla de la guía.") + ojo("Es el bloque más largo (unas 140 variables). Tómatelo con calma y compila al acabar cada Struct: "
            "así, si te equivocas, lo ves enseguida.")
    for gnom, filas in grupos:
        rem = " · <b>remanente</b>" if filas[0][4] else ""
        cuerpo_db += (f"<h4>Struct {e(gnom)} ({len(filas)}){rem}</h4>"
                      + _tabla_db([(n, t, v, x) for _g, n, t, v, _r, x in filas]))
    p3.append(paso("p-dblinea", "Crear DB_Linea (DB1)", cuerpo_db, 3))

    p3.append(paso("p-comp-datos", "Compilar los datos", lista(
        "Clic derecho en <span class='mono'>PLC_Linea</span> › Compilar › Software (solo cambios).",
        "Debe dar 0 errores. Los avisos de que un bloque no se usa son normales por ahora.",
    ) + ojo("Si DB_FIFO da el error <i>UDT_Botella no existe</i>, compila primero el UDT (clic derecho sobre él › Compilar) "
            "y luego el DB."), 3))
    P.append((3, "Tipos y bloques de datos", p3,
              "Todo lo que no es una entrada o salida física: estados, zonas, alarmas, parámetros, el FIFO, los temporizadores "
              "y las órdenes de la HMI."))

    # =====================================================================
    # PARTE 4 · KOP
    # =====================================================================
    p4 = []
    leyenda = tabla(["Dibujo", "Instrucción en TIA", "Dónde está"], [
        ("<span class='mono'>──| |──</span>", "Contacto normalmente abierto", "Barra de favoritos"),
        ("<span class='mono'>──|/|──</span>", "Contacto normalmente cerrado", "Barra de favoritos"),
        ("<span class='mono'>──|P|──</span> / <span class='mono'>──|N|──</span>",
         "Flanco positivo / negativo. Abajo lleva su bit de memoria", "Operaciones lógicas con bits"),
        ("<span class='mono'>──( )</span>", "Asignación (bobina)", "Barra de favoritos"),
        ("<span class='mono'>──(S)</span> / <span class='mono'>──(R)</span>", "Activar / desactivar salida (memoriza)", "Operaciones lógicas con bits"),
        ("<span class='mono'>──| &gt;= |──</span>", "Comparador. Arriba el valor 1, abajo el valor 2 y el tipo entre corchetes", "Comparación"),
        ("Caja MOVE", "Copia IN en OUT1, OUT2… No tiene tipo: lo toma de las variables", "Transferencia"),
        ("Caja ADD, SUB, MUL, DIV", "Operar. Se elige el tipo (Int, DInt, Real) en <span class='mono'>???</span>", "Matemáticas"),
        ("Caja NORM_X, SCALE_X", "Escalado de analógicas", "Conversión"),
        ("Caja TON, TP", "Temporizadores", "Temporizadores"),
        ("Caja CTU", "Contador ascendente", "Contadores"),
    ])
    p4.append(paso("p-kop", "Cómo leer los dibujos", (
        "<p>La barra gruesa <span class='mono'>┃</span> de la izquierda es la alimentación. Lo que va entre comillas es una "
        "variable global (<span class='mono'>\"PB_Marcha\"</span>, <span class='mono'>\"DB_Linea\".Modo.Auto</span>) y lo que "
        "empieza por <span class='mono'>#</span> es una variable Temp del propio bloque.</p>"
        "<p>Los segmentos largos no caben en la pantalla: desliza el dibujo hacia la derecha para verlo entero.</p>" + leyenda)
    , 4))
    p4.append(paso("p-maniobras", "Las maniobras que vas a repetir", lista(
        "<b>Poner un contacto o bobina</b>: arrástralo desde la barra de favoritos (encima del editor) a la línea del segmento.",
        "<b>Poner el operando</b>: doble clic en <span class='mono'>&lt;??.?&gt;</span> y escribe el nombre. "
        "Al escribir <span class='mono'>\"DB_Linea\".</span> TIA te ofrece la lista de campos.",
        "<b>Rama en paralelo (OR)</b>: selecciona el punto de inicio, pulsa <b>Abrir rama</b> (flecha hacia abajo en favoritos), "
        "pon los contactos y arrastra el final de la rama hasta la línea principal.",
        "<b>Varias bobinas a la salida</b>: igual, abre una rama justo antes de la primera bobina y pon la segunda debajo.",
        "<b>Caja</b>: búscala en el panel <b>Instrucciones</b> (derecha) y arrástrala. En ADD, SUB, MUL, DIV, los comparadores "
        "y el CTU haz clic en <span class='mono'>???</span> para elegir el tipo que indica el dibujo (Int, DInt, Real, Time). "
        "<b>MOVE no tiene tipo</b>: rellena IN y OUT y TIA lo deduce de las variables.",
        "<b>Escribir bits</b>: para poner un Bool a 1 o a 0 usamos bobinas <span class='mono'>(S)</span> y "
        "<span class='mono'>(R)</span>, nunca MOVE.",
        "<b>Más salidas en un MOVE</b>: clic en la estrella amarilla junto a <span class='mono'>OUT1</span>.",
        "<b>Temporizador o contador</b>: al soltar la caja TON, TP o CTU, TIA abre <b>Opciones de llamada</b>. Pulsa "
        "<b>Cancelar</b>. Encima de la caja aparece <span class='mono'>&lt;???&gt;</span>: escribe ahí la instancia de "
        "DB_Tiempos que indica el dibujo (por ejemplo <span class='mono'>\"DB_Tiempos\".T_Relleno_Tanque</span>).",
        "<b>Título del segmento</b>: escríbelo siempre, el mismo que en la guía.",
    ) + tip("Cuando algo no funcione, abre el bloque y pulsa <b>Activar/desactivar observación</b> (las gafas). "
            "Verás en verde por dónde pasa la corriente."), 4))
    P.append((4, "Cómo se dibuja en KOP", p4,
              "Léelo una vez antes de empezar a programar. Todos los dibujos de la guía siguen estas reglas."))

    # =====================================================================
    # PARTE 5 · OB100 y OB30
    # =====================================================================
    p5 = []
    s = Segmentos()
    ob100 = crear_bloque("Bloque de organización (OB) › Startup", "OB100_Arranque", 100) + (
        "<p>Se ejecuta una sola vez al pasar la CPU a RUN. Deja la línea parada, con la válvula cerrada, "
        "el FIFO vacío y esperando REARME.</p>"
        + s("Arranque seguro: rearme pendiente", kop([S(MOD + "Rearme_Pendiente"), S(MOD + "Parada_Seguridad")],
                                                      serie=[c(g("AlwaysTRUE"))]),
            "<span class='mono'>AlwaysTRUE</span> es la marca de sistema M1.2: vale siempre 1, así que el segmento se "
            "ejecuta siempre. Las dos bobinas en paralelo se hacen abriendo una rama antes de la primera.")
        + s("Arranque seguro: todo parado", kop([R(g("VS_Valvula_Seguridad")), R(LLE + "En_Curso"),
                                                R(MOD + "Ciclo_Marcha"), R(MOD + "Fin_Ciclo")], serie=[c(g("AlwaysTRUE"))]))
        + s("FIFO vacío: punteros a 0", kop(mv("0", "Int", [FIFO + "Ptr_Entrada", FIFO + "Idx_Z1", FIFO + "Idx_Z2",
                                                            FIFO + "Idx_Z3", FIFO + "Idx_Z4", FIFO + "N_Botellas"])))
        + s("FIFO vacío: primera botella con ID 1", kop(mv("1", "Int", [FIFO + "Siguiente_ID"])))
        + s("FIFO vacío: posiciones libres", kop([R(f'"DB_FIFO".Botella[{i}].Activa') for i in range(4)],
                                                 serie=[c(g("AlwaysTRUE"))]),
            "Así se escribe un campo de un elemento del array: <span class='mono'>Botella[2].Activa</span>.")
        + s("Zonas vacías", kop([R(f'"DB_Linea".Zonas.Z{i}') for i in range(1, 5)], serie=[c(g("AlwaysTRUE"))]))
    )
    p5.append(paso("p-ob100", "OB100 · Arranque seguro", ob100, 5))

    s = Segmentos()
    ob30 = crear_bloque("Bloque de organización (OB) › Cyclic interrupt", "OB30_Ciclo_100ms", 30,
                        [("Litros_100ms", "Real", "Litros que entran en 100 ms.")],
                        ["En <b>Tiempo de ciclo</b> escribe <span class='mono'>100000</span> µs (100 ms)."]) + (
        "<p>El OB1 no tarda siempre lo mismo. El OB30 se ejecuta exactamente cada 100 ms: nos sirve de reloj para "
        "los 40 s de cada botella y para sumar los litros del llenado.</p>"
        + s("Reloj base de 100 ms", kop(mat("ADD", "DInt", '"DB_Linea".Reloj.Base_100ms', "1", '"DB_Linea".Reloj.Base_100ms')),
            "Cada 100 ms suma 1: cuenta décimas de segundo. 40 s son 400.")
        + s("Litros que entran en 100 ms", kop(mat("DIV", "Real", LLE + "Caudal_Lmin", "600.0", "#Litros_100ms"),
                                             serie=[c(LLE + "En_Curso")]),
            "El caudal está en litros por minuto. Un minuto tiene 600 trozos de 100 ms.")
        + s("Acumular el volumen de la botella", kop(mat("ADD", "Real", LLE + "Volumen_L", "#Litros_100ms", LLE + "Volumen_L"),
                                                   serie=[c(LLE + "En_Curso")]),
            "FC5 pone el volumen a 0 al empezar cada botella.")
    )
    p5.append(paso("p-ob30", "OB30 · Reloj de 100 ms y litros", ob30, 5))
    P.append((5, "Arranque y reloj: OB100 y OB30", p5,
              "Dos bloques de organización pequeños que el sistema llama solo: uno al arrancar y otro cada 100 ms."))
    return P
