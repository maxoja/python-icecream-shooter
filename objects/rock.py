from random import *

from core.base import *
from core.components import *
from core.game_math import *
import setting
import source

class Rock ( GameObject ) :
    def __init__ ( self , target , straight = False ) :
        self.render = Render( image = source.images['rock'] , \
                              tag = 'rock' ,scale_origin = 6 )
        self.physics = Physics(  )

        velocity = None
        
        space = 200
        if randint(0,1) == 1 :
            self.render.position.y = setting.size_screen[1] * random()
            if randint(0,1) == 1 : #from left to right
                self.render.position.x = -space
                velocity = Vector2 ( 150 , 0 )
            else : #from right to left
                self.render.position.x = setting.size_screen[0] + space
                velocity = Vector2 ( -150 , 0 )
        else :
            self.render.position.x = setting.size_screen[0] * random()
            if randint(0,1) == 1 : #from top to bottom
                self.render.position.y = -space
                velocity = Vector2 ( 0 , 150 )
            else :
                self.render.position.y = setting.size_screen[1] + space
                velocity = Vector2 ( 0 , -150 )

        self.physics.drag = 0.1
        self.physics.v_angular = 200 + 500*random()
        self.physics.drag_angular = 0.1
        if straight == False :
            dx = target.x - self.render.position.x
            dy = target.y - self.render.position.y
            self.physics.v = Vector2 ( dx/2 , dy/2 )
        else :
            self.physics.v = velocity

    #abstract implementation
    def bind ( self , camera , player ) :
        self.render.bindCamera ( camera )
        self.__player = player
    
    #abstract implementation
    def update ( self ) :
        self.physics.update( self.render )

    #abstract implementation
    def draw ( self ,screen ) :
        self.render.draw ( screen )

    def destroy ( self ) :
        pass

class RockManager(GameObject) :    
    def __init__ ( self ) :
        self.__rockList = []
        self.__time = 0
        self.__period = 0.5
        self.__count = 0
        
        self.__wave = 0
        self.__amount = 10

        self.__stop = False
        
    #abstract implmentation
    def bind ( self , camera , player ) :
        self.__camera = camera
        self.__player = player

    #abstract implemetation
    def update ( self ) :
        if self.__stop == False :
            self.__time += setting.frt
            if self.__time >= self.__period :
                if self.__count % 20 == 0 and self.__count != 0 :
                    for i in range ( self.__amount ) :
                        self.create(straight = True)
                else :
                    self.create ( )
                
                self.__period = clamp (self.__period*0.995 , 0.25 , 1 )
                self.__time %= self.__period
                self.__count += 1
        
        for rock in list(self.__rockList) :
            if rock.render.position.x < -setting.size_screen[0] or \
               rock.render.position.x > setting.size_screen[0]*2 or \
               rock.render.position.y < -setting.size_screen[1] or \
               rock.render.position.y > setting.size_screen[1]*2 : 
                self.__rockList.remove ( rock )
                continue
            else :
                rock.update()

    #abstract implementation
    def draw ( self , screen ) :
        for rock in self.__rockList :
            rock.draw ( screen )
            
    def create ( self , straight = False ) :
        self.__rockList.append ( Rock ( self.__player.render.position , straight = straight ) )
        self.__rockList[-1].bind ( self.__camera , self.__player )

    def shootRock ( self , rock , direction ) :
        rock.physics.v = direction
        rock.physics.v_angular *= 2
        
    def getRocks ( self ) :
        return self.__rockList

    def deleteRock ( self , rock ) :
        self.__rockList.remove ( rock )

    def stop ( self ) :
        self.__stop = True
        for rock in self.__rockList :
            rock.physics.v_angular /= 2
            rock.physics.drag_angular = 1
            rock.physics.v.multiply ( 0.25 )
            rock.physics.drag = 1



class RockShooter(GameObject) :
    def __init__ ( self ) :
        self.__rockList = []
        self.__time = 0
        self.__period = 0.05
        
        self.__stop = False
        
    #abstract implemetation
    def update ( self ) :
        if self.__stop == False :
            self.__time += setting.frt
            if self.__time >= self.__period :
                self.create ( )
                
                self.__time %= self.__period
        
        for rock in list(self.__rockList) :
            if rock.render.position.x < -setting.size_screen[0] or \
               rock.render.position.x > setting.size_screen[0]*2 or \
               rock.render.position.y < -setting.size_screen[1] or \
               rock.render.position.y > setting.size_screen[1]*2 : 
                self.__rockList.remove ( rock )
                continue
            else :
                rock.update()

    #abstract implementation
    def draw ( self , screen ) :
        for rock in self.__rockList :
            rock.draw ( screen )
    
    def create ( self  ) :
        target = Vector2 ( \
            ( 0.2 + random()*0.6 ) * setting.size_screen[0] , \
            0.5 * setting.size_screen[1] \
        )
        
        rock = Rock ( target )
        
        rock.render.position = Vector2 ( \
            (0.1 + random()*0.8)*setting.size_screen[0] , \
            setting.size_screen[1] + 200 \
        )
        
        rock.physics.v = Vector2 ( \
            -100 + random()*200 ,\
            -300 + random()*-400 \
        )
        
        rock.physics.drag = 0
        rock.physics.a.y = 300
        self.__rockList.append ( rock )

    def deleteRock ( self , rock ) :
        self.__rockList.remove ( rock )

    def stop ( self ) :
        self.__stop = True
        for _ in range ( 20 ) :
            self.create()
            
