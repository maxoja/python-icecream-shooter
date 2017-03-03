#core components
import pygame
import math

from core.game_math import *
import setting

pygame.font.init()

class Render :
    def __init__ ( self , x = 0 , y = 0 , angle = 0 , scale = 1 \
                   ,scale_origin = 1 , image = None , layer = 0 \
                   , tag = '' , show = True) :
        self.camera = None
        self.position = Vector2(x,y)
        self.angle = angle
        self.scale = scale
        self.image = image
        self.layer = layer
        self.tag = tag
        self.__show = show
        
        self.__scale_origin = scale_origin

    def bindCamera ( self , camera ) :
        self.camera = camera
        
    def move ( self , x=0 , y=0 , direction = None ) :
        if direction is None :
            self.position.add_fps( Vector2( x, y ) )
        else :
            self.position.add( direction )

    def rotate ( self , dangle ) :
        self.angle = add_fps ( self.angle , dangle )

    def lerp ( self , dest , ratio = 1 ) :
        self.position.lerp_fps( dest , ratio )

    def show ( self ) :
        self.__show = True

    def hide ( self ) :
        self.__show = False
        
    def draw ( self , screen ) :
        if self.__show == False :
            return
        
        image_result = pygame.transform.scale( self.image , self.scaledSize() )
        orig_rect = image_result.get_rect()
        rot_image = pygame.transform.rotate(image_result, self.angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        image_result = rot_image.subsurface(rot_rect)

        x = self.position.x - image_result.get_size()[0]/2
        y = self.position.y - image_result.get_size()[1]/2

        if self.camera != None :
            x += self.camera.getShift().x
            y += self.camera.getShift().y
        
        screen.blit ( image_result , ( x,y ) )

    def _imgX ( self ) :
        return self.image.get_size()[0]

    def _imgY ( self ) :
        return self.image.get_size()[1]

    def scaledSize ( self ) :
        return (
            int(self._imgX() * self.scale * self.__scale_origin) ,\
            int(self._imgY() * self.scale * self.__scale_origin)
        )

class TextRender :
    def __init__ ( self ,x = 0 , y = 0 , text = 'text' \
                   , family='Frutiger Roman' , size=15 \
                   , color = (255,255,255) , center = False ) :
        self.position = Vector2(x,y)
        self.family = family
        self.size = size
        self.color = color
        self.center = center
        
        self._text = text

    def draw ( self , screen ) :
        font = pygame.font.SysFont ( self.family , self.size )
        surface = font.render ( self._text , 1 , (self.color) )
        
        if self.center :
            drawPos = ( self.position.x - surface.get_size()[0]/2 ,\
                        self.position.y - surface.get_size()[1]/2 )
        else :
            drawPos = ( self.position.x , self.position.y )
            
        screen.blit ( surface , drawPos )

    def setText ( self , text ) :
        self._text = text
        
class Physics :
    def __init__ ( self ) :
        self.v = Vector2()
        self.a = Vector2()
        self.drag = 0
        
        self.v_angular = 0
        self.a_angular = 0
        self.drag_angular = 0

    def update ( self , render ) :
        self.v.multiply_fps ( 1.0 - self.drag )
        self.v_angular = multiply_fps(self.v_angular , 1.0 - self.drag_angular)
        
        self.v.add_fps ( self.a )
        self.v_angular = add_fps( self.v_angular , self.a_angular )

        render.position.add_fps( self.v )
        render.angle = add_fps( render.angle , self.v_angular )
        
