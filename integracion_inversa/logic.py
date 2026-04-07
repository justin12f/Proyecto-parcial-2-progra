from integracion_numerica.clases.logica import Logic as simpson


class Logic:
    def __init__(self, dof, p, inicial_x=10, d=0.5, error=0.00001):
        self.dof = dof
        self.p = p
        self.inicial_x = inicial_x
        self.d = d
        self.error = error
        self.signo_inicial = None

    def encontrar_x(self):
        x = self.inicial_x
        d = self.d
        p_objetivo = self.p - 0.5
        signo_error_previo = None
        error_aceptable = self.error

        while True:
            p_object = simpson(x, self.dof)
            p_actual = p_object.p

            error = p_actual - p_objetivo

            if abs(error) < error_aceptable:
                return x

            signo_actual = 1 if error > 0 else -1

            if signo_error_previo is not None and signo_actual != signo_error_previo:
                d = d / 2
            if signo_actual == 1:
                x -= d
            else:
                x += d

            signo_error_previo = signo_actual


test = Logic(15, 0.95)
x = str(test.encontrar_x())
print(x)
