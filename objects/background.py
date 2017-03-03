import pygame
import setting

from core.base import *

class Background ( GameObject ):
    def __init__ ( self , color = None , img = None ) :
        if color != None :
            self.__img = pygame.Surface ( setting.size_screen )
            self.__img = self.__img.convert()
            self.__img.fill ( color )
        else :
            self.__img = img

    def draw ( self , screen , dest = (0,0) , area=None ) :
        screen.blit ( self.__img , dest , area )
