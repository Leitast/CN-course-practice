
from Game import *
from PackageMaker import *
import threading 
import multiprocessing.queues
from PayloadParser import *
from socket import *
class Server(object):
    """description of class"""
    def __init__(self):
        self.game=None
        self.server=None
        self.sendEvents=multiprocessing.queues.SimpleQueue()
        self.state=0
        return super(Server, self).__init__()
    def connect(self,address,port):
        serverAddr=(address,port)
        self.sock=socket(AF_INET,SOCK_STREAM)
        try:
            self.sock.connect(serverAddr)
            return True
        except:
            return False
            
    def run(self):
        self.recvThread = threading.Thread(target=self.recv,args=(),name='recvThread')
        self.recvThread.setDaemon(True)
        self.recvThread.start()
        self.sendThread=threading.Thread(target=self.send,args=(),name='sendThread')
        self.sendThread.start()
        
    def send(self):
        while(True):
            args=self.sendEvents.get()
            eventType=args[0]
            if(eventType==0):
                # stop:
                self.sock.shutdown(SHUT_RDWR)
                self.sock.close()
                break
                continue
            if(eventType==1):
                # login
                self.sock.sendall(PackageMaker.makeLoginPackage(args[1]))
                continue
            if(eventType==2):
                # move  
                self.sock.sendall(PackageMaker.makeMovePackage(args[1]))
                continue
            if(eventType==3):
                # attack
                self.sock.sendall(PackageMaker.makeAttackPackage(args[1]))
                continue
            if(eventType==4):
                # speak
                self.sock.sendall(PackageMaker.makeSpeakPackage(args[1]))
                continue
            if(eventType==5):
                # logout
                self.sock.sendall(PackageMaker.makeLogoutPackage())
                continue

    def recv(self):
        try:
            while(True):
                version=self.recvNbytes(1)[0]
                bs=self.recvNbytes(2)
                totalLength=bs[0]*255+bs[1]
                msgtype=self.recvNbytes(1)[0]
                payload=self.recvNbytes(totalLength-4);
                
                if(msgtype==0x02):
                    # login reply
                    code,hp,exp,x,y=PayloadParser.parseAsLoginReply(payload)
                    self.game.onLoginReply(code,hp,exp,x,y)
                    continue
                if(msgtype==0x04):
                    # move notify
                    player,x,y,hp,exp=PayloadParser.parseAsMoveNotify(payload)
                    self.game.onMoveNotify(player,x,y,hp,exp)
                    continue
                if(msgtype==0x06):
                    # attack notify
                    attacker,victim,damaged,hp=PayloadParser.parseAsAttackNotify(payload)
                    self.game.onAttackNotify(attacker,victim,damaged,hp)
                    continue
                if(msgtype==0x08):
                    # speak notify
                    player,msg=PayloadParser.parseAsSpeakNotify(payload)
                    self.game.onSpeakNotify(player,msg)
                    continue
                if(msgtype==0x0a):
                    # logout notify
                    name=PayloadParser.parseAsLogoutNotify(payload)
                    self.game.onLogoutNotify(name)
                    continue
                if(msgtype==0x0b):
                    # invalid state
                    code=PayloadParser.parseAsInvalidState(payload)
                    self.game.onInvalidState(code)
                    continue
        except:
            self.game.stop()
        
            


        
    # call by game
    def stop(self):
        self.sendEvents.put((0,))
        self.sendThread.join()
        pass
    def sendLoginMsg(self,name):
        self.sendEvents.put((1,name))
        pass
    def sendMoveMsg(self,direction):
        self.sendEvents.put((2,direction))
        pass
    def sendAttackMsg(self,victim):
        self.sendEvents.put((3,victim))
        pass
    def sendSpeakMsg(self,msg):
        self.sendEvents.put((4,msg))
        pass
    def sendLogoutMsg(self):
        self.sendEvents.put((5,))
        pass	

    def recvNbytes(self,nbytes):
        if(nbytes<=0):
            return None
        buf = bytearray(nbytes)
        view = memoryview(buf)
        if(self.sock.recv_into(view,nbytes)==0):
            # the socket has been closed
            raise Exception('the socket has been closed')
        return buf

