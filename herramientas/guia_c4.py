# -*- coding: utf-8 -*-
"""Guía completa · Partes 17 y 18: Factory I/O y pantalla HMI."""
import datos_variables as D
from guia_comun import e, lista, m, ojo, ruta, tabla, tip


def partes(G):
    paso = G.paso
    P = []

    # =====================================================================
    # PARTE 17 · Factory I/O
    # =====================================================================
    p = []
    p.append(paso("fio-escena", "Crear la escena", lista(
        "Abre Factory I/O y crea una escena vacía. Guárdala como <span class='mono'>Linea_Llenado</span>.",
        "Trabaja en modo edición (la simulación en pausa). Las piezas están en la paleta de la derecha: arrástralas al suelo.",
        "Usa la cuadrícula: las cintas encajan una detrás de otra. Con la pieza seleccionada puedes girarla.",
    ) + ojo("Factory I/O cambia algunos nombres entre versiones. Si una pieza no se llama exactamente así, busca la más parecida "
            "por su función."), 17))

    piezas = tabla(["Qué es en la línea", "Pieza de Factory I/O", "Dónde va"], [
        ("C1 (generador → detección)", "Belt Conveyor 4 m", "Primera cinta de la línea"),
        ("C2 (llenado)", "Belt Conveyor 2 m", "Seguida de C1"),
        ("C3 (TAP-01)", "Belt Conveyor 2 m", "Seguida de C2"),
        ("C4 (empujador)", "Belt Conveyor 2 m", "Seguida de C3"),
        ("C5 (transversal)", "Cinta que pueda girar en los dos sentidos", "Al final de C4, en perpendicular"),
        ("Generador de botellas", "Emitter con Small Box y Large Box", "Al principio de C1"),
        ("Sensores de altura", "2 × Diffuse Sensor", "Sobre C1: uno bajo (ve las dos cajas) y uno alto (solo la grande)"),
        ("Sensores de posición", "4 × Diffuse Sensor", "Final de C2, mitad de C3, frente al empujador en C4 y entrada de C5"),
        ("Tanque", "Tank", "Encima del final de C2: la descarga cae sobre la botella"),
        ("TAP-01", "Pick & Place (eje Z)", "Encima del sensor de C3"),
        ("Empujador", "Pusher", "Al lado de C4, frente al sensor de rechazo"),
        ("Cajas (malas, 0,5 L y 2 L)", "Pallet + Emitter (pallet) + Remover", "Al otro lado del empujador y en los dos extremos de C5"),
        ("Sensores de caja", "Retroreflective Sensor (entrada) + Diffuse Sensor (presencia)", "Encima y al lado de cada palé"),
        ("Cuadro", "Start, Stop, Emergency Stop, Reset, Selector Switch, Push Button", "Un panel frente a la línea"),
        ("Pruebas", "2 × Selector Switch", "En el mismo panel: fallo de llenado y nivel 99 %"),
        ("Lámparas de fase", "7 × Stack Light (verde, amarillo, rojo)", "Una por fase, cerca de cada estación"),
        ("Baliza y sirena", "Warning Light + Alarm Siren", "Encima del cuadro"),
    ])
    p.append(paso("fio-piezas", "Colocar las piezas", piezas + tip(
        "Las botellas son cajas: la pequeña es la de 0,5 L y la grande la de 2 L. Coloca el sensor alto a una altura que la caja "
        "pequeña no tape.")
        + tip("Cada caja de botellas es un palé. El Remover borra el palé con lo que tenga encima (caja llena) y el Emitter pone "
              "uno nuevo (caja vacía)."), 17))

    filas = [(f"<span class='mono'>{a}</span>", f"<span class='nm'>{e(n)}</span>", e(f))
             for a, n, _t, _c, _x, f in D.ENTRADAS_DIGITALES + D.SALIDAS_DIGITALES + D.ANALOGICAS if n and f]
    p.append(paso("fio-driver", "Configurar el driver y asignar las señales", lista(
        f"En Factory I/O: {ruta('Archivo', 'Drivers')} y elige <b>Siemens S7-PLCSIM</b>.",
        "Pulsa <b>Configuración</b>: modelo <b>S7-1200</b>. Entradas digitales desde el byte 0 (4 bytes, I0 a I3), "
        "salidas digitales desde el byte 0 (6 bytes, Q0 a Q5), 2 entradas de registro desde IW64 y 2 salidas de registro desde QW64.",
        "Vuelve atrás: verás a la izquierda las señales de la escena y a la derecha las direcciones del PLC.",
        "Arrastra cada señal de la escena a su dirección según esta tabla.",
    ) + tabla(["Dirección", "Variable del PLC", "Señal de Factory I/O"], filas)
        + ojo("Las lámparas: el verde, el amarillo y el rojo de cada Stack Light van a las tres lámparas de su fase "
              "(L1_… en la fase 1, L2_… en la fase 2…)."), 17))

    p.append(paso("fio-arranque", "Primer arranque", lista(
        "En TIA: carga el programa en PLCSIM y deja la CPU en RUN.",
        "En Factory I/O pulsa <b>Play</b> y en la ventana del driver <b>Conectar</b>. Debe ponerse en verde.",
        "Desenclava la seta, pon el selector en AUTO y pulsa REARME: la baliza se apaga y la bomba llena el tanque si hace falta.",
        "Las tres cajas aparecen solas (se cambian porque faltan).",
        "Pulsa MARCHA: sale la primera botella.",
    ) + ojo("Si algo se mueve al revés (por ejemplo C5), no toques el programa: en Factory I/O intercambia las dos señales."), 17))

    p.append(paso("fio-ajustes", "Calibrar y ajustar", lista(
        f"<b>Caudal</b>: mira en Factory I/O qué caudal da el caudalímetro con 10 V y escríbelo en {m('Param.Caudal_Max_Lmin')}.",
        f"<b>Apertura de llenado</b>: si las botellas se llenan demasiado rápido para verlo, baja {m('Param.Apertura_Llenado')} "
        "(13824 = 50 %).",
        "<b>30 segundos por botella</b>: cronometra una botella de principio a fin. Si tarda mucho más, acorta las cintas o baja "
        f"{m('Param.T_Taponado')}; si sale alguna alarma de tiempo, revisa dónde se queda parada.",
        f"<b>40 s</b>: si subiste {m('Param.Limite_Botella_100ms')} para las pruebas, vuelve a ponerlo a 400.",
        "<b>Botellas malas</b>: activa el selector de fallo de llenado y comprueba que van a su caja y que a la tercera seguida "
        "salta la alarma roja A303.",
        "<b>99 %</b>: activa el selector de prueba del 99 % y comprueba que la bomba sigue hasta que salta la emergencia.",
    ), 17))
    P.append((17, "Factory I/O", p,
              "Montamos la escena, la conectamos con PLCSIM y ajustamos los parámetros para que la línea funcione como la real."))

    # =====================================================================
    # PARTE 18 · HMI
    # =====================================================================
    p = []
    p.append(paso("hmi-que", "Qué es una HMI y qué vamos a hacer", (
        "<p>La HMI es la pantalla táctil del operario. Lee y escribe variables del PLC: muestra el estado de la línea y permite "
        "dar órdenes. Haremos 4 imágenes:</p>"
        + tabla(["Imagen", "Para qué"], [
            ("<b>Inicio</b>", "Sinóptico: nivel del tanque, estado de la línea, lámparas de fase y botellas en cada caja."),
            ("<b>Manual</b>", "Botones para mover cintas, TAP-01, empujador y cajas. Solo aparecen en MANUAL."),
            ("<b>Alarmas</b>", "Las 23 alarmas con su color."),
            ("<b>Producción</b>", "Contadores totales, parámetros y botón para poner la producción a 0."),
        ])), 18))

    p.append(paso("hmi-anadir", "Añadir la pantalla", lista(
        "En el árbol: " + ruta("Agregar dispositivo", "HMI", "SIMATIC Basic Panel", '7" Display', "KTP700 Basic",
                                "6AV2 123-2GB03-0AX0") + ". Versión 15.0. Aceptar.",
        "Se abre el asistente. En <b>Conexiones de PLC</b> elige <span class='mono'>PLC_Linea</span>.",
        "En <b>Avisos</b> desmarca todo. En <b>Imágenes</b> deja solo la imagen raíz. En <b>Imágenes de sistema</b> y "
        "<b>Botones</b> no marques nada. <b>Finalizar</b>.",
        "Abre <b>Dispositivos y redes</b>: la CPU y la pantalla deben estar unidas por una línea verde (PN/IE_1). "
        "Si no, arrastra del puerto verde de una al de la otra.",
    ), 18))

    p.append(paso("hmi-imagenes", "Crear las 4 imágenes y la navegación", lista(
        f"En {ruta('HMI_1', 'Imágenes')}: cambia el nombre de la imagen raíz a <span class='mono'>Inicio</span> y añade "
        "<span class='mono'>Manual</span>, <span class='mono'>Alarmas</span> y <span class='mono'>Produccion</span>.",
        "En <span class='mono'>Inicio</span> pon abajo 4 botones: Inicio, Manual, Alarmas y Producción.",
        f"Selecciona cada botón: {ruta('Propiedades', 'Eventos', 'Hacer clic')} › <b>ActivarImagen</b> › elige la imagen.",
        "Selecciona los 4 botones, cópialos y pégalos en las otras 3 imágenes.",
    ), 18))

    p.append(paso("hmi-inicio", "Imagen Inicio", lista(
        f"<b>Tanque</b>: de Elementos, arrastra una <b>Barra</b>. Variable de proceso {m('DB_Linea.Tanque.Nivel_Pct')}, "
        "mínimo 0 y máximo 100. Al lado, un <b>Campo E/S</b> en modo <b>Salida</b> con la misma variable.",
        "<b>Estado de la línea</b>: 4 círculos con texto al lado: En marcha, Terminando, Rearme pendiente y Parada de seguridad. "
        f"En cada círculo: {ruta('Propiedades', 'Animaciones', 'Apariencia')}, variable {m('DB_Linea.Modo.Ciclo_Marcha')} "
        "(y las otras), valor 0 = gris y 1 = verde, naranja o rojo.",
        "<b>Lámparas de fase</b>: una fila por fase con 3 círculos, animados con las salidas "
        f"{m('L1_Tanque_Verde')}, {m('L1_Tanque_Naranja')}, {m('L1_Tanque_Rojo')}… Haz una fila, cópiala y cambia las variables.",
        f"<b>Botellas en la línea y en cada caja</b>: Campos E/S de salida con {m('DB_FIFO.N_Botellas')}, "
        f"{m('DB_Linea.Cajas.Cnt_Malas')}, {m('DB_Linea.Cajas.Cnt_05L')} y {m('DB_Linea.Cajas.Cnt_2L')}.",
    ) + tip("Las variables del PLC se eligen con el botón <b>…</b> del campo Variable: navega por PLC_Linea › Bloques de programa "
            "› DB_Linea."), 18))

    botones = tabla(["Botón", "Pulsar → ActivarBit", "Soltar → DesactivarBit"],
                    [(e(x), f"<span class='mono'>DB_HMI.{gg}.{n}</span>", f"<span class='mono'>DB_HMI.{gg}.{n}</span>")
                     for gg, n, _t, x in D.DB_HMI if gg == "Manual"])
    p.append(paso("hmi-manual", "Imagen Manual", lista(
        "Pon un texto arriba: <i>Solo con el selector en MANUAL y la seta sin pulsar</i>.",
        "Pon un botón por cada orden de la tabla.",
        f"En cada botón: {ruta('Eventos', 'Pulsar')} › <b>ActivarBit</b> con su variable, y {ruta('Eventos', 'Soltar')} › "
        "<b>DesactivarBit</b> con la misma. Así el movimiento dura mientras mantienes el dedo.",
        f"Selecciona todos los botones: {ruta('Animaciones', 'Visibilidad')}, variable {m('DB_Linea.Modo.Manual_OK')}, "
        "visible de 1 a 1. Fuera de MANUAL desaparecen.",
    ) + botones + ojo("Los enclavamientos están en el PLC (parte 11 a 13): aunque pulses, C3 no se mueve con TAP-01 abajo "
                      "ni C4 con el empujador fuera."), 18))

    alarmas = tabla(["Alarma", "Variable", "Color con valor 1"],
                    [(f"<b>{a}</b> {e(t)}", f"<span class='mono'>DB_Linea.Alarmas.{a}</span>",
                      "rojo" if col == "R" else "naranja") for a, _f, col, t, *_ in D.ALARMAS])
    p.append(paso("hmi-alarmas", "Imagen Alarmas", lista(
        "Una fila por alarma: un círculo y un texto con su código y descripción.",
        f"Círculo: {ruta('Animaciones', 'Apariencia')} con su variable. 0 = gris, 1 = rojo o naranja.",
        "Haz la primera fila, cópiala 22 veces y cambia texto y variable.",
    ) + alarmas + tip("Más adelante, si quieres, se puede pasar a avisos de WinCC con historial. Para el TFC, esta imagen ya "
                      "muestra todas las alarmas por fase."), 18))

    p.append(paso("hmi-produccion", "Imagen Producción", lista(
        "Campos E/S de <b>salida</b> con los 6 totales de <span class='mono'>DB_Linea.Produccion</span>.",
        "Campos E/S de <b>entrada/salida</b> con los parámetros que el operario puede cambiar: "
        f"{m('Param.Max_Botellas')}, {m('Param.Pct_Llenado')}, {m('Param.Caudal_Max_Lmin')}, {m('Param.Cap_Caja_Buenas')} "
        f"y {m('Param.Cap_Caja_Malas')}.",
        f"Un botón <b>Poner a 0</b>: Pulsar → ActivarBit {m('DB_HMI.Ordenes.Reset_Produccion')}, Soltar → DesactivarBit. "
        "El PLC solo lo hace con el ciclo parado.",
    ), 18))

    p.append(paso("hmi-simular", "Compilar y simular la pantalla", lista(
        "Clic derecho en <span class='mono'>HMI_1</span> › Compilar › Software. 0 errores.",
        "Con PLCSIM en RUN, selecciona <span class='mono'>HMI_1</span> y pulsa <b>Iniciar simulación</b>.",
        "Se abre la pantalla en el PC. Comprueba que el nivel del tanque se mueve y que los botones cambian de imagen.",
    ) + ojo("Si los campos muestran <span class='mono'>####</span>, la pantalla no conecta con PLCSIM. En Windows: "
            "Panel de control › <b>Ajustar interfaz PG/PC</b>, punto de acceso <span class='mono'>S7ONLINE</span>, y elige la "
            "interfaz de PLCSIM. Luego vuelve a iniciar la simulación de la HMI."), 18))
    P.append((18, "Pantalla HMI", p,
              "Una pantalla KTP700 Basic con 4 imágenes: sinóptico, manual, alarmas y producción."))
    return P
