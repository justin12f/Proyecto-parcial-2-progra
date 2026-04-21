from integracion_numerica.clases.logica import Logic as simpson


class Logic:
    def __init__(self, dof, p, inicial_x=10, d=0.5, error=0.00000001):
        self.dof = dof
        self.p = p
        self.inicial_x = inicial_x
        self.d = d
        self.error = error
        self.signo_inicial = None

    def encontrar_x(self):
        a = 0.0
        b = float(self.inicial_x)
        p_objetivo = self.p
        error_aceptable = self.error

        for _ in range(1000):
            mid = (a + b) / 2.0
            p_object = simpson(mid, self.dof)
            p_actual = p_object.p

            if abs(p_actual - p_objetivo) < error_aceptable:
                return mid

            if p_actual > p_objetivo:
                b = mid
            else:
                a = mid

        return (a + b) / 2.0


test = Logic(15, 0.45)
x = str(test.encontrar_x())
print(x)
