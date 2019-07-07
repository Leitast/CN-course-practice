# -*- coding: utf_8 -*-
import threading
from Queue import *

from Output import *
from ClientsManager import *
from Player import *


class Server(object):
    """description of class"""
    def __init__(self,output):
        super(Server, self).__init__()
        self.events = Queue()
        self.manager = ClientsManager(self,output)
        self.players = dict()# map[player's name]->Player object
        self.output=output
        self.path=None
    def run(self,port):
        self.output.run()
        msg='Server is running'
        self.output.printMsg(msg)
        self.manager.run(port)
        thread=Thread(target=self.timer,name='timer')
        thread.setDaemon(True)
        thread.start()
        self.loop()
        pass

    
    def loop(self):
        while(True):
            args = self.events.get()
            type = args[0]
            if(type == 0):
                for player in self.players.keys():
                    self.players[player].save()
                self.manager.stop()
                # stop
                continue
            if(type == 1):
                # timer
                for player in self.players.keys():
                    self.players[player].hp = self.players[player].hp + 5
                    pass 
                continue
            if(type == 2):
                # login
                name = args[1]
                msg=''
                if(name in self.players):
                    # never happen
                    code = 1
                    self.manager.sendLoginReply(code,0,0,0,name)
                else:
                    code = 0
                    player = Player(name)
                    msg=name+': location=('+str(player.x)+','+str(player.y)+'), HP='+str(player.hp)+', EXP='+str(player.exp)+'.'
                    self.manager.sendLoginReply(code,player.hp,player.exp,player.x,player.y,name)
                    self.manager.sendMoveNotify(name,player.x,player.y,player.hp,player.exp)# notify logined players
                    for p in self.players.keys():
                        self.manager.sendMoveNotify(name,player.x,player.y,player.hp,player.exp,p)
                self.output.printMsg(msg)

                continue
            if(type == 3):
                # move
                name = args[1]
                direction = args[2]
                player = self.players[name]
                msg
                try:
                    player.move(direction)
                    msg=name+': location=('+str(player.x)+','+str(player.y)+'), HP='+str(player.hp)+', EXP='+str(player.exp)+'.'

                except:
                    pass
                self.output.printMsg(msg)

                self.manager.sendMoveNotify(name,player.x,player.y,player.hp,player.exp)
                
                continue
            if(type == 4):
                # attack
                attacker = args[1]
                victim = args[2]
                if(self.players[attacker] != None and self.players[victim] != None):
                    damage = self.players[victim].damage()
                    self.players[attacker].getEXP(damage)
                    self.manager.sendAttackNotify(attacker,victim,damage,self.players[attacker].hp)
                continue
            if(type == 5):
                # speak
                player = args[1]
                msg = args[2]

                self.output.printMsg(player+': '+msg)

                self.manager.sendSpeakNotify(player,msg)
                continue
            if(type == 6):
                # logout
                player = args[1]
                self.players[player].save(self.path)
                del self.players[player]
                self.manager.sendLogoutNotify(player)
                msg=player+' logout'
                self.output.printMsg(msg)

                continue
    
    # called by clients manager
    def onLogin(self,name):
        self.events.put((2,name))
        pass
    def onMove(self,name,direction):
        self.events.put((3,name,direction))
        pass
    def onAttack(self,attacker,victim):
        self.events.put((4,attacker,victim))
        pass
    def onSpeak(self,name,msg):
        self.events.put((5,name,msg))
        pass
    def onLogout(self,name):
        self.events.put((6,name))
        pass
    def timer(self):
        self.events.put((1,))
        pass

    def stop(self):
        self.events.put((0,))