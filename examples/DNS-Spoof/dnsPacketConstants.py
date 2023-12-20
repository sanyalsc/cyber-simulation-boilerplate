from enum import Enum

class DNSPacketConstants(Enum):
    dns_query = 0
    dns_response = 1
    opcode_query =  0           #       Query                     [RFC 1035]
    opcode_iQuery = 1           #       IQuery  (Inverse Query)   [RFC 1035]
    opcode_status = 2           #       Status                    [RFC 1035]
    opcode_available = 3        #       opcode 3 & 6-15   available for assignment
    opcode_notify = 4           #       Notify                    [RFC 1996]
    opcode_update = 5           #       Update                    [RFC 2136]
    RCODE_NoError =  0          # 0    NoError   No Error                           [RFC 1035]
    RCODE_FormatError =  1      # 1    FormErr   Format Error                       [RFC 1035]
    RCODE_ServFail =  2         # 2    ServFail  Server Failure                     [RFC 1035]
    RCODE_NXDomain =  3         # 3    NXDomain  Non-Existent Domain                [RFC 1035]
    RCODE_NotImp =  4           # 4    NotImp    Not Implemented                    [RFC 1035]
    RCODE_Refused =  5          # 5    Refused   Query Refused                      [RFC 1035]
    RCODE_YXDomain =  6         # 6    YXDomain  Name Exists when it should not     [RFC 2136]
    RCODE_YXRRSet =  7          # 7    YXRRSet   RR Set Exists when it should not   [RFC 2136]
    RCODE_NXRRSet =  8          # 8    NXRRSet   RR Set that should exist does not  [RFC 2136]
    RCODE_NotZone =  10         # 10    NotZone   Name not contained in zone         [RFC 2136]
    RCODE_Available =  11       # 11-15           available for assignment
    RCODE_BADVERS =  16         # 16    BADVERS   Bad OPT Version                    [RFC 2671]