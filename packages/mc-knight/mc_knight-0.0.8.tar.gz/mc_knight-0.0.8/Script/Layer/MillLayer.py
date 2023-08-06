from Script.Layer.Layer import Layer
from Script.mill.mill import mill
from Script.assist.Array import Array
class MillLayer(Layer):
    def __init__(self,cols,rows,array,blank,collider):
        Layer.__init__(self,cols,rows)
        self.array=array
        self.element=mill(self.array)
        self.CreateLayer(blank,collider)
    def CreateLayer(self,blank,collider):
        for i in range(self.cols):
            for j in range(self.rows):
                if self.array[i,j]!=0:
                    collider[i,j] = 7
                    blank.millList.append(self.element)
