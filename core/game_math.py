#core math
import setting
import math

def multiply_fps ( x , m ) :
    return x + (x*m - x)*( setting.frt )

def add_fps ( x , a ) :
    return x + a*( setting.frt ) 

def lerp ( a , b , ratio ) :
    return a + (b-a)*ratio

def lerp_fps ( a , b , ratio ) :
    return a + (b-a)*ratio*setting.frt

def clamp ( value , cap_min , cap_max ) :
    if value < cap_min :
        return cap_min
    elif value > cap_max :
        return cap_max
    else :
        return value

class IntVector2 :
    def __init__ ( self , x = 0 , y = 0 ) :
        self.x = int(x)
        self.y = int(y)

class Vector2:
    def __init__ ( self , x = 0 , y = 0 ) :
        self.x = x
        self.y = y

    def add ( self , v2 ) :
        self.x += v2.x
        self.y += v2.y

    def multiply ( self , m ) :
        self.x *= m
        self.y *= m

    def lerp ( self , dest , ratio) :
        self.x = lerp ( self.x , dest.x , ratio )
        self.y = lerp ( self.y , dest.y , ratio )

    def lerp_fps ( self , dest , ratio ) :
        self.x = lerp_fps ( self.x , dest.x , ratio )
        self.y = lerp_fps ( self.y , dest.y , ratio )

    def add_fps ( self , v2 ) :
        self.x = add_fps ( self.x , v2.x )
        self.y = add_fps ( self.y , v2.y )
        
    def multiply_fps ( self , m ) :
        self.x = multiply_fps ( self.x , m )
        self.y = multiply_fps ( self.y , m )

    def magnitude ( self ) :
        return math.sqrt ( self.x**2 + self.y**2 )

    def one ( self ) :
        if self.magnitude() == 0 :
            return Vector2 ( 0, 0 )

        result = Vector2 ( self.x , self.y )
        result.multiply ( 1/self.magnitude() )
        return result

    def distance ( self , v2 ) :
        dx = self.x - v2.x
        dy = self.y - v2.y
        return math.sqrt ( dx**2 + dy**2 )
    
        
