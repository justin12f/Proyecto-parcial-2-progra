
import math
import numpy as np 
from abc import ABC , abstractmethod

class LogicAB ( ABC ) :
        def __init__( self  , X : list, Y : list , XK : float = 0   ) :
            self.X = np.array( X ) 
            self.Y = np.array ( Y )
            self.N = self.calculate_N()
            self.XK = XK

            self.Xaverage = np.mean( self.X )
            self.Yaverage = np.mean ( self.Y )

            self.Xsum = np.sum( self.X )
            self.Ysum = np.sum( self.Y )

            self.SumXsquare = np.sum( self.X ** 2 )
            self.SumYsquare = np.sum( self.Y ** 2 )

            self.Xsquare_average = np.mean( self.X **2 ) 
            self.Ysquare_average = np.mean( self.Y **2 ) 

            self.SPxy = math.sumprod ( self.X , self.Y )

            self.B1 = self.calculate_B1()
            self.B0 = self.calculate_B0()

            self.Rxy = self.calculate_Rxy()
            self.Rsquare = self.calculate_Rsquare()
            self.YK = self.calculate_YK()


        @abstractmethod
        def calculate_N ( self ) : 
            pass

        @abstractmethod
        def calculate_Xaverage ( self ) : 
            pass
        @abstractmethod
        def calculate_Yaverage ( self ) : 
            pass

        @abstractmethod
        def calculate_Xsum ( self ) : 
            pass
        @abstractmethod
        def calculate_Ysum ( self ) : 
            pass


        @abstractmethod
        def calculate_SumXsquare ( self ) : 
            pass
        @abstractmethod
        def calculate_SumYsquare ( self ) : 
            pass

        @abstractmethod
        def calculate_Xsquare_average ( self ) : 
            pass
        @abstractmethod
        def calculate_Ysquare_average ( self ) : 
            pass

        @abstractmethod
        def calculate_SPxy ( self ) : 
            pass


        @abstractmethod
        def calculate_B1 ( self ) : 
            pass
        @abstractmethod
        def calculate_B0 ( self ) : 
            pass
        

        @abstractmethod
        def calculate_Rxy ( self ) : 
            pass
        @abstractmethod
        def calculate_Rsquare ( self ) : 
            pass
        @abstractmethod
        def calculate_YK ( self ) : 
            pass


class Logic : 
    def __init__( self  , X : list, Y : list , XK : float = 0   ) :
        super().__init__( X , Y , XK )

    def calculate_N ( self ) : 
        if len( self.X ) == len( self.Y ) :
            N = len( self.X )
            return N 
        else : 
            raise ValueError ( "las listas deben de tener el mismo largo" )
        

    def calculate_B1 ( self ) : 

        NXY = ( self.N * self.Xaverage * self.Yaverage )
        NXsquare_average = ( self.N * self.Xsquare_average )

        B1 = ( ( self.SPxy  - NXY ) / ( self.SumXsquare - NXsquare_average ) )
        return B1
    
    def calculate_B0 ( self ) :
        B0 = self.Yaverage - ( self.B1 * self.Xaverage )
        return B0
    

    def calculate_Rxy ( self ) : 
        NSPxy = ( self.N * self.SPxy )
        SxSy = ( self.Xsum * self.Ysum )
        NsumXsquare = ( self.N * self.SumXsquare )
        NsumYsquare = ( self.N * self.SumYsquare )
        square_sumX = ( self.Xsum ** 2 )
        square_sumY = ( self.Ysum ** 2 )

        Rxy =  ( ( NSPxy  - SxSy ) / math.sqrt( ( ( NsumXsquare - square_sumX ) * ( NsumYsquare - square_sumY ) ) ) ) 

        return Rxy 
    
    def calculate_Rsquare ( self ) : 
        Rsquare = self.Rxy ** 2 
        return Rsquare
    
    
    def calculate_YK ( self ) : 
        YK = ( self.B0 + ( self.B1 * self.XK ) )
        return YK

    


        



    

    

