# -*- coding: utf-8 -*-
"""
Fuente única de datos de la tabla de variables de la línea de llenado.

De aquí salen:
  - docs/01_Tabla_Variables.html  (documentación visual)
  - tia/Variables_PLC.xlsx        (importable en TIA Portal V15: Variables PLC > Importar)

Si cambias una variable, cámbiala aquí y vuelve a ejecutar:
    python3 herramientas/generar.py
"""

REVISION = "Rev. D"
FECHA = "28/09/2026"
TABLA_TIA = "Linea_Llenado"   # nombre de la tabla de variables en TIA

# ---------------------------------------------------------------------------
# Hardware
# (módulo, referencia, direcciones, qué conecta)
# ---------------------------------------------------------------------------
HARDWARE = [
    ("CPU 1214C DC/DC/DC", "6ES7 214-1AG40-0XB0  ·  FW V4.2",
     "I0.0–I1.5 · Q0.0–Q1.1 · IW64, IW66",
     "Cuadro de mando, sensores de posición en cinta, cintas y actuadores principales, "
     "nivel y caudal del tanque (entradas analógicas integradas 0–10 V)."),
    ("SM 1221 DI16", "6ES7 221-1BH32-0XB0",
     "I2.0–I3.7  (dirección inicial IB2)",
     "Finales de carrera de TAP-01 y empujador, sensores de las cajas, "
     "sensores de nivel reales del tanque."),
    ("SM 1222 DQ16 (1)", "6ES7 222-1BH32-0XB0",
     "Q2.0–Q3.7  (dirección inicial QB2)",
     "TAP-01, empujador, cambio de cajas, pilotos del cuadro y lámparas de las fases 1 y 2."),
    ("SM 1222 DQ16 (2)", "6ES7 222-1BH32-0XB0",
     "Q4.0–Q5.7  (dirección inicial QB4)",
     "Lámparas de las fases 2 a 7."),
    ("SM 1232 AQ2", "6ES7 232-4HB32-0XB0",
     "QW64, QW66  (dirección inicial QB64)",
     "Bomba del tanque y válvula de llenado de botellas (0–10 V)."),
]

# ---------------------------------------------------------------------------
# Entradas digitales
# (dirección, nombre, tipo, comentario TIA, explicación, Factory I/O)
# nombre == "" -> reserva (no se exporta a Excel)
# ---------------------------------------------------------------------------
ENTRADAS_DIGITALES = [
    # --- Cuadro de mando
    ("%I0.0", "PB_Marcha", "Bool", "Pulsador MARCHA (verde, NA)",
     "Arranca el ciclo automático. Solo actúa por flanco, en AUTO, sin emergencia y con el rearme hecho.",
     "Start Button"),
    ("%I0.1", "PB_Paro", "Bool", "Pulsador PARO (rojo, NC) · 0 = pulsado",
     "Pide FIN DE CICLO: no se emiten más botellas y las que ya están en la línea terminan. "
     "Es NC: si se corta el cable, el PLC lo ve como PARO.",
     "Stop Button (NC)"),
    ("%I0.2", "SETA_Emergencia", "Bool", "Seta de emergencia (NC) · 0 = pulsada",
     "Emergencia general: para todo al instante y cierra la válvula de seguridad. "
     "En KOP se programa con contacto abierto | | porque en reposo está a 1.",
     "Emergency Stop (NC)"),
    ("%I0.3", "PB_Rearme", "Bool", "Pulsador REARME (azul, NA)",
     "Quita la emergencia memorizada, siempre que la causa ya no exista. Después hay que pulsar MARCHA.",
     "Reset Button"),
    ("%I0.4", "SEL_Auto", "Bool", "Selector 1 = AUTO / 0 = MANUAL",
     "Pasar a MANUAL para la línea como una emergencia y cierra la válvula de seguridad. "
     "Volver a AUTO no arranca nada: hacen falta REARME y MARCHA.",
     "Selector Switch"),
    ("%I0.5", "PB_Prueba_Lamparas", "Bool", "Pulsador prueba de lámparas (NA)",
     "Mientras se pulsa, enciende todas las lámparas y pilotos para comprobar que ninguna está fundida.",
     "Push Button"),
    ("%I0.6", "SW_Sim_Fallo_Llenado", "Bool", "Interruptor PRUEBAS: forzar botella mala",
     "Solo para pruebas. A 1, la válvula de llenado no se abre, se acaba el tiempo y la botella sale MALA.",
     "Selector Switch"),
    ("%I0.7", "SW_Prueba_Nivel_99", "Bool", "Interruptor PRUEBAS: bomba no para al 90 %",
     "Solo para pruebas. A 1, la bomba sigue llenando por encima del 90 % para poder comprobar la emergencia del 99 %.",
     "Selector Switch"),
    # --- Sensores en cinta
    ("%I1.0", "S_Botella_Bajo", "Bool", "Sensor altura BAJA (detecta cualquier botella)",
     "Estación de detección. Solo BAJO = botella de 0,5 L.",
     "Diffuse Sensor (altura baja)"),
    ("%I1.1", "S_Botella_Alto", "Bool", "Sensor altura ALTA (solo botella 2 L)",
     "Estación de detección. BAJO y ALTO a la vez = botella de 2 L. "
     "ALTO sin BAJO = sensores incoherentes (alarma roja A201).",
     "Diffuse Sensor (altura alta)"),
    ("%I1.2", "S_Pos_Llenado", "Bool", "Botella en posición de LLENADO",
     "Para la cinta C2 y arranca el llenado de la botella.",
     "Diffuse Sensor"),
    ("%I1.3", "S_Pos_Taponado", "Bool", "Botella en posición TAP-01",
     "Para la cinta C3 y arranca la taponadora TAP-01.",
     "Diffuse Sensor"),
    ("%I1.4", "S_Pos_Rechazo", "Bool", "Botella frente al EMPUJADOR",
     "Para la cinta C4. Si la botella es MALA, el empujador la tira a la caja de malas; si es buena, sigue.",
     "Diffuse Sensor"),
    ("%I1.5", "S_Entrada_Transversal", "Bool", "Botella entra en cinta transversal C5",
     "Decide el sentido de C5 según el tipo guardado en el FIFO: 0,5 L a un lado, 2 L al otro.",
     "Diffuse Sensor"),
    # --- Módulo SM 1221
    ("%I2.0", "S_TAP01_Arriba", "Bool", "TAP-01 cabezal ARRIBA",
     "Final de carrera. La cinta C3 solo puede moverse con el cabezal arriba.",
     "Simulado en FC1 (Param.Simulacion_FIO)"),
    ("%I2.1", "S_TAP01_Abajo", "Bool", "TAP-01 cabezal ABAJO (tapón puesto)",
     "Final de carrera. Al llegar abajo empieza el tiempo de apriete del tapón.",
     "Simulado en FC1 (Param.Simulacion_FIO)"),
    ("%I2.2", "S_Empujador_Atras", "Bool", "Empujador RETROCEDIDO",
     "La cinta C4 solo puede moverse con el empujador atrás.",
     "Pusher (Back Limit)"),
    ("%I2.3", "S_Empujador_Delante", "Bool", "Empujador AVANZADO",
     "Confirma que la botella mala ha sido empujada; entonces el empujador retrocede.",
     "Pusher (Front Limit)"),
    ("%I2.4", "S_Caja_Malas_Entrada", "Bool", "Botella cae en caja MALAS",
     "Cuenta las botellas malas. A las 20 se cambia la caja.",
     "Retroreflective Sensor"),
    ("%I2.5", "S_Caja_05L_Entrada", "Bool", "Botella cae en caja 0,5 L",
     "Cuenta las botellas de 0,5 L. A las 6 se cambia la caja.",
     "Retroreflective Sensor"),
    ("%I2.6", "S_Caja_2L_Entrada", "Bool", "Botella cae en caja 2 L",
     "Cuenta las botellas de 2 L. A las 6 se cambia la caja.",
     "Retroreflective Sensor"),
    ("%I2.7", "", "", "Reserva", "", ""),
    ("%I3.0", "S_Caja_Malas_Presente", "Bool", "Caja de MALAS en su sitio",
     "Si falta la caja no se empujan botellas (alarma roja A504).",
     "Diffuse Sensor"),
    ("%I3.1", "S_Caja_05L_Presente", "Bool", "Caja de 0,5 L en su sitio",
     "Si falta, la cinta C5 no envía botellas hacia ese lado.",
     "Diffuse Sensor"),
    ("%I3.2", "S_Caja_2L_Presente", "Bool", "Caja de 2 L en su sitio",
     "Si falta, la cinta C5 no envía botellas hacia ese lado.",
     "Diffuse Sensor"),
    ("%I3.3", "S_Tanque_25", "Bool", "Sensor nivel tanque 25 % (instalación real)",
     "1 = agua por encima del 25 %. Se usa en la instalación real. "
     "En simulación se calcula desde el nivel analógico (ver DB_Linea.Tanque).",
     "No existe: se usa Level Meter (IW64)"),
    ("%I3.4", "S_Tanque_90", "Bool", "Sensor nivel tanque 90 % (instalación real)",
     "1 = agua por encima del 90 %. Para la bomba.",
     "No existe: se usa Level Meter (IW64)"),
    ("%I3.5", "S_Tanque_99", "Bool", "Sensor nivel tanque 99 % (instalación real)",
     "1 = agua por encima del 99 %. EMERGENCIA: cierra válvula de seguridad, baliza y sirena.",
     "No existe: se usa Level Meter (IW64)"),
    ("%I3.6", "", "", "Reserva", "", ""),
    ("%I3.7", "", "", "Reserva", "", ""),
]

# ---------------------------------------------------------------------------
# Salidas digitales
# ---------------------------------------------------------------------------
_FASES = [
    ("1", "Tanque"),
    ("2", "Deteccion"),
    ("3", "Llenado"),
    ("4", "Taponado"),
    ("5", "Rechazo"),
    ("6", "Clasif"),
    ("7", "General"),
]
_FASES_TEXTO = {
    "1": "Tanque", "2": "Generación y detección", "3": "Llenado",
    "4": "Taponado TAP-01", "5": "Rechazo de malas", "6": "Clasificación y cajas",
    "7": "General de línea",
}

SALIDAS_DIGITALES = [
    ("%Q0.0", "VS_Valvula_Seguridad", "Bool", "Válvula de seguridad tanque · 1 = ABIERTA",
     "Normalmente cerrada: sin tensión cierra. Solo se abre en AUTO, sin emergencia. "
     "Se cierra con CUALQUIER emergencia y al pasar a MANUAL.",
     "Sin pieza: bloquea la salida de la bomba QW64"),
    ("%Q0.1", "Baliza_Naranja", "Bool", "Baliza naranja de emergencia (intermitente)",
     "Parpadea a 2 Hz desde que aparece una emergencia hasta que se completa el rearme. No se enciende por pasar a MANUAL.",
     "Warning Light"),
    ("%Q0.2", "Sirena", "Bool", "Sirena de emergencia",
     "Suena desde que aparece una emergencia hasta pulsar REARME, aunque la causa siga activa. No suena por pasar a MANUAL.",
     "Alarm Siren"),
    ("%Q0.3", "Emisor_Botellas", "Bool", "Generador de botellas (pulso = 1 botella)",
     "Pulso corto que pide una botella nueva. El tipo (0,5 L o 2 L) sale aleatorio.",
     "Emitter"),
    ("%Q0.4", "Cinta_C1_Entrada", "Bool", "Cinta C1: generador → detección",
     "Lleva la botella desde el generador, pasando por los sensores de altura, hasta C2.",
     "Belt Conveyor"),
    ("%Q0.5", "Cinta_C2_Llenado", "Bool", "Cinta C2: zona de llenado",
     "Se para mientras se llena la botella.",
     "Belt Conveyor"),
    ("%Q0.6", "Cinta_C3_Taponado", "Bool", "Cinta C3: zona TAP-01",
     "Se para mientras TAP-01 pone el tapón.",
     "Belt Conveyor"),
    ("%Q0.7", "Cinta_C4_Rechazo", "Bool", "Cinta C4: zona empujador",
     "Se para frente al empujador para decidir si la botella es buena o mala.",
     "Belt Conveyor"),
    ("%Q1.0", "Cinta_C5_Hacia_05L", "Bool", "Cinta transversal C5 → caja 0,5 L",
     "Mueve C5 hacia la caja de 0,5 L. Enclavada con Q1.1: nunca las dos a la vez.",
     "Belt Conveyor (+) (a confirmar)"),
    ("%Q1.1", "Cinta_C5_Hacia_2L", "Bool", "Cinta transversal C5 → caja 2 L",
     "Mueve C5 hacia la caja de 2 L. Enclavada con Q1.0.",
     "Belt Conveyor (−) (a confirmar)"),
    ("%Q2.0", "TAP01_Bajar", "Bool", "TAP-01 bajar cabezal",
     "1 = baja el cabezal y pone el tapón. 0 = sube.",
     "Pick & Place eje Z (a confirmar)"),
    ("%Q2.1", "Empujador_Avanzar", "Bool", "Empujador botellas malas: avanzar",
     "1 = avanza y tira la botella a la caja de malas. 0 = retrocede.",
     "Pusher"),
    ("%Q2.2", "Caja_Malas_Retirar", "Bool", "Retirar caja MALAS (llena)",
     "Pulso cuando la caja llega a 20 botellas: la caja desaparece.",
     "Remover"),
    ("%Q2.3", "Caja_Malas_Reponer", "Bool", "Poner caja MALAS nueva",
     "Pulso después de retirar: aparece una caja vacía.",
     "Emitter"),
    ("%Q2.4", "Caja_05L_Retirar", "Bool", "Retirar caja 0,5 L (llena)",
     "Pulso cuando la caja llega a 6 botellas.",
     "Remover"),
    ("%Q2.5", "Caja_05L_Reponer", "Bool", "Poner caja 0,5 L nueva", "", "Emitter"),
    ("%Q2.6", "Caja_2L_Retirar", "Bool", "Retirar caja 2 L (llena)",
     "Pulso cuando la caja llega a 6 botellas.",
     "Remover"),
    ("%Q2.7", "Caja_2L_Reponer", "Bool", "Poner caja 2 L nueva", "", "Emitter"),
    ("%Q3.0", "Piloto_Marcha", "Bool", "Piloto verde MARCHA",
     "Fijo = ciclo automático en marcha.",
     "Start Button (Light)"),
    ("%Q3.1", "Piloto_Paro", "Bool", "Piloto rojo PARO",
     "Fijo = línea parada. Parpadea = terminando las botellas tras pulsar PARO.",
     "Stop Button (Light)"),
    ("%Q3.2", "Piloto_Rearme", "Bool", "Piloto azul REARME",
     "Parpadea = hay que pulsar REARME (causa ya eliminada). Fijo = la causa sigue activa.",
     "Reset Button (Light)"),
]

# Lámparas por fase: Q3.3 ... Q5.7 (21 salidas, 3 por fase)
_bit = (3, 3)
def _siguiente(b):
    byte, bit = b
    bit += 1
    if bit == 8:
        byte, bit = byte + 1, 0
    return (byte, bit)

LAMPARAS = []   # (fase, color, dirección, nombre)
for num, corto in _FASES:
    for color, col_txt in (("Verde", "verde"), ("Naranja", "naranja"), ("Rojo", "roja")):
        addr = "%Q{}.{}".format(*_bit)
        nombre = "L{}_{}_{}".format(num, corto, color)
        LAMPARAS.append((num, color, addr, nombre))
        SALIDAS_DIGITALES.append((
            addr, nombre, "Bool",
            "Fase {} {} · lámpara {}".format(num, _FASES_TEXTO[num], col_txt),
            {"Verde": "Fijo = fase trabajando bien. Parpadeo = fase en espera.",
             "Naranja": "Aviso: la línea sigue funcionando.",
             "Rojo": "Fallo: la línea se para."}[color],
            "Indicator Light / Stack Light",
        ))
        _bit = _siguiente(_bit)

# ---------------------------------------------------------------------------
# Analógicas
# ---------------------------------------------------------------------------
ANALOGICAS = [
    ("%IW64", "AI_Nivel_Tanque", "Int", "Nivel tanque 0–27648 = 0–100 %",
     "Entrada analógica integrada de la CPU (0–10 V). Se escala a % con NORM_X + SCALE_X en DB_Linea.Tanque.Nivel_Pct.",
     "Tank · Level Meter"),
    ("%IW66", "AI_Caudalimetro", "Int", "Caudalímetro 0–27648 = 0–Caudal_Max l/min",
     "Se escala a l/min. En el OB30 (cada 100 ms) se suman los litros que entran en la botella.",
     "Tank · Flow Meter"),
    ("%QW64", "AQ_Bomba_Tanque", "Int", "Bomba tanque · 27648 = 100 %, 0 = parada",
     "Solo recibe valor si la bomba tiene petición y la válvula de seguridad Q0.0 está abierta. "
     "Así se simula que la válvula corta el paso del agua.",
     "Tank · Fill Valve"),
    ("%QW66", "AQ_Valvula_Llenado", "Int", "Válvula llenado botellas · 0 = cerrada",
     "Apertura fija (parámetro Apertura_Llenado) mientras se llena una botella.",
     "Tank · Discharge Valve"),
]

# ---------------------------------------------------------------------------
# Marcas del sistema (las crea TIA al activarlas en Propiedades de la CPU)
# ---------------------------------------------------------------------------
MARCAS = [
    ("%M0.3", "Clock_2Hz", "Bool", "Marca de ciclo 2 Hz",
     "Parpadeo rápido: baliza naranja de emergencia."),
    ("%M0.5", "Clock_1Hz", "Bool", "Marca de ciclo 1 Hz",
     "Parpadeo lento: lámparas verdes en espera, piloto de rearme y piloto de paro."),
    ("%M1.0", "FirstScan", "Bool", "Primer ciclo tras arrancar la CPU",
     "Disponible si hace falta. La inicialización la hace el OB100."),
    ("%M1.2", "AlwaysTRUE", "Bool", "Siempre 1", "Para segmentos que deben ejecutarse siempre."),
    ("%M1.3", "AlwaysFALSE", "Bool", "Siempre 0", ""),
]

# ---------------------------------------------------------------------------
# DB_Linea  (DB1, acceso optimizado)
# (grupo, nombre, tipo, valor inicial, remanente, explicación)
# ---------------------------------------------------------------------------
DB_LINEA = [
    # Modo
    ("Modo", "Auto", "Bool", "FALSE", "", "Selector en AUTO."),
    ("Modo", "Ciclo_Marcha", "Bool", "FALSE", "", "Ciclo automático en marcha: se generan botellas."),
    ("Modo", "Fin_Ciclo", "Bool", "FALSE", "", "Se pulsó PARO. No se generan más botellas; las de la línea terminan."),
    ("Modo", "Linea_Vacia", "Bool", "TRUE", "", "No queda ninguna botella en la línea (FIFO vacío)."),
    ("Modo", "Rearme_Pendiente", "Bool", "TRUE", "", "Se activa con cualquier causa y solo se borra con REARME cuando ya no queda ninguna. Arranca a 1 al encender la CPU."),
    ("Modo", "Parada_Seguridad", "Bool", "TRUE", "", "Hay causa o falta el rearme. Todas las FC lo miran: si vale 1, nada se mueve en automático."),
    ("Modo", "Manual_OK", "Bool", "FALSE", "", "Selector en MANUAL y seta sin pulsar: se permiten los movimientos manuales desde la HMI."),
    # Emergencias (causas instantáneas)
    ("Emergencia", "Seta", "Bool", "FALSE", "", "Causa activa ahora: seta pulsada."),
    ("Emergencia", "Nivel_99", "Bool", "FALSE", "", "Causa activa ahora: tanque al 99 %."),
    ("Emergencia", "Tiempo_40s", "Bool", "FALSE", "", "Causa activa ahora: alguna botella pasa de 40 s. La escribe FC9."),
    ("Emergencia", "Manual", "Bool", "FALSE", "", "Causa activa ahora: selector en MANUAL."),
    ("Emergencia", "Fallo_Equipo", "Bool", "FALSE", "", "Causa activa ahora: alguna fase tiene un fallo rojo. La escribe FC10."),
    ("Emergencia", "Hay_Causa", "Bool", "FALSE", "", "Resumen: alguna de las 5 causas está activa ahora."),
    ("Emergencia", "Memo_Sirena", "Bool", "FALSE", "", "Sirena sonando: se activa al aparecer una emergencia y se silencia con REARME."),
    ("Emergencia", "Memo_Baliza", "Bool", "FALSE", "", "Baliza parpadeando: desde que aparece una emergencia hasta que se completa el rearme."),
    # Flancos
    ("Flancos", "Marcha_FM", "Bool", "FALSE", "", "Memoria de flanco de PB_Marcha."),
    ("Flancos", "Rearme_FM", "Bool", "FALSE", "", "Memoria de flanco de PB_Rearme."),
    ("Flancos", "Seta_FM", "Bool", "FALSE", "", "Memoria de flanco de Emergencia.Seta."),
    ("Flancos", "Nivel99_FM", "Bool", "FALSE", "", "Memoria de flanco de Emergencia.Nivel_99."),
    ("Flancos", "T40_FM", "Bool", "FALSE", "", "Memoria de flanco de Emergencia.Tiempo_40s."),
    ("Flancos", "Fallo_FM", "Bool", "FALSE", "", "Memoria de flanco de Emergencia.Fallo_Equipo."),
    ("Flancos", "Bajo_FM", "Bool", "FALSE", "", "Memoria de flanco (bajada) de S_Botella_Bajo."),
    ("Flancos", "Llenado_FM", "Bool", "FALSE", "", "Memoria de flanco de S_Pos_Llenado."),
    ("Flancos", "Taponado_FM", "Bool", "FALSE", "", "Memoria de flanco de S_Pos_Taponado."),
    ("Flancos", "Rechazo_FM", "Bool", "FALSE", "", "Memoria de flanco de S_Pos_Rechazo."),
    ("Flancos", "Transv_FM", "Bool", "FALSE", "", "Memoria de flanco de S_Entrada_Transversal."),
    ("Flancos", "Caida_Malas_FM", "Bool", "FALSE", "", "Memoria de flanco de S_Caja_Malas_Entrada."),
    ("Flancos", "Caja05_FM", "Bool", "FALSE", "", "Memoria de flanco de S_Caja_05L_Entrada."),
    ("Flancos", "Caja2_FM", "Bool", "FALSE", "", "Memoria de flanco de S_Caja_2L_Entrada."),
    ("Flancos", "Marcha_Pulso", "Bool", "FALSE", "", "Vale 1 durante un solo ciclo al pulsar MARCHA."),
    ("Flancos", "Rearme_Pulso", "Bool", "FALSE", "", "Vale 1 durante un solo ciclo al pulsar REARME."),
    # Tanque
    ("Tanque", "Nivel_Pct", "Real", "0.0", "", "Nivel del tanque en % (desde IW64)."),
    ("Tanque", "Nivel_25", "Bool", "FALSE", "", "Sensor 25 % usado por el programa. Viene de I3.3 o, en simulación, de Nivel_Pct ≥ 25."),
    ("Tanque", "Nivel_90", "Bool", "FALSE", "", "Sensor 90 % usado por el programa (I3.4 o Nivel_Pct ≥ 90)."),
    ("Tanque", "Nivel_99", "Bool", "FALSE", "", "Sensor 99 % usado por el programa (I3.5 o Nivel_Pct ≥ 99)."),
    ("Tanque", "Bomba_Marcha", "Bool", "FALSE", "", "Bomba pedida: SET por debajo del 25 %, RESET al 90 % o con parada de seguridad."),
    # Zonas: una botella como máximo en cada zona
    ("Zonas", "Z1", "Bool", "FALSE", "", "Zona 1 ocupada: cintas C1 + C2 (detección y llenado)."),
    ("Zonas", "Z2", "Bool", "FALSE", "", "Zona 2 ocupada: cinta C3 (taponado)."),
    ("Zonas", "Z3", "Bool", "FALSE", "", "Zona 3 ocupada: cinta C4 (rechazo)."),
    ("Zonas", "Z4", "Bool", "FALSE", "", "Zona 4 ocupada: cinta transversal C5."),
    ("Zonas", "Z1_Entrega", "Bool", "FALSE", "", "La botella de Z1 está llena y Z2 libre: pasa a C3."),
    ("Zonas", "Z2_Entrega", "Bool", "FALSE", "", "La botella de Z2 está taponada y Z3 libre: pasa a C4."),
    ("Zonas", "Z3_Entrega", "Bool", "FALSE", "", "La botella de Z3 es buena, Z4 libre y su caja lista: pasa a C5."),
    ("Zonas", "C12_Auto", "Bool", "FALSE", "", "Petición automática de las cintas C1 y C2."),
    ("Zonas", "C3_Auto", "Bool", "FALSE", "", "Petición automática de la cinta C3."),
    ("Zonas", "C4_Auto", "Bool", "FALSE", "", "Petición automática de la cinta C4."),
    ("Zonas", "C5_Auto", "Bool", "FALSE", "", "Petición automática de la cinta C5."),
    ("Zonas", "Dir_2L", "Bool", "FALSE", "", "Sentido de C5: 1 = hacia la caja de 2 L, 0 = hacia la de 0,5 L."),
    ("Zonas", "Caja_OK_Z3", "Bool", "FALSE", "", "La caja que corresponde a la botella de Z3 está puesta y no se está cambiando."),
    # Generador
    ("Generador", "Peticion", "Bool", "FALSE", "", "Vale 1 un solo ciclo: se emite una botella nueva."),
    # Llenado
    ("Llenado", "Caudal_Lmin", "Real", "0.0", "", "Caudal instantáneo en l/min (desde IW66)."),
    ("Llenado", "Volumen_L", "Real", "0.0", "", "Litros que han entrado en la botella actual."),
    ("Llenado", "Consigna_L", "Real", "0.0", "", "Litros a alcanzar: 90 % de 0,5 L = 0,45 L · 90 % de 2 L = 1,8 L."),
    ("Llenado", "T_Max", "Time", "T#0ms", "", "Tiempo máximo de llenado de la botella actual (según su tipo)."),
    ("Llenado", "Inicio", "Bool", "FALSE", "", "Vale 1 un ciclo: la botella acaba de llegar a la llenadora."),
    ("Llenado", "En_Curso", "Bool", "FALSE", "", "Llenando: se suman litros."),
    ("Llenado", "Hecho", "Bool", "FALSE", "", "La botella de Z1 ya está llena (buena o mala)."),
    ("Llenado", "Fin_Bueno", "Bool", "FALSE", "", "Vale 1 un ciclo: se alcanzó la consigna."),
    ("Llenado", "Fin_Malo", "Bool", "FALSE", "", "Vale 1 un ciclo: se acabó el tiempo sin llegar a la consigna."),
    ("Llenado", "Valvula", "Bool", "FALSE", "", "Válvula de llenado abierta."),
    ("Llenado", "Malas_Seguidas", "Int", "0", "", "Botellas malas consecutivas. 3 seguidas = rojo A303."),
    # Taponado
    ("Taponado", "Arriba", "Bool", "FALSE", "", "Cabezal arriba (I2.0 o simulado)."),
    ("Taponado", "Abajo", "Bool", "FALSE", "", "Cabezal abajo (I2.1 o simulado)."),
    ("Taponado", "Ciclo", "Bool", "FALSE", "", "TAP-01 poniendo un tapón."),
    ("Taponado", "Apretado", "Bool", "FALSE", "", "Ya pasó el tiempo de apriete: el cabezal sube."),
    ("Taponado", "Hecho", "Bool", "FALSE", "", "La botella de Z2 ya tiene tapón."),
    # Rechazo
    ("Rechazo", "Empujando", "Bool", "FALSE", "", "Secuencia del empujador en curso."),
    ("Rechazo", "Avanzado", "Bool", "FALSE", "", "El empujador ya llegó delante: ahora retrocede."),
    ("Rechazo", "Esperando_Caida", "Bool", "FALSE", "", "Botella empujada, esperando verla caer en la caja."),
    ("Rechazo", "Botella_Fuera", "Bool", "FALSE", "", "Vale 1 un ciclo: la botella mala cayó en su caja."),
    # Clasificación
    ("Clasif", "Fin_05L", "Bool", "FALSE", "", "Vale 1 un ciclo: una botella cayó en la caja de 0,5 L."),
    ("Clasif", "Fin_2L", "Bool", "FALSE", "", "Vale 1 un ciclo: una botella cayó en la caja de 2 L."),
    # Cajas
    ("Cajas", "Cnt_Malas", "Int", "0", "", "Botellas en la caja de malas (0…20)."),
    ("Cajas", "Cnt_05L", "Int", "0", "", "Botellas en la caja de 0,5 L (0…6)."),
    ("Cajas", "Cnt_2L", "Int", "0", "", "Botellas en la caja de 2 L (0…6)."),
    ("Cajas", "Llena_Malas", "Bool", "FALSE", "", "Vale 1 un ciclo: la caja de malas se llenó."),
    ("Cajas", "Llena_05L", "Bool", "FALSE", "", "Vale 1 un ciclo: la caja de 0,5 L se llenó."),
    ("Cajas", "Llena_2L", "Bool", "FALSE", "", "Vale 1 un ciclo: la caja de 2 L se llenó."),
    ("Cajas", "Cambiando_Malas", "Bool", "FALSE", "", "Cambio de caja de malas en curso (naranja A503)."),
    ("Cajas", "Cambiando_05L", "Bool", "FALSE", "", "Cambio de caja de 0,5 L en curso (naranja A601)."),
    ("Cajas", "Cambiando_2L", "Bool", "FALSE", "", "Cambio de caja de 2 L en curso (naranja A602)."),
    ("Cajas", "Fin_Cambio_Malas", "Bool", "FALSE", "", "Vale 1 un ciclo al terminar el cambio de la caja de malas."),
    ("Cajas", "Fin_Cambio_05L", "Bool", "FALSE", "", "Vale 1 un ciclo al terminar el cambio de la caja de 0,5 L."),
    ("Cajas", "Fin_Cambio_2L", "Bool", "FALSE", "", "Vale 1 un ciclo al terminar el cambio de la caja de 2 L."),
    # Alarmas
    ] + [("Alarmas", a, "Bool", "FALSE", "", t) for a, t in (
        ("A101", "Naranja · nivel por debajo del 25 %."),
        ("A102", "Rojo · tanque al 99 %."),
        ("A103", "Rojo · sensores de nivel incoherentes."),
        ("A104", "Naranja · la bomba no llena el tanque."),
        ("A201", "Rojo · sensor ALTO sin sensor BAJO."),
        ("A202", "Rojo · la botella no llega a detección."),
        ("A301", "Naranja · la última botella salió MALA."),
        ("A302", "Naranja · llenado esperando nivel del tanque."),
        ("A303", "Rojo · 3 botellas malas seguidas."),
        ("A401", "Rojo · TAP-01 no baja."),
        ("A402", "Rojo · TAP-01 no sube."),
        ("A501", "Rojo · empujador no llega delante."),
        ("A502", "Rojo · empujador no vuelve atrás."),
        ("A503", "Naranja · cambiando caja de malas."),
        ("A504", "Rojo · caja de malas: falta o la botella no cae."),
        ("A601", "Naranja · cambiando caja de 0,5 L."),
        ("A602", "Naranja · cambiando caja de 2 L."),
        ("A603", "Rojo · la botella no llega a su caja."),
        ("A604", "Rojo · falta la caja de 0,5 L o de 2 L."),
        ("A701", "Rojo · seta pulsada."),
        ("A702", "Rojo · botella más de 40 s."),
        ("A703", "Naranja · modo MANUAL."),
        ("A704", "Rojo · rearme pendiente."),
    )] + [
    # Memoria de rojo por fase (para que la lámpara roja siga encendida hasta el rearme)
    ("Rojo_Memo", "F1", "Bool", "FALSE", "", "Hubo un fallo rojo en la fase 1. Se borra al completar el rearme."),
    ("Rojo_Memo", "F2", "Bool", "FALSE", "", "Ídem fase 2."),
    ("Rojo_Memo", "F3", "Bool", "FALSE", "", "Ídem fase 3."),
    ("Rojo_Memo", "F4", "Bool", "FALSE", "", "Ídem fase 4."),
    ("Rojo_Memo", "F5", "Bool", "FALSE", "", "Ídem fase 5."),
    ("Rojo_Memo", "F6", "Bool", "FALSE", "", "Ídem fase 6."),
    # Reloj
    ("Reloj", "Base_100ms", "DInt", "0", "", "Se suma 1 cada 100 ms en el OB30. Sirve para medir el tiempo de cada botella (40 s = 400)."),
    # Producción (remanente: se conserva al apagar)
    ("Produccion", "Total_Buenas_05L", "DInt", "0", "Sí", "Contador histórico de botellas buenas de 0,5 L."),
    ("Produccion", "Total_Buenas_2L", "DInt", "0", "Sí", "Contador histórico de botellas buenas de 2 L."),
    ("Produccion", "Total_Malas", "DInt", "0", "Sí", "Contador histórico de botellas malas."),
    ("Produccion", "Total_Cajas_05L", "DInt", "0", "Sí", "Cajas de 0,5 L completadas."),
    ("Produccion", "Total_Cajas_2L", "DInt", "0", "Sí", "Cajas de 2 L completadas."),
    ("Produccion", "Total_Cajas_Malas", "DInt", "0", "Sí", "Cajas de malas completadas."),
    # Parámetros (remanentes)
    ("Param", "Simulacion_FIO", "Bool", "TRUE", "Sí", "TRUE = niveles y finales de TAP-01 simulados (Factory I/O). FALSE = sensores reales."),
    ("Param", "Max_Botellas", "Int", "3", "Sí", "Botellas a la vez en la línea (1 a 4)."),
    ("Param", "T_Espera_Emision", "Time", "T#3s", "Sí", "Espera desde que la zona 1 queda libre hasta emitir la siguiente botella."),
    ("Param", "Limite_Botella_100ms", "DInt", "400", "Sí", "Tiempo máximo de una botella en la línea: 400 × 100 ms = 40 s."),
    ("Param", "Pct_Llenado", "Real", "90.0", "Sí", "Porcentaje de llenado objetivo."),
    ("Param", "Vol_Botella_05", "Real", "0.5", "Sí", "Capacidad botella pequeña (L)."),
    ("Param", "Vol_Botella_2", "Real", "2.0", "Sí", "Capacidad botella grande (L)."),
    ("Param", "Caudal_Max_Lmin", "Real", "10.0", "Sí", "Caudal que corresponde a 27648 en IW66. A calibrar con Factory I/O."),
    ("Param", "Apertura_Llenado", "Int", "13824", "Sí", "Apertura de la válvula de llenado: 13824 = 50 %."),
    ("Param", "T_Max_Llenado_05", "Time", "T#5s", "Sí", "Si en este tiempo no se llega a 0,45 L, la botella es MALA."),
    ("Param", "T_Max_Llenado_2", "Time", "T#15s", "Sí", "Si en este tiempo no se llega a 1,8 L, la botella es MALA."),
    ("Param", "T_Taponado", "Time", "T#2s", "Sí", "Tiempo con el cabezal de TAP-01 abajo (apriete del tapón)."),
    ("Param", "T_Sim_TAP01", "Time", "T#1s", "Sí", "Solo simulación: lo que tarda el cabezal de TAP-01 en subir o bajar."),
    ("Param", "T_Max_Cilindro", "Time", "T#3s", "Sí", "Tiempo máximo de movimiento de TAP-01 y del empujador. Si se pasa: rojo."),
    ("Param", "T_Cambio_Caja", "Time", "T#3s", "Sí", "Duración del cambio de caja (retirar + poner nueva)."),
    ("Param", "Cap_Caja_Buenas", "Int", "6", "Sí", "Botellas por caja de buenas."),
    ("Param", "Cap_Caja_Malas", "Int", "20", "Sí", "Botellas por caja de malas."),
    ("Param", "T_Max_Relleno_Tanque", "Time", "T#120s", "Sí", "Bomba en marcha más de este tiempo sin llegar al 90 %: aviso naranja."),
]

# ---------------------------------------------------------------------------
# UDT_Botella  y  DB_FIFO (DB2)
# ---------------------------------------------------------------------------
UDT_BOTELLA = [
    ("Activa", "Bool", "FALSE", "Esta posición del FIFO tiene una botella en la línea."),
    ("ID", "Int", "0", "Número correlativo de la botella (1, 2, 3...)."),
    ("Tipo_Leido", "Bool", "FALSE", "La botella ya pasó por los sensores de altura."),
    ("Es_2L", "Bool", "FALSE", "0 = botella de 0,5 L · 1 = botella de 2 L."),
    ("Llenada", "Bool", "FALSE", "Ya pasó por la estación de llenado."),
    ("Mala", "Bool", "FALSE", "Se llenó por debajo del 90 %: irá a la caja de malas."),
    ("Volumen_L", "Real", "0.0", "Litros medidos al terminar el llenado."),
    ("T_Emision", "DInt", "0", "Valor de Reloj.Base_100ms cuando salió del generador."),
]

DB_FIFO = [
    ("Botella", "Array[0..3] of \"UDT_Botella\"", "—",
     "4 posiciones = máximo 4 botellas a la vez. Se usa en círculo: después de la 3 vuelve a la 0."),
    ("Ptr_Entrada", "Int", "0", "Posición donde se guardará la próxima botella que salga del generador."),
    ("Idx_Z1", "Int", "0", "Posición del FIFO de la botella que está en la zona 1."),
    ("Idx_Z2", "Int", "0", "Posición del FIFO de la botella que está en la zona 2."),
    ("Idx_Z3", "Int", "0", "Posición del FIFO de la botella que está en la zona 3."),
    ("Idx_Z4", "Int", "0", "Posición del FIFO de la botella que está en la zona 4."),
    ("N_Botellas", "Int", "0", "Botellas que hay ahora en la línea."),
    ("Siguiente_ID", "Int", "1", "Número que llevará la próxima botella."),
]

# ---------------------------------------------------------------------------
# DB_HMI (DB4): órdenes manuales que da la pantalla
# ---------------------------------------------------------------------------
DB_HMI = [
    ("Manual", "C12", "Bool", "Mover cintas C1 y C2 mientras se mantenga pulsado."),
    ("Manual", "C3", "Bool", "Mover cinta C3."),
    ("Manual", "C4", "Bool", "Mover cinta C4."),
    ("Manual", "C5_05L", "Bool", "Mover C5 hacia la caja de 0,5 L."),
    ("Manual", "C5_2L", "Bool", "Mover C5 hacia la caja de 2 L."),
    ("Manual", "TAP01_Bajar", "Bool", "Bajar el cabezal de TAP-01."),
    ("Manual", "Empujador", "Bool", "Avanzar el empujador."),
    ("Manual", "Retirar_Malas", "Bool", "Retirar la caja de malas."),
    ("Manual", "Reponer_Malas", "Bool", "Poner caja de malas nueva."),
    ("Manual", "Retirar_05L", "Bool", "Retirar la caja de 0,5 L."),
    ("Manual", "Reponer_05L", "Bool", "Poner caja de 0,5 L nueva."),
    ("Manual", "Retirar_2L", "Bool", "Retirar la caja de 2 L."),
    ("Manual", "Reponer_2L", "Bool", "Poner caja de 2 L nueva."),
    ("Ordenes", "Reset_Produccion", "Bool", "Pone a 0 los contadores de producción."),
]

# ---------------------------------------------------------------------------
# Temporizadores y contadores (DB_Tiempos, DB3) — instancias IEC
# ---------------------------------------------------------------------------
TEMPORIZADORES = [
    ("T_Emision_Pulso", "TP_TIME", "T#300ms", "Generador", "Ancho del pulso al emisor de botellas."),
    ("T_Espera_Emision", "TON_TIME", "Param.T_Espera_Emision", "Generador", "Espera entre botellas nuevas."),
    ("T_Llega_Deteccion", "TON_TIME", "T#10s", "Generador", "Botella emitida que no llega a los sensores de altura: rojo A202."),
    ("T_Incoherencia_Alto", "TON_TIME", "T#500ms", "Detección", "Filtro para la alarma ALTO sin BAJO (A201)."),
    ("T_Max_Llenado", "TON_TIME", "Llenado.T_Max", "Llenado", "Tiempo máximo de llenado según el tipo de botella."),
    ("T_Sim_TAP01_Abajo", "TON_TIME", "Param.T_Sim_TAP01", "Taponado", "Simulación del final de carrera ABAJO de TAP-01."),
    ("T_Sim_TAP01_Arriba", "TON_TIME", "Param.T_Sim_TAP01", "Taponado", "Simulación del final de carrera ARRIBA de TAP-01."),
    ("T_TAP01_Apriete", "TON_TIME", "Param.T_Taponado", "Taponado", "Tiempo con el cabezal abajo."),
    ("T_TAP01_Baja", "TON_TIME", "Param.T_Max_Cilindro", "Taponado", "Supervisión de bajada del cabezal: rojo A401."),
    ("T_TAP01_Sube", "TON_TIME", "Param.T_Max_Cilindro", "Taponado", "Supervisión de subida del cabezal: rojo A402."),
    ("T_Emp_Avanza", "TON_TIME", "Param.T_Max_Cilindro", "Rechazo", "Supervisión de avance del empujador: rojo A501."),
    ("T_Emp_Retrocede", "TON_TIME", "Param.T_Max_Cilindro", "Rechazo", "Supervisión de retroceso del empujador: rojo A502."),
    ("T_Caida_Malas", "TON_TIME", "T#3s", "Rechazo", "La botella empujada no llega a la caja de malas: rojo A504."),
    ("T_Transversal", "TON_TIME", "T#8s", "Clasificación", "La botella en C5 no llega a su caja: rojo A603."),
    ("T_Cambio_Malas", "TON_TIME", "Param.T_Cambio_Caja", "Cajas", "Secuencia de cambio de la caja de malas."),
    ("T_Cambio_05L", "TON_TIME", "Param.T_Cambio_Caja", "Cajas", "Secuencia de cambio de la caja de 0,5 L."),
    ("T_Cambio_2L", "TON_TIME", "Param.T_Cambio_Caja", "Cajas", "Secuencia de cambio de la caja de 2 L."),
    ("T_Relleno_Tanque", "TON_TIME", "Param.T_Max_Relleno_Tanque", "Tanque", "Bomba en marcha sin llegar al 90 %: naranja A104."),
    ("T_Incoherencia_Nivel", "TON_TIME", "T#1s", "Tanque", "Filtro para la alarma de sensores de nivel incoherentes (A103)."),
    ("C_Caja_Malas", "CTU_INT", "Param.Cap_Caja_Malas", "Cajas", "Cuenta botellas en la caja de malas."),
    ("C_Caja_05L", "CTU_INT", "Param.Cap_Caja_Buenas", "Cajas", "Cuenta botellas en la caja de 0,5 L."),
    ("C_Caja_2L", "CTU_INT", "Param.Cap_Caja_Buenas", "Cajas", "Cuenta botellas en la caja de 2 L."),
]

# ---------------------------------------------------------------------------
# Alarmas por fase
# (id, fase, color, texto, condición, qué hace la línea, cómo se quita)
# color: N = naranja, R = rojo
# ---------------------------------------------------------------------------
ALARMAS = [
    ("A101", "1", "N", "Nivel del tanque por debajo del 25 %",
     "Nivel_25 = 0", "La bomba rellena. El llenado de botellas espera.", "Sola, al superar el 25 %."),
    ("A102", "1", "R", "Tanque al 99 %: EMERGENCIA",
     "Nivel_99 = 1", "Emergencia general: cierra la válvula de seguridad, baliza y sirena.", "Nivel < 99 % + REARME."),
    ("A103", "1", "R", "Sensores de nivel incoherentes",
     "99 sin 90, o 90 sin 25, durante 1 s", "Emergencia general (fallo de equipo).", "Corregir + REARME."),
    ("A104", "1", "N", "La bomba no llena el tanque",
     "Bomba en marcha > 120 s sin llegar al 90 %", "Sigue funcionando.", "Sola, al llegar al 90 %."),
    ("A201", "2", "R", "Sensor ALTO activo sin sensor BAJO",
     "S_Botella_Alto y no S_Botella_Bajo durante 0,5 s", "Emergencia general (fallo de equipo).", "Corregir + REARME."),
    ("A202", "2", "R", "La botella no llega a detección",
     "Pasan 10 s desde la emisión sin leer su tipo", "Emergencia general (fallo de equipo).", "Retirar botellas + REARME."),
    ("A301", "3", "N", "Botella MALA: llenado por debajo del 90 %",
     "Se acaba el tiempo máximo sin llegar a la consigna", "La botella sigue y se rechaza en la fase 5.", "Sola, con la siguiente botella buena."),
    ("A302", "3", "N", "Llenado esperando nivel del tanque",
     "Llenando y Nivel_25 = 0", "La válvula se cierra hasta que el tanque se recupera.", "Sola, al superar el 25 %."),
    ("A303", "3", "R", "3 botellas malas seguidas",
     "Malas_Seguidas ≥ 3", "Emergencia general: posible fallo de válvula o caudalímetro.", "REARME."),
    ("A401", "4", "R", "TAP-01: el cabezal no baja",
     "Orden de bajar y no llega abajo en 3 s", "Emergencia general (fallo de equipo).", "REARME."),
    ("A402", "4", "R", "TAP-01: el cabezal no sube",
     "Sin orden de bajar y no llega arriba en 3 s", "Emergencia general (fallo de equipo).", "REARME."),
    ("A501", "5", "R", "Empujador: no llega delante",
     "Empujador_Avanzar = 1 y no llega S_Empujador_Delante en 3 s", "Emergencia general (fallo de equipo).", "REARME."),
    ("A502", "5", "R", "Empujador: no vuelve atrás",
     "Empujador_Avanzar = 0 y no llega S_Empujador_Atras en 3 s", "Emergencia general (fallo de equipo).", "REARME."),
    ("A503", "5", "N", "Cambiando caja de malas",
     "Cambiando_Malas = 1", "El empujador espera a que haya caja nueva.", "Sola, al terminar el cambio."),
    ("A504", "5", "R", "Caja de malas: falta o la botella no cae",
     "Tras un cambio no hay caja, o la botella empujada no pasa por S_Caja_Malas_Entrada en 3 s",
     "Emergencia general (fallo de equipo).", "REARME."),
    ("A601", "6", "N", "Cambiando caja de 0,5 L",
     "Cambiando_05L = 1", "Las botellas de 0,5 L esperan en C4.", "Sola, al terminar el cambio."),
    ("A602", "6", "N", "Cambiando caja de 2 L",
     "Cambiando_2L = 1", "Las botellas de 2 L esperan en C4.", "Sola, al terminar el cambio."),
    ("A603", "6", "R", "La botella no llega a su caja",
     "Botella en C5 durante 8 s sin ver el sensor de entrada de la caja", "Emergencia general (fallo de equipo).", "REARME."),
    ("A604", "6", "R", "Falta caja de 0,5 L o de 2 L",
     "Tras un cambio de caja, la caja nueva no está", "Emergencia general (fallo de equipo).", "Poner caja + REARME."),
    ("A701", "7", "R", "SETA DE EMERGENCIA pulsada",
     "SETA_Emergencia = 0", "Emergencia general: todo parado, válvula de seguridad cerrada.", "Desenclavar seta + REARME."),
    ("A702", "7", "R", "Botella más de 40 s en la línea",
     "Base_100ms − T_Emision > 400 en cualquier botella activa", "Emergencia general: todo parado, válvula cerrada.", "Retirar botellas + REARME."),
    ("A703", "7", "N", "Modo MANUAL seleccionado",
     "SEL_Auto = 0", "Línea parada como en emergencia, válvula de seguridad cerrada.", "Pasar a AUTO + REARME + MARCHA."),
    ("A704", "7", "R", "Rearme pendiente",
     "Rearme_Pendiente = 1", "No se puede arrancar.", "REARME."),
]

# Qué significa el verde en cada fase (fijo, parpadeo)
VERDES = [
    ("1", "Nivel entre 25 y 99 % y bomba parada.", "Bomba rellenando."),
    ("2", "Botella en camino por detección (zona 1 antes de la llenadora).", "Ciclo en marcha esperando para emitir."),
    ("3", "Llenando una botella.", "Ciclo en marcha, sin botella llenándose."),
    ("4", "TAP-01 poniendo un tapón.", "Ciclo en marcha, sin botella taponándose."),
    ("5", "Botella en la zona del empujador.", "Ciclo en marcha, zona vacía."),
    ("6", "Botella en la cinta transversal C5.", "Ciclo en marcha, C5 vacía."),
    ("7", "Ciclo automático en marcha.", "Terminando tras PARO, o lista esperando MARCHA."),
]

FASES_TEXTO = _FASES_TEXTO

# ---------------------------------------------------------------------------
# Estructura de bloques
# ---------------------------------------------------------------------------
BLOQUES = [
    ("OB1", "Main", "Ciclo principal. Llama a FC1…FC10 en este orden."),
    ("OB30", "Cyclic interrupt 100 ms", "Suma 1 a Reloj.Base_100ms y suma los litros del caudalímetro."),
    ("OB100", "Startup", "Al arrancar la CPU: FIFO vacío, rearme pendiente y válvula de seguridad cerrada."),
    ("FC1", "FC_Entradas", "Escala nivel y caudal; sensores de nivel y finales de TAP-01 (reales o simulados)."),
    ("FC2", "FC_Modos_Seguridad", "AUTO/MANUAL, MARCHA, PARO, SETA, REARME, emergencias, válvula de seguridad, baliza y sirena."),
    ("FC3", "FC_Tanque", "Bomba 25 %→90 %, prueba del 99 % y alarmas del tanque."),
    ("FC4", "FC_Generador_Deteccion", "Emisión de botellas, alta en el FIFO, lectura de altura y vaciado en parada."),
    ("FC5", "FC_Llenado", "Consigna según tipo, válvula de llenado, botella buena o mala, cintas C1 y C2."),
    ("FC6", "FC_Taponadora_TAP01", "Paso a la zona 2, secuencia bajar-apretar-subir con supervisión, cinta C3."),
    ("FC7", "FC_Rechazo", "Paso a la zona 3, empujador de malas, caja de 20, cinta C4."),
    ("FC8", "FC_Clasificacion", "Paso a la zona 4, cinta transversal C5, cajas de 6."),
    ("FC9", "FC_Vigilancia_40s", "Revisa el tiempo de cada botella del FIFO."),
    ("FC10", "FC_Alarmas_Lamparas", "Fallo de equipo, lámparas V/N/R por fase, pilotos y prueba de lámparas."),
    ("UDT1", "UDT_Botella", "Datos de una botella."),
    ("DB1", "DB_Linea", "Estados, zonas, alarmas, contadores y parámetros."),
    ("DB2", "DB_FIFO", "Seguimiento de las botellas en la línea."),
    ("DB3", "DB_Tiempos", "Temporizadores y contadores IEC."),
    ("DB4", "DB_HMI", "Órdenes manuales que da la pantalla."),
]

# ---------------------------------------------------------------------------
# Decisiones confirmadas
# ---------------------------------------------------------------------------
DECISIONES = [
    ("Tanque en Factory I/O",
     "Los sensores de 25/90/99 % se calculan desde el nivel analógico IW64 (Param.Simulacion_FIO = TRUE). "
     "Las entradas I3.3–I3.5 quedan preparadas para una instalación real."),
    ("Botellas en Factory I/O",
     "Caja pequeña = botella de 0,5 L. Caja grande = botella de 2 L."),
    ("Taponadora TAP-01",
     "Se representa con un Pick & Place moviendo el eje Z. Sus finales de carrera se simulan en FC1 con Param.Simulacion_FIO; "
     "en una máquina real vienen de I2.0 e I2.1."),
    ("Cinta transversal C5",
     "Gira en los dos sentidos: Q1.0 hacia 0,5 L y Q1.1 hacia 2 L."),
    ("Lámpara roja = emergencia general",
     "Cualquier fallo rojo para la línea y cierra la válvula de seguridad."),
    ("Baliza y sirena",
     "En todas las emergencias. REARME silencia la sirena aunque la causa siga; la baliza sigue hasta completar el rearme. "
     "En MANUAL no suenan."),
    ("Prueba del 99 %",
     "Interruptor de pruebas SW_Prueba_Nivel_99 en I0.7: la bomba no para al 90 %."),
    ("3 botellas malas seguidas",
     "Alarma roja A303 (emergencia general)."),
    ("Modo MANUAL",
     "La línea se para y la válvula queda cerrada. Los movimientos manuales se hacen desde la HMI, con enclavamientos."),
    ("Botellas tras una emergencia",
     "Con la parada de seguridad el FIFO se vacía. Antes de REARME hay que retirar a mano las botellas que queden en las cintas."),
    ("Válvula de seguridad",
     "Abierta en AUTO sin emergencia aunque el ciclo esté parado, para que el tanque mantenga su nivel."),
    ("Zonas",
     "Una botella como máximo por zona (Z1: C1+C2, Z2: C3, Z3: C4, Z4: C5). Así caben hasta 4 botellas a la vez."),
    ("Hardware",
     "CPU 1214C + SM1221 DI16 + 2× SM1222 DQ16 + SM1232 AQ2, con las direcciones de esta tabla."),
]
