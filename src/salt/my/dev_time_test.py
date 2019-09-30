 #!/usr/bin/env python
# Python Network Programming Cookbook -- Chapter - 1
# This program is optimized for Python 2.7. It may run on any
# other Python version with/without modifications

from __future__ import print_function
import ntplib
from time import ctime

x="some new time"

def print_time():
    ntp_client = ntplib.NTPClient()
    response = ntp_client.request('pool.ntp.org')
    print(ctime(response.tx_time))
    #format time 2019-09-20T17:21:06.960870

# def save_time():
#     file="/home/maxdotsenko/TEST/time.txt"
#     with open(file, "w") as f:
#         f.write("time now " +   x +"\n")
#         #print ('whatever', file=f)
#     f.close()
#
# functions = [save_time()]
# def loop():
#     y = 0
#     for i in range(10):
#         functions[i]()
#         if y == 10:
#             break
#         y += 1

if __name__ == '__main__':
    print_time()
    #save_time()
    #loop()
