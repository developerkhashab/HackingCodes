#!/usr/bin/env python3
import time
import scapy.all as scapy

def sniff (interface):
    scapy.sniff(iface=interface,store=False,prn=process_sniffed_packet)

def process_sniffed_packet(packet):
    print(packet)