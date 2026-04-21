import math


class Logic:
    def __init__(self, x, dof):
        self.x = x
        self.dof = dof
        self.num_seg = 10
        self.E = 0.0000001
        self.p = self.p()

    def t_distr(self, x):
        dof = self.dof
        log_const = (
            math.lgamma((dof + 1) / 2)
            - (0.5 * math.log(dof * math.pi))
            - math.lgamma(dof / 2)
        )

        term_potencia = (1 + (x**2 / dof)) ** (-(dof + 1) / 2)

        r_value = math.exp(log_const) * term_potencia

        return r_value

    def sumatorias(self, num_seg):
        t_distr = self.t_distr
        W = self.x / num_seg
        valuelist1 = []
        valuelist2 = []

        for i in range(0, num_seg):
            if i % 2:
                value1 = 4 * t_distr(i * W)
                valuelist1.append(value1)
            else:
                value2 = 2 * t_distr(i * W)
                valuelist2.append(value2)

        sum1 = sum(valuelist1)
        sum2 = sum(valuelist2)

        return sum1, sum2

    def p(self):
        num_seg = self.num_seg
        F0 = self.t_distr(0)
        FX = self.t_distr(self.x)

        def simpson(n):
            W = self.x / n
            sum1, sum2 = 0, 0

            for i in range(1, n):
                if i % 2 == 0:
                    sum2 += 2 * self.t_distr(i * W)
                else:
                    sum1 += 4 * self.t_distr(i * W)

            return (W / 3) * (F0 + sum1 + sum2 + FX)

        p1 = simpson(num_seg)
        p2 = simpson(num_seg * 2)

        while abs(p1 - p2) > self.E:
            num_seg *= 2
            p1 = p2
            p2 = simpson(num_seg * 2)

        return p2
