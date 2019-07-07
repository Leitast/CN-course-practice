# -*- coding: utf_8 -*-

import random
global output

class Player(object):
    """description of class"""
    def __init__(self,name):

        self.name = name
        self.x = random.randint(0,99)
        self.y = random.randint(0,99)
        self.hp = random.randint(100,120)
        self.exp = 0
        return super(Player, self).__init__()
    def save(self,path,file=True):
        try:
            if(file):
                pass# save player's info in file
            else:
                pass# create a new file in path dir for the player
        except:
            pass # maybe there is an ioexception
    def move(direction):
        pass
    def damage(self):
        pass
    def increaseExp(incresement):
        pass
    # TODO: add any methods you need here


