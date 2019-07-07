from Input import *
from Output import *
from Player import *
from Server import *
from threading import*

#   code action
#   0   login
#   1   move
#   2   attack
#   3   speak
#   4   logout
#   5   login reply
#   6   move notify
#   7   attack notify
#   8   speak notify
#   9   logout notify
#   10  invalid state

class Game(object):
    """description of class"""
    #login 0
    def __init__(self):
        self.input=Input()
        self.input.game=self
        self.output=Output()
        self.player=Player()
        self.server=Server()
        self.server.game=self
        self.locations=dict()
        self.event=multiprocessing.queues.SimpleQueue()
        
    def run(self,address,port):
        self.input.run()
        if(self.server.connect(address,port)):
            self.output.printConnectStatus(True)
        else:
            self.output.printConnectStatus(False)
            return
        self.server.run()
        self.loop()
        pass

    def loop(self):
        while(True):
            args=self.event.get();
            eventType=args[0]
            if(eventType==0):
                # disconnect
                self.output.printDisconnect()
                self.server.stop()
                self.input.stop()
                break
                continue
            if(eventType==1):
                # login
                self.server.sendLoginMsg(args[1])
                continue
            if(eventType==2):
                # move
                self.server.sendMoveMsg(args[1])
                continue
            if(eventType==3):
                # attack
                if(self.player.name!=args[1]):
                    self.server.sendAttackMsg(args[1])
                continue
            if(eventType==4):
                # speak
                self.server.sendSpeakMsg(args[1])
                continue
            if(eventType==5):
                # logout
                self.server.sendLogoutMsg()
                continue
            if(eventType==6):
                # login reply
                code=args[1]
                hp=args[2]
                exp=args[3]
                x=args[4]
                y=args[5]
                if(code==0):
                    # sucess
                    self.player.hp=hp
                    self.player.exp=exp
                    self.player.location.x=x
                    self.player.location.y=y
                    self.output.printLoginReply(True)
                    pass
                elif(code==1):
                    self.output.printLoginReply(False)
                    pass
                else:# undefined
                    pass
                continue
            if(eventType==7):
                # move notify
                player=args[1]
                x=args[2]
                y=args[3]
                hp=args[4]
                exp=args[5]
                self.locations[player]=Location(x,y)
                if(self.player.isVisible(self.locations[player])):
                    self.output.printMoveNotify(player,self.locations[player].x,self.locations[player].y,hp,exp)
                continue
            if(eventType==8):
                # attack notify
                attacker=args[1]
                victim=args[2]
                damage=args[3]
                hp=args[4]
                if(self.player.isVisible(self.locations.get(attacker)) and self.player.isVisible(self.locations.get(victim))):
                    self.output.printAttackNotify(attacker,victim,damage,hp)
                continue
            if(eventType==9):
                # speak notify
                player=args[1]
                msg=args[2]
                self.output.printSpeakNotify(player,msg)
                continue
            if(eventType==10):
                # logout notify
                name=args[1]
                self.locations.pop(name)
                self.output.printLogoutNotify(name)
                continue
            if(eventType==11):
                # invalid state
                code=args[1]
                self.output.printInvalidState(code)
                continue

        pass

    def stop(self):
        self.event.put((0,))

    

    # called by input
    def login(self,name):
        self.event.put((1,name))
    def move(self,direction):
        self.event.put((2,direction))
    def attack(self,victim):
        self.event.put((3,victim))
    def speak(self,msg):
        self.event.put((4,msg))
    def logout(self):
        self.event.put((5,))

    # called by server.recv
    def onLoginReply(self,code,x,y,hp,exp):
        self.event.put((6,code,x,y,hp,exp))
        pass
    def onMoveNotify(self,name,x,y,hp,exp):
        self.event.put((7,name,x,y,hp,exp))
        pass
    def onAttackNotify(self,attacker,victim,damaged,hp):
        self.event.put((8,attacker,victim,damaged,hp))
        pass
    def onSpeakNotify(self,player,msg):
        self.event.put((9,player,msg))
        pass
    def onLogoutNotify(self,name):
        self.event.put((10,name))
        pass
    def onInvalidState(self,code):
        self.event.put((11,code))
        pass

