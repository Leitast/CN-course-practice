from Location import *
class Player(object):
    """description of class"""

    def __init__(self):
        self.name=""
        self.location=Location()
        self.hp=0
        self.exp=0
        return super(Player, self).__init__()
    def isVisible(self,location):
        return self.location.inRange(location)




