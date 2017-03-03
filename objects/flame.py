from random import *

from core.base import *
from core.components import *
import source

class Flame ( GameObject ):
    def __init__ ( self , center ) :        
        self.render = Render ( image=source.sprites['flame'][randrange(0,3)].copy() , tag = 'flame' , scale_origin = 1)
        self.render.position = Vector2 ( center.x + (-70 + random()*140) , center.y + (-70 + random()*140) )
        self.render.scale = 0.5 + random()*2
        self.multiply = 0.001 + random()*0.8
        self.physics = Physics()

    #abstract implementation
    def bind ( self , camera ) :
        self.render.bindCamera ( camera )
        
    #abstract implementation
    def update ( self ) :
        self.render.scale = multiply_fps ( self.render.scale , self.multiply )
        self.physics.update(self.render)
    #abstract implementation
    def draw ( self , screen ):
        self.render.draw ( screen )

class FlameManager ( GameObject ) :    
    def __init__ ( self ) :
        self.__flameList = []
        self.__flamePerExplosion = 5
        self.__maxFlame = 100
        self.__stop = False

    #abstract implementation
    def bind ( self , camera ) :
        self.__camera = camera

    #abstract implementation
    def update ( self ) :        
        for flame in list ( self.__flameList ) :
            flame.update()
            if flame.render.scale <= 0.1 :
                self.__flameList.remove ( flame )

    #abstract implementation
    def draw ( self , screen ) :
        for flame in self.__flameList  :
            flame.draw ( screen )
    
    def getFlameCount ( self ) :
        return len ( self.__flameList )

    def createExplosion ( self , center ) :
        if self.__stop :
            return
        
        sumFlame = self.getFlameCount() + self.__flamePerExplosion
        
        if sumFlame > self.__maxFlame :
            for i in range ( sumFlame - self.__maxFlame ) :
                self.__flameList.remove ( self.__flameList[0] )
            
        for i in range ( self.__flamePerExplosion ) :
            self.__flameList.append ( Flame ( center ) )
            self.__flameList[-1].bind ( self.__camera )

    def stop ( self ) :
        self.__stop = True
        for flame in self.__flameList :
            flame.multiply = lerp ( flame.multiply , 1.0 , 0.85 )

class FlameShooter ( GameObject ) :
    def __init__ ( self ) :
        self.__flameList = []
        self.__time = 0
        self.__period = 0.0
        
        self.__stop = False
        
    #abstract implementation
    def update ( self ) :
        if self.__stop :
            return

        self.__time += setting.frt
        if self.__time >= self.__period :
            self.create ( )
                
        for flame in list ( self.__flameList ) :
            flame.update()
            if flame.render.scale <= 0.1 :
                self.__flameList.remove ( flame )

    #abstract implementation
    def draw ( self , screen ) :
        for flame in self.__flameList  :
            flame.draw ( screen )

    def create ( self ) :
        if self.__stop :
            return        

        center = Vector2 ( random() * setting.size_screen[0] , setting.size_screen[1] -50 )
        flame = Flame ( center )
        flame.multipy = 0.9999
        flame.physics.v = Vector2 ( 0 , 0 )
        flame.physics.a.y = -50
        self.__flameList.append ( flame )
        

    def stop ( self ) :
        self.__stop = True
        for flame in self.__flameList :
            flame.multiply = lerp ( flame.multiply , 1.0 , 0.85 )
            
        
    
