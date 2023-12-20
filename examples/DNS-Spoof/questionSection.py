
"""
                                    1  1  1  1  1  1
      0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                                               |
    /                     QNAME                     /
    /                                               /
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                     QTYPE                     |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                     QCLASS                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
"""
from Utilities import Util

class QuestionSection:

    def __init__ (self , _binary_string, _CNAME_end_index):
        self.binary_string = _binary_string
        self.CNAME_end_index = _CNAME_end_index

    def get_binaryString(self):
        """
            Returns a binary string representation of the QuestionSection
        """
        return self.binary_string

    def get_QNAME(self):
        """
        You need to be carefully when extracting the QNAME pay close attention to
        how the information is laid out. Use wireshark to debug your server and inspect.
        You can configure wireshark to capture loopback packets

        QNAME           a domain name represented as a sequence of labels, where
                        each label consists of a length octet followed by that
                        number of octets.  The domain name terminates with the
                        zero length octet for the null label of the root.  Note
                        that this field may be an odd number of octets; no
                        padding is used."""
        return Util.binaryToAsciiQNAME(self.binary_string[:self.CNAME_end_index-8]) #Don't about the zero octect


    def get_QTYPE(self):
        """
        QTYPE           a two octet code which specifies the type of the query.
                        The values for this field include all codes valid for a
                        TYPE field, together with some more general codes which
                        can match more than one type of RR. (see dnsPacket.py and dnsPacketConstants.py
                        use the same constants here) """
        return Util.binaryToInt(self.binary_string[self.CNAME_end_index:self.CNAME_end_index+16])

    def get_QCLASS(self) -> int:
        """
        QCLASS          a two octet code that specifies the class of the query.
                For example, the QCLASS field is IN for the Internet.
                """

        return Util.binaryToInt(self.binary_string[self.CNAME_end_index+16:self.CNAME_end_index+32])


    def serializeQuestionSection(self) -> int:
         """
         This function returns a byte array repsenting the question
         """
         return Util.binaryStringToHex(self.binary_string[:self.CNAME_end_index+32])

    def __str__(self):
        """ A to String implementation that used to generate the string for log
            Do not modifiy this is used by the grader
        """
        return("Question Section \n"
                +"QNAME: "+ self.get_QNAME() +"\n"
                +"QTYPE: "+ str(self.get_QTYPE()) +"\n"
                +"QCLASS: "+ str(self.get_QCLASS()) +"\n"
        )


class QuestionParsingManager():
    """Class responsible for extracting the binaryData for each question object"""


    @staticmethod
    def extractQuestionObjects(_binary_string, _question_count):
        questionArray = []
        len_binary_string = len(_binary_string)
        base = 0  # represents the end position of the last questoin
        #Each of index of the null character considering current index
        end_of_section = 0
        for currentQuestion in range(0, _question_count):
            for i in range(base, len_binary_string, 8):
                    if _binary_string[i: i+8] == "00000000" :# The CNAME Section terminates with an octect of zero \0x00
                        newbase =  i+40 # Then end of the octet + length QType+ Qclass 8+16+16
                        questionArray.append(QuestionSection(_binary_string[base:newbase], i+8))
                        base = newbase
                        end_of_section = base
                        break
        return (questionArray, end_of_section )
