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
        self.ackNum = -1
        self.wait = False
        self.resend = False

        # Packet info
        self.capacity = RDTLayer.FLOW_CONTROL_WIN_SIZE
        self.windowSize = RDTLayer.FLOW_CONTROL_WIN_SIZE
        self.seqNum = 0
        self.data = ''

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
        self.dataReceived = ''

        for element in sorted(self.sentBuffer):
            self.dataReceived = self.dataReceived + self.sentBuffer[element][0]

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
        if self.dataToSend != '':
            for packet in self.sentBuffer:
                if self.sentBuffer[packet][3] == 0:
                    if (self.currentIteration - self.sentBuffer[packet][2]) >= 3:
                        print("TIMEOUT: Resending packet %d" % packet)
                        temp_seq = self.seqNum
                        self.data = self.sentBuffer[packet][0]
                        self.seqNum = packet
                        self.processSend()
                        self.seqNum = temp_seq
            if self.windowSize == 0:
                print('window is full')
            else:
                while self.windowSize > 0:
                    self.capacity = min([RDTLayer.DATA_LENGTH, (RDTLayer.FLOW_CONTROL_WIN_SIZE - (self.nextseqnum - self.send_base))])
                    self.data = self.dataToSend[self.nextseqnum:(self.nextseqnum + self.capacity)]
                    print("Data to send: ", self.data)
                    self.nextseqnum += len(self.data)
                    print("Chars sent: %d  Chars ack: %d  Window Space: %d" % (
                        self.nextseqnum, self.charsAck, (RDTLayer.FLOW_CONTROL_WIN_SIZE - (self.nextseqnum - self.charsAck))))
                    self.processSend()
                    print("seq num is: %d" % self.seqNum)
                    self.seqNum += 1
                    print("seq num is now: %d" % self.seqNum)
                    self.windowSize = RDTLayer.FLOW_CONTROL_WIN_SIZE - (self.nextseqnum - self.send_base)
        self.processReceiveAndSendRespond()

    # ################################################################################################################ #
    # makePkt()                                                                                                        #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Takes seqNum and data as parameters and creates a packet                                                         #
    # ################################################################################################################ #
    def makePkt(self, seqNum, data):
        segmentSend = Segment()
        segmentSend.setData(seqNum, data)
        print("Sending segment: ", segmentSend.to_string())
        # self.charsSent += len(data)
        # print("Chars sent: %d  Chars ack: %d  Window Space: %d" % (
        #     self.charsSent, self.charsAck, (RDTLayer.FLOW_CONTROL_WIN_SIZE - (self.charsSent - self.charsAck))))
        print("Wait is TRUE")
        # self.wait = True

        # Add sent packet to packet buffer
        self.sentBuffer[seqNum] = [data, segmentSend, self.currentIteration, 0]

        return segmentSend

    # ################################################################################################################ #
    # udpSend()                                                                                                        #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Uses unreliable channel to send a packet                                                                         #
    #                                                                                                                  #
    # ################################################################################################################ #
    def udpSend(self, packet):
        self.sendChannel.send(packet)
        return

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
            sndPkt = self.makePkt(self.seqNum, self.data)
            self.udpSend(sndPkt)
            # segmentSend = Segment()

            # #################################################################################################### #

            # You should pipeline segments to fit the flow-control window
            # The flow-control window is the constant RDTLayer.FLOW_CONTROL_WIN_SIZE
            # The maximum data that you can send in a segment is RDTLayer.DATA_LENGTH
            # These constants are given in # characters

            # Somewhere in here you will be creating data segments to send.
            # The data is just part of the entire string that you are trying to send.
            # The seqnum is the sequence number for the segment (in character number, not bytes)


            # #################################################################################################### #
            # Display sending segment
            # segmentSend.setData(self.seqNum, data)
            # print("Sending segment: ", segmentSend.to_string())
            # self.charsSent += len(data)
            # print("Chars sent: %d  Chars ack: %d  Window Space: %d" % (self.charsSent, self.charsAck, (RDTLayer.FLOW_CONTROL_WIN_SIZE - (self.charsSent - self.charsAck))))
            # print("Wait is TRUE")
            # self.wait = True
            #
            # # Add sent packet to packet buffer
            # self.sentBuffer[self.seqNum] = [data, segmentSend, 'no']
            #
            # # Use the unreliable sendChannel to send the segment
            # self.sendChannel.send(segmentSend)

    # ################################################################################################################ #
    # processReceive()                                                                                                 #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Manages Segment receive tasks                                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processReceiveAndSendRespond(self):
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

        # ############################################################################################################ #
        # What segments have been received?
        # How will you get them back in order?
        # This is where a majority of your logic will be implemented

        # DATA SEGMENT
        # Check incoming packet. Verify checksum and assign acknum
        for item in listIncomingSegments:
            segmentAck = Segment()  # Segment acknowledging packet(s) received
            # Check if segment contains data or is ACK packet
            if item.payload != "":
                print("Data - checksum is: ", item.checkChecksum())
                self.timeOutCounter = 0
                # Data is valid, unpack data and send ACK
                if item.checkChecksum():
                    if item.seqnum < self.seqNum:
                        segmentAck.setAck(item.seqnum)
                    # If seq num matches, receive data, otherwise just send ACK
                    print("item: %d, self: %d" % (item.seqnum, self.seqNum))
                    print("item is: ", item.payload)
                    if item.seqnum == self.seqNum:
                        # self.ackNum = self.seqNum
                        self.ackNum = item.seqnum
                        self.sentBuffer[item.seqnum] = [item.payload]
                        self.seqNum += 1
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
                    print("ACK - checksum is: ", item.checkChecksum())
                    # Received NAK, resend packet
                    if self.ackNum < 0:
                        self.ackNum = 0
                    print("item: %d, self: %d" % (item.acknum, self.ackNum))
                    if item.acknum != self.ackNum:
                        print("Bad ACK")

                    # Received ACK, update seq num and send next packet
                    else:
                        # Stop timer
                        self.sentBuffer[item.acknum][3] = 1
                        # Update send window
                        # -------------------------------------------------
                        self.send_base += len(self.sentBuffer[item.acknum][0])
                        self.windowSize += len(self.sentBuffer[item.acknum][0])
                        print("send_base: %d, window size: %d" % (self.send_base, self.windowSize))
                        # ----------------------------------------------------

                        # build new packet
                        self.capacity = min([RDTLayer.DATA_LENGTH,
                                             (RDTLayer.FLOW_CONTROL_WIN_SIZE - (self.nextseqnum - self.send_base))])
                        self.data = self.dataToSend[self.nextseqnum:(self.nextseqnum + self.capacity)]
                        print("Data to send: ", self.data)
                        self.nextseqnum += len(self.data)
                        print("Chars sent: %d  Chars ack: %d  Window Space: %d" % (
                            self.nextseqnum, self.charsAck,
                            (RDTLayer.FLOW_CONTROL_WIN_SIZE - (self.nextseqnum - self.charsAck))))

                        # send packet
                        self.processSend()
                        print("seq num is: %d" % self.seqNum)

                        # update sequence number and window size
                        self.seqNum += 1
                        self.windowSize -= len(self.data)
                        print("seq num is now: %d" % self.seqNum)
                        self.timeOutCounter = 0
                        self.ackNum += 1
                        # print("ACK - Window is now: %d" % (self.charsSent - self.charsAck))


                # This was used for earlier iterations w/ stop and wait
                # Checksum is corrupted, resend packet
                else:
                    pass
                    # print("Garbled ACK/NAK - Retransmitting")
                    # self.timeOutCounter += 1
                    # # self.wait = False
                    # self.resendPacket(self.ackNum + 1)
                    # # self.processSend()

                # if self.timeOutCounter > 3:
                #     print("TIMEOUT: Resending data")
                #     # self.wait = False
                #     self.countSegmentTimeouts += 1
                #     self.resendPacket(self.ackNum)
                #     # self.processSend()

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

