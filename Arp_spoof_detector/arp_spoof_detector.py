#!/usr/bin/env python3
import time
import scapy.all as scapy

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc

# using scapy function to sniff with callback function
def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

def process_sniffed_packet(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2 :
        try:
            real_mac=get_mac(packet[scapy.ARP].psrc)
            reponse_mac=packet[scapy.ARP].hwsrc

            if real_mac != reponse_mac :
                print("you are under attack")
        except IndexError:
            pass


# currently it's hardcoded interface.
sniff("eth0")
