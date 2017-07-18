import pygame
from pygame.locals import *
from time import sleep, time
from random import *

import setting
import source
from objects.camera import Camera
from objects.background import Background
from objects.transition import *
from objects.player import Player
from objects.rock import RockManager
from objects.flame import FlameManager
from objects.text import TimeText

import scenes.menu

class Scene_Arena :
    def __init__ ( self , screen ) :
        self.__screen = screen

        source.sounds['song2'].play(-1)
            
        #create accessory objects
        camera = Camera()
        background = Background( color = setting.color_background_arena  )

        #create game objects
        time_text = TimeText(0.5, 0.05, size = 50)

        #bind(link) objects

        #list gameobjects
        #append first = draw first
        gameObjects = []
        gameObjects.append(background)
        gameObjects.append(time_text)
        gameObjects.append(camera)

        self.__camera = camera
        self.__background = background
        self.__time_text = time_text
        
        self.__gameObjects = gameObjects

        '''states'''
        #play
        #finish
        self.__state = 'play'
        self.__start_time = time()

    def update( self ) :
        if self.__state == 'play' :
            
            ''' Play Game Normally '''
            for event in pygame.event.get() :
                if event.type == QUIT :
                        return False
                elif event.type == pygame.KEYDOWN :
                    for obj in self.__gameObjects :
                        obj.control_key_down ( event.key )
                        
            for obj in self.__gameObjects :
                obj.control_key_hold ( pygame.key.get_pressed() )
                obj.update ( )
                obj.draw ( self.__screen )
                
        elif self.__state == 'finish' :
            pass
        
            
