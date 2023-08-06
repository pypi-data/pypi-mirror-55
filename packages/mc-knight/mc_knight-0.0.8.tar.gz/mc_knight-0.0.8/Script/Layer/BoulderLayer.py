from Script.Layer.Layer import Layer
from Script.boulder.boulder import boulder
from Script.assist.Array import Array
class BoulderLayer(Layer):
    def __init__(self,cols,rows,array,blank,collider):
        Layer.__init__(self,cols,rows)
        self.array=Array()
        self.array.Set(array)
        self.CreateLayer(blank,array,collider)
    def CreateLayer(self,blank,array,collider):
       temp=boulder(blank,array,collider)
                    




