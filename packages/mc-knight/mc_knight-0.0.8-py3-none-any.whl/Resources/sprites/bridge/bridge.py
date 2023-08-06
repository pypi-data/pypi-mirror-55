import random
import pygame
import sys
import os
from pygame.locals import *
from Resources.sprites.sprite import Sprite
class bridge(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        n=0
        for x in range(2):
            self.element.append(pygame.image.load(Get('bridge_' + str(n) + '.png')))
            n+=1
    def GetElement(self,x):
        return self.element[x]

def Get(name):
    return os.path.dirname(os.path.realpath(__file__))+"\\"+name