class AllEvent:
    eventA=[]
    eventB=[]
    eventC=[]
    def RunA():
        if AllEvent.eventA!=[]:
            for x in AllEvent.eventA:
                x()
    def RunC():
        if AllEvent.eventC!=[]:
            for x in AllEvent.eventC:
                x()
    def RunB():
        if AllEvent.eventB!=[]:
            for x in AllEvent.eventB:
                x()
    def AddEventA(event):
        AllEvent.eventA.append(event)
    def AddEventB(event):
        AllEvent.eventB.append(event)
    def AddEventB(event):
        AllEvent.eventB.append(event)


