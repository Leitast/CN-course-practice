# -*- coding: utf_8 -*-
# ClientsManager will call these methods
class PayloadParser(object):
    """description of class"""
    @staticmethod
    def parseAsInt8(ba):
        return ba[0]
    @staticmethod
    def parseAsString(ba):
        res=""
        cnt=0
        while(ba[cnt]!=0):
            res = res + chr(ba[cnt])
            cnt=cnt+1
        return res
    @staticmethod
    def parseAsLogin(payload):
        name=PayloadParser.parseAsString(payload[0:10])
        return name
        pass
    @staticmethod
    def parseAsMove(payload):
        direction=PayloadParser.parseAsInt8(payload[0:1])
        return direction
        pass
    @staticmethod
    def parseAsAttack(payload):
        victim=PayloadParser.parseAsString(payload[0:10])
        return victim
        pass
    @staticmethod
    def parseAsSpeak(payload):
        msg=PayloadParser.parseAsString(payload)
        return msg
        pass
    @staticmethod
    def parseAsLogout(payload):
        pass# does nothing


