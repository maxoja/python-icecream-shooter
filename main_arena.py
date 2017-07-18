import pygame
from pygame.locals import *

import setting
from scenes.arena import Scene_Arena

title = 'Shooter Arena'

screen = pygame.display.set_mode ( setting.size_screen )
pygame.display.set_caption ( title )
clock = pygame.time.Clock()

scene = Scene_Arena( screen )

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
