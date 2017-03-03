import pygame
from pygame.locals import *
from time import sleep
from random import *

import setting
from objects.camera import Camera
from objects.icecream import Icecream
from objects.background import Background
from objects.transition import Transition_GameStart
from objects.text import HighscoreText,LabelText,ScoreText
from objects.rock import RockShooter
from objects.flame import FlameShooter
import source

import scenes.game

class Scene_Menu :
    def __init__ ( self , screen ) :
        source.sounds['song1'].play(-1)
        
        self.__screen = screen
            
        #create game objects
        background = Background( color = setting.color_background_menu )
        icecream = Icecream( setting.size_screen[0]//2 , setting.size_screen[1] - 120 )
        rockShooter = RockShooter()
        flameShooter = FlameShooter()
        title1 = LabelText( setting.size_screen[0]//2 - 3 , 100 + 3 , \
                            'ICECREAM' , size = 100 , color = (0,0,0))
        title2 = LabelText( setting.size_screen[0]//2 - 3 , 200 + 3, \
                            'SHOOTER' , size = 100 , color = (0,0,0))
        title3 = LabelText( setting.size_screen[0]//2 + 3 , 100 - 3 , \
                            'ICECREAM' , size = 100 )
        title4 = LabelText( setting.size_screen[0]//2 + 3 , 200 - 3, \
                            'SHOOTER' , size = 100 )
        title5 = LabelText( setting.size_screen[0]//2 - 2 , 350 + 2 , \
                            '[SPACE] to start' , size = 50 )
        title6 = LabelText( setting.size_screen[0]//2 + 2 , 350 - 2 , \
                            '[SPACE] to start' , size = 50 , color = (0,0,0) )
        
        #list gameobjects
        #append first = draw first
        gameObjects = []
        gameObjects.append(background)
        gameObjects.append(flameShooter)
        gameObjects.append(rockShooter)
        gameObjects.append(icecream)
        gameObjects.append(title1)
        gameObjects.append(title2)
        gameObjects.append(title3)
        gameObjects.append(title4)
        gameObjects.append(title5)
        gameObjects.append(title6)

        self.__background = background
        self.__rockShooter = rockShooter
        self.__icecream = icecream
        
        self.__gameObjects = gameObjects

        self.__state = 'menu'

    def update( self ) :
        if self.__state == 'menu' :
            ''' Show Menu '''
            for event in pygame.event.get() :
                if event.type == QUIT :
                        return False
                elif event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_SPACE : 
                        self.__transition = Transition_GameStart ( )
                        source.sounds['song1'].stop()
                        source.sounds['transition1'].play()
                        self.__state = 'transition'
                        return
                    
                    for obj in self.__gameObjects :
                        obj.control_key_down ( event.key )

            for obj in self.__gameObjects :
                obj.control_key_hold ( pygame.key.get_pressed() )
                obj.update ( )
                obj.draw ( self.__screen )

        
        elif self.__state == 'transition' :
            for event in pygame.event.get() :
                if event.type == QUIT :
                        return False
                    
            ''' Animate Transition '''
            self.__transition.draw(self.__screen)
                        
            if self.__transition.isFinished() :
                return scenes.game.Scene_Game(self.__screen)  
            
