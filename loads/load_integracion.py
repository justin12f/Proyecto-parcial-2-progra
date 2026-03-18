from PyQt5 import QtWidgets , uic 
from integracion_numerica.clases.logica import Logic

class LoadIntegracion ( QtWidgets.QWidget ) :
    def __init__ ( self ) : 
        super().__init__ ( )
        uic.loadUi( "gui/integracion_window.ui"  , self )
        self.show() 

        self.btn_calcular.clicked.connect( self.calcularP )


        
    def calcularP( self ):

        x_val = float( self.input_x.text( ) )
        dof_val = float( self.input_dof.text( ) )

        objeto_integracion = Logic( x_val, dof_val )
        self.output_p.setText( str( objeto_integracion.p ) )