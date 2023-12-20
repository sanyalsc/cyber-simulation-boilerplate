from Utilities import Util
import logging

"""
                                    1  1  1  1  1  1
      0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                                               |
    /                                               /
    /                      NAME                     /
    |                                               |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      TYPE                     |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                     CLASS                     |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      TTL                      |
    |                                               |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                   RDLENGTH                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--|
    /                     RDATA                     /
    /                                               /
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

    """


class AnswerSection:
    def __init__(self, _binaryString):
        self.binaryString = _binaryString
        self.RDLENGTH = 0

    def get_binaryString(self):
        """
            Returns a binary string representation of the QuestionSection
        """
        return self.binaryString

    def get_NAME(self):
        """
        NAME            a domain name to which this resource record pertains.
        Most moderm DNS servers will use a compressed representation for the
        NAME object this compress representation
        0xc Name is a pointer
        0x00c Pointer is to the name at offset 0x00c (0x03777777...)
        You will only have to deal with the compressed respresentation value 0xc00c
        """
        if (self.binaryString[0:16] != "1100000000001100"):
            return "None Pointer Style Not supported"
            logging.info('DNS recieved unsported NAME Format %s', 'not of the form c0c0x', extra={
                         'NAME': self.binaryString[0:16]})

            # raise Exception('parse NAME block in answer section and result was not of from 0xc0 0x0c')
        return b'\xc0\x0c'

    def get_TYPE(self) -> int:
        """
        TYPE            two octets containing one of the RR type codes.  This
                        field specifies the meaning of the data in the RDATA
                        field.

        """
        return Util.binaryToInt(self.binaryString[16:32])
        # TODO: Student impment this method

    def get_CLASS(self) -> int:
        """
        CLASS           two octets which specify the class of the data in the
                        RDATA field.
        """
        return Util.binaryToInt(self.binaryString[32:48])
        # TODO: Student impment this method

    def get_TTL(self):
        """
            TTL             a 32 bit unsigned integer that specifies the time
                            interval (in seconds) that the resource record may be
                            cached before it should be discarded.  Zero values are
                            interpreted to mean that the RR can only be used for the
                            transaction in progress, and should not be cached.
        """
        return Util.binaryToInt(self.binaryString[48:80])
        # TODO: Student impment this method

    def get_RDLENGTH(self):
        """RDLENGTH        an unsigned 16 bit integer that specifies the length in
                        octets of the RDATA field.
                        """
        self.RDLENGTH = Util.binaryToInt(self.binaryString[80:96])
        #print(self.binaryString[80:96])
        return self.RDLENGTH
        # TODO: Student impment this method

    def set_RDLENGTH(self, _RDLENGTH):
        """
            Function takes an int and sets the lenght value for RD_DATA
        """
        self.binaryString = self.binaryString[:80] + \
            Util.intToBinary(_RDLENGTH, 16) + self.binaryString[96: ]
        # TODO: Student impment this method

    def get_RDATA(self) -> str:
        """
        RDATA           a variable length string of octets that describes the
                        resource.  The format of this information varies
                        according to the TYPE and CLASS of the resource record.
                        For example, the if the TYPE is A and the CLASS is IN,
                        the RDATA field is a 4 octet ARPA Internet address.
        For this assignment only have to support (Type AAAA with CLASS: IN)  and Type: A with ClASS: IN
        """
        idx = 96
        endidx = 96 + (8 * self.RDLENGTH)
        ty = self.get_TYPE()
        st = ""
        if ty == 5:
            st = Util.binaryToAscii(self.binaryString[idx:])
        elif ty == 1:
            st = Util.binaryToIpAddress(self.binaryString[idx:], 4)
        elif ty == 28:
            st = Util.binaryToIpAddress(self.binaryString[idx:], 6)
            #print(Util.binaryStringToHex(self.binaryString[idx:]))
        else:
            st = ""
        
        return st
        

    def set_RDATA(self, _ip_address):
        # TODO: Student impment this method
        ip = 6 if len(_ip_address) > 16 else 4
        self.binaryString = self.binaryString[:96] + Util.IpAddressToBinary(_ip_address, 4)
        

    def __str__(self):
        """ A to String implementation that used to generate the string for log
            Do not modifiy this is used by the grader
        """
        return ("Answer Section Information \n"
            + "Name: "+str(self.get_NAME()) + "\n"
            + "Type: " + str(self.get_TYPE()) + "\n"
            + "Class: " + str(self.get_CLASS()) + "\n"
            + "TTL: " + str(self.get_TTL()) + "\n"
            + "RDLENGTH: " + str(self.get_RDLENGTH()) + "\n"
            + "RDDATA: " + self.get_RDATA() + "\n")

    def serializeAnswerSection(self):
        """
         This function returns a byte array repsenting the answer section it should correctly
         Be carefully when serializing the RDATA field

         """
        return Util.binaryStringToHex(self.binaryString)


class AnswerParsingManager:

    @staticmethod
    def extractAnswerObjects(_binaryString, _answer_count):
        """
        Simular to question Parsing Manager the answer parsing manager class is responsible for parsing section all answer sections
        Creating a AnswerSection Array and the index of the bit representing where the next section begins.

        Returns
            A tuple of the form
                (Array_of_Answers, base )
        """
        #print(Util.binaryStringToHex(_binaryString))
        ans_array = []
        len_binary_string = len(_binaryString)
        base = 0 
        end_of_section = 0 
        for currentQuestion in range(0, _answer_count):
            rdat_len = Util.binaryToInt(_binaryString[base + 80 : base + 96])
            newbase = base + (rdat_len * 8) + 96
            ans_array.append(AnswerSection(_binaryString[base:newbase]))
            #print(Util.binaryStringToHex(_binaryString[base:newbase]))
            base = newbase
            end_of_section = base
        return (ans_array, end_of_section) 
           