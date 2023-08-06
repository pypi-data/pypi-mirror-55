from Maps.Level01 import Level01
from Maps.Level02 import Level02
from Maps.Level03 import Level03
from Maps.Level04 import Level04
from Maps.Level05 import Level05
from Maps.Level06 import Level06
from Maps.Level07 import Level07
from Maps.Level08 import Level08
from Maps.Level09 import Level09
from Maps.Level10 import Level10
from Script.mcgame.MCGame import MCGame

def LoadLevel01():
    return Level01(MCGame.GetInstance().screen,3,3)
def LoadLevel02():
    return Level02(MCGame.GetInstance().screen,4,5)
def LoadLevel03():
    return Level03(MCGame.GetInstance().screen,7,8)
def LoadLevel04():
    return Level04(MCGame.GetInstance().screen,9,9)
def LoadLevel05():
    return Level05(MCGame.GetInstance().screen,9,12)
def LoadLevel06():
    return Level06(MCGame.GetInstance().screen,6,7)
def LoadLevel07():
    return Level07(MCGame.GetInstance().screen,9,9)
def LoadLevel08():
    return Level08(MCGame.GetInstance().screen,9,9)
def LoadLevel09():
    return Level09(MCGame.GetInstance().screen,9,9)
def LoadLevel10():
    return Level10(MCGame.GetInstance().screen,9,9)