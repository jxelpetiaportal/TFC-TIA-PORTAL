# Línea de llenado de botellas · TIA Portal V15 (KOP)

Trabajo de fin de ciclo: línea de llenado con tanque, detección de botellas de 0,5 L y 2 L,
llenado con caudalímetro, taponadora TAP-01, rechazo de botellas malas y clasificación en cajas.

- **PLC:** S7-1200 CPU 1214C DC/DC/DC (FW V4.2), programado en KOP
- **Simulación:** S7-PLCSIM + Factory I/O

## Contenido

| Carpeta | Qué hay |
|---|---|
| `docs/01_Tabla_Variables.html` | Tabla de variables completa: E/S, analógicas, DBs, FIFO, temporizadores, alarmas por fase y esquema de la línea. Se abre con cualquier navegador. |
| `docs/02_Guia_Parte1.html` | Guía paso a paso, parte 1: proyecto, hardware, variables, UDT/DB, OB30, OB100 y FC1 en KOP. |
| `tia/Variables_PLC.xlsx` | Variables PLC para importar en TIA Portal (Variables PLC → Importar). |
| `tia/fuentes/` | Fuentes externas del UDT y los DB (Fuentes externas → Generar bloques a partir de la fuente). |
| `herramientas/` | Script que genera los dos ficheros anteriores desde `datos_variables.py`. |

Para regenerar después de cambiar una variable:

```
pip install openpyxl
python3 herramientas/generar.py
python3 herramientas/guia_parte1.py
```

## Estado

1. ✅ Tabla de variables (Rev. B, decisiones confirmadas)
2. ✅ DBs y UDT (fuentes externas)
3. 🔄 Bloques KOP, uno por uno: OB30, OB100 y FC1 hechos (guía parte 1); siguiente FC2
4. ⏳ Escena de Factory I/O
5. ⏳ Pantalla HMI
