class Location(object):
    """description of class"""
    
    def __init__(self,x=0,y=0):
        self.x=x
        self.y=y
        return super(Location, self).__init__()
    def inRange(self,location):
        return True
        return (self.x>=location.x-5)and(self.x>=location.x+5)and(self.y>=location.y-5)and(self.y>=location.y+5)
        return True

