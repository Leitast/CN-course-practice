# -*- coding: utf_8 -*-

class Output(object):
    """description of class"""
    def __init__(self):
        return super(Output, self).__init__()
    
    def printConnectStatus(self,success):
        if(success):
            print ('connect successfully')
            print 'command> ',

        else:
            print ('The gate to the tiny world of warcraft is not ready.')
        pass
    def printLoginReply(self,success):
        if(success):
            print ("Welcome to the tiny world of warcraft.")
        else:
            print ("A player with the same name is already in the game.")
        pass
    def printMoveNotify(self,name,x,y,hp,exp):
        print (name+': location=('+str(x)+','+str(y)+'), HP='+str(hp)+', EXP='+str(exp)+'.')
        print 'command> ',
        pass
    def printAttackNotify(self,attacker,victim,damaged,hp):
        if(hp==0):
           print attacker+' killed '+victim+'.'
        else:
           print attacker+' damaged '+victim+' by '+str(damaged)+'. '+victim+"’s HP is now "
        print 'command> ',

        pass
    def printSpeakNotify(self,player,msg):
        print player+': '+msg
        print 'command> ',

        pass
    def printLogoutNotify(self,name):
        print 'Player '+name+' has left the tiny world of warcraft.'
        print 'command> ',
        pass

    def printInvalidState(self,code):
        if(code==0):
            print "You must log in first."
        elif (code==1):
            print "You already logged in."
        print 'command> ',
    def printDisconnect(self):
        print "! recv: Connection reset by peer"


