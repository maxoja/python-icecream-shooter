from abc import ABCMeta,abstractmethod

class GameObject ( metaclass = ABCMeta ) :
    abstractmethod
    def bind ( self ) :
        pass
    
    abstractmethod
    def draw ( self , screen ) :
        pass

    abstractmethod
    def update ( self ) :
        pass

    abstractmethod
    def control_key_down ( self , keys ) :
        pass

    abstractmethod
    def control_key_hold ( self , key ) :
        pass

class Scene ( metaclass = ABCMeta ) :
    abstractmethod
    def update ( self ) :
        pass
