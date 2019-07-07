# -*- coding: utf_8 -*-
from Queue import *


import threading 
from Server import *
from Client import *
from PackageMaker import *
from PayloadParser import *



class ClientsManager(object):
    """description of class"""
    def __init__(self,server,output):
        self.output=output
        self.server = server
        self.events = Queue()
        self.names = dict()# map[client object]->name
        self.clients = dict()# map[name]->client object
        # above are clients logined
        self.unloginedClients = set()
        self.listener = None# listening socket
        return super(ClientsManager, self).__init__()
    def listen(self,port):
        addr=('',port)
        self.listener=socket(AF_INET,SOCK_STREAM)
        self.listener.bind(addr)
        self.listener.listen(5)
        while(True):
            try:
                sock,addr = self.listener.accept()
                args=(1,Client(sock,self,self.output))
                args[1].addr=addr
                self.events.put(args)
                self.output.printMsg('new connection from'+addr[0]+':'+str(addr[1]))
            except:
                msg='stop listening'
                self.output.printMsg(msg)
                self.server.stop()
                break
        pass


    def run(self,port):
        thread=threading.Thread(target=self.loop,args=(port,),name='managerLoop')
        thread.start()
        self.loopThread=thread
        thread=threading.Thread(target=self.listen,args=(port,),name='connectionListener')
        thread.setDaemon(True)
        thread.start()
        self.listenThread=thread
        pass
    
    def loop(self,port):
        while(True):
            args = self.events.get()
            type = args[0]
            if(type == 0):
                # stop
                for client in self.names.key():
                    client.stop()
                for client in self.unloginedClients():
                    client.stop()
                self.listener.close()
                break
                continue
            if(type == 1):
                # new connection
                client = args[1]
                self.unloginedClients.add(client)
                client.run()
                continue
            if(type == 2):
                # recv a package
                client = args[1]
                msgtype = args[2]
                payload = args[3]
                if(msgtype == 0x01):
                    # login request
                    msg='login request from '+client.addr[0]+':'
                    name = PayloadParser.parseAsLogin(payload)
                    if(client in self.names):# the client has already logined
                        msg=msg+'the client has already logined'
                        package = PackageMaker.makeInvalidState(1)
                        client.sendPackage(package)
                    elif(name in self.clients):# the name has been used
                        msg=msg+'the name has been used'
                        package = PackageMaker.makeLoginReply(1,0,0,0,0)
                        client.sendPackage(package)
                    else:
                        msg=msg+'succeed'
                        self.unloginedClients.remove(client)
                        self.names[client] = name
                        self.clients[name] = client
                        self.server.onLogin(name)

                    self.output.printMsg(msg)

                    continue
                if(msgtype == 0x03):
                    # move request
                    direction = PayloadParser.parseAsMove(payload)
                    if(self.names.has_key(client)):
                        self.server.onMove(self.names[client],direction)
                    else:
                        client.sendPackage(PackageMaker.makeInvalidState(0))
                    continue
                if(msgtype == 0x05):
                    # attack request
                    victim = PayloadParser.parseAsAttack(payload)
                    if(self.names.has_key(client)):
                        self.server.onAttack(self.names[client],victim)
                    else:
                        client.sendPackage(PackageMaker.makeInvalidState(0))
                    continue
                if(msgtype == 0x07):
                    # speak request
                    msg = PayloadParser.parseAsSpeak(payload)
                    if(self.names.has_key(client)):
                        self.server.onSpeak(self.names[client],msg)
                    else:
                        # 未登录的用户
                        client.sendPackage(PackageMaker.makeInvalidState(0))
                    continue
                if(msgtype == 0x09):
                    # logout request

                    if(self.names.has_key(client)):
                        name=self.names[client]
                        del self.names[client]
                        del self.clients[name]
                        client.stop()
                        self.server.onLogout(name)
                    else:
                        client.sendPackage(PackageMaker.makeInvalidState(0))
                    continue
            if(type == 3):
                # a client disconnect
                client=args[1]
                if(client in self.names):
                    name=self.names[client]
                    del self.names[client]
                    del self.clients[name]
                    self.server.onLogout(name)
                    client.stop()
                elif(client in self.unloginedClients):
                    self.unloginedClients.remove(client)
                    client.stop()
                else:
                    pass# the serve stop the connection first
                
                continue
        pass 
    

    # called by clients
    def onReceivePackage(self,client,type,payload):
        self.events.put((2,client,type,payload))
        pass
    def onDisconnect(self,client):
        self.events.put((3,client,))
        pass
    # 暂时先由server线程发送,本来应该投递给manager的主循环
    # called by the server,if client==None,send the package to all players
    def sendLoginReply(self,code,hp,exp,x,y,receiver=None):
        if(receiver == None):
            pass # shouldn't send it to all
        else:
            if(code == 0):
                # succeed
                self.clients[receiver].setName(receiver)
                package = PackageMaker.makeLoginReply(code,hp,exp,x,y)
                self.clients[receiver].sendPackage(package)
            else:
                # the server refused the name（impossible）
                client = self.clients[receiver]
                self.names.remove(client)
                self.clients.remove(receiver)
                self.unloginedClients.add(client)
                package = PackageMaker.makeLoginReply(code,hp,exp,x,y)
                client.sendPackage(package)
        pass
    def sendMoveNotify(self,name,x,y,hp,exp,receiver=None):
        package = PackageMaker.makeMoveNotify(name,x,y,hp,exp)
        if(receiver == None):
            for client in self.names.keys():
                client.sendPackage(package)
        else:
            self.clients[receiver].sendPackage(package)
        pass
    def sendAttackNotify(self,attacker,victim,damage,hp,receiver=None):
        package = PackageMaker.makeAttackNotify(attacker,victim,damage,hp)
        if(receiver == None):
            for client in self.names.keys():
                client.sendPackage(package)
        else:
            self.clients[receiver].sendPackage(package)
        pass
    def sendSpeakNotify(self,name,msg,receiver=None):
        package = PackageMaker.makeSpeakNotify(name,msg)
        if(receiver == None):
            for client in self.names.keys():
                client.sendPackage(package)
        else:
            self.clients[receiver].sendPackage(package)
        pass
    def sendLogoutNotify(self,name,receiver=None):
        package = PackageMaker.makeLogoutNotify(name)
        if(receiver == None):
            for client in self.names.keys():
                client.sendPackage(package)
        else:
            self.clients[receiver].sendPackage(package)
        pass

    def stop(self):
        self.events.put((0,))
        self.loopThread.join()

        pass


