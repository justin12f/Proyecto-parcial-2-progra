from PyQt5 import QtWidgets , uic 
from loads.load_regresion_lineal import LoadRegresionLineal
from loads.load_integracion import LoadIntegracion

class LoadPrincipal ( QtWidgets.QMainWindow ) :
    def __init__ ( self ) : 
        super().__init__ ( )
        uic.loadUi( "gui/main_window.ui"  , self )
        self.show() 

        self.actionRegresion.triggered.connect( self.integracion )
        self.actionIntegracion.triggered.connect( self.regresion)
        self.btnIntegracion.clicked.connect( self.integracion )
        self.btnRegresion.clicked.connect( self.regresion )
        
 

    def regresion ( self ) : 
        
        self.loadregresion = LoadRegresionLineal( )

    def integracion ( self ) : 
        self.loadintegracion = LoadIntegracion( )

