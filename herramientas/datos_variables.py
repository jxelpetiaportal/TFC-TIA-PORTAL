# -*- coding: utf-8 -*-
"""
Fuente única de datos de la tabla de variables de la línea de llenado.

De aquí salen:
  - docs/01_Tabla_Variables.html  (documentación visual)
  - tia/Variables_PLC.xlsx        (importable en TIA Portal V15: Variables PLC > Importar)

Si cambias una variable, cámbiala aquí y vuelve a ejecutar:
    python3 herramientas/generar.py
"""

REVISION = "Rev. B"
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
     "Solo para pruebas. A 1, la válvula de llenado corta antes del 90 % y la botella sale MALA.",
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
     "Pick & Place eje Z (a confirmar)"),
    ("%I2.1", "S_TAP01_Abajo", "Bool", "TAP-01 cabezal ABAJO (tapón puesto)",
     "Final de carrera. Al llegar abajo empieza el tiempo de apriete del tapón.",
     "Pick & Place eje Z (a confirmar)"),
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
     "Parpadea a 2 Hz mientras hay una emergencia.",
     "Warning Light"),
    ("%Q0.2", "Sirena", "Bool", "Sirena de emergencia",
     "Suena mientras hay una emergencia. Se silencia al pulsar REARME.",
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
    ("Modo", "Rearme_Pendiente", "Bool", "TRUE", "", "Hubo una emergencia y falta pulsar REARME. Arranca a 1 tras encender la CPU."),
    ("Modo", "Parada_Seguridad", "Bool", "TRUE", "", "Resumen: hay alguna emergencia activa o memorizada. Para todo y cierra la válvula de seguridad."),
    # Emergencias (memorizadas hasta REARME)
    ("Emergencia", "Seta", "Bool", "FALSE", "", "Seta pulsada."),
    ("Emergencia", "Nivel_99", "Bool", "FALSE", "", "Tanque al 99 %."),
    ("Emergencia", "Tiempo_40s", "Bool", "FALSE", "", "Una botella lleva más de 40 s en la línea."),
    ("Emergencia", "Manual", "Bool", "FALSE", "", "Selector en MANUAL."),
    ("Emergencia", "Fallo_Equipo", "Bool", "FALSE", "", "Alguna fase tiene lámpara roja (fallo de cilindro, sensor, etc.)."),
    # Tanque
    ("Tanque", "Nivel_Pct", "Real", "0.0", "", "Nivel del tanque en % (desde IW64)."),
    ("Tanque", "Nivel_25", "Bool", "FALSE", "", "Sensor 25 % usado por el programa. Viene de I3.3 o, en simulación, de Nivel_Pct ≥ 25."),
    ("Tanque", "Nivel_90", "Bool", "FALSE", "", "Sensor 90 % usado por el programa (I3.4 o Nivel_Pct ≥ 90)."),
    ("Tanque", "Nivel_99", "Bool", "FALSE", "", "Sensor 99 % usado por el programa (I3.5 o Nivel_Pct ≥ 99)."),
    ("Tanque", "Bomba_Marcha", "Bool", "FALSE", "", "Bomba pedida: SET por debajo del 25 %, RESET al 90 % o con emergencia."),
    ("Tanque", "Aviso_Nivel_Bajo", "Bool", "FALSE", "", "Nivel por debajo del 25 %: el llenado de botellas espera (naranja)."),
    # Llenado
    ("Llenado", "Caudal_Lmin", "Real", "0.0", "", "Caudal instantáneo en l/min (desde IW66)."),
    ("Llenado", "Volumen_L", "Real", "0.0", "", "Litros que han entrado en la botella actual."),
    ("Llenado", "Consigna_L", "Real", "0.0", "", "Litros a alcanzar: 90 % de 0,5 L = 0,45 L · 90 % de 2 L = 1,8 L."),
    ("Llenado", "En_Curso", "Bool", "FALSE", "", "Válvula de llenado abierta, sumando litros."),
    ("Llenado", "Malas_Seguidas", "Int", "0", "", "Botellas malas consecutivas. 3 seguidas = rojo A303."),
    # Generador
    ("Generador", "Peticion", "Bool", "FALSE", "", "Se cumplen las condiciones para pedir una botella nueva."),
    # Contadores de caja
    ("Cajas", "Cnt_Malas", "Int", "0", "", "Botellas en la caja de malas (0…20)."),
    ("Cajas", "Cnt_05L", "Int", "0", "", "Botellas en la caja de 0,5 L (0…6)."),
    ("Cajas", "Cnt_2L", "Int", "0", "", "Botellas en la caja de 2 L (0…6)."),
    ("Cajas", "Cambiando_Malas", "Bool", "FALSE", "", "Cambio de caja de malas en curso (naranja)."),
    ("Cajas", "Cambiando_05L", "Bool", "FALSE", "", "Cambio de caja de 0,5 L en curso (naranja)."),
    ("Cajas", "Cambiando_2L", "Bool", "FALSE", "", "Cambio de caja de 2 L en curso (naranja)."),
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
    ("Param", "Simulacion_FIO", "Bool", "TRUE", "Sí", "TRUE = niveles desde el nivel analógico (Factory I/O). FALSE = sensores reales I3.3–I3.5."),
    ("Param", "Max_Botellas", "Int", "3", "Sí", "Botellas a la vez en la línea (1 a 4)."),
    ("Param", "T_Espera_Emision", "Time", "T#8s", "Sí", "Tiempo mínimo entre dos botellas nuevas."),
    ("Param", "Limite_Botella_100ms", "DInt", "400", "Sí", "Tiempo máximo de una botella en la línea: 400 × 100 ms = 40 s."),
    ("Param", "Pct_Llenado", "Real", "90.0", "Sí", "Porcentaje de llenado objetivo."),
    ("Param", "Vol_Botella_05", "Real", "0.5", "Sí", "Capacidad botella pequeña (L)."),
    ("Param", "Vol_Botella_2", "Real", "2.0", "Sí", "Capacidad botella grande (L)."),
    ("Param", "Caudal_Max_Lmin", "Real", "10.0", "Sí", "Caudal que corresponde a 27648 en IW66. A calibrar con Factory I/O."),
    ("Param", "Apertura_Llenado", "Int", "13824", "Sí", "Apertura de la válvula de llenado: 13824 = 50 %."),
    ("Param", "T_Max_Llenado_05", "Time", "T#6s", "Sí", "Si en este tiempo no se llega a 0,45 L, la botella es MALA."),
    ("Param", "T_Max_Llenado_2", "Time", "T#10s", "Sí", "Si en este tiempo no se llega a 1,8 L, la botella es MALA."),
    ("Param", "T_Taponado", "Time", "T#2s", "Sí", "Tiempo con el cabezal de TAP-01 abajo (apriete del tapón)."),
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
    ("Ptr_Entrada", "Int", "0", "Posición donde se guarda la próxima botella que sale del generador."),
    ("Ptr_Deteccion", "Int", "0", "Próxima botella que llegará a los sensores de altura."),
    ("Ptr_Llenado", "Int", "0", "Próxima botella que llegará a la estación de llenado."),
    ("Ptr_Rechazo", "Int", "0", "Próxima botella que llegará al empujador."),
    ("Idx_Transversal", "Int", "0", "Botella que está ahora en la cinta C5 (solo cabe una)."),
    ("N_Botellas", "Int", "0", "Botellas que hay ahora en la línea."),
    ("Siguiente_ID", "Int", "1", "Número que llevará la próxima botella."),
]

# ---------------------------------------------------------------------------
# Temporizadores y contadores (DB_Tiempos, DB3) — instancias IEC
# ---------------------------------------------------------------------------
TEMPORIZADORES = [
    ("T_Emision_Pulso", "TP_TIME", "T#300ms", "Generador", "Ancho del pulso al emisor de botellas."),
    ("T_Espera_Emision", "TON_TIME", "Param.T_Espera_Emision", "Generador", "Espera entre botellas nuevas."),
    ("T_Llega_Deteccion", "TON_TIME", "T#10s", "Generador", "Botella emitida que no llega a los sensores de altura: rojo A202."),
    ("T_Incoherencia_Alto", "TON_TIME", "T#500ms", "Detección", "Filtro para la alarma ALTO sin BAJO (A201)."),
    ("T_Max_Llenado", "TON_TIME", "T_Max_Llenado_05 / _2", "Llenado", "Tiempo máximo de llenado según el tipo de botella."),
    ("T_TAP01_Apriete", "TON_TIME", "Param.T_Taponado", "Taponado", "Tiempo con el cabezal abajo."),
    ("T_TAP01_Superv", "TON_TIME", "Param.T_Max_Cilindro", "Taponado", "Supervisión de bajada o subida del cabezal."),
    ("T_Empujador_Superv", "TON_TIME", "Param.T_Max_Cilindro", "Rechazo", "Supervisión de avance o retroceso del empujador."),
    ("T_Caida_Malas", "TON_TIME", "T#3s", "Rechazo", "La botella empujada no llega a la caja de malas: rojo."),
    ("T_Transversal", "TON_TIME", "T#8s", "Clasificación", "La botella en C5 no llega a su caja: rojo."),
    ("T_Cambio_Malas", "TON_TIME", "Param.T_Cambio_Caja", "Cajas", "Secuencia de cambio de la caja de malas."),
    ("T_Cambio_05L", "TON_TIME", "Param.T_Cambio_Caja", "Cajas", "Secuencia de cambio de la caja de 0,5 L."),
    ("T_Cambio_2L", "TON_TIME", "Param.T_Cambio_Caja", "Cajas", "Secuencia de cambio de la caja de 2 L."),
    ("T_Relleno_Tanque", "TON_TIME", "Param.T_Max_Relleno_Tanque", "Tanque", "Bomba en marcha sin llegar al 90 %: naranja A104."),
    ("T_Incoherencia_Nivel", "TON_TIME", "T#1s", "Tanque", "Filtro para la alarma de sensores de nivel incoherentes (A103)."),
    ("C_Caja_Malas", "CTU_INT", "PV = 20", "Cajas", "Cuenta botellas en la caja de malas. Q = caja llena."),
    ("C_Caja_05L", "CTU_INT", "PV = 6", "Cajas", "Cuenta botellas en la caja de 0,5 L."),
    ("C_Caja_2L", "CTU_INT", "PV = 6", "Cajas", "Cuenta botellas en la caja de 2 L."),
]

# ---------------------------------------------------------------------------
# Alarmas por fase
# (id, fase, color, texto, condición, qué hace la línea, cómo se quita)
# color: V = verde, N = naranja, R = rojo
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
     "Pasan 10 s desde la emisión sin ver S_Botella_Bajo", "Emergencia general (fallo de equipo).", "REARME."),
    ("A301", "3", "N", "Botella MALA: llenado por debajo del 90 %",
     "Se acaba T_Max_Llenado sin llegar a la consigna", "La botella sigue y se rechaza en la fase 5.", "Sola, con la siguiente botella buena."),
    ("A302", "3", "N", "Llenado esperando nivel del tanque",
     "Botella en posición y Nivel_25 = 0", "La botella espera en C2.", "Sola, al superar el 25 %."),
    ("A303", "3", "R", "3 botellas malas seguidas",
     "Malas_Seguidas ≥ 3", "Emergencia general: posible fallo de válvula o caudalímetro.", "REARME."),
    ("A401", "4", "R", "TAP-01: el cabezal no baja",
     "TAP01_Bajar = 1 y no llega S_TAP01_Abajo en 3 s", "Emergencia general (fallo de equipo).", "REARME."),
    ("A402", "4", "R", "TAP-01: el cabezal no sube",
     "TAP01_Bajar = 0 y no llega S_TAP01_Arriba en 3 s", "Emergencia general (fallo de equipo).", "REARME."),
    ("A501", "5", "R", "Empujador: no llega delante",
     "Empujador_Avanzar = 1 y no llega S_Empujador_Delante en 3 s", "Emergencia general (fallo de equipo).", "REARME."),
    ("A502", "5", "R", "Empujador: no vuelve atrás",
     "Empujador_Avanzar = 0 y no llega S_Empujador_Atras en 3 s", "Emergencia general (fallo de equipo).", "REARME."),
    ("A503", "5", "N", "Cambiando caja de malas",
     "Cnt_Malas = 20", "El empujador espera a que haya caja nueva.", "Sola, al terminar el cambio."),
    ("A504", "5", "R", "Falta la caja de malas / botella no cae",
     "Sin S_Caja_Malas_Presente, o la botella no pasa por S_Caja_Malas_Entrada en 3 s",
     "Emergencia general (fallo de equipo).", "REARME."),
    ("A601", "6", "N", "Cambiando caja de 0,5 L",
     "Cnt_05L = 6", "Las botellas de 0,5 L esperan en C4/C5.", "Sola, al terminar el cambio."),
    ("A602", "6", "N", "Cambiando caja de 2 L",
     "Cnt_2L = 6", "Las botellas de 2 L esperan en C4/C5.", "Sola, al terminar el cambio."),
    ("A603", "6", "R", "La botella no llega a su caja",
     "C5 en marcha 8 s sin ver el sensor de entrada de la caja", "Emergencia general (fallo de equipo).", "REARME."),
    ("A604", "6", "R", "Falta caja de 0,5 L o de 2 L",
     "Sin S_Caja_05L_Presente o S_Caja_2L_Presente fuera de un cambio", "Emergencia general (fallo de equipo).", "Poner caja + REARME."),
    ("A701", "7", "R", "SETA DE EMERGENCIA pulsada",
     "SETA_Emergencia = 0", "Emergencia general: todo parado, válvula de seguridad cerrada.", "Desenclavar seta + REARME."),
    ("A702", "7", "R", "Botella más de 40 s en la línea",
     "Base_100ms − T_Emision > 400 en cualquier botella activa", "Emergencia general: todo parado, válvula cerrada.", "Retirar la botella + REARME."),
    ("A703", "7", "N", "Modo MANUAL seleccionado",
     "SEL_Auto = 0", "Línea parada como en emergencia, válvula de seguridad cerrada.", "Pasar a AUTO + REARME + MARCHA."),
    ("A704", "7", "R", "Rearme pendiente",
     "Rearme_Pendiente = 1", "No se puede arrancar.", "REARME."),
]

# Qué significa el verde en cada fase
VERDES = [
    ("1", "Nivel entre 25 y 99 %, sensores correctos.", "Bomba rellenando."),
    ("2", "Generando y detectando botellas.", "Esperando: línea completa o tiempo entre botellas."),
    ("3", "Llenando una botella.", "Sin botella en la estación."),
    ("4", "TAP-01 poniendo un tapón.", "Sin botella en la estación."),
    ("5", "Empujando una botella mala o dejando pasar una buena.", "Sin botella en la estación."),
    ("6", "Cinta C5 llevando una botella a su caja.", "Sin botella en C5."),
    ("7", "Ciclo automático en marcha.", "Terminando botellas tras PARO, o esperando MARCHA."),
]

FASES_TEXTO = _FASES_TEXTO

# ---------------------------------------------------------------------------
# Estructura de bloques
# ---------------------------------------------------------------------------
BLOQUES = [
    ("OB1", "Main", "Ciclo principal. Llama a las FC en este orden."),
    ("OB30", "Cyclic interrupt 100 ms", "Suma 1 a Reloj.Base_100ms y suma los litros del caudalímetro."),
    ("OB100", "Startup", "Al arrancar la CPU: FIFO vacío, rearme pendiente y válvula de seguridad cerrada."),
    ("FC1", "FC_Entradas", "Escala el nivel y el caudal y obtiene los sensores de nivel (reales o simulados)."),
    ("FC2", "FC_Modos_Seguridad", "AUTO/MANUAL, MARCHA, PARO, SETA, REARME, emergencias, válvula de seguridad, baliza y sirena."),
    ("FC3", "FC_Tanque", "Bomba 25 %→90 %, alarmas de nivel."),
    ("FC4", "FC_Generador_Deteccion", "Petición de botellas, FIFO de entrada y lectura de altura."),
    ("FC5", "FC_Llenado", "Consigna según tipo, válvula de llenado, botella buena o mala."),
    ("FC6", "FC_Taponadora_TAP01", "Secuencia bajar, apretar y subir con supervisión."),
    ("FC7", "FC_Rechazo", "Empujador de botellas malas y caja de 20."),
    ("FC8", "FC_Clasificacion", "Cinta transversal C5 y cajas de 6."),
    ("FC9", "FC_Vigilancia_40s", "Revisa el tiempo de cada botella del FIFO."),
    ("FC10", "FC_Alarmas_Lamparas", "Alarmas por fase, lámparas V/N/R, pilotos y prueba de lámparas."),
    ("UDT1", "UDT_Botella", "Datos de una botella."),
    ("DB1", "DB_Linea", "Estados, contadores y parámetros."),
    ("DB2", "DB_FIFO", "Seguimiento de las botellas en la línea."),
    ("DB3", "DB_Tiempos", "Temporizadores y contadores IEC."),
]

# ---------------------------------------------------------------------------
# Decisiones confirmadas (antes "pendiente de confirmar")
# ---------------------------------------------------------------------------
DECISIONES = [
    ("Tanque en Factory I/O",
     "Los sensores de 25/90/99 % se calculan desde el nivel analógico IW64 (Param.Simulacion_FIO = TRUE). "
     "Las entradas I3.3–I3.5 quedan preparadas para una instalación real."),
    ("Botellas en Factory I/O",
     "Caja pequeña = botella de 0,5 L. Caja grande = botella de 2 L."),
    ("Taponadora TAP-01",
     "Pick & Place de 2 ejes moviendo solo el eje Z como cabezal. Si no da finales de carrera, se supervisa por tiempo."),
    ("Cinta transversal C5",
     "Una cinta que gira en los dos sentidos: Q1.0 hacia 0,5 L y Q1.1 hacia 2 L."),
    ("Lámpara roja = emergencia general",
     "Cualquier fallo rojo para la línea y cierra la válvula de seguridad."),
    ("Baliza y sirena",
     "En todas las emergencias. En MANUAL no suena la sirena: solo se enciende la naranja de la fase 7."),
    ("Prueba del 99 %",
     "Interruptor de pruebas SW_Prueba_Nivel_99 en I0.7: la bomba no para al 90 %."),
    ("3 botellas malas seguidas",
     "Alarma roja A303 (emergencia general)."),
    ("Modo MANUAL",
     "La línea se para y la válvula queda cerrada. Los movimientos manuales se harán desde la HMI, con enclavamientos."),
    ("Hardware",
     "CPU 1214C + SM1221 DI16 + 2× SM1222 DQ16 + SM1232 AQ2, con las direcciones de esta tabla."),
]
