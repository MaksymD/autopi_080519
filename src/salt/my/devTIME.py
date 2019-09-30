import ntplib
from time import ctime


import time
import urllib2
from datetime import datetime

def time():
    c = ntplib.NTPClient()
    response = c.request('pool.ntp.org')
    print(ctime(response.tx_time))
    #Returns Mon Sep 30 11:10:45 2019 (ADD Time Zone)
    return time
    ######################################


def save_time():
    f=open("/home/maxdotsenko/TEST/time.txt", "w")
    for i in range(10):
        f.write("time %d\r\n" % (i+1))
    f.close()


counter = -1
running = False
def stopwatch(label):
    def count():
        if running:
            global counter
            if counter==-1:
                #print to file start counte


def internet_on():
    try:
        urllib2.urlopen('http://216.58.192.142', timeout=1)
        return True
    except urllib2.URLError as err:
        return False