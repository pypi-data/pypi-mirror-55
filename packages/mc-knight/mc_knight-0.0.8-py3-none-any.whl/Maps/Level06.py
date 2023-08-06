from Maps.LevelBase import LevelBase
from Script.assist.Array import Array
class Level06(LevelBase):
    def __init__(self,screen,cols,rows):
        LevelBase.__init__(self,screen,cols,rows)
    def LoadLevel(self):
        temp = Array()
        temp.Clear()
        temp.SetSA([[1,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0]])
        self.CreateCastle(temp)
        temp.Clear()
        temp.SetSA([[0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,2,0,0],
                    [0,0,0,0,1,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0]])
        self.CreateSpikes(temp)
        temp.Clear()
        temp.SetSA([[0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,1,0,0,0,0,0]])
        self.CreateMill(temp)
        temp.SetSA([[0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,1,0,0,0,0,0],
                    [0,1,1,0,0,0,0],
                    [1,0,0,0,0,0,0],
                    [1,0,0,0,0,0,0]])
        self.CreateFlovers(temp)
        temp.Clear()
        temp.SetSA([[0,0,0,0,0,0,0],
                    [2,2,2,0,0,0,0],
                    [0,0,1,2,0,0,0],
                    [0,0,0,1,0,0,0],
                    [0,0,2,1,0,0,0],
                    [0,0,1,1,0,0,0]])
        self.CreateWater(temp)
        temp.Clear()
        temp.SetSA([[0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,2,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0]])
        self.CreateBridge(temp)
        temp.Clear()
        temp.SetSA([[0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,1,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0]])
        self.CreatePlayer(temp)
        self.UpdateCollision()