# -*- coding: utf-8 -*-
"""Guía completa · Partes 6 a 10: FC1 Entradas, FC2 Modos y seguridad, FC3 Tanque, FC4 Generador, FC5 Llenado."""
from guia_comun import (ALM, EMG, FIFO, FLA, GEN, HMI, LLE, MOD, NIV, PAR, PRO, R, S, TAP, TIM, ZON,  # noqa: F401
                        Segmentos, b, bot, c, cmp_, crear_bloque, g, kop, lista, llamada, m, mat, mv, nc, neg,
                        ojo, pos, tabla, tip, ton_, tp_)
from kop import caja


def ob1(n, fc, titulo):
    return ("<p>Abre <span class='mono'>Main [OB1]</span>, añade el segmento " + str(n) + " y arrastra "
            f"<span class='mono'>{fc}</span> desde el árbol. Título: <span class='mono'>{titulo}</span>.</p>"
            "<div class='kopw'><pre class='kop'>" + __import__("html").escape(kop(llamada(fc))) + "</pre></div>")


def pruebas(filas, intro=""):
    return (f"<p>{intro}</p>" if intro else "") + tabla(["#", "Qué haces", "Qué debes ver"],
                                                         [(str(i + 1), a, bb) for i, (a, bb) in enumerate(filas)])


def partes(G):
    paso = G.paso
    P = []

    # =====================================================================
    # PARTE 6 · FC1 Entradas
    # =====================================================================
    p = []
    s = Segmentos()
    p.append(paso("fc1-crear", "Crear FC1 · FC_Entradas", crear_bloque(
        "Función (FC)", "FC_Entradas", 1,
        [("Nivel_Norm", "Real", "Nivel en tanto por uno (0.0 a 1.0)."),
         ("Caudal_Norm", "Real", "Caudal en tanto por uno (0.0 a 1.0)."),
         ("Sim_Abajo", "Bool", "Final ABAJO de TAP-01 simulado."),
         ("Sim_Arriba", "Bool", "Final ARRIBA de TAP-01 simulado.")])
        + "<p>La entrada analógica da un número de 0 a 27648. <b>NORM_X</b> lo pasa a 0.0…1.0 y <b>SCALE_X</b> a la unidad "
          "que queremos (% o l/min).</p>", 6))
    seg_an = (
        s("Nivel del tanque: normalizar", kop(caja("NORM_X", "Int to Real",
          [("0", "MIN"), (g("AI_Nivel_Tanque"), "VALUE"), ("27648", "MAX")], [("OUT", "#Nivel_Norm")])),
          "Elige los tipos en <span class='mono'>???</span>: primero Int (lo que entra) y luego Real (lo que sale).")
        + s("Nivel del tanque: escalar a %", kop(caja("SCALE_X", "Real to Real",
            [("0.0", "MIN"), ("#Nivel_Norm", "VALUE"), ("100.0", "MAX")], [("OUT", NIV + "Nivel_Pct")])),
            "Si IW64 vale 13824 (la mitad), Nivel_Pct vale 50.0.")
        + s("Caudalímetro: normalizar", kop(caja("NORM_X", "Int to Real",
            [("0", "MIN"), (g("AI_Caudalimetro"), "VALUE"), ("27648", "MAX")], [("OUT", "#Caudal_Norm")])))
        + s("Caudalímetro: escalar a l/min", kop(caja("SCALE_X", "Real to Real",
            [("0.0", "MIN"), ("#Caudal_Norm", "VALUE"), (PAR + "Caudal_Max_Lmin", "MAX")], [("OUT", LLE + "Caudal_Lmin")])),
            "El máximo es un parámetro porque lo calibraremos con Factory I/O.")
    )
    p.append(paso("fc1-an", "Segmentos 1 a 4 · Analógicas", seg_an, 6))

    def nivel(pct, sensor):
        return kop([b(NIV + f"Nivel_{pct}")], paralelo=[
            [c(PAR + "Simulacion_FIO"), cmp_(NIV + "Nivel_Pct", ">=", f"{pct}.0", "Real")],
            [nc(PAR + "Simulacion_FIO"), c(g(sensor))]])
    seg_niv = (
        s("Sensor de nivel 25 %", nivel(25, "S_Tanque_25"),
          "<p>Rama de arriba: en simulación, el sensor se calcula comparando el nivel con 25.0. Rama de abajo: en una "
          "instalación real se copia el sensor I3.3. El resto del programa usa siempre "
          "<span class='mono'>\"DB_Linea\".Tanque.Nivel_25</span>.</p>"
          "<p><b>Si TIA dice que un Real no concuerda con Bool en la bobina</b>: en DB_Linea, Nivel_25, Nivel_90 y Nivel_99 "
          "se quedaron como Real (TIA copia el tipo de Nivel_Pct, la fila de arriba). Cámbialos a Bool y compila DB_Linea.</p>")
        + s("Sensor de nivel 90 %", nivel(90, "S_Tanque_90"))
        + s("Sensor de nivel 99 %", nivel(99, "S_Tanque_99"), "Este es el que dispara la emergencia del 99 %.")
        + tip("Haz el segmento 5, cópialo (Ctrl+C, Ctrl+V) y en la copia cambia solo el número y el sensor.")
    )
    p.append(paso("fc1-niv", "Segmentos 5 a 7 · Sensores de nivel", seg_niv, 6))

    seg_tap = (
        "<p>Factory I/O no da finales de carrera para el cabezal de TAP-01. En simulación los fabricamos: el cabezal "
        "\"llega abajo\" 1 s después de mandarlo bajar y \"llega arriba\" 1 s después de mandarlo subir.</p>"
        + tip("En la salida Q del TON: doble clic en los <span class='mono'>...</span> de la derecha de Q y escribe "
              "<span class='mono'>Sim_Abajo</span>. TIA le pone el <span class='mono'>#</span> solo porque es una variable Temp "
              "de este bloque. Comprueba en la interfaz que <span class='mono'>Sim_Abajo</span> y <span class='mono'>Sim_Arriba</span> "
              "son <b>Bool</b>: al estar debajo de dos Real, TIA las crea como Real.")
        + s("TAP-01 simulado: llega abajo", kop(ton_("T_Sim_TAP01_Abajo", PAR + "T_Sim_TAP01", "#Sim_Abajo"),
                                              serie=[c(g("TAP01_Bajar"))]))
        + s("TAP-01 simulado: llega arriba", kop(ton_("T_Sim_TAP01_Arriba", PAR + "T_Sim_TAP01", "#Sim_Arriba"),
                                               serie=[nc(g("TAP01_Bajar"))]))
        + s("TAP-01: final ABAJO", kop([b(TAP + "Abajo")], paralelo=[
            [c(PAR + "Simulacion_FIO"), c("#Sim_Abajo")], [nc(PAR + "Simulacion_FIO"), c(g("S_TAP01_Abajo"))]]))
        + s("TAP-01: final ARRIBA", kop([b(TAP + "Arriba")], paralelo=[
            [c(PAR + "Simulacion_FIO"), c("#Sim_Arriba")], [nc(PAR + "Simulacion_FIO"), c(g("S_TAP01_Arriba"))]]))
    )
    p.append(paso("fc1-tap", "Segmentos 8 a 11 · Finales de carrera de TAP-01", seg_tap, 6))
    p.append(paso("fc1-ob1", "Llamar a FC1 desde el OB1", ob1(1, "FC_Entradas", "FC1 · Entradas"), 6))
    p.append(paso("fc1-prueba", "Probar FC1", (
        "<p>Compila, pulsa <b>Iniciar simulación</b>, carga en PLCSIM (interfaz PN/IE, <b>Iniciar búsqueda</b>, "
        "<b>Cargar</b>, <b>Arrancar todos</b>) y abre en PLCSIM la <b>vista del proyecto › Tablas SIM</b>. "
        "En TIA abre DB_Linea y pulsa <b>Observar todo</b>.</p>"
        + pruebas([
            ("AI_Nivel_Tanque = 13824", "Nivel_Pct = 50.0 · Nivel_25 = TRUE · Nivel_90 = FALSE"),
            ("AI_Nivel_Tanque = 27400", "Nivel_90 = TRUE · Nivel_99 = TRUE"),
            ("AI_Caudalimetro = 27648", "Caudal_Lmin = 10.0"),
            ("Espera 1 s sin tocar nada", "Taponado.Arriba = TRUE (simulado)"),
        ]))
    , 6))
    P.append((6, "FC1 · Entradas", p,
              "Prepara las señales que usa el resto del programa: nivel y caudal en unidades reales, y los sensores de nivel "
              "y de TAP-01, reales o simulados."))

    # =====================================================================
    # PARTE 7 · FC2 Modos y seguridad
    # =====================================================================
    p = []
    s = Segmentos()
    estados = tabla(["Estado", "Cómo lo ve el programa", "Cómo se sale"], [
        ("<b>Parada de seguridad</b>", m("Hay_Causa = 1"), "Quitar la causa"),
        ("<b>Rearme pendiente</b>", m("Hay_Causa = 0 y Rearme_Pendiente = 1"), "Pulsar REARME"),
        ("<b>Lista</b>", m("Parada_Seguridad = 0 y Ciclo_Marcha = 0"), "Pulsar MARCHA"),
        ("<b>En marcha</b>", m("Ciclo_Marcha = 1 y Fin_Ciclo = 0"), "PARO → Terminando"),
        ("<b>Terminando</b>", m("Ciclo_Marcha = 1 y Fin_Ciclo = 1"), "Se vacía la línea → Lista. MARCHA → En marcha"),
    ])
    p.append(paso("fc2-idea", "Cómo funciona la seguridad", (
        lista("Cada <b>causa</b> (seta, 99 %, 40 s, MANUAL, fallo rojo) vale 1 solo mientras existe.",
              f"La memoria está en {m('Modo.Rearme_Pendiente')}: se activa con cualquier causa y solo se borra con REARME "
              "cuando ya no queda ninguna.",
              f"{m('Modo.Parada_Seguridad')} = hay causa o falta el rearme. Todas las FC lo miran.",
              "Con la parada de seguridad el FIFO se vacía (FC4): antes de REARME hay que retirar a mano las botellas de las cintas.",
              ordenada=False)
        + estados)
    , 7))
    p.append(paso("fc2-crear", "Crear FC2 · FC_Modos_Seguridad", crear_bloque("Función (FC)", "FC_Modos_Seguridad", 2), 7))
    txt = (
        s("Modo AUTO", kop([b(MOD + "Auto")], serie=[c(g("SEL_Auto"))]))
        + s("Causa: seta pulsada", kop([b(EMG + "Seta")], serie=[nc(g("SETA_Emergencia"))]),
            "La seta es NC: pulsada vale 0. Con el contacto cerrado <span class='mono'>|/|</span> obtenemos 1 cuando está pulsada "
            "o si se corta el cable.")
        + s("Causa: tanque al 99 %", kop([b(EMG + "Nivel_99")], serie=[c(NIV + "Nivel_99")]))
        + s("Causa: modo MANUAL", kop([b(EMG + "Manual")], serie=[nc(g("SEL_Auto"))]))
        + s("Manual permitido", kop([b(MOD + "Manual_OK")], serie=[c(EMG + "Manual"), nc(EMG + "Seta")]),
            "Los movimientos manuales de la HMI solo se permiten en MANUAL y con la seta sin pulsar.")
        + s("Resumen de causas", kop([b(EMG + "Hay_Causa")], paralelo=[
            [c(EMG + "Seta")], [c(EMG + "Nivel_99")], [c(EMG + "Tiempo_40s")], [c(EMG + "Manual")], [c(EMG + "Fallo_Equipo")]]),
            "Tiempo_40s la escribe FC9 y Fallo_Equipo FC10. Hasta que existan valen 0.")
    )
    p.append(paso("fc2-g1", "Segmentos 1 a 6 · Modo y causas", txt, 7))
    txt = (
        s("Pulso de MARCHA", kop([b(FLA + "Marcha_Pulso")], serie=[pos(g("PB_Marcha"), FLA + "Marcha_FM")]),
          "El contacto |P| da 1 un solo ciclo cuando la entrada pasa de 0 a 1. Debajo lleva su bit de memoria, que no se usa "
          "en ningún otro sitio.")
        + s("Pulso de REARME", kop([b(FLA + "Rearme_Pulso")], serie=[pos(g("PB_Rearme"), FLA + "Rearme_FM")]))
        + s("Rearme pendiente: se activa con cualquier causa", kop([S(MOD + "Rearme_Pendiente")], serie=[c(EMG + "Hay_Causa")]))
        + s("Rearme pendiente: REARME lo borra si no queda ninguna causa",
            kop([R(MOD + "Rearme_Pendiente")], serie=[c(FLA + "Rearme_Pulso"), nc(EMG + "Hay_Causa")]))
        + s("Parada de seguridad", kop([b(MOD + "Parada_Seguridad")], paralelo=[[c(EMG + "Hay_Causa")], [c(MOD + "Rearme_Pendiente")]]),
            "La variable que miran todas las FC: si vale 1, nada se mueve en automático.")
    )
    p.append(paso("fc2-g2", "Segmentos 7 a 11 · Pulsos, rearme y parada", txt, 7))
    txt = (
        s("Sirena: REARME la silencia", kop([R(EMG + "Memo_Sirena")], serie=[c(FLA + "Rearme_Pulso")]))
        + s("Emergencia nueva: sirena y baliza", kop([S(EMG + "Memo_Sirena"), S(EMG + "Memo_Baliza")], paralelo=[
            [pos(EMG + "Seta", FLA + "Seta_FM")], [pos(EMG + "Nivel_99", FLA + "Nivel99_FM")],
            [pos(EMG + "Tiempo_40s", FLA + "T40_FM")], [pos(EMG + "Fallo_Equipo", FLA + "Fallo_FM")]]),
            "Se disparan cuando aparece una causa. MANUAL no está: no hace sonar la sirena. Este segmento va después del "
            "anterior para que, si todo pasa en el mismo ciclo, gane la emergencia.")
        + s("Baliza: se apaga al completar el rearme", kop([R(EMG + "Memo_Baliza")], serie=[nc(MOD + "Rearme_Pendiente")]))
        + s("Salida: sirena", kop([b(g("Sirena"))], serie=[c(EMG + "Memo_Sirena")]))
        + s("Salida: baliza intermitente y prueba de lámparas", kop([b(g("Baliza_Naranja"))], paralelo=[
            [c(EMG + "Memo_Baliza"), c(g("Clock_2Hz"))], [c(g("PB_Prueba_Lamparas"))]]))
    )
    p.append(paso("fc2-g3", "Segmentos 12 a 16 · Sirena y baliza", txt, 7))
    txt = (
        s("Línea vacía", kop([b(MOD + "Linea_Vacia")], serie=[cmp_(FIFO + "N_Botellas", "==", "0", "Int")]))
        + s("MARCHA: arrancar el ciclo", kop([S(MOD + "Ciclo_Marcha"), R(MOD + "Fin_Ciclo")], serie=[
            c(FLA + "Marcha_Pulso"), c(MOD + "Auto"), nc(MOD + "Parada_Seguridad"), c(g("PB_Paro"))]),
            "PARO es NC: el contacto abierto vale 1 cuando PARO <b>no</b> está pulsado. MARCHA durante el fin de ciclo lo anula.")
        + s("PARO: pedir fin de ciclo", kop([S(MOD + "Fin_Ciclo")], serie=[nc(g("PB_Paro")), c(MOD + "Ciclo_Marcha")]),
            "PARO no para en seco: deja de pedir botellas y espera a que salgan las que hay.")
        + s("Parar el ciclo: fin de ciclo terminado o emergencia", kop([R(MOD + "Ciclo_Marcha"), R(MOD + "Fin_Ciclo")], paralelo=[
            [c(MOD + "Fin_Ciclo"), c(MOD + "Linea_Vacia")], [c(MOD + "Parada_Seguridad")]]))
        + s("Válvula de seguridad del tanque", kop([b(g("VS_Valvula_Seguridad"))], serie=[c(MOD + "Auto"), nc(MOD + "Parada_Seguridad")]),
            "Abierta en AUTO sin parada de seguridad, aunque el ciclo esté parado: así el tanque mantiene su nivel.")
    )
    p.append(paso("fc2-g4", "Segmentos 17 a 21 · Ciclo y válvula de seguridad", txt, 7))
    p.append(paso("fc2-ob1", "Llamar a FC2 desde el OB1", ob1(2, "FC_Modos_Seguridad", "FC2 · Modos y seguridad"), 7))
    p.append(paso("fc2-prueba", "Probar FC2", pruebas([
        ("Carga el programa sin tocar nada", "Sirena = 1: PLCSIM arranca con todo a 0 y eso es seta pulsada (NC)"),
        ("SETA = 1 · PB_Paro = 1 · SEL_Auto = 1 · AI_Nivel_Tanque = 13824", "Hay_Causa = 0 · Rearme_Pendiente = 1 · VS = 0"),
        ("Pulsa REARME (1 y luego 0)", "Rearme_Pendiente = 0 · Sirena = 0 · Baliza = 0 · VS = 1"),
        ("Pulsa MARCHA", "Ciclo_Marcha = 1"),
        ("Pulsa PARO (1 → 0 → 1)", "Ciclo_Marcha = 0 enseguida: no hay botellas"),
        ("MARCHA y luego SETA = 0", "Sirena = 1 · Baliza parpadea · VS = 0 · Ciclo_Marcha = 0"),
        ("Con la seta aún a 0, REARME", "Sirena = 0 · la baliza sigue · Rearme_Pendiente = 1"),
        ("SETA = 1 y REARME", "Todo limpio · VS = 1"),
        ("SEL_Auto = 0", "Parada = 1 · VS = 0 · sin sirena ni baliza · Manual_OK = 1"),
    ], "Crea en TIA una tabla de observación con las variables de Modo y Emergencia, y en la tabla SIM las entradas del cuadro."), 7))
    P.append((7, "FC2 · Modos y seguridad", p,
              "El corazón de la línea: decide si la línea puede funcionar, arranca y para el ciclo, y gestiona emergencias, "
              "rearme, sirena, baliza y válvula de seguridad."))

    # =====================================================================
    # PARTE 8 · FC3 Tanque
    # =====================================================================
    p = []
    s = Segmentos()
    p.append(paso("fc3-crear", "Crear FC3 · FC_Tanque", crear_bloque("Función (FC)", "FC_Tanque", 3), 8))
    txt = (
        s("Bomba: arranca por debajo del 25 %", kop([S(NIV + "Bomba_Marcha")], serie=[nc(NIV + "Nivel_25"), nc(MOD + "Parada_Seguridad")]))
        + s("Bomba: para al 90 % o con parada de seguridad", kop([R(NIV + "Bomba_Marcha")], paralelo=[
            [c(NIV + "Nivel_90"), nc(g("SW_Prueba_Nivel_99"))], [c(MOD + "Parada_Seguridad")]]),
            "Con el interruptor de prueba a 1 la bomba no para al 90 %: sigue hasta el 99 % y salta la emergencia.")
        + s("Salida bomba: parada", kop(mv("0", "Int", [g("AQ_Bomba_Tanque")]), paralelo=[
            [nc(NIV + "Bomba_Marcha")], [nc(g("VS_Valvula_Seguridad"))]]),
            "Si la válvula de seguridad está cerrada, la bomba no da agua: así simulamos que la válvula corta el paso.")
        + s("Salida bomba: en marcha al 100 %", kop(mv("27648", "Int", [g("AQ_Bomba_Tanque")]), serie=[
            c(NIV + "Bomba_Marcha"), c(g("VS_Valvula_Seguridad"))]))
    )
    p.append(paso("fc3-bomba", "Segmentos 1 a 4 · Bomba", txt, 8))
    txt = (
        s("A101 · nivel por debajo del 25 %", kop([b(ALM + "A101")], serie=[nc(NIV + "Nivel_25")]))
        + s("A102 · tanque al 99 %", kop([b(ALM + "A102")], serie=[c(NIV + "Nivel_99")]))
        + s("A103 · sensores de nivel incoherentes", kop(ton_("T_Incoherencia_Nivel", "T#1s", ALM + "A103"), paralelo=[
            [c(NIV + "Nivel_99"), nc(NIV + "Nivel_90")], [c(NIV + "Nivel_90"), nc(NIV + "Nivel_25")]]),
            "Un sensor alto activo sin el de debajo es imposible: sensor averiado. El TON filtra 1 s.")
        + s("A104 · la bomba no llena el tanque", kop(ton_("T_Relleno_Tanque", PAR + "T_Max_Relleno_Tanque", ALM + "A104"),
                                                     serie=[c(NIV + "Bomba_Marcha")]))
    )
    p.append(paso("fc3-alarmas", "Segmentos 5 a 8 · Alarmas del tanque", txt, 8))
    p.append(paso("fc3-ob1", "Llamar a FC3 desde el OB1", ob1(3, "FC_Tanque", "FC3 · Tanque"), 8))
    p.append(paso("fc3-prueba", "Probar FC3", pruebas([
        ("Línea rearmada en AUTO. AI_Nivel_Tanque = 5000", "Bomba_Marcha = 1 · AQ_Bomba_Tanque = 27648 · A101 = 1"),
        ("AI_Nivel_Tanque = 13824", "La bomba sigue (no ha llegado al 90 %) · A101 = 0"),
        ("AI_Nivel_Tanque = 25500", "Bomba_Marcha = 0 · AQ_Bomba_Tanque = 0"),
        ("SW_Prueba_Nivel_99 = 1 y baja el nivel a 5000 y súbelo a 26000", "La bomba no para al 90 %"),
        ("AI_Nivel_Tanque = 27400", "Emergencia: sirena, VS = 0, bomba parada"),
    ]), 8))
    P.append((8, "FC3 · Tanque", p,
              "La bomba mantiene el tanque entre el 25 % y el 90 %. Aquí están también las alarmas A101 a A104."))

    # =====================================================================
    # PARTE 9 · FC4 Generador y detección
    # =====================================================================
    p = []
    s = Segmentos()
    zonas = tabla(["Zona", "Cintas", "Qué pasa ahí", "Sensor de llegada"], [
        ("Z1", "C1 + C2", "Detección de altura y llenado", "—"),
        ("Z2", "C3", "Taponado TAP-01", m("S_Pos_Taponado")),
        ("Z3", "C4", "Empujador de malas", m("S_Pos_Rechazo")),
        ("Z4", "C5", "Cinta transversal a las cajas", m("S_Entrada_Transversal")),
    ])
    p.append(paso("fc4-idea", "Zonas y FIFO", (
        "<p>La línea se divide en 4 zonas y en cada zona cabe <b>una botella como máximo</b>. Así pueden ir hasta 4 botellas "
        "a la vez sin chocar. Cada zona sabe qué botella tiene con su índice "
        f"{m('Idx_Z1')}…{m('Idx_Z4')}, que apunta a una posición del FIFO.</p>" + zonas
        + lista("Una botella nueva solo sale si la zona 1 está libre, ha pasado el tiempo de espera, hay menos de "
                f"{m('Max_Botellas')} en la línea y su posición del FIFO está libre.",
                "Al llegar a la zona siguiente se copia el índice y se libera la anterior.",
                "Al caer en una caja se borra del FIFO.", ordenada=False)), 9))
    p.append(paso("fc4-crear", "Crear FC4 · FC_Generador_Deteccion", crear_bloque(
        "Función (FC)", "FC_Generador_Deteccion", 4, [("Espera_OK", "Bool", "Ya pasó el tiempo de espera entre botellas.")])
        + tip("Los operandos del tipo <span class='mono'>\"DB_FIFO\".Botella[\"DB_FIFO\".Ptr_Entrada].Activa</span> usan como "
              "índice otra variable. Escríbelos tal cual. Si TIA los marcara en rojo, copia el índice a una variable Temp Int "
              "con un MOVE y usa <span class='mono'>Botella[#i]</span>."), 9))
    txt = (
        s("Vaciar la línea en parada (1)", kop([R(f'"DB_FIFO".Botella[{i}].Activa') for i in range(4)],
                                              serie=[c(MOD + "Parada_Seguridad")]),
          "Con la parada de seguridad se olvidan todas las botellas. Antes de REARME hay que retirarlas de las cintas.")
        + s("Vaciar la línea en parada (2)", kop([R(ZON + f"Z{i}") for i in range(1, 5)],
                                                serie=[c(MOD + "Parada_Seguridad")]))
        + s("Vaciar la línea en parada (3)", kop(mv("0", "Int", [FIFO + "N_Botellas", FIFO + "Ptr_Entrada"]),
                                                serie=[c(MOD + "Parada_Seguridad")]))
    )
    p.append(paso("fc4-vaciar", "Segmentos 1 a 3 · Vaciado en parada de seguridad", txt, 9))
    peticion = kop([b(GEN + "Peticion")], serie=[
        c(MOD + "Ciclo_Marcha"), nc(MOD + "Fin_Ciclo"), nc(MOD + "Parada_Seguridad"), nc(ZON + "Z1"), c("#Espera_OK"),
        cmp_(FIFO + "N_Botellas", "<", PAR + "Max_Botellas", "Int"), nc(bot("Ptr_Entrada", "Activa"))])
    txt = (
        s("Espera entre botellas", kop(ton_("T_Espera_Emision", PAR + "T_Espera_Emision", "#Espera_OK"),
                                       serie=[c(MOD + "Ciclo_Marcha"), nc(ZON + "Z1")]),
          "Cuenta desde que la zona 1 queda libre.")
        + s("Petición de botella nueva", peticion,
            "Siete condiciones en serie. Petición dura un solo ciclo: en cuanto se ocupa la zona 1 deja de cumplirse.")
        + s("Pulso al generador", kop(tp_("T_Emision_Pulso", "T#300ms", g("Emisor_Botellas")), serie=[c(GEN + "Peticion")]),
            "El TP da un pulso de 300 ms aunque la petición dure un ciclo.")
    )
    p.append(paso("fc4-peticion", "Segmentos 4 a 6 · Pedir una botella", txt, 9))
    txt = (
        s("Alta en el FIFO: activa y zona 1 ocupada", kop([S(bot("Ptr_Entrada", "Activa")), S(ZON + "Z1")],
                                                         serie=[c(GEN + "Peticion")]))
        + s("Alta en el FIFO: datos a 0", kop([R(bot("Ptr_Entrada", x)) for x in ("Tipo_Leido", "Es_2L", "Llenada", "Mala")],
                                             serie=[c(GEN + "Peticion")]))
        + s("Alta en el FIFO: número de botella", kop(mv(FIFO + "Siguiente_ID", "Int", [bot("Ptr_Entrada", "ID")]),
                                                     serie=[c(GEN + "Peticion")]))
        + s("Alta en el FIFO: hora de salida", kop(mv('"DB_Linea".Reloj.Base_100ms', "DInt", [bot("Ptr_Entrada", "T_Emision")]),
                                                  serie=[c(GEN + "Peticion")]),
            "Con esta hora FC9 calculará cuánto lleva la botella en la línea.")
        + s("La zona 1 apunta a esta botella", kop(mv(FIFO + "Ptr_Entrada", "Int", [FIFO + "Idx_Z1"]), serie=[c(GEN + "Peticion")]))
        + s("Una botella más en la línea", kop(mat("ADD", "Int", FIFO + "N_Botellas", "1", FIFO + "N_Botellas"), serie=[c(GEN + "Peticion")]))
        + s("Siguiente número de botella", kop(mat("ADD", "Int", FIFO + "Siguiente_ID", "1", FIFO + "Siguiente_ID"), serie=[c(GEN + "Peticion")]))
        + s("Avanzar el puntero de entrada", kop(mat("ADD", "Int", FIFO + "Ptr_Entrada", "1", FIFO + "Ptr_Entrada"), serie=[c(GEN + "Peticion")]))
        + s("Puntero en círculo: después de 3 vuelve a 0", kop(mv("0", "Int", [FIFO + "Ptr_Entrada"]),
                                                             serie=[cmp_(FIFO + "Ptr_Entrada", ">=", "4", "Int")]))
        + ojo("El orden importa: los segmentos que usan <span class='mono'>Ptr_Entrada</span> van antes del que lo avanza.")
    )
    p.append(paso("fc4-alta", "Segmentos 7 a 15 · Alta de la botella en el FIFO", txt, 9))
    txt = (
        s("Detección: botella de 2 L", kop([S(bot("Idx_Z1", "Es_2L"))], serie=[
            c(ZON + "Z1"), c(g("S_Botella_Bajo")), c(g("S_Botella_Alto")), nc(bot("Idx_Z1", "Tipo_Leido"))]),
          "Mientras la botella tapa el sensor BAJO, si también tapa el ALTO es de 2 L.")
        + s("Detección: tipo leído", kop([S(bot("Idx_Z1", "Tipo_Leido"))], serie=[
            c(ZON + "Z1"), neg(g("S_Botella_Bajo"), FLA + "Bajo_FM")]),
            "Flanco negativo: cuando la botella deja de tapar el sensor BAJO damos el tipo por leído.")
        + s("A201 · sensor ALTO sin sensor BAJO", kop(ton_("T_Incoherencia_Alto", "T#500ms", ALM + "A201"),
                                                     serie=[c(g("S_Botella_Alto")), nc(g("S_Botella_Bajo"))]))
        + s("A202 · la botella no llega a detección", kop(ton_("T_Llega_Deteccion", "T#10s", ALM + "A202"),
                                                         serie=[c(ZON + "Z1"), nc(bot("Idx_Z1", "Tipo_Leido"))]))
    )
    p.append(paso("fc4-deteccion", "Segmentos 16 a 19 · Detección de altura", txt, 9))
    p.append(paso("fc4-ob1", "Llamar a FC4 desde el OB1", ob1(4, "FC_Generador_Deteccion", "FC4 · Generador y detección"), 9))
    p.append(paso("fc4-prueba", "Probar FC4", pruebas([
        ("Rearma y pulsa MARCHA", "A los 3 s: Emisor_Botellas da un pulso · Z1 = 1 · N_Botellas = 1 · Botella[0].Activa = 1"),
        ("S_Botella_Bajo = 1 y S_Botella_Alto = 1", "Botella[0].Es_2L = 1"),
        ("S_Botella_Bajo = 0 y S_Botella_Alto = 0", "Botella[0].Tipo_Leido = 1"),
        ("Pulsa la seta", "Todo el FIFO se vacía: N_Botellas = 0 · Z1 = 0"),
    ]), 9))
    P.append((9, "FC4 · Generador y detección", p,
              "Pide botellas al generador, las da de alta en el FIFO y lee su altura. También vacía el FIFO con la parada de seguridad."))

    # =====================================================================
    # PARTE 10 · FC5 Llenado
    # =====================================================================
    p = []
    s = Segmentos()
    p.append(paso("fc5-crear", "Crear FC5 · FC_Llenado", crear_bloque(
        "Función (FC)", "FC_Llenado", 5, [("Aux", "Real", "Resultado intermedio para la consigna.")]), 10))
    txt = (
        s("Llega una botella a la llenadora", kop([b(LLE + "Inicio")], serie=[
            c(ZON + "Z1"), pos(g("S_Pos_Llenado"), FLA + "Llenado_FM"), nc(LLE + "Hecho")]),
          "Inicio vale 1 un solo ciclo. Lo usan los segmentos siguientes para preparar el llenado.")
        + s("Consigna 2 L: capacidad × %", kop(mat("MUL", "Real", PAR + "Vol_Botella_2", PAR + "Pct_Llenado", "#Aux"),
                                              serie=[c(LLE + "Inicio"), c(bot("Idx_Z1", "Es_2L"))]))
        + s("Consigna 0,5 L: capacidad × %", kop(mat("MUL", "Real", PAR + "Vol_Botella_05", PAR + "Pct_Llenado", "#Aux"),
                                                serie=[c(LLE + "Inicio"), nc(bot("Idx_Z1", "Es_2L"))]))
        + s("Consigna en litros", kop(mat("DIV", "Real", "#Aux", "100.0", LLE + "Consigna_L"), serie=[c(LLE + "Inicio")]),
            "2 × 90 / 100 = 1,8 L · 0,5 × 90 / 100 = 0,45 L.")
        + s("Tiempo máximo 2 L", kop(mv(PAR + "T_Max_Llenado_2", "Time", [LLE + "T_Max"]),
                                    serie=[c(LLE + "Inicio"), c(bot("Idx_Z1", "Es_2L"))]))
        + s("Tiempo máximo 0,5 L", kop(mv(PAR + "T_Max_Llenado_05", "Time", [LLE + "T_Max"]),
                                      serie=[c(LLE + "Inicio"), nc(bot("Idx_Z1", "Es_2L"))]))
        + s("Volumen a 0", kop(mv("0.0", "Real", [LLE + "Volumen_L"]), serie=[c(LLE + "Inicio")]))
        + s("Empezar a llenar", kop([S(LLE + "En_Curso")], serie=[c(LLE + "Inicio")]))
    )
    p.append(paso("fc5-inicio", "Segmentos 1 a 8 · Preparar el llenado", txt, 10))
    txt = (
        s("Válvula de llenado", kop([b(LLE + "Valvula")], serie=[
            c(LLE + "En_Curso"), c(NIV + "Nivel_25"), nc(g("SW_Sim_Fallo_Llenado")), nc(MOD + "Parada_Seguridad")]),
          "Si el tanque baja del 25 % la válvula espera cerrada. Con el interruptor de pruebas no se abre y la botella saldrá mala.")
        + s("Salida válvula: cerrada", kop(mv("0", "Int", [g("AQ_Valvula_Llenado")]), serie=[nc(LLE + "Valvula")]))
        + s("Salida válvula: abierta", kop(mv(PAR + "Apertura_Llenado", "Int", [g("AQ_Valvula_Llenado")]), serie=[c(LLE + "Valvula")]))
        + s("Fin bueno: se llegó a la consigna", kop([b(LLE + "Fin_Bueno")], serie=[
            c(LLE + "En_Curso"), cmp_(LLE + "Volumen_L", ">=", LLE + "Consigna_L", "Real")]))
        + s("Fin malo: se acabó el tiempo", kop(ton_("T_Max_Llenado", LLE + "T_Max", LLE + "Fin_Malo"), serie=[
            c(LLE + "En_Curso"), c(NIV + "Nivel_25"), nc(LLE + "Fin_Bueno")]))
    )
    p.append(paso("fc5-llenar", "Segmentos 9 a 13 · Llenar", txt, 10))
    fin = [[c(LLE + "Fin_Bueno")], [c(LLE + "Fin_Malo")]]
    txt = (
        s("Terminar el llenado", kop([R(LLE + "En_Curso"), S(LLE + "Hecho"), S(bot("Idx_Z1", "Llenada"))], paralelo=fin))
        + s("Guardar los litros en la botella", kop(mv(LLE + "Volumen_L", "Real", [bot("Idx_Z1", "Volumen_L")]), paralelo=fin))
        + s("Botella mala", kop([S(bot("Idx_Z1", "Mala")), S(ALM + "A301")], serie=[c(LLE + "Fin_Malo")]))
        + s("Contar malas seguidas", kop(mat("ADD", "Int", LLE + "Malas_Seguidas", "1", LLE + "Malas_Seguidas"), serie=[c(LLE + "Fin_Malo")]))
        + s("Botella buena: quita el aviso", kop([R(ALM + "A301")], serie=[c(LLE + "Fin_Bueno")]))
        + s("Botella buena: malas seguidas a 0", kop(mv("0", "Int", [LLE + "Malas_Seguidas"]), serie=[c(LLE + "Fin_Bueno")]))
        + s("A302 · llenado esperando nivel", kop([b(ALM + "A302")], serie=[c(LLE + "En_Curso"), nc(NIV + "Nivel_25")]))
        + s("A303 · 3 malas seguidas", kop([b(ALM + "A303")], serie=[cmp_(LLE + "Malas_Seguidas", ">=", "3", "Int")]))
        + s("A303: contador a 0", kop(mv("0", "Int", [LLE + "Malas_Seguidas"]), serie=[c(ALM + "A303")]),
            "A303 dura un ciclo: basta para que FC10 dé el fallo y FC2 pare la línea. Así REARME funciona a la primera.")
        + s("Parada de seguridad: cancelar llenado", kop([R(LLE + "En_Curso"), R(LLE + "Hecho")], serie=[c(MOD + "Parada_Seguridad")]))
    )
    p.append(paso("fc5-fin", "Segmentos 14 a 23 · Resultado y alarmas", txt, 10))
    txt = (
        s("Zona 1 entrega a la zona 2", kop([b(ZON + "Z1_Entrega")], serie=[c(ZON + "Z1"), c(LLE + "Hecho"), nc(ZON + "Z2")]))
        + s("Cintas C1 y C2: petición automática", kop([b(ZON + "C12_Auto")], paralelo=[
            [nc(g("S_Pos_Llenado"))], [c(ZON + "Z1_Entrega")]], serie=[c(ZON + "Z1"), nc(MOD + "Parada_Seguridad")]),
            "Se mueven si hay botella en la zona 1 y no está en la llenadora, o si ya está llena y la zona 2 está libre.")
        + s("Cintas C1 y C2: salidas", kop([b(g("Cinta_C1_Entrada")), b(g("Cinta_C2_Llenado"))], paralelo=[
            [c(ZON + "C12_Auto")], [c(MOD + "Manual_OK"), c(HMI + "C12")]]),
            "Rama de abajo: movimiento manual desde la HMI.")
    )
    p.append(paso("fc5-cintas", "Segmentos 24 a 26 · Cintas C1 y C2", txt, 10))
    p.append(paso("fc5-ob1", "Llamar a FC5 desde el OB1", ob1(5, "FC_Llenado", "FC5 · Llenado"), 10))
    p.append(paso("fc5-prueba", "Probar FC5", pruebas([
        ("Con una botella de 2 L en Z1 (parte 9), S_Pos_Llenado = 1", "Consigna_L = 1.8 · En_Curso = 1 · C1 y C2 paradas"),
        ("AI_Caudalimetro = 27648", "Volumen_L sube 1 L cada 6 s · a 1,8 L: Hecho = 1 · Malas_Seguidas = 0"),
        ("Repite con SW_Sim_Fallo_Llenado = 1", "La válvula no se abre · a los 15 s: Mala = 1 · A301 = 1"),
    ], "Para probar con calma sube antes Param.Limite_Botella_100ms a 3000 (5 min), o saltará la alarma de 40 s. "
       "Vuelve a 400 al acabar."), 10))
    P.append((10, "FC5 · Llenado", p,
              "Calcula la consigna según el tipo, abre la válvula, decide si la botella es buena o mala y mueve las cintas C1 y C2."))
    return P
