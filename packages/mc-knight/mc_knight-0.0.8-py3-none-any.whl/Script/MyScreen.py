class MyScreen:
    Width=0
    Height=0
    Mixed = None
    cols = 0
    rows = 0
    game = 0
    def SetScreen(width,height,mix):
        MyScreen.Width=width
        MyScreen.Height=height
        MyScreen.Mixed = mix
    def SetBox(cols,rows):
        MyScreen.cols = cols
        MyScreen.rows = rows