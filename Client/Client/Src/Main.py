from Game import*
import argparse
import sys
def usage():
    print 'error'
    pass
def parseArgs():
    if(len(sys.argv)!=5):
        usage()
        return
    address=None
    port=None
    if(sys.argv[1]=='-p'):
        port=sys.argv[2]
    if(sys.argv[3]=='-s'):
        address=sys.argv[4]
    if(port!=None and address!= None):
        return address,port
    usage()  
if (__name__ == '__main__'):

    address,port='192.168.110.134',3344
    #address,port=parseArgs()
    print address
    print port
    Game().run(address,port)
    pass