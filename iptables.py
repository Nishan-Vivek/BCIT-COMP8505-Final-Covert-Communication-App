import iptc
from config import *
import os
import subprocess
#### close port

def closeport():
    command = "iptables -D INPUT -p tcp --destination-port " + str(FILE_TRANSFER_PORT) +  " -j ACCEPT"
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

def openport():
    command = "iptables -A INPUT -p tcp --destination-port " + str(FILE_TRANSFER_PORT) + " -j ACCEPT"
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)


# openport()
closeport()