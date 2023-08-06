from Script.Layer.Layer import Layer
from Script.spikes.spikes import spikes
from Script.assist.Array import Array
class SpikesLayer(Layer):
    def __init__(self,cols,rows,array,blank,collider):
        Layer.__init__(self,cols,rows)
        self.array=Array()
        self.array.Set(array)
        self.CreateLayer(blank,collider)
    def CreateLayer(self,blank,collider):
        for i in range(self.cols):
            for j in range(self.rows):
                if self.array[i,j]!=0:
                    if self.array[i,j] == 1:
                        collider[i,j]=6
                        spikes(blank,i,j).GetImage()




