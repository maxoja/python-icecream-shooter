#source loader
import os
import pygame
from abc import ABCMeta,abstractmethod

class Loader(metaclass = ABCMeta) :
    def __init__ ( self , name_folder , name_source ) :
        self.path = os.path.join ( name_folder , name_source )

    abstractmethod
    def load ( self ) :
        pass

class ImageLoader ( Loader ) :
    def __init__ ( self , name_folder , name_source , size = 1 ) :
        super().__init__ ( name_folder , name_source )
        self.__size = size

    def load ( self ) :
        try :
            img = pygame.image.load ( self.path )
            
            if type(self.__size) == tuple :
                img = pygame.transform.scale(img , self.__size)
            else :
                newSize = (int(img.get_size()[0]*self.__size),)
                newSize += (int(img.get_size()[1]*self.__size),)
                img = pygame.transform.scale(img , newSize)
                
            result = img
        except :
            result = None
            print ( "cannot load from path : '"+self.path+"'" )
        finally :
            return result

class SpriteLoader ( Loader ) :
    def __init__ ( self , name_folder , name_source , extension , frames , size = 1 ) :
        super().__init__( name_folder , name_source )
        self.__size = size
        self.__frames = frames
        self.__extension = extension

    def load ( self ) :
        result = []
        try :
            for index_str in [ str(x) for x in range(self.__frames) ] :
                img = pygame.image.load ( self.path + index_str + self.__extension )

                if type(self.__size) == tuple :
                    img = pygame.transform.scale(img , self.__size)
                else :
                    newSize = (int(img.get_size()[0]*self.__size),)
                    newSize += (int(img.get_size()[1]*self.__size),)
                    img = pygame.transform.scale(img , newSize)

                result.append(img)
        except :
            result = None
            print("cannot load sprite from path : '"+self.path+"' ("+str(frames)+")")
        
        return result


class AudioLoader ( Loader ) :
    def __init__ ( self , name_folder , name_source ) :
        super().__init__( name_folder , name_source )

    def load ( self ) :
        try :
            result = pygame.mixer.Sound ( self.path )
        except :
            result = None
            print ( "cannot load from path : '"+self.path+"'" )
        finally :
            return result
        
pygame.mixer.init()

#main image loading
images = {}
image_loaders = {\
    'gunner_dead'   : ImageLoader ( '_img/objects' , 'gunner_dead.png' ) ,\
    'rock'          : ImageLoader ( '_img/objects' , 'rock.png' ),\
}

#main sprite loading
sprites = {}
sprite_loaders = {\
    'icecream'      : SpriteLoader ( '_img/objects' , 'icecream' , '.png', 8 ),\
    'gunner'        : SpriteLoader ( '_img/objects' , 'gunner' , '.png' , 3 ),\
    'beam'          : SpriteLoader ( '_img/effects' , 'beam' , '.png' , 3 ),\
    'flame'         : SpriteLoader ( '_img/effects' , 'flame' , '.png' , 3 ),\
}

#main sound loading
sounds = {}
sound_loaders = {\
    'song1'         : AudioLoader ( '_audio' , 'song1.wav' ) ,\
    'song2'         : AudioLoader ( '_audio' , 'song2.wav' ) ,\
    'beam'          : AudioLoader ( '_audio' , 'beam.wav' ) ,\
    'die'           : AudioLoader ( '_audio' , 'die.wav' ) ,\
    'text'          : AudioLoader ( '_audio' , 'text.wav' ) ,\
    'step'          : AudioLoader ( '_audio' , 'step.wav' ) ,\
    'transition1'    : AudioLoader ( '_audio' , 'transition1.wav' ) ,\
    'transition2'    : AudioLoader ( '_audio' , 'transition2.wav' ) ,\
}

for key in image_loaders.keys() :
    images[key] = image_loaders[key].load()

for key in sprite_loaders.keys() :
    sprites[key] = sprite_loaders[key].load()

for key in sound_loaders :
    sounds[key] = sound_loaders[key].load()
