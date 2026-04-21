from integracion_inversa.logic import Logic as integracion_inversa
from integracion_numerica.clases.logica import Logic as simpson
from Regresion_lineal.clases.logic import Logic as regresion_lineal
import numpy as np


class Logic:
    def sigma(self, x, y):
        regresion = regresion_lineal(x, y)
        n = len(x)
        beta0 = regresion.B0
        beta1 = regresion.B1

        sigma = np.sqrt((np.sum((y - (beta0 + beta1 * x)) ** 2)) / (n - 2))
        return sigma

    def range_function(self, dof, x, y):
        simpson_object = simpson(x, dof)
        t_value = simpson_object.t_distr(x)
        sigma = self.sigma(x, y)
        n = len(x)

        range_function = (t_value * sigma) * np.sqrt(
            1 + (1 / n) + ((x - np.mean(x)) ** 2) / np.sum((x - np.mean(x)) ** 2)
        )
        return range_function

    def get_x_value(self, dof, p, x, y):
        n = len(x)
        range_result = self.range_function(dof, x, y)
        numerador = abs(range_result * np.sqrt(n - 2))
        denominador = np.sqrt(1 - (range_result**2))
        x_value = numerador / denominador
        return x_value

    def tail_value(self, dof, p):
        integracion_inversa_object = integracion_inversa(dof, p)
        tail_value = integracion_inversa_object.encontrar_x()
        return tail_value


x = 130
y = 163

logic = Logic(x, y)
print(logic.get_x_value(15, 0.45, x, y))
