from Script.MyScreen import MyScreen
from Script.AllEvent import AllEvent
from Script.Player.Knight import Knight
from Resources.sprites.boulder.boulder import boulder as b
import copy
import time
class boulder:
    def __init__(self,blank,array,collider):
        self.e = b()
        self.blank = blank
        self.collider = collider
        self.active=False
        self.array = array
        self.active = False
        for i in range(MyScreen.cols):
            for j in range(MyScreen.rows):
                if self.array[i,j] == 1:
                    self.aa=(i,j)
                    collider[i,j] = 1
                if self.array[i,j] == 2:
                    self.bb = (i,j)
        self.posX,self.posY = self.GetPos()
        self.AddList()
        AllEvent.AddEventA(self.SetActive)
    def AddList(self):
        self.blank.boulderList.append(self)
        pass
    def GetImage(self):
        return self.e.GetElement()
    def GetPos(self):
        a=int((1000-MyScreen.rows*65)/2+self.aa[1]*65)
        b=int((800-MyScreen.cols*65)/2+self.aa[0]*65)
        return (a,b)
    def GetBPos(self):
        return (self.posX,self.posY)
    def SetActive(self):
        self.active = not self.active
        self.Move()
    def Move(self):
        a = self.aa[0] - self.bb[0]
        b = self.aa[1] - self.bb[1]
        if self.active:
            if b>0:
                for x in range(0,b):
                    for i in range(65):
                        time.sleep(0.01)
                        self.posX-=1
            else:
                for x in range(0,b*-1):
                    for i in range(65):
                        time.sleep(0.01)
                        self.posX+=1
            if a>0:
                for x in range(0,a):
                    for i in range(65):
                        time.sleep(0.01)
                        self.posY-=1
            else:
                for x in range(0,a*-1):
                    for i in range(65):
                        time.sleep(0.01)
                        self.posY+=1
            Knight.GetInstance().collider[self.aa[0],self.aa[1]] = 0
            Knight.GetInstance().collider[self.bb[0],self.bb[1]] = 1
        else:
            if b>0:
                for x in range(0,b):
                    for i in range(65):
                        time.sleep(0.01)
                        self.posX+=1
            else:
                for x in range(0,b*-1):
                    for i in range(65):
                        time.sleep(0.01)
                        self.posX-=1
            if a>0:
                for x in range(0,a):
                    for i in range(65):
                        time.sleep(0.01)
                        self.posY+=1
            else:
                for x in range(0,a*-1):
                    for i in range(65):
                        time.sleep(0.01)
                        self.posY-=1
            Knight.GetInstance().collider[self.aa[0],self.aa[1]] = 1
            Knight.GetInstance().collider[self.bb[0],self.bb[1]] = 0
        print('.OK')
