# -*- coding: utf-8 -*-
"""Guía completa · Partes 11 a 16: FC6 TAP-01, FC7 Rechazo, FC8 Clasificación, FC9 Vigilancia, FC10 Lámparas, OB1 y prueba."""
import html

import datos_variables as D
from guia_comun import (ALM, CAJ, CLA, EMG, FIFO, FLA, HMI, LLE, MOD, NIV, PAR, PRO, R, REC, ROJ, S, TAP, TIM, ZON,  # noqa: F401
                        Segmentos, b, bot, c, cmp_, crear_bloque, ctu_, g, kop, lista, llamada, m, mat, mv, nc,
                        ojo, pos, tabla, tip, ton_)
from guia_c2 import ob1, pruebas


def segs_caja(s, suf, sensor_ent, sensor_pres, cap, retirar, reponer, hmi_ret, hmi_rep, total_cajas, alarma_n):
    """Segmentos del contador y del cambio automático de una caja (malas, 0,5 L o 2 L)."""
    cnt, llena, camb, fin = CAJ + f"Cnt_{suf}", CAJ + f"Llena_{suf}", CAJ + f"Cambiando_{suf}", CAJ + f"Fin_Cambio_{suf}"
    et = TIM + f"T_Cambio_{suf}.ET"
    return (
        s(f"Caja {suf}: contar botellas", kop(ctu_(f"C_Caja_{suf}", fin, PAR + cap, cnt), serie=[c(g(sensor_ent))]),
          "El CTU cuenta cada flanco de subida de CU. Se pone a 0 con R al terminar el cambio de caja.")
        + s(f"Caja {suf}: llena", kop([b(llena)], serie=[cmp_(cnt, ">=", PAR + cap, "Int"), nc(camb), nc(MOD + "Parada_Seguridad")]))
        + s(f"Caja {suf}: contar cajas completas", kop(mat("ADD", "DInt", PRO + total_cajas, "1", PRO + total_cajas), serie=[c(llena)]))
        + s(f"Caja {suf}: empezar el cambio (llena o falta)", kop([S(camb)], paralelo=[
            [c(llena)], [nc(g(sensor_pres)), nc(camb), nc(MOD + "Parada_Seguridad")]]),
            "También se cambia si no hay caja, por ejemplo al arrancar Factory I/O.")
        + s(f"Caja {suf}: duración del cambio", kop(ton_(f"T_Cambio_{suf}", PAR + "T_Cambio_Caja", fin), serie=[c(camb)]))
        + s(f"Caja {suf}: terminar el cambio", kop([R(camb)], serie=[c(fin)]))
        + s(f"Caja {suf}: retirar (primer segundo)", kop([b("#Retirar")], serie=[c(camb), cmp_(et, "<", "T#1s", "Time")]),
            "Comparamos el tiempo transcurrido (ET) del temporizador: de 0 a 1 s se retira la caja llena.")
        + s(f"Caja {suf}: poner caja nueva (de 1,5 a 2 s)", kop([b("#Reponer")], serie=[
            c(camb), cmp_(et, ">=", "T#1500ms", "Time"), cmp_(et, "<", "T#2s", "Time")]))
        + s(f"Caja {suf}: salida retirar", kop([b(g(retirar))], paralelo=[[c("#Retirar")], [c(MOD + "Manual_OK"), c(HMI + hmi_ret)]]))
        + s(f"Caja {suf}: salida poner nueva", kop([b(g(reponer))], paralelo=[[c("#Reponer")], [c(MOD + "Manual_OK"), c(HMI + hmi_rep)]]))
        + s(f"{alarma_n} · cambiando caja {suf}", kop([b(ALM + alarma_n)], serie=[c(camb)]))
    )


def partes(G):
    paso = G.paso
    P = []
    temps_caja = [("Retirar", "Bool", "Retirar la caja (automático)."), ("Reponer", "Bool", "Poner caja nueva (automático).")]
    orden_caja = ojo("El orden de los segmentos de la caja importa: el contador va primero y el final del cambio después "
                     "del inicio. Así, al acabar el cambio, el contador se pone a 0 antes de volver a mirar si la caja está llena.")

    # =====================================================================
    # PARTE 11 · FC6 Taponadora TAP-01
    # =====================================================================
    p = []
    s = Segmentos()
    p.append(paso("fc6-crear", "Crear FC6 · FC_Taponadora_TAP01", crear_bloque(
        "Función (FC)", "FC_Taponadora_TAP01", 6,
        [("Llega", "Bool", "Una botella acaba de llegar a TAP-01."),
         ("Bajar_Auto", "Bool", "Orden automática de bajar el cabezal."),
         ("Apriete_OK", "Bool", "Ya pasó el tiempo de apriete.")]), 11))
    txt = (
        s("Llega una botella a TAP-01", kop([b("#Llega")], serie=[c(ZON + "Z1"), c(LLE + "Hecho"),
                                                                pos(g("S_Pos_Taponado"), FLA + "Taponado_FM")]))
        + s("La zona 2 apunta a la botella", kop(mv(FIFO + "Idx_Z1", "Int", [FIFO + "Idx_Z2"]), serie=[c("#Llega")]))
        + s("Paso de zona 1 a zona 2", kop([S(ZON + "Z2"), R(ZON + "Z1"), R(LLE + "Hecho"), S(TAP + "Ciclo"), R(TAP + "Hecho")],
                                           serie=[c("#Llega")]),
            "La zona 1 queda libre: FC4 ya puede pedir la siguiente botella.")
    )
    p.append(paso("fc6-llega", "Segmentos 1 a 3 · Llegada de la botella", txt, 11))
    txt = (
        s("Bajar el cabezal", kop([b("#Bajar_Auto")], serie=[c(TAP + "Ciclo"), nc(TAP + "Apretado"), nc(MOD + "Parada_Seguridad")]))
        + s("Tiempo de apriete abajo", kop(ton_("T_TAP01_Apriete", PAR + "T_Taponado", "#Apriete_OK"),
                                           serie=[c(TAP + "Ciclo"), c(TAP + "Abajo")]))
        + s("Apriete terminado", kop([S(TAP + "Apretado")], serie=[c("#Apriete_OK")]),
            "Lo memorizamos: al subir el cabezal deja de estar abajo y el TON se pone a 0, pero ya no debe volver a bajar.")
        + s("Tapón puesto: cabezal arriba", kop([R(TAP + "Ciclo"), R(TAP + "Apretado"), S(TAP + "Hecho")],
                                               serie=[c(TAP + "Ciclo"), c(TAP + "Apretado"), c(TAP + "Arriba")]))
        + s("Salida TAP01_Bajar", kop([b(g("TAP01_Bajar"))], paralelo=[
            [c("#Bajar_Auto")], [c(MOD + "Manual_OK"), c(HMI + "TAP01_Bajar"), nc(g("Cinta_C3_Taponado"))]]),
            "En manual no se deja bajar el cabezal con la cinta en marcha.")
        + s("A401 · el cabezal no baja", kop(ton_("T_TAP01_Baja", PAR + "T_Max_Cilindro", ALM + "A401"),
                                            serie=[c(g("TAP01_Bajar")), nc(TAP + "Abajo")]))
        + s("A402 · el cabezal no sube", kop(ton_("T_TAP01_Sube", PAR + "T_Max_Cilindro", ALM + "A402"),
                                            serie=[nc(g("TAP01_Bajar")), nc(TAP + "Arriba")]))
        + s("Parada de seguridad: cancelar", kop([R(TAP + "Ciclo"), R(TAP + "Apretado"), R(TAP + "Hecho")],
                                                serie=[c(MOD + "Parada_Seguridad")]))
    )
    p.append(paso("fc6-secuencia", "Segmentos 4 a 11 · Secuencia bajar, apretar y subir", txt, 11))
    txt = (
        s("Zona 2 entrega a la zona 3", kop([b(ZON + "Z2_Entrega")], serie=[c(ZON + "Z2"), c(TAP + "Hecho"), nc(ZON + "Z3")]))
        + s("Cinta C3: petición automática", kop([b(ZON + "C3_Auto")], paralelo=[
            [c(ZON + "Z1_Entrega")], [c(ZON + "Z2"), nc(g("S_Pos_Taponado"))], [c(ZON + "Z2_Entrega")]],
            serie=[c(TAP + "Arriba"), nc(MOD + "Parada_Seguridad")]),
            "C3 se mueve para recibir la botella de la zona 1, para acercarla a TAP-01 y para entregarla a la zona 3. "
            "Nunca con el cabezal abajo.")
        + s("Cinta C3: salida", kop([b(g("Cinta_C3_Taponado"))], paralelo=[
            [c(ZON + "C3_Auto")], [c(MOD + "Manual_OK"), c(HMI + "C3"), c(TAP + "Arriba")]]))
    )
    p.append(paso("fc6-cinta", "Segmentos 12 a 14 · Cinta C3", txt, 11))
    p.append(paso("fc6-ob1", "Llamar a FC6 desde el OB1", ob1(6, "FC_Taponadora_TAP01", "FC6 · Taponadora TAP-01"), 11))
    P.append((11, "FC6 · Taponadora TAP-01", p,
              "Recibe la botella llena, baja el cabezal, aprieta el tapón, sube y la entrega al empujador. Supervisa los movimientos."))

    # =====================================================================
    # PARTE 12 · FC7 Rechazo
    # =====================================================================
    p = []
    s = Segmentos()
    p.append(paso("fc7-crear", "Crear FC7 · FC_Rechazo", crear_bloque(
        "Función (FC)", "FC_Rechazo", 7,
        [("Llega", "Bool", "Una botella acaba de llegar al empujador."),
         ("Avanzar_Auto", "Bool", "Orden automática de avanzar el empujador."),
         ("Caida_Tarde", "Bool", "La botella empujada no llegó a la caja a tiempo.")] + temps_caja), 12))
    txt = (
        s("Llega una botella al empujador", kop([b("#Llega")], serie=[c(ZON + "Z2"), c(TAP + "Hecho"),
                                                                    pos(g("S_Pos_Rechazo"), FLA + "Rechazo_FM")]))
        + s("La zona 3 apunta a la botella", kop(mv(FIFO + "Idx_Z2", "Int", [FIFO + "Idx_Z3"]), serie=[c("#Llega")]))
        + s("Paso de zona 2 a zona 3", kop([S(ZON + "Z3"), R(ZON + "Z2"), R(TAP + "Hecho")], serie=[c("#Llega")]))
    )
    p.append(paso("fc7-llega", "Segmentos 1 a 3 · Llegada de la botella", txt, 12))
    txt = (
        s("Empezar a empujar una botella mala", kop([S(REC + "Empujando")], serie=[
            c(ZON + "Z3"), c(g("S_Pos_Rechazo")), c(bot("Idx_Z3", "Mala")), nc(REC + "Empujando"), nc(REC + "Esperando_Caida"),
            c(g("S_Caja_Malas_Presente")), nc(CAJ + "Cambiando_Malas"), nc(MOD + "Parada_Seguridad")]),
          "Solo si la caja de malas está puesta y no se está cambiando.")
        + s("Avanzar", kop([b("#Avanzar_Auto")], serie=[c(REC + "Empujando"), nc(REC + "Avanzado"), nc(MOD + "Parada_Seguridad")]))
        + s("Llegó delante: ahora retrocede", kop([S(REC + "Avanzado")], serie=[c(REC + "Empujando"), c(g("S_Empujador_Delante"))]))
        + s("De vuelta atrás: esperar la caída", kop([R(REC + "Empujando"), R(REC + "Avanzado"), S(REC + "Esperando_Caida")],
                                                    serie=[c(REC + "Empujando"), c(REC + "Avanzado"), c(g("S_Empujador_Atras"))]))
        + s("Salida del empujador", kop([b(g("Empujador_Avanzar"))], paralelo=[
            [c("#Avanzar_Auto")], [c(MOD + "Manual_OK"), c(HMI + "Empujador"), nc(g("Cinta_C4_Rechazo"))]]))
        + s("La botella mala cae en su caja", kop([b(REC + "Botella_Fuera")], serie=[
            c(REC + "Esperando_Caida"), pos(g("S_Caja_Malas_Entrada"), FLA + "Caida_Malas_FM")]))
        + s("Borrar la botella del FIFO", kop([R(bot("Idx_Z3", "Activa")), R(ZON + "Z3"), R(REC + "Esperando_Caida")],
                                             serie=[c(REC + "Botella_Fuera")]))
        + s("Una botella menos en la línea", kop(mat("SUB", "Int", FIFO + "N_Botellas", "1", FIFO + "N_Botellas"),
                                                serie=[c(REC + "Botella_Fuera")]))
        + s("Contar botellas malas", kop(mat("ADD", "DInt", PRO + "Total_Malas", "1", PRO + "Total_Malas"),
                                        serie=[c(REC + "Botella_Fuera")]))
        + s("A501 · el empujador no llega delante", kop(ton_("T_Emp_Avanza", PAR + "T_Max_Cilindro", ALM + "A501"),
                                                       serie=[c(g("Empujador_Avanzar")), nc(g("S_Empujador_Delante"))]))
        + s("A502 · el empujador no vuelve atrás", kop(ton_("T_Emp_Retrocede", PAR + "T_Max_Cilindro", ALM + "A502"),
                                                      serie=[nc(g("Empujador_Avanzar")), nc(g("S_Empujador_Atras"))]))
        + s("La botella no cae a tiempo", kop(ton_("T_Caida_Malas", "T#3s", "#Caida_Tarde"), serie=[c(REC + "Esperando_Caida")]))
    )
    p.append(paso("fc7-empujar", "Segmentos 4 a 15 · Empujar la botella mala", txt, 12))
    txt = (segs_caja(s, "Malas", "S_Caja_Malas_Entrada", "S_Caja_Malas_Presente", "Cap_Caja_Malas",
                     "Caja_Malas_Retirar", "Caja_Malas_Reponer", "Retirar_Malas", "Reponer_Malas", "Total_Cajas_Malas", "A503")
           + s("A504 · caja de malas: falta o la botella no cae", kop([b(ALM + "A504")], paralelo=[
               [c(CAJ + "Fin_Cambio_Malas"), nc(g("S_Caja_Malas_Presente"))], [c("#Caida_Tarde")]]))
           + orden_caja)
    p.append(paso("fc7-caja", "Segmentos 16 a 27 · Caja de malas (20)", txt, 12))
    txt = (
        s("Parada de seguridad: cancelar", kop([R(REC + "Empujando"), R(REC + "Avanzado"), R(REC + "Esperando_Caida"),
                                               R(CAJ + "Cambiando_Malas")], serie=[c(MOD + "Parada_Seguridad")]))
        + s("¿Está lista la caja de esta botella?", kop([b(ZON + "Caja_OK_Z3")], paralelo=[
            [c(bot("Idx_Z3", "Es_2L")), c(g("S_Caja_2L_Presente")), nc(CAJ + "Cambiando_2L")],
            [nc(bot("Idx_Z3", "Es_2L")), c(g("S_Caja_05L_Presente")), nc(CAJ + "Cambiando_05L")]]))
        + s("Zona 3 entrega a la zona 4", kop([b(ZON + "Z3_Entrega")], serie=[
            c(ZON + "Z3"), nc(bot("Idx_Z3", "Mala")), nc(ZON + "Z4"), c(ZON + "Caja_OK_Z3")]),
            "Las buenas pasan sin pararse si C5 está libre y su caja lista. Si no, esperan frente al empujador.")
        + s("Cinta C4: petición automática", kop([b(ZON + "C4_Auto")], paralelo=[
            [c(ZON + "Z2_Entrega")], [c(ZON + "Z3"), nc(g("S_Pos_Rechazo"))], [c(ZON + "Z3_Entrega")]],
            serie=[c(g("S_Empujador_Atras")), nc(REC + "Empujando"), nc(MOD + "Parada_Seguridad")]),
            "Nunca con el empujador fuera.")
        + s("Cinta C4: salida", kop([b(g("Cinta_C4_Rechazo"))], paralelo=[
            [c(ZON + "C4_Auto")], [c(MOD + "Manual_OK"), c(HMI + "C4"), c(g("S_Empujador_Atras"))]]))
    )
    p.append(paso("fc7-cinta", "Segmentos 28 a 32 · Cinta C4", txt, 12))
    p.append(paso("fc7-ob1", "Llamar a FC7 desde el OB1", ob1(7, "FC_Rechazo", "FC7 · Rechazo"), 12))
    P.append((12, "FC7 · Rechazo de malas", p,
              "Las botellas malas se empujan a su caja; las buenas siguen a la cinta transversal. La caja de malas se cambia sola cada 20."))

    # =====================================================================
    # PARTE 13 · FC8 Clasificación
    # =====================================================================
    p = []
    s = Segmentos()
    p.append(paso("fc8-crear", "Crear FC8 · FC_Clasificacion", crear_bloque(
        "Función (FC)", "FC_Clasificacion", 8, [("Llega", "Bool", "Una botella acaba de entrar en C5.")] + temps_caja), 13))
    fin2 = [[c(CLA + "Fin_05L")], [c(CLA + "Fin_2L")]]
    txt = (
        s("Llega una botella a la cinta transversal", kop([b("#Llega")], serie=[
            c(ZON + "Z3"), nc(bot("Idx_Z3", "Mala")), pos(g("S_Entrada_Transversal"), FLA + "Transv_FM")]))
        + s("La zona 4 apunta a la botella", kop(mv(FIFO + "Idx_Z3", "Int", [FIFO + "Idx_Z4"]), serie=[c("#Llega")]))
        + s("Paso de zona 3 a zona 4", kop([S(ZON + "Z4"), R(ZON + "Z3")], serie=[c("#Llega")]))
        + s("Sentido de C5", kop([b(ZON + "Dir_2L")], paralelo=[
            [c(ZON + "Z4"), c(bot("Idx_Z4", "Es_2L"))], [nc(ZON + "Z4"), c(bot("Idx_Z3", "Es_2L"))]]),
            "Si C5 tiene botella manda su tipo. Si está vacía, el de la botella que está a punto de entrar.")
        + s("Cinta C5: petición automática", kop([b(ZON + "C5_Auto")], paralelo=[[c(ZON + "Z4")], [c(ZON + "Z3_Entrega")]],
                                                serie=[nc(MOD + "Parada_Seguridad")]))
        + s("Salida C5 hacia 2 L", kop([b(g("Cinta_C5_Hacia_2L"))], paralelo=[
            [c(ZON + "C5_Auto"), c(ZON + "Dir_2L")], [c(MOD + "Manual_OK"), c(HMI + "C5_2L")]],
            serie=[nc(g("Cinta_C5_Hacia_05L"))]), "Enclavamiento: nunca los dos sentidos a la vez.")
        + s("Salida C5 hacia 0,5 L", kop([b(g("Cinta_C5_Hacia_05L"))], paralelo=[
            [c(ZON + "C5_Auto"), nc(ZON + "Dir_2L")], [c(MOD + "Manual_OK"), c(HMI + "C5_05L")]],
            serie=[nc(g("Cinta_C5_Hacia_2L"))]))
    )
    p.append(paso("fc8-c5", "Segmentos 1 a 7 · Cinta transversal C5", txt, 13))
    txt = (
        s("Cae en la caja de 0,5 L", kop([b(CLA + "Fin_05L")], serie=[c(ZON + "Z4"), pos(g("S_Caja_05L_Entrada"), FLA + "Caja05_FM")]))
        + s("Cae en la caja de 2 L", kop([b(CLA + "Fin_2L")], serie=[c(ZON + "Z4"), pos(g("S_Caja_2L_Entrada"), FLA + "Caja2_FM")]))
        + s("Borrar la botella del FIFO", kop([R(bot("Idx_Z4", "Activa")), R(ZON + "Z4")], paralelo=fin2))
        + s("Una botella menos en la línea", kop(mat("SUB", "Int", FIFO + "N_Botellas", "1", FIFO + "N_Botellas"), paralelo=fin2))
        + s("Contar buenas de 0,5 L", kop(mat("ADD", "DInt", PRO + "Total_Buenas_05L", "1", PRO + "Total_Buenas_05L"),
                                         serie=[c(CLA + "Fin_05L")]))
        + s("Contar buenas de 2 L", kop(mat("ADD", "DInt", PRO + "Total_Buenas_2L", "1", PRO + "Total_Buenas_2L"),
                                       serie=[c(CLA + "Fin_2L")]))
        + s("A603 · la botella no llega a su caja", kop(ton_("T_Transversal", "T#8s", ALM + "A603"), serie=[c(ZON + "Z4")]))
    )
    p.append(paso("fc8-fin", "Segmentos 8 a 14 · La botella llega a su caja", txt, 13))
    txt = (segs_caja(s, "05L", "S_Caja_05L_Entrada", "S_Caja_05L_Presente", "Cap_Caja_Buenas",
                     "Caja_05L_Retirar", "Caja_05L_Reponer", "Retirar_05L", "Reponer_05L", "Total_Cajas_05L", "A601") + orden_caja)
    p.append(paso("fc8-caja05", "Segmentos 15 a 25 · Caja de 0,5 L (6)", txt, 13))
    txt = segs_caja(s, "2L", "S_Caja_2L_Entrada", "S_Caja_2L_Presente", "Cap_Caja_Buenas",
                    "Caja_2L_Retirar", "Caja_2L_Reponer", "Retirar_2L", "Reponer_2L", "Total_Cajas_2L", "A602")
    txt += (
        s("A604 · falta la caja de 0,5 L o de 2 L", kop([b(ALM + "A604")], paralelo=[
            [c(CAJ + "Fin_Cambio_05L"), nc(g("S_Caja_05L_Presente"))], [c(CAJ + "Fin_Cambio_2L"), nc(g("S_Caja_2L_Presente"))]]),
          "Si al terminar un cambio no hay caja nueva, el generador de cajas no funciona.")
        + s("Parada de seguridad: cancelar cambios", kop([R(CAJ + "Cambiando_05L"), R(CAJ + "Cambiando_2L")],
                                                        serie=[c(MOD + "Parada_Seguridad")]))
    )
    p.append(paso("fc8-caja2", "Segmentos 26 a 38 · Caja de 2 L (6)", txt, 13))
    p.append(paso("fc8-ob1", "Llamar a FC8 desde el OB1", ob1(8, "FC_Clasificacion", "FC8 · Clasificación"), 13))
    P.append((13, "FC8 · Clasificación y cajas", p,
              "La cinta transversal lleva cada botella buena a su caja. Las cajas de 0,5 L y de 2 L se cambian solas cada 6."))

    # =====================================================================
    # PARTE 14 · FC9 Vigilancia 40 s
    # =====================================================================
    p = []
    s = Segmentos()
    temps = []
    for i in range(4):
        temps += [(f"Tiempo_{i}", "DInt", f"Décimas de segundo de la botella {i}."),
                  (f"Excede_{i}", "Bool", f"La botella {i} pasa de 40 s.")]
    p.append(paso("fc9-crear", "Crear FC9 · FC_Vigilancia_40s", crear_bloque("Función (FC)", "FC_Vigilancia_40s", 9, temps), 14))
    txt = ""
    for i in range(4):
        txt += s(f"Botella {i}: tiempo en la línea", kop(mat("SUB", "DInt", '"DB_Linea".Reloj.Base_100ms', bot(str(i), "T_Emision"),
                                                              f"#Tiempo_{i}"), serie=[c(bot(str(i), "Activa"))]),
                 "Hora actual menos hora de salida = décimas que lleva en la línea." if i == 0 else "")
        txt += s(f"Botella {i}: ¿más de 40 s?", kop([b(f"#Excede_{i}")], serie=[
            c(bot(str(i), "Activa")), cmp_(f"#Tiempo_{i}", ">", PAR + "Limite_Botella_100ms", "DInt")]))
    txt += s("Causa de emergencia: 40 s", kop([b(EMG + "Tiempo_40s")], paralelo=[[c(f"#Excede_{i}")] for i in range(4)]),
             "FC2 la usa como causa de emergencia en el ciclo siguiente.")
    p.append(paso("fc9-segs", "Segmentos 1 a 9 · Vigilar las 4 posiciones del FIFO", txt, 14))
    p.append(paso("fc9-ob1", "Llamar a FC9 desde el OB1", ob1(9, "FC_Vigilancia_40s", "FC9 · Vigilancia 40 s"), 14))
    P.append((14, "FC9 · Vigilancia de 40 s", p,
              "Si cualquier botella lleva más de 40 s en la línea, emergencia general."))

    # =====================================================================
    # PARTE 15 · FC10 Alarmas y lámparas
    # =====================================================================
    p = []
    s = Segmentos()
    p.append(paso("fc10-crear", "Crear FC10 · FC_Alarmas_Lamparas", crear_bloque("Función (FC)", "FC_Alarmas_Lamparas", 10), 15))
    rojas = ["A103", "A201", "A202", "A303", "A401", "A402", "A501", "A502", "A504", "A603", "A604"]
    txt = (
        s("A701 · seta", kop([b(ALM + "A701")], serie=[c(EMG + "Seta")]))
        + s("A702 · 40 s", kop([b(ALM + "A702")], serie=[c(EMG + "Tiempo_40s")]))
        + s("A703 · MANUAL", kop([b(ALM + "A703")], serie=[c(EMG + "Manual")]))
        + s("A704 · rearme pendiente", kop([b(ALM + "A704")], serie=[c(MOD + "Rearme_Pendiente")]))
        + s("Fallo de equipo: cualquier alarma roja de fase", kop([b(EMG + "Fallo_Equipo")], paralelo=[[c(ALM + a)] for a in rojas]),
            "Once ramas en paralelo. Es la quinta causa de emergencia de FC2.")
    )
    p.append(paso("fc10-alarmas", "Segmentos 1 a 5 · Alarmas generales y fallo de equipo", txt, 15))
    memo = {1: ["A102", "A103"], 2: ["A201", "A202"], 3: ["A303"], 4: ["A401", "A402"], 5: ["A501", "A502", "A504"], 6: ["A603", "A604"]}
    txt = s("Borrar las memorias de rojo al completar el rearme", kop([R(ROJ + f"F{i}") for i in range(1, 7)],
                                                                      serie=[nc(MOD + "Rearme_Pendiente")]),
            "Va antes de los segmentos que las activan.")
    for f, al in memo.items():
        txt += s(f"Memoria de rojo fase {f}", kop([S(ROJ + f"F{f}")], paralelo=[[c(ALM + a)] for a in al]))
    p.append(paso("fc10-memo", "Segmentos 6 a 12 · Memorias de rojo", txt + (
        "<p>La lámpara roja de una fase se queda encendida hasta el rearme, aunque la alarma ya haya desaparecido. "
        "Así el operario sabe dónde fue el fallo.</p>"), 15))

    FA = {1: "Tanque", 2: "Deteccion", 3: "Llenado", 4: "Taponado", 5: "Rechazo", 6: "Clasif", 7: "General"}
    CM = MOD + "Ciclo_Marcha"
    fijo = {1: [c(NIV + "Nivel_25"), nc(NIV + "Nivel_99"), nc(NIV + "Bomba_Marcha")],
            2: [c(ZON + "Z1"), nc(g("S_Pos_Llenado")), nc(LLE + "Hecho")],
            3: [c(LLE + "En_Curso")], 4: [c(TAP + "Ciclo")], 5: [c(ZON + "Z3")], 6: [c(ZON + "Z4")]}
    parp = {1: [c(NIV + "Bomba_Marcha")], 2: [c(CM), nc(ZON + "Z1")], 3: [c(CM), nc(LLE + "En_Curso")],
            4: [c(CM), nc(TAP + "Ciclo")], 5: [c(CM), nc(ZON + "Z3")], 6: [c(CM), nc(ZON + "Z4")]}
    naranja = {1: ["A101", "A104"], 2: [], 3: ["A301", "A302"], 4: [], 5: ["A503"], 6: ["A601", "A602"]}
    prueba = [c(g("PB_Prueba_Lamparas"))]
    txt = ""
    for f in range(1, 7):
        lamp = f"L{f}_{FA[f]}_"
        txt += s(f"Fase {f} · verde", kop([b(g(lamp + "Verde"))], paralelo=[
            fijo[f] + [nc(ROJ + f"F{f}")], parp[f] + [c(g("Clock_1Hz")), nc(ROJ + f"F{f}")], prueba]),
            "Arriba: fijo. En medio: parpadeo (en espera). Abajo: prueba de lámparas." if f == 1 else "")
        txt += s(f"Fase {f} · naranja", kop([b(g(lamp + "Naranja"))], paralelo=[[c(ALM + a)] for a in naranja[f]] + [prueba]),
                 "Esta fase no tiene avisos naranja: solo la enciende la prueba de lámparas." if not naranja[f] else "")
        txt += s(f"Fase {f} · roja", kop([b(g(lamp + "Rojo"))], paralelo=[[c(ROJ + f"F{f}")], prueba]))
    p.append(paso("fc10-fases", "Segmentos 13 a 30 · Lámparas de las fases 1 a 6", txt, 15))
    txt = (
        s("Fase 7 · verde", kop([b(g("L7_General_Verde"))], paralelo=[
            [c(CM), nc(MOD + "Fin_Ciclo")], [c(MOD + "Fin_Ciclo"), c(g("Clock_1Hz"))],
            [nc(CM), nc(MOD + "Parada_Seguridad"), c(g("Clock_1Hz"))], prueba]),
          "Fijo en marcha. Parpadea al terminar tras PARO y cuando la línea está lista esperando MARCHA.")
        + s("Fase 7 · naranja", kop([b(g("L7_General_Naranja"))], paralelo=[[c(ALM + "A703")], prueba]))
        + s("Fase 7 · roja", kop([b(g("L7_General_Rojo"))], paralelo=[
            [c(EMG + "Memo_Baliza")], [c(ALM + "A704"), c(g("Clock_1Hz"))], prueba]),
            "Fija tras una emergencia hasta completar el rearme. Parpadea si solo falta el rearme (por ejemplo tras MANUAL).")
        + s("Piloto MARCHA", kop([b(g("Piloto_Marcha"))], paralelo=[[c(CM), nc(MOD + "Fin_Ciclo")], prueba]))
        + s("Piloto PARO", kop([b(g("Piloto_Paro"))], paralelo=[[nc(CM)], [c(MOD + "Fin_Ciclo"), c(g("Clock_1Hz"))], prueba]))
        + s("Piloto REARME", kop([b(g("Piloto_Rearme"))], paralelo=[
            [c(EMG + "Hay_Causa")], [c(MOD + "Rearme_Pendiente"), c(g("Clock_1Hz"))], prueba]),
            "Fijo: la causa sigue. Parpadeando: ya puedes pulsar REARME.")
        + s("Poner a 0 la producción desde la HMI", kop(mv("0", "DInt", [PRO + x for x in (
            "Total_Buenas_05L", "Total_Buenas_2L", "Total_Malas", "Total_Cajas_05L", "Total_Cajas_2L", "Total_Cajas_Malas")]),
            serie=[c('"DB_HMI".Ordenes.Reset_Produccion'), nc(CM)]), "Solo con el ciclo parado.")
    )
    p.append(paso("fc10-general", "Segmentos 31 a 37 · Fase 7, pilotos y producción", txt, 15))
    p.append(paso("fc10-ob1", "Llamar a FC10 desde el OB1", ob1(10, "FC_Alarmas_Lamparas", "FC10 · Alarmas y lámparas"), 15))
    P.append((15, "FC10 · Alarmas y lámparas", p,
              "Junta las alarmas rojas en el fallo de equipo y enciende las 21 lámparas de fase y los 3 pilotos del cuadro."))

    # =====================================================================
    # PARTE 16 · OB1 completo y prueba de una botella en PLCSIM
    # =====================================================================
    p = []
    filas = [(str(i + 1), f"<span class='mono'>{e}</span>", html.escape(x)) for i, (e, x) in enumerate([
        ("FC_Entradas", "Prepara las señales."),
        ("FC_Modos_Seguridad", "Decide si la línea puede funcionar."),
        ("FC_Tanque", "Bomba y alarmas del tanque."),
        ("FC_Generador_Deteccion", "Vacía en parada, emite y detecta."),
        ("FC_Llenado", "Llena y mueve C1 y C2."),
        ("FC_Taponadora_TAP01", "Tapona y mueve C3."),
        ("FC_Rechazo", "Rechaza malas y mueve C4."),
        ("FC_Clasificacion", "Clasifica y mueve C5."),
        ("FC_Vigilancia_40s", "Vigila los 40 s."),
        ("FC_Alarmas_Lamparas", "Fallo de equipo y lámparas."),
    ])]
    p.append(paso("ob1", "Comprobar el OB1", tabla(["Segmento", "Llama a", "Para qué"], filas)
                  + "<p>Si falta alguna llamada, añádela en su sitio. El orden importa.</p>", 16))
    sim = [
        ("SETA_Emergencia, PB_Paro, SEL_Auto", "1", "Cuadro en reposo y en AUTO."),
        ("S_Empujador_Atras", "1", "El empujador de verdad está atrás; si no, salta A502."),
        ("S_Caja_Malas_Presente, S_Caja_05L_Presente, S_Caja_2L_Presente", "1", "Las tres cajas puestas."),
        ("AI_Nivel_Tanque", "13824", "Tanque al 50 %."),
    ]
    recorrido = [
        ("Pulsa REARME y MARCHA", "A los 3 s: pulso en Emisor_Botellas · Z1 = 1 · C1 y C2 en marcha"),
        ("S_Botella_Bajo = 1, luego 0", "Botella de 0,5 L: Tipo_Leido = 1 · Es_2L = 0"),
        ("S_Pos_Llenado = 1", "C1 y C2 paradas · Consigna_L = 0.45 · válvula abierta"),
        ("AI_Caudalimetro = 27648", "En unos 3 s: Hecho = 1 · C1, C2 y C3 en marcha"),
        ("S_Pos_Llenado = 0 y S_Pos_Taponado = 1", "Z2 = 1 · Z1 = 0 · TAP01_Bajar = 1 · baja, aprieta 2 s y sube"),
        ("S_Pos_Taponado = 0 y S_Pos_Rechazo = 1", "Z3 = 1 · como es buena: C4 y C5 (hacia 0,5 L) en marcha"),
        ("S_Pos_Rechazo = 0 y S_Entrada_Transversal = 1, luego 0", "Z4 = 1 · Z3 = 0"),
        ("S_Caja_05L_Entrada = 1, luego 0", "Z4 = 0 · N_Botellas = 0 · Cnt_05L = 1 · Total_Buenas_05L = 1"),
    ]
    p.append(paso("prueba-botella", "Prueba completa de una botella en PLCSIM", (
        "<p>Antes de Factory I/O, recorre una botella a mano para comprobar que todo encaja.</p>"
        + ojo("Sube primero <span class='mono'>Param.Limite_Botella_100ms</span> a 3000 (5 minutos): haciendo la prueba a mano "
              "tardarás más de 40 s. Al acabar, vuelve a 400.")
        + "<h4>Deja estas entradas fijas en la tabla SIM</h4>"
        + tabla(["Entradas", "Valor", "Por qué"], sim)
        + "<h4>Recorrido</h4>" + pruebas(recorrido)
        + tip("Repite con una botella de 2 L (S_Botella_Alto = 1 junto con el bajo) y con SW_Sim_Fallo_Llenado = 1 para ver una "
              "mala ir a su caja: en el empujador pon S_Empujador_Delante = 1 cuando avance, S_Empujador_Atras = 1 cuando vuelva, "
              "y luego S_Caja_Malas_Entrada = 1.")
    ), 16))
    P.append((16, "OB1 completo y prueba en PLCSIM", p,
              "Con las 10 FC hechas, comprobamos el OB1 y hacemos pasar una botella entera moviendo los sensores a mano."))
    return P
