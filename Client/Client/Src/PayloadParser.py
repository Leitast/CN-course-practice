class PayloadParser(object):
    """description of class"""
    @staticmethod
    def parseAsInt8(ba):
        return ba[0]
    @staticmethod
    def parseAsInt32(ba):
        n=0
        n=n*255+ba[0]
        n=n*255+ba[1]
        n=n*255+ba[2]
        n=n*255+ba[3]
        return n
    @staticmethod
    def parseAsString(ba):
        res=""
        cnt=0
        while(ba[cnt]!=0):
            res = res + chr(ba[cnt])
            cnt=cnt+1
        return res


    @staticmethod
    def parseAsLoginReply(payload):
        code=PayloadParser.parseAsInt8(payload[0:1])
        hp=PayloadParser.parseAsInt32(payload[1:5])
        exp=PayloadParser.parseAsInt32(payload[5:9])
        x=PayloadParser.parseAsInt8(payload[9:10])
        y=PayloadParser.parseAsInt8(payload[10:11])
        return code,hp,exp,x,y
        pass
    @staticmethod
    def parseAsMoveNotify(payload):
        player=PayloadParser.parseAsString(payload[0:10])
        x=PayloadParser.parseAsInt8(payload[10:11])
        y=PayloadParser.parseAsInt8(payload[11:12])
        hp=PayloadParser.parseAsInt32(payload[12:16])
        exp=PayloadParser.parseAsInt32(payload[16:20])
        return player,x,y,hp,exp
        pass
    @staticmethod
    def parseAsAttackNotify(payload):
        attacker_name = PayloadParser.parseAsString(payload[0:10])
        victim_name = PayloadParser.parseAsString(payload[10:20])
        damage = PayloadParser.parseAsInt8(payload[20:21])
        HP = PayloadParser.parseAsInt32(payload[21:25])
        return attacker_name, victim_name, damage, HP
        pass
    @staticmethod
    def parseAsSpeakNotify(payload):
        #bytearray().
        player=PayloadParser.parseAsString(payload[0:10])
        msg=PayloadParser.parseAsString(payload[10:])
        return player,msg
        pass
    @staticmethod
    def parseAsLogoutNotify(payload):
        player=PayloadParser.parseAsString(payload[0:10])
        return player
        pass
    @staticmethod
    def parseAsInvalidState(payload):
        code=PayloadParser.parseAsInt8(payload[0:1])
        return code
        pass


