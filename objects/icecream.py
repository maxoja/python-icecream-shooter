from core.base import *
from core.components import *

import pygame
import setting
import source
import math
        
class Icecream ( GameObject ):
    def __init__ ( self , x , y ) :
        self.render = Render( x=x , y=y , \
                              image=source.sprites['icecream'][0].copy() ,\
                              scale_origin = 15 , tag = 'icecream')
        self.__frames = source.sprites['icecream']
        return
        
    #abstract implementation
    def draw ( self , screen ) :
        self.render.draw ( screen )
        return
    
    #abstract implementation
    def update ( self ) :

        #update player to look at mouse position
        mx = pygame.mouse.get_pos()[0]
        my = pygame.mouse.get_pos()[1]
        dx = mx - self.render.position.x
        dy = my - self.render.position.y
        degree = int(math.degrees ( math.atan2 ( dy , dx ) ))
        if degree < 0 :
            degree *= -1
        elif degree > 0 :
            degree = 360-degree

        degree += 22
        degree %= 360
        
        self.render.image = self.__frames[degree//45]
        
                
        return
