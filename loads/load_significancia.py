import numpy as np
from PyQt5 import QtWidgets, uic
from significancia.logic import Logic

# ── Historical data from Table 1 ────────────────────────────────────────────
_X  = [130, 650, 99, 150, 128, 302, 95, 945, 368, 961]   # Estimated Proxy Size
_Y1 = [186, 699, 132, 272, 291, 331, 199, 1890, 788, 1601] # Actual Added/Modified Size
_Y2 = [15.0, 69.9, 6.5, 22.4, 28.4, 65.9, 19.4, 198.7, 38.8, 138.2]  # Dev Hours
_XK = 386.0

TESTS = [
    {
        "label": "Caso 1",
        "x":  _X,
        "y":  _Y1,
        "xk": _XK,
    },
    {
        "label": "Caso 2",
        "x":  _X,
        "y":  _Y2,
        "xk": _XK,
    },
]


class LoadSignificancia(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("gui/significancia_window.ui", self)
        self.show()

        self._logic = Logic()

        self.btn_calcular.clicked.connect(self._calcular)
        self.btn_test1.clicked.connect(lambda: self._cargar_test(0))
        self.btn_test2.clicked.connect(lambda: self._cargar_test(1))

    # ── helpers ──────────────────────────────────────────────────────────────
    def _cargar_test(self, idx: int):
        t = TESTS[idx]
        self.input_x.setText(", ".join(str(v) for v in t["x"]))
        self.input_y.setText(", ".join(str(v) for v in t["y"]))
        self.input_xk.setText(str(t["xk"]))
        self._calcular()

    def _limpiar_resultados(self):
        for name in ("out_rxy", "out_r2", "out_tail", "out_conclusion",
                     "out_b0", "out_b1", "out_yk", "out_range", "out_upi", "out_lpi"):
            getattr(self, name).clear()
        self.lbl_error.setText("")
        # Reset conclusion style
        self.out_conclusion.setStyleSheet(
            "background-color: #161b22; color: #3fb950; border: 1px solid #238636;"
            "font-weight: bold; border-radius: 5px; padding: 5px 8px;"
        )

    def _mostrar_resultados(self, res: dict):
        self.out_rxy.setText(f"{res['rxy']:.9f}")
        self.out_r2.setText(f"{res['r2']:.9f}")
        self.out_tail.setText(f"{res['tail']:.6e}")
        self.out_b0.setText(f"{res['beta0']:.9f}")
        self.out_b1.setText(f"{res['beta1']:.9f}")
        self.out_yk.setText(f"{res['yk']:.9f}")
        self.out_range.setText(f"{res['range']:.9f}")
        self.out_upi.setText(f"{res['upi']:.9f}")
        self.out_lpi.setText(f"{res['lpi']:.9f}")

        tail = res["tail"]
        if tail <= 0.05:
            conclusion = f"Significativo  (tail={tail:.2e} ≤ 0.05)"
            color = "#f85149"
            border = "#da3633"
        elif tail >= 0.20:
            conclusion = f"Azar  (tail={tail:.2e} ≥ 0.20)"
            color = "#e3b341"
            border = "#9e6a03"
        else:
            conclusion = f"Indeterminado  (0.05 < tail={tail:.2e} < 0.20)"
            color = "#58a6ff"
            border = "#1f6feb"

        self.out_conclusion.setText(conclusion)
        self.out_conclusion.setStyleSheet(
            f"background-color: #161b22; color: {color}; border: 1px solid {border};"
            f"font-weight: bold; border-radius: 5px; padding: 5px 8px;"
        )

    # ── slots ─────────────────────────────────────────────────────────────────
    def _calcular(self):
        self._limpiar_resultados()
        try:
            x_raw  = self.input_x.text().strip()
            y_raw  = self.input_y.text().strip()
            xk_raw = self.input_xk.text().strip()

            if not x_raw or not y_raw or not xk_raw:
                self.lbl_error.setText("Completa todos los campos antes de calcular.")
                return

            x  = np.array([float(v.strip()) for v in x_raw.split(",")])
            y  = np.array([float(v.strip()) for v in y_raw.split(",")])
            xk = float(xk_raw)

            if len(x) != len(y):
                self.lbl_error.setText(
                    f"Error: X tiene {len(x)} valores e Y tiene {len(y)}. Deben ser iguales."
                )
                return

            if len(x) < 3:
                self.lbl_error.setText("Se necesitan al menos 3 pares de datos.")
                return

            res = self._logic.full_results(xk, x, y)
            self._mostrar_resultados(res)
            self.statusbar.showMessage(
                f"Calculado con n={len(x)} datos, xk={xk}  |  "
                f"tail={res['tail']:.2e}  |  UPI={res['upi']:.4f}  LPI={res['lpi']:.4f}"
            )

        except ValueError as e:
            self.lbl_error.setText(f"Error de formato: {e}")
        except Exception as e:
            self.lbl_error.setText(f"Error: {e}")
            import traceback; traceback.print_exc()
