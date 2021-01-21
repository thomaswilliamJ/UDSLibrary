'''
Created on 18-Jan-2021

@author: thomas
'''
from lib import PCANBasic
import sys
from driver import canmessageframe
class peakdriver(object):
    '''
    This class will create interface between Peak and our uds library
    '''
    
    
    def __init__(self, baud = 500000):
        
        global objPCAN,channel
        objPCAN = PCANBasic.PCANBasic()
        if baud == 500000:
            brd = PCANBasic.PCAN_BAUD_500K
        elif baud == 250000:
            brd = PCANBasic.PCAN_BAUD_250K
        elif baud == 100000:
            brd = PCANBasic.PCAN_BAUD_100K
        elif baud == 125000:
            brd = PCANBasic.PCAN_BAUD_125K
        channel = PCANBasic.PCAN_USBBUS1
        stat=objPCAN.Initialize(channel, brd)
        if stat == 0:
            print('DEBUG   >   PCAN STATUS:CONNECTED')
        else:
            print('DEBUG   >   PCAN STATUS:NOTCONNECTED')
            sys.exit()
            
    def getmessageframe(self):
        global  objPCAN,channel
        value = objPCAN.Read(channel)
        readmsg = value[1]
        if readmsg.MSGTYPE == PCANBasic.PCAN_MESSAGE_EXTENDED:
            ext = True
        else:
            ext = False
        if value[0] == 0:
            return canmessageframe.messageframe(readmsg.ID,ext,readmsg.DATA,readmsg.LEN)
    def sendmessageframe(self,ids,data,isext = False):
        global  objPCAN,channel
        rqmsg = PCANBasic.TPCANMsg()
        rqmsg.ID = ids
        if isext:
            rqmsg.MSGTYPE = PCANBasic.PCAN_MESSAGE_EXTENDED
        else:
            rqmsg.MSGTYPE = PCANBasic.PCAN_MESSAGE_STANDARD
        rqmsg.LEN = len(data)
        rqmsg.DATA = data
        result = objPCAN.Write(channel,rqmsg)
        if objPCAN.GetErrorText(result)[1] == b'No Error':
            return True
        else:
            return False
        
        
        