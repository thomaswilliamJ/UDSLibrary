'''
Created on 18-Jan-2021

@author: thomas
'''
driver = None
address = None
diag_txid = None
diag_rxid = None
diag_funcid = None

'''Handshaking Flag'''
Active   = 1
Deactive = 0
Debug    = 0             #Set = 1 for print the debug
Physical = 0
Functional = 1
UDS_Active = Deactive
ResponsePending = 0

Final_data_output = {}
tempres_length = 0
tempres_buffer = []
tempreq_buffer = []
receivedbytes = 0
remainingbytes = 0
messagereceived = 0
req_id = 0

'''Frame Masking'''
FrameMask   = 0xF0
DTCMask     = 0x09
SingleFrame = 0x00
FirstFrame  = 0x10
Consecutive = 0x20
FlowControl = 0x30
ECU_Response= 0x40
TP_Mask     = 0x80
MultiFrame  = 0x21
Negativeresponse = 0x7F
Responsependingmask = 0x78
Testerpresent = 0x7E

'''Timing Control'''
P2TIMEOUT = 150
P2EXTTIME = 2000
S3TIMEOUT = 5000
STmin = 0x14
bSTmin = 20
FrameWaitTime = 20

exitcommandvalue = False
