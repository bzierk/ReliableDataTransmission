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
#                                                                                                                      #
#                                                                                                                      #
# SOURCES:                                                                                                             #
# https://gaia.cs.umass.edu/kurose_ross/interactive/rdt30.php                                                          #
# https://www.youtube.com/watch?v=vxgH6r-II2Q                                                                          #
# http://www2.ic.uff.br/~michael/kr1999/3-transport/3_040-principles_rdt.htmo                                          #
# https://www.d.umn.edu/~gshute/net/reliable-data-transfer.xhtml                                                       #
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
    TIMEOUT_LIMIT = 3                                   # Number of iterations before a timeout is called
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
        self.ackNum = -1
        self.wait = False
        self.resend = False

        # Track sent and ack characters
        self.send_base = 0
        self.nextseqnum = 0

        # Handles tracking timeouts
        self.timeOutCounter = 0
        self.countSegmentTimeouts = 0

        # use for printing
        self.charsAck = 0
        self.charsSent = 0

        # Holds record of sent segments
        self.sentBuffer = dict()

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
            capacity = min([RDTLayer.DATA_LENGTH, (RDTLayer.FLOW_CONTROL_WIN_SIZE - (self.nextseqnum - self.send_base))])
            data = self.dataToSend[self.charsSent:(self.charsSent + capacity)]

            # #################################################################################################### #
            # Display sending segment
            segmentSend.setData(self.seqNum, data)
            print("Sending segment: ", segmentSend.to_string())
            self.charsSent += len(data)
            print("Chars sent: %d  Chars ack: %d  Window Space: %d" % (self.charsSent, self.charsAck, (RDTLayer.FLOW_CONTROL_WIN_SIZE - (self.charsSent - self.charsAck))))
            print("Wait is TRUE")
            self.wait = True

            # Add sent packet to packet buffer
            self.sentBuffer[self.seqNum] = [data, segmentSend, 'no']

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
            self.timeOutCounter += 1
            print("Timeout counter: ", self.timeOutCounter)

            # TIMEOUT - If timeout counter is exceeded, increment Timeout Count and resend packet
            if self.timeOutCounter > 3:
                print("TIMEOUT: Resending data")
                self.wait = False
                self.countSegmentTimeouts += 1
                self.processSend()

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
                self.timeOutCounter = 0
                # Data is valid, unpack data and send ACK
                if item.checkChecksum():
                    # If seq num matches, receive data, otherwise just send ACK
                    print("item: %d, self: %d" % (item.seqnum, self.seqNum))
                    if item.seqnum == self.seqNum:
                        # self.ackNum = self.seqNum
                        self.ackNum = item.seqnum
                        self.dataReceived = self.dataReceived + item.payload
                    self.seqNum += 1
                    # if self.seqNum == 0:
                    #     self.seqNum = 1
                    # else:
                    #     self.seqNum = 0
                    segmentAck.setAck(self.ackNum)
                    print("Sending ack: ", segmentAck.to_string())
                    self.sendChannel.send(segmentAck)

                # send NAK
                else:
                    segmentAck.setAck(self.ackNum)
                    print("Sending ack: ", segmentAck.to_string())
                    print("Need to send: %d" % self.seqNum)
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
                    # if item.acknum != self.seqNum:
                    if item.acknum != self.seqNum:
                        self.timeOutCounter += 1
                        print("NAK - Wait FALSE")
                        # self.wait = False
                        print("Resending data for ack: %d" % (self.ackNum + 1))
                        self.resendPacket(self.ackNum + 1)
                        # self.processSend()

                    # Received ACK, update seq num and send next packet
                    else:
                        # if self.seqNum == 0:
                        #     self.seqNum = 1
                        # else:
                        #     self.seqNum = 0
                        self.send_base += len(self.sentBuffer[self.seqNum][0])
                        self.seqNum += 1
                        print("ACK - Wait FALSE")
                        self.wait = False
                        self.timeOutCounter = 0
                        self.ackNum = item.acknum
                        # print("ACK - Window is now: %d" % (self.charsSent - self.charsAck))
                        # self.dataToSend = self.dataToSend[4:]
                        self.processSend()

                # Checksum is corrupted, resend packet
                else:
                    print("Garbled ACK/NAK - Retransmitting")
                    self.timeOutCounter += 1
                    # self.wait = False
                    self.resendPacket(self.ackNum + 1)
                    # self.processSend()

                if self.timeOutCounter > 3:
                    print("TIMEOUT: Resending data")
                    # self.wait = False
                    self.countSegmentTimeouts += 1
                    self.resendPacket(self.ackNum + 1)
                    # self.processSend()

        # Somewhere in here you will be setting the contents of the ack segments to send.
        # The goal is to employ cumulative ack, just like TCP does...
        # acknum = "0"

        # ############################################################################################################ #
        # Display response segment
        # segmentAck.setAck(acknum)
        # print("Sending ack: ", segmentAck.to_string())

        # Use the unreliable sendChannel to send the ack packet
        # self.sendChannel.send(segmentAck)

    def resendPacket(self, sequenceNumber):
        segmentSend = self.sentBuffer[sequenceNumber][1]
        segmentSend.setData(sequenceNumber, self.sentBuffer[sequenceNumber][0])
        print("Sending segment: ", segmentSend.to_string())
        self.sendChannel.send(segmentSend)

