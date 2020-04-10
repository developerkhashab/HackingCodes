#!/usr/bin/env python3
import netfilterqueue
import scapy.all as scapy


def process_packet(packet):
    scapy_packet=scapy.IP(packet.get_payload())
    print(scapy_packet.show())
    packet.accept()


queue = netfilterqueue.Netfilterqueue()
# in binding we specify the queue that we choose in iptable command
queue.bind(0, process_packet)
queue.run()

# we activate the arp_spoofer so we can intercept any request.
# what happens in this file is we trap the requests from target in our queue
# so we can drop/ accpet/ modify it.

# this is how to insall netfilterqueue in python 3.8
# apt install python3-pip git libnfnetlink-dev libnetfilter-queue-dev
# pip3 install -U git+https://github.com/kti/python-netfilterqueue

# in terminal : iptables -I FORWARD -j NFQUEUE --queue-num 0
# to delete ip tables in terminal : iptables --flush
