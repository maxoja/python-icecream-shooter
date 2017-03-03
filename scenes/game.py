import pygame
from pygame.locals import *
from time import sleep
from random import *

import setting
import source
from objects.camera import Camera
from objects.background import Background
from objects.transition import *
from objects.player import Player
from objects.rock import RockManager
from objects.flame import FlameManager
from objects.text import ScoreText,HighscoreText,LabelText

import scenes.menu

class Scene_Game :
    def __init__ ( self , screen ) :
        self.__screen = screen

        source.sounds['song2'].play(-1)
            
        #create accessory objects
        camera = Camera()
        background = Background( color = setting.color_background_game )

        #create game objects
        player = Player( setting.size_screen[0]/2 , setting.size_screen[1]/2 )
        rockManager = RockManager ( )
        flameManager = FlameManager ( )
        scoreText = ScoreText ( score = 0 )
        highscoreText = HighscoreText ( )

        #bind(link) objects
        player.bind ( camera , rockManager , flameManager , scoreText )
        rockManager.bind ( camera , player )
        flameManager.bind ( camera )

        #list gameobjects
        #append first = draw first
        gameObjects = []
        gameObjects.append(background)
        gameObjects.append(scoreText)
        gameObjects.append(highscoreText)
        gameObjects.append(flameManager)
        gameObjects.append(player)
        gameObjects.append(rockManager)
        gameObjects.append(camera)

        self.__camera = camera
        self.__background = background
        self.__player = player
        self.__rockManager = rockManager
        self.__flameManager = flameManager
        self.__scoreText = scoreText
        self.__highscoreText = highscoreText
        
        self.__gameObjects = gameObjects

        self.__state = 'play'
        self.__timeCounter = 0

    def update( self ) :
        if self.__state == 'play' or self.__state == 'dying' :
            
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

            if self.__player.isDead() :
                self.__timeCounter += setting.frt
                if self.__timeCounter >= 2.5 :
                    ''' Ending Animation Initialize '''
                    self.__transition = Transition_GameEnd ( self.__scoreText )
                    self.__timeCounter = 0
                    source.sounds['song2'].stop()
                    source.sounds['transition2'].play()
                    self.__state = 'ending'
        
        elif self.__state == 'ending' :
            
            for event in pygame.event.get() :
                if event.type == QUIT :
                        return False
                    
            ''' Animate Transition '''
            self.__transition.draw(self.__screen)
                        
            if self.__transition.isFinished() :
                texts = [ 
                           LabelText ( 240,150 ,"YOU"  , color =(255, 131, 15) , size = 70),\
                           LabelText ( 400,150 ,"SHOT"  , color =(255, 131, 15), size = 70),\
                           LabelText ( 325,470 ,"COOKIES"  , color =(255, 131, 15) , size = 70),\
                           LabelText ( 190,590 ,"[SPACE]  RETRY" , color = (240,240,240) ),\
                           LabelText ( 475,590 ,"[ESC]  BACK"  , color = (240,240,240) ),\
                           None,
                        ]

                if self.__highscoreText.score > self.__scoreText.score :
                    texts[5] = LabelText ( 325 , 75 , "YOU NOT THE BEST :(" , size = 75 )
                else :
                    texts[5] = LabelText ( 325 , 75 , "YOU ARE THE BEST!" , size = 75 )
                    
            
                for text in texts :
                    sleep(0.6)
                    source.sounds['text'].play()
                    text.draw(self.__screen)
                    pygame.display.flip()

                if self.__scoreText.score > self.__highscoreText.score  :
                    file = open('highscore.txt','w')
                    file.write(str(self.__scoreText.score))
                    file.close()

                self.__state = 'ended'
        
        elif self.__state == 'ended' :
            ''' Show Score and Options '''
            
            for event in pygame.event.get() :
                if event.type == QUIT :
                        return False
                elif event.type == pygame.KEYDOWN :
                    
                    if event.key == pygame.K_SPACE :
                        ''' Start new game Transition '''
                        self.__transition = Transition_GameStart ( )
                        source.sounds['transition1'].play()
                        while self.__transition.isFinished() == False :
                            self.__transition.draw( self.__screen )
                            pygame.display.flip()
                            
                        return Scene_Game( self.__screen )

                    
                    elif event.key == pygame.K_ESCAPE :
                        ''' Menu Transition '''
                        self.__transition = Transition_Menu ( )
                        source.sounds['transition1'].play()
                        while self.__transition.isFinished() == False :
                            self.__transition.draw( self.__screen )
                            pygame.display.flip()
                        
                        return scenes.menu.Scene_Menu ( self.__screen )
            
