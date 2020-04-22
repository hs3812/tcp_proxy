import sqlite3
import optparse
import os


class FireFox:
    def __init__(self,name,dbpath,cmd):
        self.name = name
        self.dbpath = dbpath
        self.cmd = cmd
    def __repr__(self):
        return "Firefox database at %s"%self.dbpath

    def printdb(self):
        try:
            conn = sqlite3.connect(self.dbpath)
            c = conn.cursor()
            c.execute(self.cmd)
            print ("Retrived the following for db %s:"%self.dbpath)
            print ("Records for "+self.name)
            for row in c:
                for i in range(len(row)):
                    print (row[i])
        except Exception, e:
            if 'encrypted' in str(e):
                print('Update Sqlite3 please')
                return
            else:
                print("Error loading db %s" % self.name)
        finally:
            conn.close()
            return

def printp(Skype):
    try:
        conn = sqlite3.connect(Skype)
        c = conn.cursor()
        c.execute("SELECT fullname,skypename,city,country FROM Accounts;")
        for row in c:
            print('[*] Found the following:')
            print ('User :'+str(row[0]))
            print (str(row[1]))
            print (str(row[2]))
    except:
        print('Error')

    finally:
        conn.close()

def printcontact(Skype):
    try:
        conn = sqlite3.connect(Skype)
        c = conn.cursor()
        c.execute("SELECT displayname,skypename,city,country FROM Contacts;")
        for row in c:
            print('[*] Found the following:')
            print ('User :'+str(row[0]))
            print (str(row[1]))
            print (str(row[2]))
    except:
        print('Error')

    finally:
        conn.close()

def main():
    parser = optparse.OptionParser("Usage%prog"+"-p/-f <skype/firefox databse path> For firefox seperate by ,")
    parser.add_option('-p',dest='pathn',type='string',help='skype database file path')
    parser.add_option('-f',dest='pathn',type='string',help='firefox database file path')
    ops, args =parser.parse_args()
    paths = ops.pathn

    if len(paths)<2:
        if os.path.isdir(path)==False:
            print ("%s doesn't exist"%path)
            exit(-1)

        else:
            Skype = os.path.join(path,'main.db')
            if os.path.isfile(Skype):
                printp(Skype)
                printcontact(Skype)
            else:
                print('Looks like skype databse doesnt exist!')
                exit(0)
    else:
        for path in paths.split(','):
            name = os.path.basename(path)
            cmd = input('Input SQL query command')
            firefox = FireFox(name=name,dbpath=path,cmd=cmd)
            firefox.printdb()


if __name__ == '__main__':
    main()
