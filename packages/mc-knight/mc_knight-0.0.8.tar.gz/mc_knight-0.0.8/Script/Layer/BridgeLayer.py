from Script.Layer.Layer import Layer
from Resources.sprites.bridge.bridge import bridge
from Script.assist.Array import Array
class BridgeLayer(Layer):
    def __init__(self,cols,rows,array,blank,collider):
        Layer.__init__(self,cols,rows)
        self.array=Array()
        self.array.Set(array)
        self.element=bridge()
        self.CreateLayer(blank,collider)
    def CreateLayer(self,blank,collider):
        for i in range(self.cols):
            for j in range(self.rows):
                if self.array[i,j]!=0:
                    if self.array[i,j] == 1:
                        collider[i,j]=0
                        blank.myLayer[i,j]=self.element.GetElement(0)
                    elif self.array[i,j] == 2:
                        collider[i,j]=0
                        blank.myLayer[i,j]=self.element.GetElement(1)



