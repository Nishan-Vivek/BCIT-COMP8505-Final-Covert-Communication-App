# BCIT COMP8505 Final Assignment - Covert Communication Application

Originally submitted by Adam Harrison & Nishan Vivekanandan

# Table of Contents


[**Objective**](#objective)

**[Design](#design)**

> [Architecture Diagram](#architecture-diagram)
> 
> [System Diagram](#system-diagram)
> 
> [Pseudo Code](#pseudo-code)
> 
> [program: victim](#program-victim)
> 
> [program: attacker](#program-attacker)
> 
> [program: door](#program-door)
> 
> [program: victim\_file](#program-victim_file)

**[Program Instructions](#program-instructions)**

**[Tests](#tests)**

> [Basic Functionality](#basic-functionality)
> 
> [Send Commands](#send-commands)
> 
> [File Watching Exfiltration](#file-watching-exfiltration)
> 
> [File Get Exfiltration](#file-get-exfiltration)
> 
> [Port Knocking](#port-knocking)
> 
> [Process Hiding](#process-hiding)
> 
> [Firewall Bypassing](#firewall-bypassing)
> 
> [Encryption](#encryption)

 

   

# Objective

To bring together several stealth software and backdoor concepts covered
in class into a single covert communication application. To learn how to
use such an application in allowing stealthy access to a network or to
exfiltrate data from systems within a network.

# Design

## Architecture Diagram

![](.//media/image6.png)

## System Diagram

![](.//media/image16.png)

## Pseudo Code

### program: victim
```
Set process name to hide backdoor  
DO Sniff for trigger packet on specific ports  
    If trigger packet  
        Authenticate and Decrypt command playload with public key  
            If authenticated  
                CALL ProcessPayload(command) returns reply  
                numberOfpackets = reply.size / max\_payload\_size  
                CALL SendReply(reply, numberOfpackets, command.clientIP)  
            ENDIF  
    ENDIF  
UNTIL program terminated  

FUNCTION ProcessPayload(decrypted\_command)  
    IF command is type shell  
        Run shell command and capture output  
        return output  
    IF command is type fileWatch  
        CALL program victim\_file in own thread  
        return "ok"  
    IF command is type ?OTHER?  
        CALL ?OTHER? function and ouput  
        return output  
......//other payload types  
    ENDIF  
END FUNCTION  

FUNCTION SendReply(reply, numberOfpackets, IP)  
    encrypted\_reply = ENCRYPT reply with KEY  
    IF numberOfpackets \> 0  
        FOR numberOfpackets  
            send(reply, packetnumber, numberOfpackets, IP)  
            listen for confirmation  
        END FOR  
    ELSE  
        send(reply, 0, 1, IP)  
    ENDIF  
END FUNCTION
```
### program: attacker
```
READ from Args: targetIP  
DO  
    READ from user prompt: command  
    IF NOT valid command  
        PRINT "Re-input command"  
        CONTINUE  
    ELSE  
        CALL SendCommand(targetIP, command)  
    ENDIF  
UNTIL program terminated  
  
  
FUNCTION SendCommand(targetIP, command)  
    encrypted\_command = ENCRYPT command with key  
    sendTriggerPacket(encrypted\_command, targetIP)  
    CALL listenForResponse()  
END FUNCTION  
  
FUNCTION listenForResponse()  
    sniff for response\_packet  
        IF response\_packet.numberOfpackets == 1  
            DECRYPT response\_packet.reply  
            PRINT reply  
            RETURN  
        ELSE  
            FOR numberOfpackets  
                sniff for multi packet response  
                reply += reponse\_packet.reply  
                sendConfirmationPacket(response\_packet.packetnumber)  
            END FOR  
            DECRYPT reply  
            PRINT REPLY  
        END IF  
END FUNCTION
```
### program: door
```
DO sniff for file\_knock packet  
    IF authenticated file\_trigger packet  
        OPEN scp\_port  
        SLEEP for portopen\_duration  
        CLOSE scp\_port  
    ENDIF  
UNTIL program terminated
```
### program: victim\_file
```
READ from args file\_path, file\_key, SCP\_auth  
DO watch file\_path  
    IF file\_path triggered  
        ZIP file and encrypte with file\_key  
        SEND file\_knock packet  
        SCP zip file using SCP\_auth auth parameters  
    END IF  
UNTIL program terminated
```
# Program Instructions

This project was written and tested on Fedora 26 64bit X86 workstations.
Using Python 2.7 and the *scapy*, *pycrypto*, *setproctitle* and *watchdog*
python libraries. Please ensure these requirements are met before
attempting to run. A setup.py file has been included with the pip
commands for convenience.

Extract the submitted zip file on the test systems and go to the app
folder. The config.py houses all the configuration needed for all parts
of the program. You can set the encryption keys and password (or leave
the defaults), the victim and attacker covert channel port combination,
the victim and attacker IP’s, the port used for the file exfiltration as
well the IP addresses that are used for the source IP field in the port
knocks. For the purposes of testing only the IP addresses need be
changed to match the test machines, the other settings may be left at
the provided values.

On the Victim machine launch the following:

`python victim.py`

On the attacker machine launch the following in two separate terminal
sessions:

`python attacker.py`

`python door.py`

The attacker.py program will then prompt for a command. There are 3
types of commands.

> 1\. Terminal Commands - Just type any bash shell command. The command
> will be run on the victim machine and the output displayed back on the
> attacker.
> 
> 2\. File retrieval – Type `getfile`. You will then be prompted for the
> path of the file you wish to exfiltrate. Upon entering the path, the
> victim will send knock packets back to the attacker machine which will
> be picked up by door.py. The file transfer port will be opened, and
> the file send via socket transfer to the attacker machine. Upon
> completion the port will be closed again.
> 
> 3\. File watching – Type `watchfile`. You will then be prompted for
> the path to the file you wish to watch. The victim machine will launch
> a watchdog thread to monitor the file for activity upon any file
> creation or update the victim will automatically send knock packets to
> the attacker and transfer the file.

   

# Tests

## Basic Functionality

### Send Commands

The basic functionality for sending commands, is sending a command from
the attacker machine to the victim in a covert manner. Our application
satisfies this constraint and handles command results of any size by
chunking the data into sendable chunks. Encryption and password
authentication are enforced on both sides of the transmission. The
transmission is done using raw sockets, the packets however to have a
transport layer protocol attached for filtering and camouflage from IDS
and other detection systems.

![](.//media/image5.png)

We are able to send command like **ls** and get back the full result.

![](.//media/image8.png)

Ifconfig works great as well.

![](.//media/image7.png)

The victim just outputs when it sends a packet.

### File Watching Exfiltration

Our file watching exfiltration takes advantage of a cross platform
library; built in python called watchdog. Watchdog has the ability to
watch directories and create threaded handlers that will handle the
condition you supply. In our projects case, we are watching for file
updates on a given file. When this occurs, we start a port knocker to
open up a port on the attacker and follow by sending the encrypted data
to the attacker application. The application authenticates and decrypts
the packets data, which includes the file name, and crafts a file from
the contents. We can start watching, or change the watching file by
entering **watchfie** in the command box, which follows with a prompt
for the file you would like to watch.

![](.//media/image22.png)

We can easily watch a file by entering **watchfile** as the command.
This will then prompt for a file to watch, in our case we use
**/var/log/secure**.

When the file is touched our attacker door application receives a port
knock from the victim machine.

![](.//media/image19.png)

The victim sends three knocks, and then once the port it opened, send
the file to the attacker.

Our attacker gets output like this, as well as the file being saved into
the current working directory.

![](.//media/image11.png)

The attacker decodes the knocks from the victim, and opens the port and
application for file transfer.

![](.//media/image12.png)

Depicted below are the firewall rules changing for opening and closing
of the ports.

![](.//media/image4.png)

Port opened on 8505 for file transfer.

![](.//media/image18.png)

Accept rule removed after transfer.

### File Get Exfiltration

Having the ability to watch files is cool, but if we want to download a
file this second, we need a way to get it covertly. Since we have the
functionality to send files, we just need to implement a way for the
user to request the file. The user can request a file by entering
**getfile** as the command. This will proceed with a second prompt to
enter the absolute path of the file that you want to download. The get
file uses the same concealing, encryption and authentication as the
watching.

![](.//media/image10.png)

![](.//media/image17.png)

We can request a file from the victim by using the **getfile** command.
It follows the exact same workflow for getting access as the watch file
exfiltration does.

### Port Knocking

The port knocking is implemented for the file transfer part of the
application. When requesting, or a change is captured by a set watcher,
we must port knock the attacker to get it to open a port so we can send
the encrypted data to it. We implemented the port knocking by sending
three distinct packets with special source IPs, the port knocker
authenticates these and ensures they are within the configurations set
timeframe. The port knocker then inserts a firewall rule to allows
packets to the requested port and starts the file transfer server.

![](.//media/image21.png)

![](.//media/image11.png)

## Process Hiding

Our application implements a process disguise so analysts and monitoring
applications, won’t be alerted by it’s presence.

![](.//media/image13.png)

We decided to hide our backdoor as **dwarf-shell** but our application
allows for any name viable for the use case of the backdoor.

## Firewall Bypassing

For the sending and receiving of the command, we are using libpcap, this
is on the same level as kernel applications such as netfilter. This
allows us to capture packets at the same level as the firewall. We can
capture and do whatever we want with the packets that we receive. In our
projects case, reading and parsing command, and sending the results
back.

![](.//media/image20.png)

![](.//media/image9.png)

Our application still works great with a total restricted firewall. We
can still send a receive commands as usual.

## Encryption

Every component that produces transmission, encrypts the data before
transmission. This keeps the data from our application safe from
analysts and some network monitoring applications.

![](.//media/image1.png)

![](.//media/image3.png)

All data in our application is encrypted, as depicted above in one of
our command transfers.
