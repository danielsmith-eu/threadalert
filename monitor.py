from bs4 import BeautifulSoup
from pync import Notifier
import requests
import sys
import time

if len(sys.argv) < 2:
    print "You must specify the URL to monitor as an argument to the script"
    sys.exit(1)

url = sys.argv[1]
grp = "monitor-{0}".format(url)

threads_seen = {}
while True:
    r = requests.get(url)
    if (r.status_code != 200):
        print "Error getting URL"
    else:
        b = BeautifulSoup(r.text, "html.parser")
        found_forum = False
        got_threads = False
        for tr in b.findAll("tbody"):
            forum_id = tr.attrs.get("id")
            if forum_id and forum_id.startswith("threadbits_forum"):
                found_forum = True
                for td in tr.findAll("a"):
                    thread_id = td.attrs.get("id")
                    if thread_id and thread_id.startswith("thread_title"):
                        if not threads_seen.get(thread_id):
                            threads_seen[thread_id] = True
                            print td.text
                            link = td.attrs.get("href")
                            Notifier.notify(td.text.encode("utf-8"), title = "New Thread Added", open = link, sound = "Submarine", group = grp, sender = "com.google.Chrome")
                        got_threads = True

        if not found_forum:
            print "Couldn't find forum in HTML"
        if not got_threads:
            print "Couldn't find threads in HTML"

    time.sleep(60)
