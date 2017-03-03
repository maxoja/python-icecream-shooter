#main of icecream shooter
import pygame
from pygame.locals import *

import setting
from scenes.game import Scene_Game
from scenes.menu import Scene_Menu

screen = pygame.display.set_mode ( setting.size_screen )
pygame.display.set_caption ( "Icecream Shooter" )
clock = pygame.time.Clock()

scene = Scene_Menu( screen )

while True :                
    update_result = scene.update ( )

    if update_result == False :
        break
    elif update_result != None :
        scene = update_result
        continue

    pygame.display.flip()
    clock.tick( setting.fps )

pygame.quit()
