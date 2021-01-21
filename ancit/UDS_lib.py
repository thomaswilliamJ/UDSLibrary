'''
Created on 09-Jan-2021

@author: thomas
'''

import threading
from ancit import globalvariables as gv
class udslibrary(object):
    '''
    This class contain the operation of uds on demand
    '''
    
    def __init__(self, busdriver = None,address = 0, physical_msgid = 0x102, functional_msgid = 0x101,receive_msgid = 0x100):
        '''
        This function is used to define Global varaible defined in CAPL
        @param driver: This will be used for sending and receiving can frame
        '''
        
        ''' Message ID for your Project '''
        
        gv.driver = busdriver
        gv.diag_txid = physical_msgid
        gv.diag_rxid = receive_msgid
        gv.diag_funcid = functional_msgid
        gv.address = address
        
        
    def onmessage_Event(self):
        '''
        * This function receives all CAN messages from the driver defined in constructor
        * This function have to run parallel in a thread to watch the can bus
        '''
        while gv.exitcommandvalue == False:
            if gv.UDS_Active == gv.Active:
                msg = gv.driver.getmessageframe()
                if msg.id == gv.diag_rxid:
                    th_res = threading.Thread(target = self.receivediagresponse,args = (msg,))
                    th_res.start()
    
    def senddiagrequest(self,requestdata):
        '''
        This Function will send the Request frame in the pysical/function address
        @param address: This will be Functional or Physical
        @param requestdata: Request data list
        '''
        
        if not gv.UDS_Active == gv.Deactive:return False
        if len(requestdata > 7):
            gv.tempreq_buffer = requestdata
            
        if gv.address == gv.Physical:
            res = gv.driver.sendmessageframe(gv.diag_txid,requestdata)
        else:
            res = gv.driver.sendmessageframe(gv.diag_funcid,requestdata)
        if res['result'] == 'success':
            gv.tempreq_buffer = requestdata
            gv.req_id = gv.req_id+1
            gv.Final_data_output[gv.req_id] = [{'request':res['request']}]
            gv.UDS_Active = gv.Active
            gv.messagereceived = 0
            return True
        else:
            return False
    
    def receivediagresponse(self,msg):
        '''
        This Function records the data from the frames using Transfer protocol and assign it to the corresponding Request
        @param msg: A single can msg with ID, data, length, etc.
        '''
        framedata = msg.data
        frame = framedata[0] & gv.FrameMask
        
        if frame == gv.FirstFrame:
            print('INFO    >   First Frame Received')
            self.SendFlowControl([0x30,0x00,gv.STmin,0x00,0x00,0x00,0x00,0x00])
            gv.tempres_length = int((str(hex(msg.data[0] & 0x0F))[2:3]+str(hex(msg.data[1]))[2:4]),16)
            gv.tempres_buffer[0:6] = msg.data[2:8]
            gv.receivedbytes = 6
            gv.remainingbytes = gv.tempres_length - 6
            gv.messagereceived = 0
            
        elif frame == gv.Consecutive:
            print('INFO    >   Consecutive Frame Received')
            if (gv.tempres_length - gv.receivedbytes) > 7:
                gv.tempres_buffer[gv.receivedbytes:(gv.receivedbytes+7)] = msg.data[1:8]
                gv.receivedbytes = gv.receivedbytes + 7
                gv.remainingbytes = gv.remainingbytes - 7
                gv.messagereceived = 0
            else:
                gv.tempres_buffer[gv.receivedbytes:gv.tempres_length] = msg.data[1:(gv.tempres_length - gv.receivedbytes)+1]
                gv.remainingbytes = gv.remainingbytes - (gv.tempres_length - gv.receivedbytes)
                gv.messagereceived = 1
                
        elif frame == gv.FlowControl:
            print('INFO    >   Flowcontrol Frame Received')
            
        elif frame == gv.SingleFrame:
            print('INFO    >   Single Frame Received')
            gv.tempres_length = msg.data[0]
            gv.tempres_buffer[0:gv.tempres_length] = msg.data[1:gv.tempres_length+1]
            gv.messagereceived = 1
        
        if gv.messagereceived == 1:
            if gv.tempres_buffer[0] == gv.tempreq_buffer[0] + gv.ECU_Response:
                print('INFO    >   Positive Response Received')
                gv.UDS_Active = gv.Deactive
                gv.Responsepending = 0
                gv.Final_data_output[gv.req_id][0]['response'] = gv.tempreq_buffer
                gv.Final_data_output[gv.req_id][0]['status'] = 'Positive'
                gv.tempres_buffer = []
                gv.tempreq_buffer = []
            elif gv.tempres_buffer[0] == gv.Negativeresponse:
                
                if gv.tempres_buffer[2] == gv.Responsependingmask:
                    gv.Responsepending = 1
                else:
                    print('INFO    >   Negative Response Received')
                    gv.Responsepending = 0
                    gv.tempres_buffer = []
                    gv.UDS_Active = gv.Deactive
            elif gv.tempres_buffer[0] == gv.Testerpresent:
                pass
            
            
    def SendFlowControl(self,flwdata):
        
        '''
        This Function will transmit the Flow control message to targeted ID
        '''
        if gv.address == gv.Physical:
            res = gv.driver.sendmessageframe(gv.diag_txid,flwdata)
        else:
            res = gv.driver.sendmessageframe(gv.diag_funcid,flwdata)
        if res['result'] == 'success':
            print('Flow Control Frame sent!!!')
            return True
        else:
            return False
        
            
        
        