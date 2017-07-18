from core.base import *
from core.components import *
from time import time as current_time
import setting


class LabelText ( GameObject ) :
    def __init__ ( self , x , y , text , color = (255,255,255) , size = 50 ) :
        self.textRender = TextRender ( size = size , color = color , center = True)
        self.text = text
        self.textRender.position.x = x
        self.textRender.position.y = y
        
    def draw ( self , screen ) :
        self.textRender.setText ( self.text )
        self.textRender.draw ( screen )
        


class ScoreText ( GameObject ) :
    def __init__ ( self , score=0 ) :
        self.textRender = TextRender ( size = 450 , color = ( 255,255,255 ) , center = True)
        self.textRender.position.x = setting.size_screen[0]/2
        self.textRender.position.y = setting.size_screen[1]/2
        self.score = score
        
    def draw ( self , screen ) :
        self.textRender.setText ( str(self.score) )
        self.textRender.draw ( screen )



class HighscoreText ( GameObject ) :
    def __init__ ( self ) :
        
        try :
            file = open('highscore.txt','r')
            self.score = int(file.readline())
            file.close()
        except :
            self.score = 0
            
        self.textRender = TextRender ( size = 50 , color = (107, 178, 0) , center = True )#(238, 132, 255)
        self.textRender.position.x = setting.size_screen[0]/2
        self.textRender.position.y = setting.size_screen[1]/2 + 125

    def draw ( self , screen ) :
        self.textRender.setText ( "best " + str ( self.score ) )
        self.textRender.draw ( screen )


class TimeText ( GameObject ) :
    def __init__ ( self ,x_ratio=0.5 ,y_ratio=0.5 ,size=100 , color=(255,255,255)) :
        self.textRender = TextRender ( size = size , color = color , center = True)
        self.textRender.position.x = setting.size_screen[0]*x_ratio
        self.textRender.position.y = setting.size_screen[1]*y_ratio
        
        self.start_count()
        
    def draw ( self , screen ) :
        self.textRender.draw ( screen )

    def update( self ) :
        if not self.__stop and not self.__pause :
            time_delta = current_time() - self.__start_time
        
        self.textRender.setText( format(time_delta, '.2f') )

    def pause_count ( self ) :
        self.__pause = True

    def continue_count ( self ) :
        self.__pause = False
        
    def start_count ( self ) :
        self.textRender.setText( format(0.0,'.2f') )
        
        self.__start_time = current_time()
        self.__stop = False
        self.__pause = False

    def stop_count ( self ) :
        self.__stop = True

    def get_start_time ( self ) :
        return self.__start_time

    def get_time_since_start ( self ) :
        return current_time() - self.get_start_time()
