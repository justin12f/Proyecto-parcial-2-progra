from PyQt5 import QtWidgets , uic 
from loads.load_regresion_lineal import LoadRegresionLineal
from loads.load_integracion import LoadIntegracion
from loads.load_integracion_inversa import LoadIntegracionInversa

class LoadPrincipal ( QtWidgets.QMainWindow ) :
    def __init__ ( self ) : 
        super().__init__ ( )
        uic.loadUi( "gui/main_window.ui"  , self )
        self.show() 

        self.actionRegresion.triggered.connect( self.integracion )
        self.actionIntegracion.triggered.connect( self.regresion)
        self.actionIntegracionInversa.triggered.connect( self.integracion_inversa )
        self.btnIntegracion.clicked.connect( self.integracion )
        self.btnRegresion.clicked.connect( self.regresion )
        self.btnIntegracionInversa.clicked.connect( self.integracion_inversa )
        
 

    def regresion ( self ) : 
        
        self.loadregresion = LoadRegresionLineal( )

    def integracion ( self ) : 
        self.loadintegracion = LoadIntegracion( )

    def integracion_inversa ( self ) :
        self.loadintegracioninversa = LoadIntegracionInversa( )

