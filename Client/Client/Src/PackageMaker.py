# coding= utf-8
import socket
import ctypes
import struct


class PackageMaker(object):
    """description of class"""
   
    @staticmethod
    def makeLoginPackage(name):
        # version-8bits totalLength-16bits msgType-bits
        #           payload-96bits(12bytes)
        #print socket.ntohs(16)
        version=0x04
        totalLength=0x10
        msgType=0x01
        ba=bytearray()
        ba.append(version)
        ba.append((totalLength>>8)&0xFF)
        ba.append((totalLength)&0xFF)
        ba.append(msgType)
        for ch in str(name):
            ba.append(ord(ch))
        ba=ba+bytearray(12)
        ba=ba[0:16]
        return ba.decode()
        pass
    @staticmethod
    def makeMovePackage(direction):
        version=0x04
        totalLength=0x08
        msgType=0x03
        ba=bytearray()
        ba.append(version)
        ba.append((totalLength>>8)&0xFF)
        ba.append((totalLength)&0xFF)
        ba.append(msgType)

        direction=direction.lower();
        if direction=="north":
            direction=0x00;
        elif direction=="south":
            direction=0x01;
        elif direction=="east":
            direction=0x02;
        elif direction=="west":
            direction=0x03;
        else:
            direction=0xff;
        ba.append(direction)
        ba=ba+bytearray(12)
        ba=ba[0:totalLength]
        return ba.decode()
        pass
    @staticmethod
    def makeAttackPackage(victim):
        version=0x04
        totalLength=0x10#16
        msgType=0x05
        ba=bytearray()
        ba.append(version)
        ba.append((totalLength>>8)&0xFF)
        ba.append((totalLength)&0xFF)
        ba.append(msgType)
        for ch in str(victim):
            ba.append(ord(ch))
        ba=ba+bytearray(16)
        ba=ba[0:totalLength]
        return ba.decode()
        pass
    @staticmethod
    def makeSpeakPackage(msg):
        len=0
        bstr=bytearray()
        for ch in str(msg):
            bstr.append(ord(ch))
            len=len+1


        version=0x04
        totalLength=(4+len+3)/4*4#向上32位对齐
        msgType=0x07
        ba=bytearray()
        ba.append(version)
        ba.append((totalLength>>8)&0xFF)
        ba.append((totalLength)&0xFF)
        ba.append(msgType)
        ba=ba+bstr
        ba=ba+bytearray(4)
        ba=ba[0:totalLength]
        return ba.decode()
        pass
    @staticmethod
    def makeLogoutPackage():
        version = 0x04
        len = 0x04
        type = 0x09
        ba=bytearray()
        ba.append(version)
        ba.append((len>>8)&0xFF)
        ba.append((len)&0xFF)
        ba.append(type)
        return ba.decode()
        pass	


