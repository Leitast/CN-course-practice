# -*- coding: utf_8 -*-
import threading 
from socket import *
from Queue import *




from ClientsManager import *




class Client(object):
    """description of class"""
    def __init__(self,sock,manager,output):
        self.output=output
        self.manager=manager
        self.sendEvents=Queue()
        self.sock=sock
        self.addr=None
        self.name=None
        return super(Client, self).__init__()
    def run(self):
        # begin mainloop
        self.name=self.addr[0]+':'+str(self.addr[1])
        thread=threading.Thread(target=self.send,args=(),name=self.name+'send')
        thread.start()
        self.sendThread=thread
        thread=threading.Thread(target=self.recv,args=(),name=self.name+'recv')
        thread.setDaemon(True)
        thread.start()
        self.recvThread=thread
        pass

    # recv loop
    def recv(self):
        try:
            while(True):
            
                version=self.recvNbytes(1)
                bs=self.recvNbytes(2)
                totalLength=bs[0]*255+bs[1]
                msgtype=self.recvNbytes(1)[0]
                payload=self.recvNbytes(totalLength-4);
                self.manager.onReceivePackage(self,msgtype,payload)
        except:
            # just exit this thread
            msg='disconnected'
            self.output.printMsg(msg)
            self.manager.onDisconnect(self)
        pass
    # send loop
    def send(self):
        while(True):
            args=self.sendEvents.get()
            type=args[0]
            if(type==0):
                self.sock.shutdown(SHUT_RDWR)
                self.sock.close()
                break
                continue
            if(type==1):
                self.sock.sendall(args[1])
                continue
        pass

    #called by the manager
    def sendPackage(self,package):
        self.sendEvents.put((1,package))
        pass
    def setName(self,name):
        self.name=name
        self.sendThread.setName(name+'send')
        self.recvThread.setName(name+'recv')
    def stop(self):
        self.sendEvents.put((0,))
        self.sendThread.join()
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
   
    

