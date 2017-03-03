from core.base import *
from core.components import *
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

        
