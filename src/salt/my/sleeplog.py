# from src.salt.base.ext._modules.power import hibernate
import mmap
import os


def errors_scan():
    path = '/home/maksymd/Desktop/Work/Aviloo/test/'
    filename = 'testlog'
    for filename in os.listdir(path):
        f = open(filename, 'r')
        s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        if s.find('error') != -1:
            print('True')
        else:
            print('False')

#
# def sleepcan(textContent, keyword):
#     if lines=textContent.split("\n")
#     count=len([1 for line in lines if line.find(keyword)!=-1])
#     return count
#
#     file=open(r "\var\log'salt\minion", "r", encoding="utf-8-sig")
#
# >>> yourTextFile="hello world\n some words here\n goodbye world"
# >>> kwdCount(ourTextFile,"ERROR")
#     2:
#     hibernate() #calling hibernate function
