import random
import socket, time
from dnsPacket import DNSPacket

class DNSPacketModifier:

    def __init__(self, _serverNames, _DNS_UDP_PORT, _BUFFERSIZE):
        self.DNS_UDP_PORT = _DNS_UDP_PORT
        self.BUFFERSIZE = _BUFFERSIZE
        self.serverNames = _serverNames
        self.socket_DNS_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dnsCache = {}

    def modify(self, dnsPacket: DNSPacket):

        t = time.time()
        a = dnsPacket.ArrayOfQuestions[0].get_QNAME()

        if a in self.dnsCache:
            print(self.dnsCache)
            dnsPacket.replaceAllAnswers(self.dnsCache[a][0])
            return dnsPacket

        server = random.choice(self.serverNames)
        self.socket_DNS_out.sendto(dnsPacket.serializePacket(),(server, self.DNS_UDP_PORT))
        data = self.socket_DNS_out.recv(self.BUFFERSIZE)
        packet = DNSPacket(data)
        self.dnsCache[a] = (packet.ArrayOfAnswers, time.time())

        return packet
