# Línea de llenado de botellas · TIA Portal V15 (KOP)

Trabajo de fin de ciclo: línea de llenado con tanque, detección de botellas de 0,5 L y 2 L,
llenado con caudalímetro, taponadora TAP-01, rechazo de botellas malas y clasificación en cajas.

- **PLC:** S7-1200 CPU 1214C DC/DC/DC (FW V4.2), programado en KOP
- **Simulación:** S7-PLCSIM + Factory I/O

## Contenido

| Carpeta | Qué hay |
|---|---|
| `docs/01_Tabla_Variables.html` | Tabla de variables completa: E/S, analógicas, DBs, FIFO, temporizadores, alarmas por fase y esquema de la línea. Se abre con cualquier navegador. |
| `docs/02_Guia_Completa.html` | Guía completa, todo a mano y en 18 partes: proyecto, variables, datos, los 12 bloques KOP segmento a segmento, pruebas en PLCSIM, Factory I/O y HMI. |
| `tia/Variables_PLC.xlsx` | Variables PLC para importar en TIA Portal (Variables PLC → Importar). |
| `tia/fuentes/` | Fuentes externas del UDT y los DB (Fuentes externas → Generar bloques a partir de la fuente). |
| `herramientas/` | Scripts que generan todo lo anterior. Los datos están en `datos_variables.py` y los dibujos KOP salen de `kop.py`. |

Para regenerar después de cambiar algo:

```
pip install openpyxl
python3 herramientas/generar.py
python3 herramientas/guia_completa.py
```

## Estado

1. ✅ Tabla de variables (Rev. D: diseño final de todos los bloques)
2. ✅ DBs y UDT
3. ✅ Guía completa: OB1, OB30, OB100 y FC1…FC10 en KOP (224 segmentos)
4. ✅ Guía de la escena de Factory I/O y de la pantalla HMI
5. ⏳ Montarlo en TIA Portal y probarlo en PLCSIM + Factory I/O
