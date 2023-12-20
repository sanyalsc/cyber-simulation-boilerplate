import argparse
import logging, sys
import socket
from  dnsPacket import DNSPacket
from dnsPacketModifier import DNSPacketModifier

DNS_UDP_PORT = 53
BUFFERSIZE = 1024

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-rServer', action='append', 
        help='the DNS server to forward recursive queries to.  If multiple entries are passed, random lookup will be enabled.')
    parser.add_argument('-local-ip', help='host ip address')
    args = parser.parse_args()


    #Setup UDP socket that will  receice DNS request
    sock_DNS_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_DNS_in.bind((args.local_ip, DNS_UDP_PORT))

    #New instance of the Modifier
    modifier = DNSPacketModifier(args.rServer, DNS_UDP_PORT, BUFFERSIZE)

    while True:
        data, addr = sock_DNS_in.recvfrom(BUFFERSIZE) # buffer size is 1024 bytes
        logging.info('DNS Server State: %s', 'started and recieved first packet', extra={'bufferSize': BUFFERSIZE})
        dnsPacket = DNSPacket(data)
        print("----------------Packet Recieved------------\n " + str(dnsPacket))
        dnsPacketModified = modifier.modify(dnsPacket)
        print("----------------Packet Sent--------------\n " + str(dnsPacketModified))
        sock_DNS_in.sendto(dnsPacketModified.serializePacket(), addr)

main()
