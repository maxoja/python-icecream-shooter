from core.base import *
from core.components import *

import pygame
import setting
import source
import math
        
class Player ( GameObject ):
    def __init__ ( self , x , y ) :
        self.render = Render( x=x , y=y , \
                              image=source.sprites['gunner'][0].copy() ,\
                              scale_origin = 8 , tag = 'player')
        self.beam = Beam ( )
        
        self.__step = 100
        self.__pos = Vector2 ( x/self.__step , y/self.__step )

        self.__minX = 0.5
        self.__minY = 0.5
        self.__maxX = setting.size_screen[0]/self.__step - 0.5
        self.__maxY = setting.size_screen[1]/self.__step - 0.5

        self.__frames = source.sprites['gunner']
        
        self.__time = 0
        self.__period = 0.75
        self.__current_frame = 0

        self.__dead = False
        return

    #abstract implementation
    def bind ( self , camera , rockManager , flameManager , scoreText ) :
        self.beam.bind ( camera , self )
        self.render.bindCamera ( camera )
        self.__camera = camera
        self.__rockManager = rockManager
        self.__flameManager = flameManager
        self.__scoreText = scoreText
        
    #abstract implementation
    def draw ( self , screen ) :
        self.beam.draw ( screen )
        self.render.draw ( screen )
        return
    
    #abstract implementation
    def update ( self ) :
        if self.__dead :
            return
            
        #update beam effect animation
        self.beam.update ( )
        
        #update player frame animation
        self.__time += setting.frt
        if self.__time >= self.__period :
            self.__time %= self.__period
            self.__current_frame += 1
            self.__current_frame %= len ( self.__frames )
            self.render.image = self.__frames[self.__current_frame]
            if self.__current_frame == 0 :
                self.shoot ( )

        #update player position
        x = self.__pos.x * self.__step
        y = self.__pos.y * self.__step
        self.render.lerp ( Vector2 ( x, y ) , 4 )

        #update player to look at mouse position
        mx = pygame.mouse.get_pos()[0]
        my = pygame.mouse.get_pos()[1]
        dx = mx - self.render.position.x
        dy = my - self.render.position.y
        self.render.angle = - math.degrees ( math.atan2 ( dy , dx ) )

        deathDist = 30
        #check hit with rocks
        for rock in self.__rockManager.getRocks() :
            if rock.render.position.distance ( self.render.position ) <= deathDist :
                self.die ( )
                
        return

    #abstract implementation
    def control_key_down ( self , key ) :
        if key == pygame.K_w :
            if self.__pos.y > self.__minY :
                 self.move ( 0 , -1 )
        elif key == pygame.K_s :
            if self.__pos.y < self.__maxY :
                self.move ( 0 , 1 )
        elif key == pygame.K_a :
            if self.__pos.x > self.__minX :
                self.move ( -1 , 0 )
        elif key == pygame.K_d :
            if self.__pos.x < self.__maxX :
                self.move ( 1 , 0 )
                
    def move ( self , x , y ) :
        source.sounds['step'].play()
        self.__pos.x += x
        self.__pos.y += y
        return
    
    def die ( self ) :
        source.sounds['song2'].stop()
        source.sounds['die'].play()
        self.__dead = True
        self.render.image = source.images['gunner_dead']
        self.__rockManager.stop()
        self.__flameManager.stop()
        
    def isDead ( self ) :
        return self.__dead

    def shoot ( self ) :
        source.sounds['beam'].play()
        self.beam.explode ( )
        shootCount = 0
        aimingDirection = Vector2 ( math.sin ( math.radians ( self.render.angle ) ),\
                                    math.cos ( math.radians ( self.render.angle ) ) ) 
        
        for rock in list( self.__rockManager.getRocks() ) :
            dx = rock.render.position.x - self.render.position.x
            dy = rock.render.position.y - self.render.position.y
            angle = - math.degrees ( math.atan2 ( dy , dx ) )
            da = abs(angle - self.render.angle)
            if da <= 25 :
                direction = Vector2 ( dx , dy )
                direction = direction.one()
                direction.multiply ( 2000 )
                self.__flameManager.createExplosion ( rock.render.position )
                self.__rockManager.shootRock ( rock , direction )
                shootCount += 1

        self.__camera.shakeY ( aimingDirection.x * shootCount * 2 )
        self.__camera.shakeX ( aimingDirection.y * shootCount * 2 )

        self.__period *= 0.99
        self.__period = clamp ( self.__period , 0.4 , 1 )

        self.__scoreText.score += shootCount


class Beam ( GameObject ) :
    def __init__ ( self ) :
        self.render = Render ( image = source.sprites['beam'][0].copy() \
                               , scale_origin = 16 , tag = 'beam' , show = False )

        self.__frames = source.sprites['beam']

        self.__current_frame = 0
        self.__time = 0
        self.__period = 0.025

    #abstract implementation
    def bind ( self , camera , player ) :
        self.render.bindCamera ( camera )
        self.__player = player

    #abstract implementation
    def update ( self ) :
        self.__time += setting.frt
        if self.__time >= self.__period or self.__period <= 0 :
            self.__time %= self.__period
            self.__current_frame += 1
        
        if self.__current_frame >= len(self.__frames) :
            self.render.hide()
        else :
            self.render.image = self.__frames[self.__current_frame]

    #abstract implementation
    def draw ( self , screen ) :
        #set beam rotation
        self.render.angle = self.__player.render.angle
        
        #find where center of beam should be
        size = self.render.scaledSize() 
        drawPos = Vector2 ( size[0]/2 , size[1]/2 )
        cos = math.cos ( math.radians ( -self.render.angle ) )
        sin = math.sin ( math.radians ( -self.render.angle ) )
        drawPos.x *= cos
        drawPos.x += self.__player.render.position.x
        drawPos.y *= sin
        drawPos.y += self.__player.render.position.y

        #set beam position
        self.render.position = drawPos

        #call render of beam to draw
        self.render.draw ( screen )

    def explode ( self ) :
        self.__time = 0
        self.__current_frame = 0
        self.render.show()
