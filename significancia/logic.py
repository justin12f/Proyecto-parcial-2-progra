from integracion_inversa.logic import Logic as integracion_inversa
from integracion_numerica.clases.logica import Logic as simpson
from Regresion_lineal.clases.logic import Logic as regresion_lineal
import numpy as np


class Logic:
    """
    Significancia 

    
       x_stat = |rxy * sqrt(n-2)| / sqrt(1 - rxy^2)
       p      = integral(t_distr, 0 -> x_stat, dof = n-2)
       tail   = 1 - 2*p
       Range  = t(0.35, dof) * sigma * sqrt(1 + 1/n + (xk-xmean)^2/sum((xi-xmean)^2))
       UPI    = yk + Range
       LPI    = yk - Range

      tail <= 0.05  -> fuerte evidencia de correlacion
      tail >= 0.20  -> correlacion debida al azar
    """

    def _regresion(self, x, y):
        return regresion_lineal(list(x), list(y))

    def sigma(self, x, y):
        """Desviacion estandar de los residuos."""
        reg = self._regresion(x, y)
        n = len(x)
        residuals = y - (reg.B0 + reg.B1 * x)
        return float(np.sqrt(np.sum(residuals ** 2) / (n - 2)))

    def rxy(self, x, y):
        """Coeficiente de correlacion de Pearson."""
        reg = self._regresion(x, y)
        return float(reg.Rxy)

    def rsquare(self, x, y):
        """Coeficiente de determinacion r^2."""
        reg = self._regresion(x, y)
        return float(reg.Rsquare)

    def x_stat(self, x, y):
        """Estadistico t para probar la significancia de la correlacion.
           x = |rxy * sqrt(n-2)| / sqrt(1 - rxy^2)
        """
        r = self.rxy(x, y)
        n = len(x)
        return float(abs(r * np.sqrt(n - 2)) / np.sqrt(1 - r ** 2))

    def p_integral(self, x, y):
        """Probabilidad p = integral de la distribucion t desde 0 hasta x_stat
           con dof = n-2.
        """
        x_val = self.x_stat(x, y)
        n = len(x)
        dof = n - 2
        obj = simpson(x_val, dof)
        return float(obj.p)

    def tail_area(self, x, y):
        """Area de cola = 1 - 2*p.
           Si tail <= 0.05  -> fuerte evidencia de correlacion.
           Si tail >= 0.20  -> correlacion debida al azar.
        """
        p = self.p_integral(x, y)
        return float(1 - 2 * p)

    def yk(self, xk, x, y):
        """Valor predicho yk = B0 + B1*xk."""
        reg = self._regresion(x, y)
        return float(reg.B0 + reg.B1 * xk)

    def prediction_range(self, xk, x, y):
        """Range del intervalo de prediccion al 70%:
           Range = t(0.35, dof) * sigma * sqrt(1 + 1/n + (xk-xmean)^2/sum((xi-xmean)^2))
           donde dof = n-2 y t(0.35, dof) se obtiene via integracion inversa.
        """
        n = len(x)
        dof = n - 2
        # t para p=0.35 con dof grados de libertad (70% interval -> cola = 0.35)
        t_val = float(integracion_inversa(dof, 0.35).encontrar_x())
        sig = self.sigma(x, y)
        xmean = float(np.mean(x))
        xk_f = float(xk)

        factor = np.sqrt(
            1 + (1 / n) + ((xk_f - xmean) ** 2) / float(np.sum((x - xmean) ** 2))
        )
        return float(t_val * sig * factor)

    def upi(self, xk, x, y):
        """Upper Prediction Interval = yk + Range."""
        return self.yk(xk, x, y) + self.prediction_range(xk, x, y)

    def lpi(self, xk, x, y):
        """Lower Prediction Interval = yk - Range."""
        return self.yk(xk, x, y) - self.prediction_range(xk, x, y)

    def beta0(self, x, y):
        return float(self._regresion(x, y).B0)

    def beta1(self, x, y):
        return float(self._regresion(x, y).B1)

    def full_results(self, xk, x, y):
        """Devuelve todos los resultados como diccionario."""
        reg = self._regresion(x, y)
        r = float(reg.Rxy)
        r2 = float(reg.Rsquare)
        b0 = float(reg.B0)
        b1 = float(reg.B1)
        yk_val = float(b0 + b1 * float(xk))
        sig = self.sigma(x, y)
        tail = self.tail_area(x, y)
        rang = self.prediction_range(xk, x, y)
        return {
            "rxy":   r,
            "r2":    r2,
            "tail":  tail,
            "beta0": b0,
            "beta1": b1,
            "yk":    yk_val,
            "sigma": sig,
            "range": rang,
            "upi":   yk_val + rang,
            "lpi":   yk_val - rang,
        }
