
#from loads.load_regresion_lineal import LoadRegresionLineal
from loads.load_integracion import LoadIntegracion
from PyQt5 import QtWidgets
import sys

def main ( ) : 

    app = QtWidgets.QApplication ( sys.argv )
    #loadregresion = LoadRegresionLineal()
    loadintegracion = LoadIntegracion( )
    sys.exit( app.exec_( ) )

            
if __name__ == "__main__" :
    main( )
