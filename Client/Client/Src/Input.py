from Game import *
from threading import*
import sys
class Input(object):
    """description of class"""

    def __init__(self):
        self.game=None
    def run(self):
        thread=Thread(target=self.loop,name='inputThread')
        thread.setDaemon(True)
        thread.start()

        pass
    def loop(self):
        while(True):
            #ine=input()
            try:
                str=raw_input("")
                line=str.split(' ', 1 )
                if(line[0]=='login'):
                    self.game.login(line[1])
                    continue
                if(line[0]=='move'):
                    if(line[1]=='north' or line[1]=='south'or line[1]=='west'or line[1]=='east'):
                        self.game.move(line[1])
                    else:
                        print '! Invalid direction: '+line[1]
                    continue
                if(line[0]=='attack'):
                    self.game.attack(line[1])
                    continue
                if(line[0]=='speak'):
                    self.game.speak(line[1])
                    continue
                if(line[0]=='logout'):
                    self.game.logout()
                    continue
            except:
                print '! Invalid syntax'
    def stop(self):
        pass
