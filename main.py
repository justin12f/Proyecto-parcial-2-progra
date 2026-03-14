
from numpy.testing import clear_and_catch_warnings
from loads.load_regresion_lineal import LoadRegresionLineal
from PyQt5 import QtWidgets
import sys

def main ( ) : 
    app = QtWidgets.QApplication ( sys.argv )
    regresion = LoadRegresionLineal()
    sys.exit(app.exec_())

            
if __name__ == "__main__" :
    main()
