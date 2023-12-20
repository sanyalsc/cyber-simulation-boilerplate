#!/bin/bash
python /code/ARP-spoof/arp_spoofer.py 192.168.12.60 192.168.12.1 & disown
python /code/ARP-spoof/dns_spoofer.py
