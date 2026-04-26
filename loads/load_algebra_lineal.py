"""
loads/load_algebra_lineal.py
============================
Controlador de la ventana de Algebra Lineal.
Usa los objetos de algebra_lineal.logic para ejecutar las operaciones
y mostrar el procedimiento completo paso a paso.

Flujo por operacion:
  1. Leer texto del QPlainTextEdit
  2. Parser.matriz() / Parser.vector()  ->  objetos Matriz, List[float]
  3. Construir SistemaLineal / Matriz directamente
  4. OperacionXxx.ejecutar()            ->  ResultadoXxx (datos almacenados)
  5. ResultadoXxx.como_texto()          ->  mostrar en output_log
"""

import sys
from PyQt5 import QtWidgets, QtGui, uic

from algebra_lineal.logic import (
    Parser,
    SistemaLineal,
    OperacionCramer,
    OperacionMultiplicacion,
    OperacionTranspuesta,
)


# ──────────────────────────────────────────────
# REDIRECCION DE STDOUT -> QTextEdit
# ──────────────────────────────────────────────

class EmisorStream:
    """Redirige sys.stdout al widget QTextEdit de salida."""

    def __init__(self, text_edit: QtWidgets.QTextEdit):
        self.text_edit = text_edit
        self._original = sys.__stdout__

    def write(self, text: str):
        self.text_edit.insertPlainText(text)
        self.text_edit.ensureCursorVisible()

    def flush(self):
        pass

    def restore(self):
        sys.stdout = self._original


# ──────────────────────────────────────────────
# CONTROLADOR PRINCIPAL
# ──────────────────────────────────────────────

class LoadAlgebraLineal(QtWidgets.QWidget):
    """
    Ventana de Algebra Lineal.

    Instancia las clases de operacion del modulo logic.py
    y delega toda la logica matematica en ellas.
    Los resultados (objetos ResultadoXxx) se guardan como atributos
    para poder ser consultados despues si se necesita.

    Atributos de resultado (None hasta que se ejecuta la operacion):
        self.resultado_cramer        : ResultadoCramer | None
        self.resultado_multiplicacion: ResultadoMultiplicacion | None
        self.resultado_transpuesta   : ResultadoTranspuesta | None
    """

    # ── Datos de los casos de prueba (del algebra_lineal.docx) ──
    TEST_CRAMER_A  = "2, 1, -1\n-3, -1, 2\n-2, 1, 2"
    TEST_CRAMER_B  = "8\n-11\n-3"
    TEST_MULTI_A   = "1, 2, 3\n4, 5, 6\n7, 8, 9"
    TEST_MULTI_B   = "9, 8, 7\n6, 5, 4\n3, 2, 1"
    TEST_TRANS_A   = "1, 2, 3, 4\n5, 6, 7, 8\n9, 10, 11, 12"

    def __init__(self):
        super().__init__()

        # ── Cargar interfaz ──
        uic.loadUi("gui/interfaz_algebra_lineal.ui", self)

        # ── Redirigir stdout ──
        self._stream = EmisorStream(self.output_log)
        sys.stdout = self._stream

        # ── Fuente monoespaciada ──
        font = QtGui.QFont("Consolas", 11)
        font.setStyleHint(QtGui.QFont.Monospace)
        self.output_log.setFont(font)

        # ── Resultados almacenados (OOP) ──
        self.resultado_cramer         = None
        self.resultado_multiplicacion = None
        self.resultado_transpuesta    = None

        # ── Conectar botones de test ──
        self.btn_test_cramer.clicked.connect(self.cargar_test_cramer)
        self.btn_test_multi.clicked.connect(self.cargar_test_multiplicacion)
        self.btn_test_trans.clicked.connect(self.cargar_test_transpuesta)

        # ── Conectar botones de operacion ──
        self.btn_calc_cramer.clicked.connect(self.ejecutar_cramer)
        self.btn_calc_multi.clicked.connect(self.ejecutar_multiplicacion)
        self.btn_calc_trans.clicked.connect(self.ejecutar_transpuesta)

        # ── Conectar limpiar ──
        self.btn_limpiar.clicked.connect(self._limpiar_todo)

        self._bienvenida()
        self.show()

    # ──────────────────────────────────────────
    # HELPERS
    # ──────────────────────────────────────────

    def _bienvenida(self):
        msg = (
            "  Instrucciones:\n"
            "  1. Usa los botones  [Cargar Test]  para pre-cargar\n"
            "     los datos del documento de referencia.\n"
            "  2. O ingresa tu propia matriz en los campos de texto.\n"
            "     Formato: valores separados por coma, una fila por linea\n"
            "     Ejemplo: 2, 1, -1\n"
            "              -3, -1, 2\n"
            "              -2, 1, 2\n"
            "  3. Presiona el boton de la operacion deseada.\n\n"
        )
        self.output_log.setPlainText(msg)

    def _limpiar_todo(self):
        self.input_matriz_a.clear()
        self.input_matriz_b.clear()
        self.resultado_cramer         = None
        self.resultado_multiplicacion = None
        self.resultado_transpuesta    = None
        self.output_log.clear()
        self._bienvenida()

    def _mostrar_resultado(self, texto: str):
        self.output_log.append("\n" + texto + "\n")

    def _mostrar_error(self, operacion: str, excepcion: Exception):
        msg = (
            f"\n{'─' * 60}\n"
            f"  ERROR en {operacion}\n"
            f"{'─' * 60}\n"
            f"  {type(excepcion).__name__}: {excepcion}\n\n"
            f"  Verifica que los datos sean correctos:\n"
            f"  * Valores numericos separados por coma\n"
            f"  * Una fila por linea\n"
            f"  * Para Cramer: b debe tener un numero por fila\n"
            f"{'─' * 60}\n"
        )
        self.output_log.append(msg)

    # ──────────────────────────────────────────
    # CARGA DE TESTS
    # ──────────────────────────────────────────

    def cargar_test_cramer(self):
        self.input_matriz_a.setPlainText(self.TEST_CRAMER_A)
        self.input_matriz_b.setPlainText(self.TEST_CRAMER_B)
        self.output_log.append(
            "\n  [TEST] Cramer cargado - Sistema 3x3\n"
            "    2x + y - z = 8\n"
            "    -3x - y + 2z = -11\n"
            "    -2x + y + 2z = -3\n"
            "    Resultado esperado: x=2, y=3, z=-1\n"
        )

    def cargar_test_multiplicacion(self):
        self.input_matriz_a.setPlainText(self.TEST_MULTI_A)
        self.input_matriz_b.setPlainText(self.TEST_MULTI_B)
        self.output_log.append(
            "\n  [TEST] Multiplicacion cargado - Matrices 3x3\n"
            "    A = [1,2,3 / 4,5,6 / 7,8,9]\n"
            "    B = [9,8,7 / 6,5,4 / 3,2,1]\n"
            "    Resultado esperado: C = [30,24,18 / 84,69,54 / 138,114,90]\n"
        )

    def cargar_test_transpuesta(self):
        self.input_matriz_a.setPlainText(self.TEST_TRANS_A)
        self.input_matriz_b.clear()
        self.output_log.append(
            "\n  [TEST] Transpuesta cargado - Matriz 3x4\n"
            "    A = [1,2,3,4 / 5,6,7,8 / 9,10,11,12]\n"
            "    Resultado esperado: At = matriz 4x3\n"
        )

    # ──────────────────────────────────────────
    # OPERACIONES — usan las clases de logic.py
    # ──────────────────────────────────────────

    def ejecutar_cramer(self):
        """
        Flujo OOP:
          Parser -> Matriz, vector
          SistemaLineal(A, b)
          OperacionCramer(sistema).ejecutar() -> ResultadoCramer
          resultado.como_texto() -> mostrar
        """
        texto_a = self.input_matriz_a.toPlainText().strip()
        texto_b = self.input_matriz_b.toPlainText().strip()

        if not texto_a or not texto_b:
            self.output_log.append(
                "\n  Ingresa la Matriz A y el Vector b antes de continuar.\n"
                "  Usa [Cargar Test Cramer] para el ejemplo.\n"
            )
            return

        try:
            # 1. Parsear entradas con la clase Parser
            A = Parser.matriz(texto_a)
            b = Parser.vector(texto_b)

            # 2. Construir el contenedor del sistema
            sistema = SistemaLineal(A=A, b=b)

            # 3. Ejecutar la operacion (almacena todo en el objeto resultado)
            operacion = OperacionCramer(sistema)
            self.resultado_cramer = operacion.ejecutar()

            # 4. Mostrar el reporte completo
            self._mostrar_resultado(self.resultado_cramer.como_texto())

        except Exception as e:
            self._mostrar_error("Regla de Cramer", e)

    def ejecutar_multiplicacion(self):
        """
        Flujo OOP:
          Parser -> Matriz A, Matriz B
          OperacionMultiplicacion(A, B).ejecutar() -> ResultadoMultiplicacion
          resultado.como_texto() -> mostrar
        """
        texto_a = self.input_matriz_a.toPlainText().strip()
        texto_b = self.input_matriz_b.toPlainText().strip()

        if not texto_a or not texto_b:
            self.output_log.append(
                "\n  Ingresa la Matriz A y la Matriz B antes de continuar.\n"
                "  Usa [Cargar Test Multiplicar] para el ejemplo.\n"
            )
            return

        try:
            # 1. Parsear ambas matrices
            A = Parser.matriz(texto_a)
            B = Parser.matriz(texto_b)

            # 2. Ejecutar (valida dimensiones internamente)
            operacion = OperacionMultiplicacion(A=A, B=B)
            self.resultado_multiplicacion = operacion.ejecutar()

            # 3. Mostrar
            self._mostrar_resultado(self.resultado_multiplicacion.como_texto())

        except Exception as e:
            self._mostrar_error("Multiplicacion de Matrices", e)

    def ejecutar_transpuesta(self):
        """
        Flujo OOP:
          Parser -> Matriz A
          OperacionTranspuesta(A).ejecutar() -> ResultadoTranspuesta
          resultado.como_texto() -> mostrar
        """
        texto_a = self.input_matriz_a.toPlainText().strip()

        if not texto_a:
            self.output_log.append(
                "\n  Ingresa la Matriz A antes de continuar.\n"
                "  Usa [Cargar Test Transpuesta] para el ejemplo.\n"
            )
            return

        try:
            # 1. Parsear
            A = Parser.matriz(texto_a)

            # 2. Ejecutar
            operacion = OperacionTranspuesta(A=A)
            self.resultado_transpuesta = operacion.ejecutar()

            # 3. Mostrar
            self._mostrar_resultado(self.resultado_transpuesta.como_texto())

        except Exception as e:
            self._mostrar_error("Transpuesta", e)

    # ──────────────────────────────────────────
    # CIERRE
    # ──────────────────────────────────────────

    def closeEvent(self, event):
        if hasattr(self, "_stream"):
            self._stream.restore()
        super().closeEvent(event)