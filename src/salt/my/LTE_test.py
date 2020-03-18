#!/usr/bin/env python3
# coding: utf8

import time
import os
import os.path
import datetime
import socket
import fileinput
from pathlib import Path
from subprocess import Popen, PIPE
from time import sleep

date = datetime.datetime.now().strftime("%a %b %e %H:%M:%S")
before_date = (" <-> ")
date_log = datetime.datetime.now().strftime("%a %b %e %H:%M")
hostname = socket.gethostname()
file_temp_log = '/opt/lte_log.txt'
file_log = '/opt/{}-{}.txt'.format(date_log,hostname)
file_counter = '/opt/counter.txt'

# color
CRED = '\033[91m' # Red
CEND = '\033[0m' # Default
# background color
RED_B = '\u001b[41;1m'  # Red
WHITE_B = '\u001b[47;1m'  # White
GREEN_B = '\u001b[42;1m'  # Green
YELLOW_B = '\u001b[43;1m'  # Yellow
BLACK_B = 'u001b[40;1m'  # Black
# text style
BIWhite = "\033[1;97m"  # White
BIGreen = "\033[1;92m"  # Green
BIBlack = "\033[1;90m"  # Black


def create_file():
    # Create the files if it does not exist
    file_log2 = Path(file_temp_log)
    if file_log2.is_file():
        pass
    else:
        print("Log File not exist, Creating a file")
        a=open(file_temp_log, 'w')
        a.write(hostname + '\n')
        a.close()
    file_counter2 = Path(file_counter)
    if file_counter2.is_file():
        pass
    else:
        print("counter File not exist, Creating a file")
        init_counter = 0
        b = open(file_counter, 'w')
        b.write(str(init_counter))
        b.close()


# def number_lines(file_log):
#     # Number lines in the "file_log" inplace counting from start
#     with fileinput.FileInput(file_log, inplace=True, backup='.bak') as file:
#         for n, line in enumerate(file, start=0):
#             print(n, line, end='')
#     os.unlink(file_log + '.bak')  # remove backup on success


def countdown_start(seconds_onstart):
    # Countdown before test start
    seconds_onstart = int(5)
    create_file()
    print("LTE test starts in ", seconds_onstart, " seconds")
    if seconds_onstart == 0:
        print("LTE test starting!")
        status()
    else:
        for i in range(seconds_onstart):
            print(str(seconds_onstart - i) + " seconds")
            time.sleep(1)
        print("LTE test starting!")
        status()


def countdown_reboot(seconds_reboot):
    # Countdown before reboot
    print("Rebooting in 3 seconds")
    for i in range(seconds_reboot):
        print(str(seconds_reboot - i) + " seconds to rebooting")
        time.sleep(1)
    print("Rebooting")
    os.system('reboot')


def status_qmi():
    proc = Popen(["qmi-manager", "status"], stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    return out, err


def status():
    # Checking connection
    ok_write = " ->INFO: device is online"
    not_write = " ->ERROR: LTE connection down!"
    create_file()
    counter = open(file_counter, 'r').read()
    counter_now = int(counter)
    out, err = status_qmi()
    if counter_now < 20:
        print("Test number: " + YELLOW_B + BIBlack + str(counter_now) + CEND)
        if "online" in str(out):
            print(GREEN_B + BIBlack + ok_write + CEND)
            f = open(file_temp_log, 'a')
            f.write('Test number ' + before_date + str(counter_now) + date + ok_write + '\n')
            f.close()
            counter_new = int(counter_now) + 1
            c = open(file_counter, 'w+')
            c.write(str(counter_new))
            c.close()
            countdown_reboot(3)
        else:
            print(RED_B + BIWhite + "ERROR: LTE connection down!" + CEND)
            sleep(5)
            e = open(file_temp_log, 'a')
            e.write('Test number ' + before_date + str(counter_now) + date + not_write + '\n')
            e.close()
            h = open(file_temp_log, 'a')
            output_temp = os.popen('systemctl status network-manager.service')
            output = output_temp.read()
            h.write(str(output) + '\n')
            h.close()
            counter_new = int(counter_now) + 1
            k = open(file_counter, 'w+')
            k.write(str(counter_new))
            k.close()
            countdown_reboot(3)
    else:
        print((GREEN_B + BIBlack + "LTE TEST IS FINISHED" + CEND))
        os.system('cp {} {}'.format(file_temp_log, file_log))
        os.system('rm -r {}'.format(file_temp_log))
        os.system('rm -r {}'.format(file_counter))
        exit()
        sleep(3600)
        os.system('sudo poweroff')


countdown_start(5)
