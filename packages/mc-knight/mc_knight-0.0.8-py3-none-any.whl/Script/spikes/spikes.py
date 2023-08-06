from Resources.sprites.spikes.spikes import spikes as sp
from Script.MyScreen import MyScreen
from Script.AllEvent import AllEvent
from Script.Player.Knight import Knight
class spikes:
    def __init__(self,blank,i,j):
        self.e = sp()
        self.i = i
        self.j = j
        self.blank = blank
        self.active=False
        AllEvent.AddEventA(self.SetActive)
    def GetImage(self): 
        if self.active:
            self.blank.myLayer[self.i,self.j] = self.e.GetEement(1)
        else:
            self.blank.myLayer[self.i,self.j] = self.e.GetEement(0)
    def SetActive(self):
        self.active = not self.active
        if Knight.GetInstance().collider[self.i,self.j] == 6:
            Knight.GetInstance().collider[self.i,self.j] = 0
        elif Knight.GetInstance().collider[self.i,self.j] == 0:
            Knight.GetInstance().collider[self.i,self.j] = 6
        self.GetImage()


