
import math
import numpy as np 
from abc import ABC , abstractmethod
from dataclasses import dataclass , field

@dataclass
class LogicAB ( ABC ) :

        x_input: list
        y_input: list
        XK: float = 0.0 

        X: np.ndarray = field( init = False )
        Y: np.ndarray = field( init = False )
        N: int = field( init = False )
        B1: float = field( init = False )
        B0: float = field( init = False )
        
        def __post_init__ ( self ) :
            
            self.X = np.array( self.x_input ) 
            self.Y = np.array ( self.y_input )
            self.N = self.calculate_N()
            self.XK = self.XK

            self.Xaverage = np.mean( self.X )
            self.Yaverage = np.mean ( self.Y )

            self.Xsum = np.sum( self.X )
            self.Ysum = np.sum( self.Y )

            self.SumXsquare = np.sum( self.X ** 2 )
            self.SumYsquare = np.sum( self.Y ** 2 )

            self.Xsquare_average = (self.Xaverage ** 2)
            self.Ysquare_average = (self.Yaverage ** 2) 

            self.SPxy = math.sumprod ( self.X , self.Y )

            self.B1 = self.calculate_B1()
            self.B0 = self.calculate_B0()

            self.Rxy = self.calculate_Rxy()
            self.Rsquare = self.calculate_Rsquare()
            self.YK = self.calculate_YK()



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

        def __str__ ( self ) : 
            return f"N: { self.N }\nXaverage: { self.Xaverage }\nYaverage: { self.Yaverage } \nXsum: { self.Xsum }\nYsum: { self.Ysum }\nSumXsquare: { self.SumXsquare }\nSumYsquare: { self.SumYsquare }\nXsquare_average: { self.Xsquare_average }\nYsquare_average: { self.Ysquare_average }\nSPxy: { self.SPxy }\nB1: { self.B1 }\nB0: { self.B0 }\nRxy: { self.Rxy }\nRsquare: { self.Rsquare }\nYK: { self.YK } \n\n "


class Logic ( LogicAB ) : 

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
        return  B1 
    
    def calculate_B0 ( self ) :
        B0 = self.Yaverage - ( self.B1 * self.Xaverage )
        return  B0  
    

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
