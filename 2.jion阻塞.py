#-*-coding:utf-8-*-
# Author:Lu Wei
from multiprocessing import Process
import os
import random

def func(a):
    random.random()
    print(random.random())
    print('start',a,os.getpid(),os.getppid())

if __name__=='__main__':
    l=[]
    for i in range(10):
        p=Process(target=func,args=(i,))
        p.start()
        l.append(p)
    for p in l:
        p.join()
    print('hahhahaha')
