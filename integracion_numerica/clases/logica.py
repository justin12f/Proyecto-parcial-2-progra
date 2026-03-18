
import math 

    



class Logic : 
    def __init__ ( self , x , dof   ) : 
        self.x = x 
        self.dof = dof 
        self.num_seg = 10 
        self.E = 0.00001
        self.p = self.p()
        
       
        


    def t_distr(self, x):
        dof = self.dof
        gamma = math.gamma
        pi = math.pi
        
        num_const = gamma((dof + 1) / 2)
        
        den_const = ((dof * pi) ** 0.5) * gamma(dof / 2)
        
        term_potencia = (1 + (x**2 / dof)) ** (-(dof + 1) / 2)
        
        r_value = (num_const / den_const) * term_potencia

        return r_value

    def sumatorias ( self , num_seg ) : 
        t_distr = self.t_distr
        W = self.x / num_seg
        valuelist1 = []
        valuelist2 = []

        for i in range( 0 , num_seg ) : 
            if i % 2  : 
                value1 =  4 * t_distr( i * W  )
                valuelist1.append( value1)
            else :
                value2 =  2 * t_distr( i * W  )
                valuelist2.append( value2 )

        sum1 = sum( valuelist1 )
        sum2 = sum( valuelist2 ) 

        return sum1 , sum2 
    
    def p ( self ) : 
        num_seg1 = self.num_seg
        num_seg2 = self.num_seg**2

        W1= ( self.x / num_seg1 ) / 3 
        W2= ( self.x / num_seg2 ) / 3 

        sum1 , sum2 = self.sumatorias( num_seg1 )
        sum11 , sum22 = self.sumatorias( num_seg2 )
        F0 = self.t_distr( 0 )
        FX = self.t_distr( self.x )

        p1= W1*( F0 + sum1 + sum2 + FX )
        p2 = W2*( F0 + sum11 + sum22 + FX )

        while ( abs( p1 ) - abs( p2 ) ) > self.E :
            p1 = p2 

            self.num_seg *= 2
            sum1 , sum2 = self.sumatorias( self.num_seg )

            p2 = W1*( F0 + sum1 + sum2 + FX )

        return p1 
    




        
    



            