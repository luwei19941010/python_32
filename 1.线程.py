#-*-coding:utf-8-*-
# Author:Lu Wei
from multiprocessing import Process
import os
import time

def func():
    print('start', os.getpid())
    time.sleep(3)
    print('end', os.getpid(),os.getppid())

if __name__=='__main__':
    p=Process(target=func)
    p.start()
    print('main1', os.getpid())
print('main2',os.getpid())