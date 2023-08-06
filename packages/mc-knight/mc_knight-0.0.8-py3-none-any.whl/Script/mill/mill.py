from Resources.sprites.mill.mill import mill as ml
from Script.assist.Array import Array
import pygame
from Script.MyScreen import MyScreen
class mill:
    def __init__(self,array):
        self.cols=array.cols
        self.rows=array.rows
        self.array=array
        self.n=-1
        temp=self.GetPos()
        self.x=temp[0]
        self.y=temp[1]
        self.posY=temp[3]
        self.posX=temp[2]
        self.equn=0
        self.m=ml()
        self.a = self.m.GetElement(0)
        self.b = self.m.GetElement(1)
        self.c = self.b
        self.rect = self.b.get_rect()
        self.rect = self.rect.move((MyScreen.Width - self.rect.width) / 2,(MyScreen.Height - self.rect.height) / 2)
        self.angle = 0
        self.isR = False
        pass
    def SetRotate(self):
        self.isR = not self.isR
    def GetPos(self):
        for i in range(0,self.cols):  
             for j in range(self.rows):
                a=int((1000-self.rows*65)/2+j*65)
                b=int((800-self.cols*65)/2+i*65)
                if self.array[i,j]:
                    return (a,b,i,j)
    def Rotate(self,x,y):
        if self.isR:
            self.b = pygame.transform.rotate(self.c, self.angle)
            self.angle += 2
            if self.angle > 360:
                self.angle -= 360
        newR = self.b.get_rect(center=self.rect.center)
        newR = newR.move(x,y)
        return (self.b,newR)
        pass

