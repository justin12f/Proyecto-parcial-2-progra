from PyQt5 import QtWidgets , uic 
from loads.load_regresion_lineal import LoadRegresionLineal
from loads.load_integracion import LoadIntegracion

class LoadPrincipal ( QtWidgets.QMainWindow ) :
    def __init__ ( self ) : 
        super().__init__ ( )
        uic.loadUi( "gui/main_window.ui"  , self )
        self.show() 

        self.btnIntegracion.clicked.connect( self.regresion )
        self.btnRegresion.clicked.connect( self.integracion )
        
 

    def regresion ( self ) : 
        
        self.loadregresion = LoadRegresionLineal( )

    def integracion ( self ) : 
        self.loadintegracion = LoadIntegracion( )

