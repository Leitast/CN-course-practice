# -*- coding: utf_8 -*-
# ClientsManager will call these methods
from socket import *
class PackageMaker(object):
    """description of class"""
    @staticmethod
    def makeHeader(totalLength,msgType):
        version=0x04
        ba=bytearray()
        ba.append(version)
        ba.append((totalLength>>8)&0xFF)
        ba.append((totalLength)&0xFF)
        ba.append(msgType)
        return ba
    @staticmethod
    def makeName(name):
        bstr=bytearray()
        cnt=0
        for ch in name:
            cnt=cnt+1
            bstr.append(ord(ch))
        bstr=bstr+bytearray(10)
        bstr=bstr[0:10]
        return bstr
        pass
    
    @staticmethod
    def makeString(string):
        bstr=bytearray()
        for ch in string:
            bstr.append(ord(ch))
        bstr=bstr+bytearray(0x00)
        
        return bstr
    @staticmethod
    def makeInt8(n):
        ba=bytearray()
        ba.append(n)
        return ba
        pass
    @staticmethod
    def makeInt32(n):
        ba=bytearray()

        ba.append((n>>24)&0xFF)
        ba.append((n>>16)&0xFF)
        ba.append((n>>8)&0xFF)
        ba.append((n)&0xFF)
        return ba
        pass
    @staticmethod
    def makePadding(nbytes):
        if(nbytes<=0):
            return None
        return bytearray(4)[0:nbytes]
    @staticmethod
    def makeLoginReply(code,hp,exp,x,y):
        ba=PackageMaker.makeHeader(0x10,0x02)+PackageMaker.makeInt8(code)+PackageMaker.makeInt32(hp)
        ba=ba+PackageMaker.makeInt32(exp)+PackageMaker.makeInt8(x)+PackageMaker.makeInt8(y)+PackageMaker.makePadding(1)
        return ba.decode()
        pass
    @staticmethod
    def makeMoveNotify(name,x,y,hp,exp):
        ba=PackageMaker.makeHeader(0x18,0x04)+PackageMaker.makeName(name)
        ba=ba+PackageMaker.makeInt8(x)+PackageMaker.makeInt8(y)+PackageMaker.makeInt32(hp)+PackageMaker.makeInt32(exp)
        return ba.decode()
        pass
    @staticmethod
    def makeAttackNotify(attacker,victim,damage,hp):
        ba=PackageMaker.makeHeader(0x18,0x04)+PackageMaker.makeName(player)+PackageMaker.makeName(victim)
        ba=ba+PackageMaker.makeInt8(damage)+PackageMaker.makeInt32(hp)+PackageMaker.makePadding(3)
        return ba.decode()
        pass
    @staticmethod
    def makeSpeakNotify(name,msg):
        length=len(msg)
        totalLength=(4+10+length+3)/4*4
        padding=totalLength-(4+10+length)
        ba=PackageMaker.makeHeader(totalLength,0x08)+PackageMaker.makeName(name)+PackageMaker.makeString(msg)
        padding=PackageMaker.makePadding(padding)
        if(padding!=None):
            ba=ba+padding
        return ba.decode()
        
        pass
    @staticmethod
    def makeLogoutNotify(name):
        ba=PackageMaker.makeHeader(16,0x0a)+PackageMaker.makeName(name)+PackageMaker.makePadding(2)
        return ba.decode()
        pass
    @staticmethod
    def makeInvalidState(code):
        ba=PackageMaker.makeHeader(8,0x0b)+PackageMaker.makeInt8(code)+PackageMaker.makePadding(3)
        return ba.decode()
        pass




