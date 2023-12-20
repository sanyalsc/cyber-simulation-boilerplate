
from Utilities import Util
from questionSection import  *
from answerSection import *
from dnsPacketConstants import DNSPacketConstants

# This class is responsible for parsing the DNS packet
# from a byte array.
#
#                                1  1  1  1  1  1
#  0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
# |                      ID                       |
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
# |QR|   Opcode  |AA|TC|RD|RA|   Z |    RCODE     |
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
# |                QDCOUNT/ZOCOUNT                |
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
# |                ANCOUNT/PRCOUNT                |
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
# |                NSCOUNT/UPCOUNT                |
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
# |                    ARCOUNT                    |
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+


class DNSPacket:

    def __init__(self, _input_Bytes: bytes):
        """
            This is the contructor that creates a new DNS packet from a stream

            Parameters:
            _input_Bytes (bytes[]): The byte array containing the DNS

            Returns:
             a new DNS Packet Object From A byte Stream.

        """
        self.input_Bytes = _input_Bytes
        self.binaryString = Util.hexToBinaryString(_input_Bytes)
        self.ArrayOfQuestions = []
        self.ArrayOfAnswers = []
        self.endOfQuestionSection = 0
        self.endOfAnswerSection = 0
        self.parseQuestionSection() ## Need to Extract Question seciton First The order of the extraction matters
        self.parseAnswerSection()



    def get_ID(self) -> int:
        """
            This function extract the ID A 16 bit identifier assigned by the program
            that generates any kind of query. This identifier
            is copied the corresponding reply and can be used by the requester to match up replies to
            outstanding queries.

        Returns:
            Int: representing the ID.
        """
        return Util.binaryToInt(self.binaryString[0:16])

    def set_ID(self, ID):
        self.binaryString= Util.intToBinary(ID, 16)+self.binaryString[16:]


    def get_QR(self) -> bool:
        """
           This function Extracts the QR bit
           QR A one bit field that specifies whether this message is a query (0), or a response (1).

           Returns:
            (enum) DNSPacketConstants.query or DNSPacketConstants.response

        """
        return Util.binaryToBool(self.binaryString[16])

    def set_QR(self, QR):
        self.binaryString[16] = Util.boolToBinary(QR)

    def get_Opcode(self) -> int:
        """
            OPCODE A four bit field that specifies kind of query in this message.
            Returns:
                (enum) DNSPacketContants.opcode_* depending on the value of the field.
        """
        return Util.binaryToInt(self.binaryString[17:21])

    def set_Opcode(self, opcode):
        self.binaryString =  self.binaryString[17:] + Util.intToBinary(opcode, 4) + self.binaryString[21:]

    def get_Flags(self):
        """
            This function extract the byte containing all the flags. Each flag is extracted individually below
        """
        return self.binaryString[16:32]

    def set_Flags(self, flags):
        self.binaryString =  self.binaryString[16:] + flags + self.binaryString[32:]


    def get_AA(self):
        """
            AA Authoritative Answer - this bit is only meaningful in responses, and specifies that the
            responding name server is an authority for the domain name in question section. You should use this
            bit to report whether or not the response you receive is authoritative.

            Returns:
                boolean: True if it is Authoritative Answer, False otherwize.
        """
        return Util.boolToBinary(self.binaryString[21])

    def set_AA(self, AA):
        self.binaryString[21] =  Util.boolToBinary(AA)

    def get_TC(self) ->bool:
        """
            TC TrunCation - specifies that this message was truncated. For this project, you should treat the packet as dropped if
        Returns:
            boolean:  True if the message was truncated, False otherwize.

        """
        return Util.boolToBinary(self.binaryString[22])

    def set_TC(self, TC):
        self.binaryString[22] =  Util.boolToBinary(TC)

    def get_RD(self)-> bool:
        """
            RD Recursion Desired - this bit directs the name server to pursue the query recursively. You should
            use 1, representing that you desire recursion.

            Returns:
                Boolean: returns True is RD flag is set returns false otherzie
        """
        return Util.boolToBinary(self.binaryString[23])

    def set_RD(self, RD):
        self.binaryString[23] =  Util.boolToBinary(RD)

    def extract_RA(self):
        """ RA Recursion Available - this be is set or cleared in a response, and denotes whether recursive
        query support is available in the name server. For this project you will always set the value to false.

        Returns:
            Boolean: based on RA flag. (It is ok to just return false from this)
        """
        return Util.boolToBinary(self.binaryString[24])

    def get_RA(self, RA)-> bool:
        self.binaryString[24] =  Util.boolToBinary(RA)

    def get_Z(self):
       """ Z Reserved for future use. You must set this field to 0.
            Returns a Boolean (Defaults to false since this is still an experimental field)
       """
       return self.binaryString[25: 28]

    def set_Z(self, binaryStringZ):
        self.binaryString =  self.binaryString[25:] + binaryStringZ + self.binaryString[28:]


    def get_RCODE(self)-> int:
        """
        RCODE Response code - this 4 bit field is set as part of responses. See the DNSPacketConstants For interpretation
        Parse the 4 bit field and return appropriate constant.
        """
        return Util.binaryToInt(self.binaryString[28: 32])

    def set_RCODE(self, RCODE):
        self.binaryString =  self.binaryString[28:] + Util.intToBinary(RCODE, 4) + self.binaryString[32:]


    def get_QDCOUNT(self) -> int:
        """
            QDCOUNT an unsigned 16 bit integer specifying the number of entries in the question section.

            Return:
                Int : represending the number of answers.
        """
        return Util.binaryToInt(self.binaryString[32: 48])

    def set_QDCOUNT(self, QDCOUNT):
        self.binaryString =  self.binaryString[32:] + Util.intToBinary(QDCOUNT, 16) + self.binaryString[48:]


    def get_ANCOUNT(self)-> int:
        """
        ANCOUNT an unsigned 16 bit integer specifying the number of resource records in the answer
        section. If packet does not contain any answers the value of this field will be zero.
        """
        return Util.binaryToInt(self.binaryString[48: 64])

    def set_ANCOUNT(self, ANCOUNT):
        self.binaryString =  self.binaryString[48:] + Util.intToBinary(ANCOUNT, 16) + self.binaryString[64:]


    def get_NSCOUNT(self) -> int:
        """
        NSCOUNT an unsigned 16 bit integer specifying the number of name server resource records in the
        authority records section.

        Return:
            Int: NSCOUNT
        """
        return Util.binaryToInt(self.binaryString[64: 80])

    def set_NSCOUNT(self, NSCOUNT):
        self.binaryString =  self.binaryString[64:] + Util.intToBinary(NSCOUNT, 16) + self.binaryString[80:]


    def get_ARCOUNT(self) -> int:
        """
        ARCOUNT an unsigned 16 bit integer specifying the number of resource records in the additional
        records section.

        Return:
            Int: ARCOUNT
        """
        return Util.binaryToInt(self.binaryString[80: 96])

    def set_ARCOUNT(self, ARCOUNT):
        self.binaryString =  self.binaryString[80:] + Util.intToBinary(ARCOUNT, 16) + self.binaryString[96:]


    def parseQuestionSection(self):
        """
        This function will parse the question section of
        the binary stream and return an array of question
        section object

        Return:
            Array of question section objects. (See QuestionSection Class)
        """
        if(self.get_QDCOUNT() > 0):
            (self.ArrayOfQuestions, length_Question_Section) = QuestionParsingManager.extractQuestionObjects(self.binaryString[96:], self.get_QDCOUNT())
            self.endOfQuestionSection = 96 + length_Question_Section

    def getQuestionSectionAtIndex(self, _index):
        "Returns the question at articular index in the packet"
        return self.ArrayOfQuestions[_index]


    def parseAnswerSection(self):
        """This Function will parse the answer section of the binary stream and return
        an array of answer section objects

        Return:
            Array of answer section objects.

        """
        #print(self.get_ANCOUNT())
        if(self.get_ANCOUNT() > 0):
            (self.ArrayOfAnswers, length_of_answerSection) = AnswerParsingManager.extractAnswerObjects(self.binaryString[self.endOfQuestionSection:], self.get_ANCOUNT())
            self.endOfAnswerSection = self.endOfQuestionSection + length_of_answerSection

    def getAnswerSectionAtIndex(self, _index):
        "Returns the answer at articular index in the packet"
        return self.ArrayOfAnswers[_index]

    def replaceAnswerSection(self, _AnswerObject, _index_to_replace):
        """
            This replaces the answerSection section at the supplied index with the new
            AnswerObject that was passed in as a parameter.

            Returns:
                Does not return anything. Instead in modify the object directly
        """
        self.ArrayOfAnswers[_index_to_replace] = _AnswerObject
        #Now generate the binary string and replace it approprpiate area in self.binaryString
        binaryRepresentation = ''
        for answerSection in self.ArrayOfAnswers:
            binaryRepresentation+= answerSection.get_binaryString()
        self.binaryString = self.binaryString[: self.endOfQuestionSection] + binaryRepresentation + self.binaryString[self.endOfAnswerSection :]

    def replaceAllAnswers(self, list_ans):
        binaryRepresentation = ''
        for answerSection in list_ans:
            binaryRepresentation+= answerSection.get_binaryString()
        end = len(binaryRepresentation)
        self.binaryString = self.binaryString[: self.endOfQuestionSection] + binaryRepresentation + self.binaryString[self.endOfAnswerSection :]
        self.endOfAnswerSection = self.endOfQuestionSection + end


    def serializePacket(self):
        """ Returns a bytes array that can be sent to socket. This binary
        represent the correctly formated packet"""
        return Util.binaryStringToHex(self.binaryString)

    def __str__(self):
        """ A to String implementation that used to generate the string for log
            Do not modifiy this is used by the grader
        """
        string_DNS_packet = ("PACKET HEADER information \n" +
            "ID: " + str(self.get_ID()) +"\n"
             + "QR: "+ str(self.get_QR())  +"\n"
             + "Opcode: " + str(self.get_Opcode()) + "\n"
             + "Flags " + str(self.get_Flags()) +"\n"
             + "AA: " + str(self.get_AA()) + "\n"
             + "TC: " + str(self.get_TC()) + "\n"
             + "RD: " + str(self.get_RD()) + "\n"
             + "Z: " + str(self.get_Z()) + "\n"
             + "RCODE: " + str(self.get_RCODE()) + "\n"
             + "QDCOUNT: " + str(self.get_QDCOUNT()) + "\n"
             + "ANCOUNT: " + str(self.get_ANCOUNT()) + "\n"
             + "NSCOUNT: " + str(self.get_NSCOUNT()) + "\n"
             + "ARCOUNT: " + str(self.get_ARCOUNT()) + "\n")

        for questionSection in self.ArrayOfQuestions:
            string_DNS_packet += "\n" + str(questionSection)

        for answerSection in self.ArrayOfAnswers:
            string_DNS_packet += "\n" + str(answerSection)

        return string_DNS_packet
