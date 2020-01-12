<
# BCIT COMP8505 Final Assignment - Covert Communication Application

## Objective 

- To bring together several stealth software and backdoor concepts covered in class into a single covert communication application.

- To learn how to use such an application in allowing stealthy access to a network or to exfiltrate data from systems within a network.

## Design

### Pseudo Code
 
**program: victim**
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

 **program: client**
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
**program: client\_file**
```
DO sniff for file\_knock packet

    IF authenticated file\_trigger packet

        OPEN scp\_port

        SLEEP for portopen\_duration

        CLOSE scp\_port

    ENDIF

UNTIL program terminated
```
**program: victim\_file**
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
## Tasks and Timeline

<table>
<thead>
<tr class="header">
<th><strong>Task</strong></th>
<th><strong>Notes</strong></th>
<th><strong>Date</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>Multi-packet replies</td>
<td>Allow for command replies with payloads larger than one packet.</td>
<td>11/10</td>
</tr>
<tr class="even">
<td>Packet AUTH system</td>
<td><p>Design and implement improved packet encryption and authentication as current system uses pre determined shared key.</p>
<p>Possible solutions public/private key + password.</p></td>
<td>11/11</td>
</tr>
<tr class="odd">
<td>File-transfers Transfers</td>
<td><p>Determine best file transfer method eg, SCP, SFTP, other. How to authenticate</p>
<p>Test basic standalone functions</p></td>
<td>11/12</td>
</tr>
<tr class="even">
<td>File-watcher</td>
<td>Implement basic file watcher program/thread(no auth or port knocking). That monitors file/dir, zips and sends to open client</td>
<td>11/15</td>
</tr>
<tr class="odd">
<td>Portknocking</td>
<td>Implement port knocking. Will listen for trigger packet and open port to file receiver for set time. Includes auth</td>
<td>11/16</td>
</tr>
<tr class="even">
<td>Port-knocking extra!</td>
<td>Implement Keepalive check for large/slow transfers</td>
<td>11/16 (if time)</td>
</tr>
<tr class="odd">
<td>Testing of above basic functionality</td>
<td>Test/debug the above minimum functionality. Design/determine weaknesses, error handling, resiliency, reliability improvements (keepalives, error handling, retries).</td>
<td>11/17-11/18</td>
</tr>
<tr class="even">
<td>Implement reliability improvements</td>
<td>Implement improvements designed above</td>
<td>11/20 – 11/22</td>
</tr>
<tr class="odd">
<td></td>
<td></td>
<td></td>
</tr>
<tr class="even">
<td></td>
<td></td>
<td></td>
</tr>
<tr class="odd">
<td></td>
<td></td>
<td></td>
</tr>
<tr class="even">
<td></td>
<td></td>
<td></td>
</tr>
<tr class="odd">
<td></td>
<td></td>
<td></td>
</tr>
<tr class="even">
<td></td>
<td></td>
<td></td>
</tr>
<tr class="odd">
<td></td>
<td></td>
<td></td>
</tr>
</tbody>
</table>

## Tests

| **Test**                                  | **Notes**                                                                                                   |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Single packet responses to shell command  | Test received output of Ls, pwd, etc.                                                                       |
| Multipacket responses                     | Test received output of ifconfig, du, etc.                                                                  |
| Test above again with new auth/encryption |                                                                                                             |
| File watch                                | Directory update watch, file create, file update. Ensure above changes are picked up and trigger file send. |
| File watch compression                    | Ensure files are compress/encrypted before file send. And are decompress and decryptable                    |
| Porknocking basic                         | Test opening of file transfer port when trigger packet received.                                            |
| Filewatch + Portknocking + File transfer  | Test all components together.                                                                               |
| Retest above after keepalive implemented  |                                                                                                             |
| Retest all after reliability improvments  |                                                                                                             |
