#!/usr/bin/env python3
import netfilterqueue
import scapy.all as scapy

ack_list=[]
# processing packet for further changes, like now we are redirecting to another IP
def process_packet(packet):
    # loading  packet with scapy
    scapy_packet = scapy.IP(packet.get_payload())

    # check scapy packet if it has dns response
    if scapy_packet.haslayer(scapy.Raw):
        # checking if it is HTTP request by destination port (dport)
        if scapy_packet[scapy.TCP].dport == 80:
            print("HTTP Request")

            # checking request if contain any excutable file requested to download
            # you can change the type of file as u want like .pdf
            if ".exe" in scapy_packet[scapy.Raw].load:
                print("[+] exe request")
                print(scapy_packet.show())
        elif scapy_packet[scapy.TCP].sport == 80:
            print("HTTP Response")
            print(scapy_packet.show())

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
