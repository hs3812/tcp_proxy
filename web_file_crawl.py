import urllib2
import os
import threading
import Queue

Num_threads = 100

directory = "/Users/testuser/Downloads/webhost-2.0" # This is the downloaded web application
target = "www.sometarget.com" # set target
ext_to_ignore = [".jpg",".txt".".gif",".png",".css"] #ignore these file extension

def main():
    os.chdir(directory)
    possible_file=Queue.Queue
    for root,dir,file in os.walk("."):
        for f in file:
            path = "%s/%s" %(root,f)
            if path.startswith("."):
                path=path[1:]
            elif os.path.splitext(f)[1] not in ext_to_ignore:
                possible_file.put(path)
    for i in range(Num_threads):
        print "Creating thread %d" %i
        thread = threading.Thread(target=is_on_server(queue=possible_file))
        thread.start()

def is_on_server(queue):
    while not queue.empty():
        path = queue.get()
        url = "%s%s" %(target, path)
        request = urllib2.Request(url)

        try:
            reply = urllib2.urlopen(request)
            html_content = reply.read()
            print "%d ------> %s" %(reply.code, html_content)
            html_content.close()

        except urllib2.HTTPError:
            print "Error occured with %s" %url
            pass

if __name__ == '__main__':
    main()