import socket
import sys
import threading

from pip._vendor.urllib3.connectionpool import xrange


def proxy_handler(client_sock,r_host,r_port,rf):
    r_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r_sock.connect((r_host,r_port))
    if rf:
        r_buffer = receive_from (r_sock)
        hexdump(r_buffer)

        r_buffer = response_handler(r_buffer)
        if len(r_buffer):
            client_sock.send(r_buffer)
    while 1:
        l_buffer = receive_from(client_sock)

        if len(l_buffer):
            hexdump(l_buffer)
            l_buffer = request_handler(l_buffer)
            r_sock.send(l_buffer)
            print("sent to remote")
        r_buffer=receive_from(r_sock)
        if len(r_buffer):
            hexdump(r_buffer)
            r_buffer = response_handler(r_buffer)
            client_sock.send(r_buffer)
            print("sent to lhost")


        if not len(l_buffer) or not len(r_buffer):
            client_sock.close()
            r_sock.close()
            print("connection closed")
            break

def main():

    if len(sys.argv[1:]) != 6:
        print("Usage: python proxy.py [l_host][L-port][r-host][r-port][rf]")
        sys.exit(0)

    else:
        l_host,l_port = sys.argv[2],sys.argv[3]
        r_host,r_port = sys.argv[4],sys.argv[5]
        rf = sys.argv[6]
        server_loop(l_host, l_port, r_host, r_port, rf)

def server_loop(l_host,l_port,r_host,r_port,receive_first):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((l_host,l_port))

    except:
        print("Fail to listen on &s:%d" %(l_host,l_port))
        sys.exit(-1)
    print("listening on %s:%d", %(l_host,l_port))
    server.listen(3)

    while 1:
        client_sock, address = server.accept()
        print("Received from %s:%d" % (address[0],address[1]))
        threads = threading.Thread(target=proxy_handler, args=(client_sock,r_host,r_port,receive_first))
        threads.start()

def hexdump(src):
    leng = 16
    result = []
    digits = 4 if isinstance(src,unicode) else 2
    for i in xrange(0,len(src),leng):
        s = src[i:i+leng]
        hexa = b''.join()



def receive_from(conn):
    buff = ""
    conn.settimeout(2)
    try:

        while 1:

            data = conn.recv(2048)
            if not data:
                break
            buff += data
    except:
        pass
    return buff

def request_handler(buff):
    return buff

def response_handler(buff):
    return buff






main()