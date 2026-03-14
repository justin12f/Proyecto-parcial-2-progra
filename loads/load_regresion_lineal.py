from PyQt5 import QtWidgets , uic 
from Regresion_lineal.tests.tests import CalcTests , RealTests

test1c , test2c , test3c , test4c = CalcTests.mis_tests
test1r , test2r , test3r , test4r = RealTests.mis_tests

class LoadRegresionLineal ( QtWidgets.QMainWindow ) :
    def __init__ ( self ) : 
        super().__init__ ( )
        uic.loadUi( "gui/regresion_window.ui"  , self )
        self.show() 

        self.btn_test_1.clicked.connect( self.test1 )
        self.btn_test_2.clicked.connect( self.test2 )
        self.btn_test_3.clicked.connect( self.test3 )
        self.btn_test_4.clicked.connect( self.test4 )

    def test1 ( self ) :

        self.lbl_real_b0.setText( str ( test1r.B0 ) )  
        self.lbl_real_b1.setText( str ( test1r.B1 ) )  
        self.lbl_real_rxy.setText( str ( test1r.Rxy ) )  
        self.lbl_real_r2.setText( str ( test1r.Rsquare ) )  
        self.lbl_real_yk.setText( str ( test1r.YK ) )  



        self.lbl_calc_b0.setText( str ( test1c.B0 ) )  
        self.lbl_calc_b1.setText( str ( test1c.B1 ) )  
        self.lbl_calc_rxy.setText( str ( test1c.Rxy ) )  
        self.lbl_calc_r2.setText( str ( test1c.Rsquare ) )  
        self.lbl_calc_yk.setText( str ( test1c.YK ) )  

    def test2 ( self ) :

        self.lbl_real_b0.setText( str ( test2r.B0 ) )  
        self.lbl_real_b1.setText( str ( test2r.B1 ) )  
        self.lbl_real_rxy.setText( str ( test2r.Rxy ) )  
        self.lbl_real_r2.setText( str ( test2r.Rsquare ) )  
        self.lbl_real_yk.setText( str ( test2r.YK ) )  



        self.lbl_calc_b0.setText( str ( test2c.B0 ) )  
        self.lbl_calc_b1.setText( str ( test2c.B1 ) )  
        self.lbl_calc_rxy.setText( str ( test2c.Rxy ) )  
        self.lbl_calc_r2.setText( str ( test2c.Rsquare ) )  
        self.lbl_calc_yk.setText( str ( test2c.YK ) )  

    def test3 ( self ) :

        self.lbl_real_b0.setText( str ( test3r.B0 ) )  
        self.lbl_real_b1.setText( str ( test3r.B1 ) )  
        self.lbl_real_rxy.setText( str ( test3r.Rxy ) )  
        self.lbl_real_r2.setText( str ( test3r.Rsquare ) )  
        self.lbl_real_yk.setText( str ( test3r.YK ) )  



        self.lbl_calc_b0.setText( str ( test3c.B0 ) )  
        self.lbl_calc_b1.setText( str ( test3c.B1 ) )  
        self.lbl_calc_rxy.setText( str ( test3c.Rxy ) )  
        self.lbl_calc_r2.setText( str ( test3c.Rsquare ) )  
        self.lbl_calc_yk.setText( str ( test3c.YK ) )  

    def test4 ( self ) :

        self.lbl_real_b0.setText( str ( test4r.B0 ) )  
        self.lbl_real_b1.setText( str ( test4r.B1 ) )  
        self.lbl_real_rxy.setText( str ( test4r.Rxy ) )  
        self.lbl_real_r2.setText( str ( test4r.Rsquare ) )  
        self.lbl_real_yk.setText( str ( test4r.YK ) )  



        self.lbl_calc_b0.setText( str ( test4c.B0 ) )  
        self.lbl_calc_b1.setText( str ( test4c.B1 ) )  
        self.lbl_calc_rxy.setText( str ( test4c.Rxy ) )  
        self.lbl_calc_r2.setText( str ( test4c.Rsquare ) )  
        self.lbl_calc_yk.setText( str ( test4c.YK ) )  

