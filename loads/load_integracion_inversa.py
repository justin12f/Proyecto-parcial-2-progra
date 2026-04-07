from PyQt5 import QtWidgets , uic 
from integracion_inversa.logic import Logic

class LoadIntegracionInversa ( QtWidgets.QWidget ) :
    def __init__ ( self ) : 
        super().__init__ ( )
        uic.loadUi( "gui/integracion_inversa_window.ui"  , self )
        self.show() 

        self.btn_calcular.clicked.connect( self.calcularX )

    def calcularX( self ):
        try:
            p_val = float( self.input_p.text( ) )
            dof_val = float( self.input_dof.text( ) )

            objeto_integracion = Logic( dof_val, p_val )
            resultado_x = objeto_integracion.encontrar_x()
            self.output_x.setText( str( round(resultado_x, 5) ) )
        except Exception as e:
            self.output_x.setText("Error")
            print(f"Error calculating X: {e}")
