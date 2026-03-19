from PyQt5 import QtWidgets , uic 
from loads.load_regresion_lineal import LoadRegresionLineal
from loads.load_integracion import LoadIntegracion

class LoadPrincipal ( QtWidgets.QWidget ) :
    def __init__ ( self ) : 
        super().__init__ ( )
        uic.loadUi( "gui/main_window.ui"  , self )
        self.show() 


        loadregresion = LoadRegresionLineal( )
        loadintegracion = LoadIntegracion( )
