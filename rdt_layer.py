from segment import Segment


# #################################################################################################################### #
# RDTLayer                                                                                                             #
#                                                                                                                      #
# Description:                                                                                                         #
# The reliable data transfer (RDT) layer is used as a communication layer to resolve issues over an unreliable         #
# channel.                                                                                                             #
#                                                                                                                      #
#                                                                                                                      #
# Notes:                                                                                                               #
# This file is meant to be changed.                                                                                    #
#                                                                                                                      #
#                                                                                                                      #
# #################################################################################################################### #


class RDTLayer(object):
    # ################################################################################################################ #
    # Class Scope Variables                                                                                            #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    DATA_LENGTH = 4 # in characters                     # The length of the string data that will be sent per packet...
    FLOW_CONTROL_WIN_SIZE = 15 # in characters          # Receive window size for flow-control
    sendChannel = None
    receiveChannel = None
    dataToSend = ''
    currentIteration = 0                                # Use this for segment 'timeouts'
    # Add items as needed

    # ################################################################################################################ #
    # __init__()                                                                                                       #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def __init__(self):
        self.sendChannel = None
        self.receiveChannel = None
        self.dataToSend = ''
        self.dataReceived = ''
        self.currentIteration = 0
        self.seqNum = 0
        self.countSegmentTimeouts = 0
        self.wait = False
        # Add items as needed

    # ################################################################################################################ #
    # setSendChannel()                                                                                                 #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the unreliable sending lower-layer channel                                                 #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setSendChannel(self, channel):
        self.sendChannel = channel

    # ################################################################################################################ #
    # setReceiveChannel()                                                                                              #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the unreliable receiving lower-layer channel                                               #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setReceiveChannel(self, channel):
        self.receiveChannel = channel

    # ################################################################################################################ #
    # setDataToSend()                                                                                                  #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the string data to send                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setDataToSend(self, data):
        self.dataToSend = data

    # ################################################################################################################ #
    # getDataReceived()                                                                                                #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to get the currently received and buffered string data, in order                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def getDataReceived(self):
        # ############################################################################################################ #
        # Identify the data that has been received...

        print('getDataReceived(): Complete this...')

        # ############################################################################################################ #
        return self.dataReceived

    # ################################################################################################################ #
    # processData()                                                                                                    #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # "timeslice". Called by main once per iteration                                                                   #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processData(self):
        self.currentIteration += 1
        self.processSend()
        self.processReceiveAndSendRespond()

    # ################################################################################################################ #
    # processSend()                                                                                                    #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Manages Segment sending tasks                                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processSend(self):

        # Create data segments to send
        # packetList = []
        # char = 0
        # while char < len(self.dataToSend):
        #     packetList.append(self.dataToSend[char:(char+4)])
        #     char += 4
        #
        # while self.sentPackets < len(packetList):
        #     if self.sentNotAck < RDTLayer.FLOW_CONTROL_WIN_SIZE:

        # If there is no data to send, skip this
        if self.dataToSend == '':
            print("No data to send")
            return

        if not self.wait:
            segmentSend = Segment()

            # #################################################################################################### #

            # You should pipeline segments to fit the flow-control window
            # The flow-control window is the constant RDTLayer.FLOW_CONTROL_WIN_SIZE
            # The maximum data that you can send in a segment is RDTLayer.DATA_LENGTH
            # These constants are given in # characters

            # Somewhere in here you will be creating data segments to send.
            # The data is just part of the entire string that you are trying to send.
            # The seqnum is the sequence number for the segment (in character number, not bytes)

            # Create packet to send and increment packets sent
            # while self.sentNotAck < RDTLayer.FLOW_CONTROL_WIN_SIZE:
            # print("data should be: ", self.dataToSend[charsToSend:(charsToSend + 4)])
            # data = packetList[self.sentPackets]
            data = self.dataToSend[:4]

            # #################################################################################################### #
            # Display sending segment
            segmentSend.setData(self.seqNum, data)
            print("Sending segment: ", segmentSend.to_string())
            print("Wait is TRUE")
            self.wait = True

            # Use the unreliable sendChannel to send the segment
            self.sendChannel.send(segmentSend)

    # ################################################################################################################ #
    # processReceive()                                                                                                 #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Manages Segment receive tasks                                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processReceiveAndSendRespond(self):
        segmentAck = Segment()                  # Segment acknowledging packet(s) received
        # This call returns a list of incoming segments (see Segment class)...

        # If not incoming data, skip this
        listIncomingSegments = self.receiveChannel.receive()
        if len(listIncomingSegments) == 0:
            print("No segments received")
            return

        # This just displays the incoming segments
        # for item in listIncomingSegments:
        #     print("Item is: ")
        #     item.printToConsole()

        # ############################################################################################################ #
        # What segments have been received?
        # How will you get them back in order?
        # This is where a majority of your logic will be implemented

        # DATA SEGMENT
        # Check incoming packet. Verify checksum and assign acknum
        for item in listIncomingSegments:
            print("checksum is: ", item.checkChecksum())
            # Check if segment contains data or is ACK packet
            if item.payload != "":
                # Data is valid, unpack data and send ACK
                if item.checkChecksum():
                    # If seq num matches, receive data, otherwise just send ACK
                    if item.seqnum == self.seqNum:
                        self.dataReceived = self.dataReceived + item.payload
                    if self.seqNum == 0:
                        self.seqNum = 1
                    else:
                        self.seqNum = 0
                    acknum = "0"
                    segmentAck.setAck(acknum)
                    print("Sending ack: ", segmentAck.to_string())
                    self.sendChannel.send(segmentAck)

                # send NAK
                else:
                    acknum = "-1"
                    segmentAck.setAck(acknum)
                    print("Sending ack: ", segmentAck.to_string())
                    self.sendChannel.send(segmentAck)




        # ############################################################################################################ #
        # How do you respond to what you have received?
        # How can you tell data segments apart from ack segemnts?

        # ACK/NAK SEGMENT
        for item in listIncomingSegments:
            if item.payload == "":
                # Checksum is valid
                if item.checkChecksum():
                    # Received NAK, resend packet
                    if item.acknum == '-1':
                        print("NAK - Wait FALSE")
                        self.wait = False
                        print("Resending data")
                        self.processSend()

                    # Received ACK, update seq num and send next packet
                    else:
                        if self.seqNum == 0:
                            self.seqNum = 1
                        else:
                            self.seqNum = 0
                        print("ACK - Wait FALSE")
                        self.wait = False
                        self.dataToSend = self.dataToSend[4:]
                        self.processSend()

                # Checksum is corrupted, resend packet
                else:
                    print("Garbled ACK/NAK - Retransmitting")
                    self.wait = False
                    self.processSend()

        # Somewhere in here you will be setting the contents of the ack segments to send.
        # The goal is to employ cumulative ack, just like TCP does...
        # acknum = "0"


        # ############################################################################################################ #
        # Display response segment
        # segmentAck.setAck(acknum)
        # print("Sending ack: ", segmentAck.to_string())

        # Use the unreliable sendChannel to send the ack packet
        # self.sendChannel.send(segmentAck)

