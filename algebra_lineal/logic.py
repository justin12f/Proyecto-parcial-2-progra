"""
algebra_lineal/logic.py
=======================
Módulo de Álgebra Lineal con arquitectura orientada a objetos.

Jerarquía de clases:
  Matriz                   — Encapsula una matriz y sus operaciones
  Determinante             — Calcula y almacena det con pasos
  SistemaLineal            — Almacena A y b de un sistema Ax=b
  ResultadoCramer          — Almacena la solución completa de Cramer
  OperacionCramer          — Orquesta la Regla de Cramer
  ResultadoMultiplicacion  — Almacena C = A×B y pasos
  OperacionMultiplicacion  — Orquesta la multiplicación matricial
  ResultadoTranspuesta     — Almacena Aᵀ y verificación
  OperacionTranspuesta     — Orquesta la transpuesta
  Parser                   — Convierte texto en objetos Matriz/vector
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional


# ══════════════════════════════════════════════════════════════════
#  UTILIDADES DE FORMATO
# ══════════════════════════════════════════════════════════════════

def _fmt(val: float) -> str:
    return f"{val:.0f}" if val == int(val) else f"{val:.4f}"


def _sep(char: str = "─", largo: int = 60) -> str:
    return char * largo


# ══════════════════════════════════════════════════════════════════
#  CLASE: MATRIZ
# ══════════════════════════════════════════════════════════════════

class Matriz:
    """
    Encapsula una matriz numérica (lista de listas).

    Atributos:
        datos    : List[List[float]]
        filas    : int
        columnas : int
    """

    def __init__(self, datos: List[List[float]]):
        if not datos or not datos[0]:
            raise ValueError("La matriz no puede estar vacía.")
        self.datos: List[List[float]] = datos
        self.filas: int = len(datos)
        self.columnas: int = len(datos[0])

    # ── Acceso ──────────────────────────────────────────────────

    def fila(self, i: int) -> List[float]:
        return self.datos[i]

    def col(self, j: int) -> List[float]:
        return [self.datos[i][j] for i in range(self.filas)]

    def elem(self, i: int, j: int) -> float:
        return self.datos[i][j]

    def es_cuadrada(self) -> bool:
        return self.filas == self.columnas

    def dimension_str(self) -> str:
        return f"{self.filas}x{self.columnas}"

    # ── Operaciones ─────────────────────────────────────────────

    def reemplazar_columna(self, j: int, vector: List[float]) -> "Matriz":
        """Retorna nueva Matriz con la columna j reemplazada por vector."""
        nueva = [fila[:] for fila in self.datos]
        for i in range(self.filas):
            nueva[i][j] = vector[i]
        return Matriz(nueva)

    def transponer(self) -> "Matriz":
        """Retorna la transpuesta como nueva Matriz."""
        datos_t = [
            [self.datos[i][j] for i in range(self.filas)]
            for j in range(self.columnas)
        ]
        return Matriz(datos_t)

    # ── Representación visual ────────────────────────────────────

    def como_texto(self, ancho: int = 8) -> str:
        n = self.filas
        lineas = []
        for i, fila in enumerate(self.datos):
            contenido = "  ".join(f"{_fmt(v):>{ancho}}" for v in fila)
            if n == 1:
                linea = f"  [ {contenido} ]"
            elif i == 0:
                linea = f"  r {contenido} r"
            elif i == n - 1:
                linea = f"  L {contenido} J"
            else:
                linea = f"  | {contenido} |"
            lineas.append(linea)
        return "\n".join(lineas)

    def con_encabezado(self, nombre: str, ancho: int = 8) -> str:
        return f"  {nombre}\n{self.como_texto(ancho)}"

    def __str__(self) -> str:
        return self.como_texto()


# ══════════════════════════════════════════════════════════════════
#  CLASE: DETERMINANTE
# ══════════════════════════════════════════════════════════════════

@dataclass
class Determinante:
    """
    Calcula y almacena el determinante de una Matriz cuadrada.

    Atributos (poblados después de calcular()):
        matriz      : Matriz
        valor       : float  — valor del determinante
        explicacion : str    — desarrollo paso a paso en texto
    """

    matriz: Matriz
    valor: float = field(init=False, default=0.0)
    explicacion: str = field(init=False, default="")

    def calcular(self) -> "Determinante":
        if not self.matriz.es_cuadrada():
            raise ValueError("El determinante solo existe para matrices cuadradas.")
        n = self.matriz.filas
        if n == 2:
            self._calcular_2x2()
        elif n == 3:
            self._calcular_3x3_sarrus()
        else:
            self._calcular_cofactores()
        return self

    # ── Métodos privados ─────────────────────────────────────────

    def _calcular_2x2(self):
        m = self.matriz.datos
        a, b = m[0][0], m[0][1]
        c, d = m[1][0], m[1][1]
        self.valor = a * d - b * c
        self.explicacion = (
            f"  det = ({_fmt(a)})({_fmt(d)}) - ({_fmt(b)})({_fmt(c)})\n"
            f"      = {_fmt(a * d)} - {_fmt(b * c)}\n"
            f"      = {_fmt(self.valor)}"
        )

    def _calcular_3x3_sarrus(self):
        m = self.matriz.datos
        a, b, c = m[0]
        d, e, f = m[1]
        g, h, i = m[2]
        t1, t2, t3 = a * e * i, b * f * g, c * d * h
        t4, t5, t6 = c * e * g, b * d * i, a * f * h
        self.valor = t1 + t2 + t3 - t4 - t5 - t6
        self.explicacion = (
            f"  Regla de Sarrus:  det = a(ei-fh) - b(di-fg) + c(dh-eg)\n\n"
            f"  = {_fmt(a)}*[({_fmt(e)})({_fmt(i)}) - ({_fmt(f)})({_fmt(h)})]"
            f" - {_fmt(b)}*[({_fmt(d)})({_fmt(i)}) - ({_fmt(f)})({_fmt(g)})]"
            f" + {_fmt(c)}*[({_fmt(d)})({_fmt(h)}) - ({_fmt(e)})({_fmt(g)})]\n\n"
            f"  = {_fmt(a)}*({_fmt(e * i - f * h)})"
            f" - {_fmt(b)}*({_fmt(d * i - f * g)})"
            f" + {_fmt(c)}*({_fmt(d * h - e * g)})\n\n"
            f"  = {_fmt(t1)} + {_fmt(t2)} + {_fmt(t3)}"
            f" - {_fmt(t4)} - {_fmt(t5)} - {_fmt(t6)}\n\n"
            f"  = {_fmt(self.valor)}"
        )

    def _calcular_cofactores(self):
        self.valor = self._det_recursivo(self.matriz.datos)
        self.explicacion = (
            f"  Expansion de cofactores (recursiva)\n"
            f"  = {_fmt(self.valor)}"
        )

    def _det_recursivo(self, m: List[List[float]]) -> float:
        n = len(m)
        if n == 1:
            return m[0][0]
        if n == 2:
            return m[0][0] * m[1][1] - m[0][1] * m[1][0]
        det = 0.0
        for j in range(n):
            menor = [fila[:j] + fila[j + 1:] for fila in m[1:]]
            det += ((-1) ** j) * m[0][j] * self._det_recursivo(menor)
        return det


# ══════════════════════════════════════════════════════════════════
#  CLASE: SISTEMA LINEAL
# ══════════════════════════════════════════════════════════════════

@dataclass
class SistemaLineal:
    """
    Almacena los datos de un sistema de ecuaciones Ax = b.

    Atributos:
        A : Matriz       — coeficientes
        b : List[float]  — terminos independientes
    """

    A: Matriz
    b: List[float]

    def __post_init__(self):
        if not self.A.es_cuadrada():
            raise ValueError("La matriz A debe ser cuadrada para la Regla de Cramer.")
        if len(self.b) != self.A.filas:
            raise ValueError(
                f"El vector b debe tener {self.A.filas} elemento(s), "
                f"tiene {len(self.b)}."
            )


# ══════════════════════════════════════════════════════════════════
#  CLASE: RESULTADO CRAMER
# ══════════════════════════════════════════════════════════════════

@dataclass
class ResultadoCramer:
    """
    Almacena la solucion completa de la Regla de Cramer.

    Atributos:
        sistema         : SistemaLineal
        det_A           : Determinante
        dets_Ai         : List[Determinante]  — uno por variable
        variables       : List[str]           — ['x', 'y', 'z', ...]
        soluciones      : List[float]         — valores xᵢ
        verificacion_ok : bool
    """

    sistema: SistemaLineal
    det_A: Determinante = field(init=False)
    dets_Ai: List[Determinante] = field(init=False, default_factory=list)
    variables: List[str] = field(init=False, default_factory=list)
    soluciones: List[float] = field(init=False, default_factory=list)
    verificacion_ok: bool = field(init=False, default=False)

    def tiene_solucion_unica(self) -> bool:
        return abs(self.det_A.valor) > 1e-12

    def como_texto(self) -> str:
        s = self.sistema
        n = s.A.filas
        out: List[str] = []

        out += [_sep("="), "  REGLA DE CRAMER - PROCEDIMIENTO COMPLETO", _sep("=")]

        # Sistema
        out.append("\n  SISTEMA DE ECUACIONES  Ax = b\n")
        out.append(s.A.con_encabezado("Matriz A:"))
        out.append("")
        vec_mat = Matriz([[v] for v in s.b])
        out.append(vec_mat.con_encabezado("Vector b:"))

        # det(A)
        out += [f"\n{_sep()}", "  PASO 1 - Calcular det(A)", _sep()]
        out.append(s.A.como_texto())
        out.append("")
        out.append(self.det_A.explicacion)
        out.append(f"\n  >>  det(A) = {_fmt(self.det_A.valor)}")

        if not self.tiene_solucion_unica():
            out.append("\n  X  SISTEMA SIN SOLUCION UNICA - det(A) = 0")
            return "\n".join(out)

        # det(Ai) por variable
        for i, det_i in enumerate(self.dets_Ai):
            var = self.variables[i]
            out += [
                f"\n{_sep()}",
                f"  PASO {i + 2} - Calcular det(A{i + 1})  [columna {i + 1} reemplazada por b]",
                _sep(),
            ]
            Ai = s.A.reemplazar_columna(i, s.b)
            out.append(Ai.con_encabezado(f"Matriz A{i + 1}:"))
            out.append("")
            out.append(det_i.explicacion)
            out.append(f"\n  >>  det(A{i + 1}) = {_fmt(det_i.valor)}")

        # Aplicar Cramer
        out += [
            f"\n{_sep()}",
            f"  PASO {n + 2} - Aplicar  xi = det(Ai) / det(A)",
            _sep(),
        ]
        for i, var in enumerate(self.variables):
            xi = self.soluciones[i]
            out.append(
                f"  {var} = det(A{i + 1}) / det(A) = "
                f"{_fmt(self.dets_Ai[i].valor)} / {_fmt(self.det_A.valor)} = {_fmt(xi)}"
            )

        # Tabla
        out += [f"\n{_sep()}", "  RESULTADOS", _sep()]
        out.append(f"  {'Variable':<10} {'det(Ai)':<14} {'det(A)':<10} Resultado")
        out.append("  " + "-" * 52)
        for i, var in enumerate(self.variables):
            xi = self.soluciones[i]
            out.append(
                f"  {var:<10} {_fmt(self.dets_Ai[i].valor):<14} "
                f"{_fmt(self.det_A.valor):<10} >>  {var} = {_fmt(xi)}"
            )

        # Verificacion
        out += [f"\n{_sep()}", "  VERIFICACION - sustituir en sistema original", _sep()]
        for i, fila in enumerate(s.A.datos):
            resultado = sum(fila[j] * self.soluciones[j] for j in range(n))
            match = abs(resultado - s.b[i]) < 1e-8
            simbolo = "OK" if match else "ERROR"
            terminos = " + ".join(
                f"({_fmt(fila[j])})({_fmt(self.soluciones[j])})" for j in range(n)
            )
            out.append(
                f"  Ec.{i + 1}: {terminos} = {_fmt(resultado)} aprox {_fmt(s.b[i])}  [{simbolo}]"
            )

        estado = "OK  Verificacion exitosa." if self.verificacion_ok else "ERROR en verificacion."
        out.append(f"\n  {estado}")
        out.append(_sep("="))
        return "\n".join(out)


# ══════════════════════════════════════════════════════════════════
#  CLASE: OPERACION CRAMER
# ══════════════════════════════════════════════════════════════════

class OperacionCramer:
    """
    Orquesta la Regla de Cramer sobre un SistemaLineal.

    Uso:
        sistema  = SistemaLineal(A, b)
        op       = OperacionCramer(sistema)
        resultado = op.ejecutar()
        print(resultado.como_texto())
    """

    _VARS = ["x", "y", "z", "w", "v", "u"]

    def __init__(self, sistema: SistemaLineal):
        self.sistema = sistema
        self._resultado: Optional[ResultadoCramer] = None

    def ejecutar(self) -> ResultadoCramer:
        s = self.sistema
        n = s.A.filas

        resultado = ResultadoCramer(sistema=s)

        # Calcular det(A)
        resultado.det_A = Determinante(s.A).calcular()

        if not resultado.tiene_solucion_unica():
            self._resultado = resultado
            return resultado

        # Nombres de variables
        resultado.variables = [
            self._VARS[i] if i < len(self._VARS) else f"x{i + 1}"
            for i in range(n)
        ]

        # Calcular det(Ai) y xᵢ
        for i in range(n):
            Ai = s.A.reemplazar_columna(i, s.b)
            det_i = Determinante(Ai).calcular()
            resultado.dets_Ai.append(det_i)
            resultado.soluciones.append(det_i.valor / resultado.det_A.valor)

        # Verificar
        resultado.verificacion_ok = all(
            abs(sum(s.A.elem(i, j) * resultado.soluciones[j] for j in range(n)) - s.b[i]) < 1e-8
            for i in range(n)
        )

        self._resultado = resultado
        return resultado

    @property
    def resultado(self) -> Optional[ResultadoCramer]:
        return self._resultado


# ══════════════════════════════════════════════════════════════════
#  CLASE: RESULTADO MULTIPLICACION
# ══════════════════════════════════════════════════════════════════

@dataclass
class ResultadoMultiplicacion:
    """
    Almacena C = A x B con todos los pasos de calculo.

    Atributos:
        A         : Matriz
        B         : Matriz
        C         : Matriz         — resultado
        pasos_cij : List[str]     — texto de cada elemento cij
    """

    A: Matriz
    B: Matriz
    C: Matriz = field(init=False)
    pasos_cij: List[str] = field(init=False, default_factory=list)

    def como_texto(self) -> str:
        out: List[str] = []
        out += [_sep("="), "  MULTIPLICACION DE MATRICES  C = A x B", _sep("=")]
        out.append(
            f"\n  Dimensiones - A: {self.A.dimension_str()}   B: {self.B.dimension_str()}"
        )
        out.append("")
        out.append(self.A.con_encabezado("Matriz A:"))
        out.append("")
        out.append(self.B.con_encabezado("Matriz B:"))

        out += [f"\n{_sep()}", "  PASO 1 - Verificar dimensiones", _sep()]
        out.append(
            f"  OK  Columnas de A ({self.A.columnas}) = Filas de B ({self.B.filas})"
            f"  ->  Multiplicacion posible"
        )
        out.append(
            f"  La matriz resultado C tendra dimension "
            f"{self.A.filas}x{self.B.columnas}"
        )

        out += [
            f"\n{_sep()}",
            "  PASO 2 - Calcular cada elemento  cij = Suma(aik * bkj)",
            _sep(),
        ]
        for paso in self.pasos_cij:
            out.append(paso)

        out += [f"\n{_sep()}", "  PASO 3 - Matriz resultado  C = A x B", _sep()]
        out.append(self.C.con_encabezado("Matriz C:"))
        out.append(_sep("="))
        return "\n".join(out)


# ══════════════════════════════════════════════════════════════════
#  CLASE: OPERACION MULTIPLICACION
# ══════════════════════════════════════════════════════════════════

class OperacionMultiplicacion:
    """
    Orquesta la multiplicacion C = A x B.

    Uso:
        op = OperacionMultiplicacion(A, B)
        resultado = op.ejecutar()
        print(resultado.como_texto())
    """

    def __init__(self, A: Matriz, B: Matriz):
        if A.columnas != B.filas:
            raise ValueError(
                f"Dimensiones incompatibles: columnas de A ({A.columnas}) "
                f"!= filas de B ({B.filas})."
            )
        self.A = A
        self.B = B
        self._resultado: Optional[ResultadoMultiplicacion] = None

    def ejecutar(self) -> ResultadoMultiplicacion:
        A, B = self.A, self.B
        m, n, p = A.filas, A.columnas, B.columnas

        resultado = ResultadoMultiplicacion(A=A, B=B)

        datos_C: List[List[float]] = []
        for i in range(m):
            fila_C = []
            for j in range(p):
                terminos = [A.elem(i, k) * B.elem(k, j) for k in range(n)]
                valor = sum(terminos)
                fila_C.append(valor)
                partes = " + ".join(
                    f"({_fmt(A.elem(i, k))})({_fmt(B.elem(k, j))})" for k in range(n)
                )
                sumas = " + ".join(_fmt(t) for t in terminos)
                resultado.pasos_cij.append(
                    f"  c{i + 1}{j + 1} = {partes}\n"
                    f"       = {sumas}\n"
                    f"       = {_fmt(valor)}\n"
                )
            datos_C.append(fila_C)

        resultado.C = Matriz(datos_C)
        self._resultado = resultado
        return resultado

    @property
    def resultado(self) -> Optional[ResultadoMultiplicacion]:
        return self._resultado


# ══════════════════════════════════════════════════════════════════
#  CLASE: RESULTADO TRANSPUESTA
# ══════════════════════════════════════════════════════════════════

@dataclass
class ResultadoTranspuesta:
    """
    Almacena At (transpuesta de A) y la verificacion (At)t = A.

    Atributos:
        A              : Matriz
        At             : Matriz
        verificacion_ok: bool
    """

    A: Matriz
    At: Matriz = field(init=False)
    verificacion_ok: bool = field(init=False, default=False)

    def como_texto(self) -> str:
        out: List[str] = []
        out += [_sep("="), "  TRANSPUESTA DE MATRIZ  At", _sep("=")]
        out.append(f"\n  Dimension original - A: {self.A.dimension_str()}")
        out.append("")
        out.append(self.A.con_encabezado("Matriz A:"))

        out += [f"\n{_sep()}", "  PASO 1 - Identificar dimensiones", _sep()]
        out.append(
            f"  Matriz A: {self.A.dimension_str()} "
            f"({self.A.filas} filas, {self.A.columnas} columnas)"
        )
        out.append(
            f"  Transpuesta At: {self.At.dimension_str()} "
            f"({self.At.filas} filas, {self.At.columnas} columnas)"
        )

        out += [f"\n{_sep()}", "  PASO 2 - Aplicar la regla  (At)ij = Aji", _sep()]
        out.append("  Las FILAS de A se convierten en COLUMNAS de At:\n")
        for i, fila in enumerate(self.A.datos):
            vals = ", ".join(_fmt(v) for v in fila)
            out.append(f"  Fila {i + 1} de A = [{vals}]  ->  Columna {i + 1} de At")

        out += [f"\n{_sep()}", "  PASO 3 - Construir la matriz transpuesta At", _sep()]
        out.append(self.At.con_encabezado(f"Matriz At ({self.At.dimension_str()}):"))

        out += [f"\n{_sep()}", "  PASO 4 - Verificar  (At)t = A", _sep()]
        Att = self.At.transponer()
        out.append(Att.con_encabezado(f"(At)t ({Att.dimension_str()}):"))
        estado = "OK  (At)t = A - Propiedad verificada." if self.verificacion_ok else "ERROR en verificacion."
        out.append(f"\n  {estado}")

        out += [f"\n{_sep()}", "  PROPIEDADES DE LA TRANSPUESTA", _sep()]
        for prop in [
            "(At)t = A",
            "(A + B)t = At + Bt",
            "(AB)t = Bt*At  (el orden se invierte)",
            "(kA)t = k*At",
            "det(At) = det(A)",
        ]:
            out.append(f"  *  {prop}")

        out.append(_sep("="))
        return "\n".join(out)


# ══════════════════════════════════════════════════════════════════
#  CLASE: OPERACION TRANSPUESTA
# ══════════════════════════════════════════════════════════════════

class OperacionTranspuesta:
    """
    Orquesta el calculo de la transpuesta At.

    Uso:
        op = OperacionTranspuesta(A)
        resultado = op.ejecutar()
        print(resultado.como_texto())
    """

    def __init__(self, A: Matriz):
        self.A = A
        self._resultado: Optional[ResultadoTranspuesta] = None

    def ejecutar(self) -> ResultadoTranspuesta:
        resultado = ResultadoTranspuesta(A=self.A)
        resultado.At = self.A.transponer()

        Att = resultado.At.transponer()
        resultado.verificacion_ok = all(
            abs(Att.elem(i, j) - self.A.elem(i, j)) < 1e-12
            for i in range(self.A.filas)
            for j in range(self.A.columnas)
        )

        self._resultado = resultado
        return resultado

    @property
    def resultado(self) -> Optional[ResultadoTranspuesta]:
        return self._resultado


# ══════════════════════════════════════════════════════════════════
#  CLASE: PARSER
# ══════════════════════════════════════════════════════════════════

class Parser:
    """
    Convierte texto plano en objetos Matriz o vectores.
    Todos los metodos son estaticos (no requiere instancia).

    Uso:
        A = Parser.matriz(texto_a)
        b = Parser.vector(texto_b)
    """

    @staticmethod
    def matriz(texto: str) -> Matriz:
        """Parsea texto con filas separadas por salto de linea y valores por coma."""
        datos: List[List[float]] = []
        for linea in texto.strip().splitlines():
            linea = linea.strip()
            if not linea:
                continue
            fila = [float(x.strip()) for x in linea.replace(";", ",").split(",")]
            datos.append(fila)
        if not datos:
            raise ValueError("La entrada esta vacia.")
        cols = len(datos[0])
        if any(len(f) != cols for f in datos):
            raise ValueError("Todas las filas deben tener el mismo numero de columnas.")
        return Matriz(datos)

    @staticmethod
    def vector(texto: str) -> List[float]:
        """Parsea texto con un numero por linea en vector."""
        vector: List[float] = []
        for linea in texto.strip().splitlines():
            linea = linea.strip()
            if not linea:
                continue
            vector.append(float(linea.replace(",", ".")))
        if not vector:
            raise ValueError("El vector b esta vacio.")
        return vector