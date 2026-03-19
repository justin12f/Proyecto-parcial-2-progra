from loads.load_principal_window import LoadPrincipal

from PyQt5 import QtWidgets
import sys

def main ( ) : 

    app = QtWidgets.QApplication ( sys.argv )
    principal = LoadPrincipal()
    sys.exit( app.exec_( ) )

            
if __name__ == "__main__" :
    main( )
