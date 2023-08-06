import random
import pygame
import sys
import os
from pygame.locals import *
from Resources.sprites.sprite import Sprite
class flovers(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        n=0
        for x in range(3):
            self.element.append(pygame.image.load(Get('flovers_' + str(n) + '.png')))
            n+=1
    def GetElement(self):
        return pygame.transform.flip(self.element[random.randint(0,2)],random.randint(0,1),random.randint(0,1))

def Get(name):
    return os.path.dirname(os.path.realpath(__file__))+"\\"+name