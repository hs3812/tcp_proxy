import ftplib

def login(hostname):
    try:
        ftp = ftplib.FTP(hostname)
        ftp.login('anonymous','12@google.com')
        print 'it accepts anonymous login'
        print hostname
        ftp.quit()
        return 1
    except Exception, e:
        print "%s not accepting anonymous login" % hostname
        return 0



if __name__ == '__main__':
    host = "192.168.0."
    targets = [host + str(ip) for ip in range(0, 255)]
    for ip in targets:
        login(ip)




