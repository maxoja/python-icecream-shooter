import setting

from core.base import *
from core.game_math import *

class Camera ( GameObject ):
    def __init__ ( self , multi = 0.8 , period = 0.05 ) :
        self.period = period
        self.multi = multi
        
        self.__shift = Vector2 ( 0 , 0 )
        self.__time = 0

    def shakeX ( self , amp ) :
        self.__shift.x = amp
        self.__time = 0

    def shakeY ( self , amp ) :
        self.__shift.y = amp
        self.__time = 0

    def update ( self ) :
        self.__time += setting.frt
        if self.__time >= self.period :
            self.__time %= self.period
            self.__shift.multiply ( self.multi*-1 )

    def getShift ( self ) :
        return self.__shift

