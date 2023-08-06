from Script.Layer.Layer import Layer
from Script.assist.Array import Array
from Script.Player.Knight import Knight
class CollisionLayer(Layer):
    def __init__(self,cols,rows):
        Layer.__init__(self,cols,rows)
    def UpdateCollision(self,array):
        for i in range(self.cols):
            for j in range(self.rows):
                if array[i,j] == 1:
                    Knight.GetInstance().collider[i,j] = 1
                elif array[i,j] == 2:
                    Knight.GetInstance().collider[i,j] = 2
                elif array[i,j] == 3:
                    Knight.GetInstance().collider[i,j] = 3
                elif array[i,j] == 4:
                    Knight.GetInstance().collider[i,j] = 4
                elif array[i,j] == 5:
                    Knight.GetInstance().collider[i,j] = 5
                elif array[i,j] == 6:
                    Knight.GetInstance().collider[i,j] = 6
                elif array[i,j] == 7:
                    Knight.GetInstance().collider[i,j] = 7
                elif array[i,j] == 8:
                    Knight.GetInstance().collider[i,j] = 8
                elif array[i,j] == 9:
                    Knight.GetInstance().collider[i,j] = 9
                elif array[i,j] == 10:
                    Knight.GetInstance().collider[i,j] = 10
                elif array[i,j] == 11:
                    Knight.GetInstance().collider[i,j] = 11
        print('更新碰撞完成，碰撞矩阵为：')
        for x in Knight.GetInstance().collider.array:
            print(x)
        print('----------end----------')