from bs4 import BeautifulSoup
from pync import Notifier
import requests
import sys
import time
import json
from pushbullet import Pushbullet

config_file = "config.json"
if len(sys.argv) == 2:
    config_file = sys.argv[1];

with open(config_file) as config_open:
    config = json.load(config_open)

grp = "monitor-{0}".format(config_file)
out_type = config.get("output").lower()
pb = None

def output(text, link):
    global pb
    if out_type == "osx":
        Notifier.notify(text, title = "New Thread Added", open = link, sound = "Submarine", group = grp, sender = "com.google.Chrome")
    elif out_type == "pushbullet":
        if pb is None:
            pb = Pushbullet(config.get("pushbullet_access_token"))
        pb.push_link(text, link)

threads_seen = {}
while True:
    for url in config.get("watch"):
        r = requests.get(url)
        if (r.status_code != 200):
            print "Error getting URL " + url
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
                                output(td.text.encode("utf-8"), td.attrs.get("href"))
                            got_threads = True

            if not found_forum:
                print "Couldn't find forum in HTML for " + url
            if not got_threads:
                print "Couldn't find threads in HTML for " + url

    time.sleep(60)

