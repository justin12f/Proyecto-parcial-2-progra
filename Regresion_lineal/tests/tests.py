from Regresion_lineal.clases.logic import Logic 

class TestData:
    def __init__(self, b0, b1, rxy, rsquare, yk):
        self.B0 = b0
        self.B1 = b1
        self.Rxy = rxy
        self.Rsquare = rsquare
        self.YK = yk

class RealTests:

    test1 = TestData(-22.55, 1.7279, 0.9545, 0.9111, 644.429)
    test2 = TestData(-4.039, 0.1681, 0.9333, 0.8711, 60.858)
    test3 = TestData(-23.92, 1.43097, 0.9631, 0.9276, 528.4294)
    test4 = TestData(-4.604, 0.140164, 0.9480, 0.8988, 49.4994)

    mis_tests = [test1, test2, test3, test4]


class CalcTests ( ) : 
    # Test 1
    test1 = Logic(x_input=[130, 650, 99, 150, 128, 302, 95, 945, 368, 961], 
                    y_input=[186, 1131, 175, 272, 214, 426, 190, 1630, 567, 1712], 
                    XK=386.0)

    # Test 2
    test2 = Logic(x_input=[130, 650, 99, 150, 128, 302, 95, 945, 368, 961], 
                    y_input=[15.0, 69.9, 6.5, 22.4, 28.4, 65.9, 19.4, 198.7, 38.8, 138.2], 
                    XK=386.0)

    # Test 3
    test3 = Logic(x_input=[163, 765, 141, 166, 137, 355, 136, 1206, 433, 1130], 
                    y_input=[186, 1131, 175, 272, 214, 426, 190, 1630, 567, 1712], 
                    XK=386.0)

    # Test 4
    test4 = Logic(x_input=[163, 765, 141, 166, 137, 355, 136, 1206, 433, 1130], 
                    y_input=[15.0, 69.9, 6.5, 22.4, 28.4, 65.9, 19.4, 198.7, 38.8, 138.2], 
                    XK=386.0)
                    
    mis_tests = [test1, test2, test3, test4]