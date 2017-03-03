import pygame
import random

import setting
from core.base import *
from objects.text import ScoreText,HighscoreText,LabelText

class Transition ( GameObject ):
    def __init__ ( self , img = None , color = None , quality = 5 ) :
        if img == None :
            self._img = pygame.Surface ( setting.size_screen )
            self._img = self._img.convert()
            self._img.fill ( color )
        else :
            self._img = img

        self._finished = False
        self._size_block = [setting.size_screen[0]//quality,setting.size_screen[1]//quality]
        self._blocks = [ [x,y] for x in range(quality) for y in range ( quality) ]
        random.shuffle ( self._blocks )

    def draw ( self , screen ) :
        if len ( self._blocks ) == 0 :
            self._finished = True
            return
        
        dest = self._blocks.pop()
        dest[0] *= self._size_block[0]
        dest[1] *= self._size_block[1]
        
        area = dest + self._size_block
        
        screen.blit ( self._img , dest , area )

    def isFinished( self ) :
        return self._finished

class Transition_GameEnd ( Transition ) :
    def __init__ ( self , scoreText ) :
        super().__init__( color = (255,0,0) )
        scoreText.draw ( self._img )

class Transition_GameStart ( Transition ) :
    def __init__ ( self ) :
        super().__init__( color = setting.color_background_game )
        ScoreText().draw( self._img )
        HighscoreText().draw ( self._img )

class Transition_Menu ( Transition ) :
    def __init__ ( self ) :
        super().__init__( color = setting.color_background_menu )
        LabelText( setting.size_screen[0]//2 - 3 , 100 + 3 , \
                   'ICECREAM' , size = 100 , color = (0,0,0)).draw ( self._img)
        LabelText( setting.size_screen[0]//2 - 3 , 200 + 3, \
                   'SHOOTER' , size = 100 , color = (0,0,0)).draw ( self._img)
        LabelText( setting.size_screen[0]//2 + 3 , 100 - 3 , \
                   'ICECREAM' , size = 100 ).draw ( self._img)
        LabelText( setting.size_screen[0]//2 + 3 , 200 - 3, \
                   'SHOOTER' , size = 100 ).draw ( self._img)
        LabelText( setting.size_screen[0]//2 - 2 , 350 + 2 , \
                   '[SPACE] to start' , size = 50 ).draw ( self._img)
        LabelText( setting.size_screen[0]//2 + 2 , 350 - 2 , \
                   '[SPACE] to start' , size = 50 , color = (0,0,0) ).draw ( self._img)

        
        
    
