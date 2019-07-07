# -*- coding: utf_8 -*-
from Queue import *
from threading import *




class Output(object):
    def __init__(self):
        self.events=Queue()
        return super(Output, self).__init__()
    def run(self):
        thread=Thread(target=self.loop,name='outputMainloop')
        thread.setDaemon(True)
        thread.start()
    def loop(self):
        while(True):
            args=self.events.get()
            type=args[0]
            if(type==0):
                continue
            if(type==1):
                msg=args[1]
                print (msg)
            pass
    def printMsg(self,msg):
        self.events.put((1,msg))
        pass

