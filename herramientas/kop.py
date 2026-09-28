# -*- coding: utf-8 -*-
"""
Dibujo de segmentos KOP en texto (estilo  ──| |──( )── ).

Un segmento se describe con:
    segmento(
        paralelo=[[contacto(...), ...], [contacto(...)]],   # ramas OR pegadas a la barra (opcional)
        serie=[contacto(...), comparar(...)],               # contactos en serie después (opcional)
        salida=[bobina(...), bobina(...)]  ó  caja(...)     # bobinas en paralelo o una caja
    )
y devuelve el dibujo como texto.
"""

H = "─"


class _Bloque:
    """Rectángulo de texto con una fila 'mid' por donde pasa la corriente."""

    def __init__(self, filas, mid):
        ancho = max((len(f) for f in filas), default=0)
        self.filas = [f.ljust(ancho) for f in filas]
        self.mid = mid

    @property
    def ancho(self):
        return len(self.filas[0]) if self.filas else 0


def _elemento(arriba, centro, abajo=""):
    w = max(len(centro), len(arriba) + 2, len(abajo) + 2)
    extra = w - len(centro)
    izq = extra // 2
    centro = H * izq + centro + H * (extra - izq)
    return _Bloque([arriba.center(w), centro, abajo.center(w)], 1)


def contacto(op, sym="| |"):
    return ("c", op, sym)


def comparar(op1, cmp, op2, tipo):
    return ("cmp", op1, cmp, op2, tipo)


def bobina(op, sym="( )"):
    return ("b", op, sym)


def caja(nombre, tipo, entradas, salidas):
    """entradas: [(operando, pin)], salidas: [(pin, operando)]"""
    return ("caja", nombre, tipo, entradas, salidas)


def _render_el(el):
    if el[0] == "c":
        return _elemento(el[1], H * 2 + el[2] + H * 2)
    if el[0] == "cmp":
        _, op1, cmp, op2, tipo = el
        return _elemento(op1, H * 2 + f"| {cmp} |" + H * 2, f"{op2}   [{tipo}]")
    raise ValueError(el)


def _serie(elementos):
    if not elementos:
        return _Bloque(["", H * 3, ""], 1)
    bloques = [_render_el(x) for x in elementos]
    return _Bloque(["".join(b.filas[i] for b in bloques) for i in range(3)], 1)


def _paralelo(ramas):
    bls = [_serie(r) for r in ramas]
    w = max(b.ancho for b in bls)
    filas, mids = [], []
    for b in bls:
        base = len(filas)
        for i, f in enumerate(b.filas):
            filas.append(f + (H if i == 1 else " ") * (w - len(f)) if i == 1 else f.ljust(w))
        mids.append(base + 1)
    out = []
    for r, f in enumerate(filas):
        if len(bls) == 1:
            c = H if r == mids[0] else " "
        elif r == mids[0]:
            c = "┬"
        elif r == mids[-1]:
            c = "┘"
        elif r in mids:
            c = "┤"
        elif mids[0] < r < mids[-1]:
            c = "│"
        else:
            c = " "
        out.append(f + c)
    return _Bloque(out, 1)


def _bobinas(lista):
    bls = []
    for op, sym in [(b[1], b[2]) for b in lista]:
        centro = H * 2 + sym + H
        w = max(len(centro) + 4, len(op) + 2)
        bls.append([op.rjust(w - 1) + " ", centro.rjust(w, H), " " * w])
    w = max(len(b[0]) for b in bls)
    bls = [[b[0].rjust(w), b[1].rjust(w, H), b[2].rjust(w)] for b in bls]
    filas, mids = [], []
    for b in bls:
        mids.append(len(filas) + 1)
        filas.extend(b)
    out = []
    for r, f in enumerate(filas):
        if len(bls) == 1:
            c = H if r == 1 else " "
        elif r == mids[0]:
            c = "┬"
        elif r == mids[-1]:
            c = "└"
        elif r in mids:
            c = "├"
        elif mids[0] < r < mids[-1]:
            c = "│"
        else:
            c = " "
        out.append(H * 2 + c + f if r == mids[0] else "  " + c + f)
    return _Bloque(out, 1)


def _caja(el):
    _, nombre, tipo, entradas, salidas = el
    pins_in = ["EN"] + [p for _, p in entradas]
    ops_in = [""] + [o for o, _ in entradas]
    pins_out = ["ENO"] + [p for p, _ in salidas]
    ops_out = [""] + [o for _, o in salidas]
    n = max(len(pins_in), len(pins_out))
    pins_in += [""] * (n - len(pins_in))
    ops_in += [""] * (n - len(ops_in))
    pins_out += [""] * (n - len(pins_out))
    ops_out += [""] * (n - len(ops_out))
    wi = max(len(p) for p in pins_in)
    wo = max(len(p) for p in pins_out)
    interior = max(len(nombre), len(tipo), wi + wo + 3) + 2
    wop = max(len(o) for o in ops_in) + 3
    filas = [
        " " * wop + " ┌" + H * interior + "┐",
        " " * wop + " │" + nombre.center(interior) + "│",
        " " * wop + " │" + tipo.center(interior) + "│",
    ]
    for i in range(n):
        if i == 0:
            izq = H * (wop + 1) + "┤"
        elif pins_in[i]:
            izq = ops_in[i].rjust(wop - 3) + " " + H * 3 + "┤"
        else:
            izq = " " * (wop + 1) + "│"
        centro = pins_in[i].ljust(wi) + " " * (interior - wi - wo) + pins_out[i].rjust(wo)
        if pins_out[i]:
            der = "├" + H * 3 + (" " + ops_out[i] if ops_out[i] else "")
        else:
            der = "│"
        filas.append(izq + centro + der)
    filas.append(" " * wop + " └" + H * interior + "┘")
    return _Bloque(filas, 3)


def _unir(a, b):
    off = max(a.mid, b.mid)
    fa = [" " * a.ancho] * (off - a.mid) + a.filas
    fb = [" " * b.ancho] * (off - b.mid) + b.filas
    alto = max(len(fa), len(fb))
    fa += [" " * a.ancho] * (alto - len(fa))
    fb += [" " * b.ancho] * (alto - len(fb))
    return _Bloque([x + y for x, y in zip(fa, fb)], off)


def segmento(salida, paralelo=None, serie=None):
    izq = _paralelo(paralelo) if paralelo else _Bloque(["", "", ""], 1)
    if serie:
        izq = _unir(izq, _serie(serie))
    if not paralelo and not serie:
        izq = _Bloque(["", H * 2, ""], 1)
    der = _caja(salida) if isinstance(salida, tuple) else _bobinas(salida)
    total = _unir(izq, der)
    filas = [("┃" + f).rstrip() for f in total.filas]
    while filas and filas[0] == "┃":
        filas.pop(0)
    while filas and filas[-1] == "┃":
        filas.pop()
    return "\n".join(filas)


if __name__ == "__main__":
    print(segmento(
        paralelo=[[contacto('"PB_Marcha"', "|P|")], [contacto('"DB_Linea".Modo.Ciclo_Marcha')]],
        serie=[contacto('"PB_Paro"'), comparar('"DB_Linea".Tanque.Nivel_Pct', ">=", "25.0", "Real")],
        salida=[bobina('"DB_Linea".Modo.Ciclo_Marcha'), bobina('"Piloto_Marcha"', "(S)")]))
    print()
    print(segmento(
        serie=[contacto('"DB_Linea".Llenado.En_Curso')],
        salida=caja("NORM_X", "Int to Real",
                    [("0", "MIN"), ('"AI_Nivel_Tanque"', "VALUE"), ("27648", "MAX")],
                    [("OUT", "#Nivel_Norm")])))
