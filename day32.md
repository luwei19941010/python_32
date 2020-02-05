### day32

#### 今日内容

#### 1.进程

​	进程是计算机中最小的资源分配单位

​			1.数据隔离的

进程特点：

- ​	创建进程	时间开销大
- ​	销毁进程	时间开销大
- ​	进程之间切换 	时间开销大

如果两个程序，分别要做两个事



#### 2.线程

​			只负责执行代码，不负责存储共享数据，也不负责资源分配。

- 是进程中的一部分
- 每个进程至少有一个线程，线程是负责执行具体代码的
- 进程是负责圈资源的



进程是计算机中最小的资源分配单位（进程是负责圈资源）

线程是计算机中能被CPU调度的最小单位

线程特点：

- ​	线程的创建 ，也需要一些开销（一个存储局部变量的结构，记录状态）
  
  -    创建、销毁、切换远远小于进程
  
- 线程是进程的一部分，每个进程至少有一个线程

- 能被CPU调度的最小单位  

- 一个进程中的多个线程是可以共享这个进程的数据的，---- 数据共享

  

​		

#### 3.multiprocessing

#注意：主进程负责子进程创建并且负责子进程资源回收。

Process类

- 开启进程的方式
  - 面向函数
    - def 函数名：要在子进程内执行代码
    - p=Process（target=函数名，args=（参数1，）)
    - p.start()开启了进程
  - 面向对象
    - class 类名（Process）
      - def __ init __(self,参数1，参数2)：
        - self.a=参数1
        - self.b=参数2
        - super（）.__ init __()
      - def run（self）：
        - 要在子进程执行的代码
    - p=类名（参数1，参数2）
    - p.start（）

主进程的结束逻辑

- 主进程的代码结束
- 所有子进程结束
- 给子进程回收资源
- 主进程结束

```
from multiprocessing import Process
import time,os

def func():
	print('start',os.getpid)
	time.sleep(5)
	print('end',os.getpid)

if __name__=='__main__':
	p=Process(target=func)
	p.start()
	print(os.getpid)
```

```
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
print('main2', os.getpid())
```

##### 3.1在windows操作系统中必须加上下面这条代码： 

- 由于windows操作系统执行开启进程代码
  - 实际上新的子进程需要通过import父进程的代码来完成数据的导入工作
  - 所以一些内容我们只希望在父进程中完成，就写在下方代码的下面

```
if __name__=='__main__'
```

Windows操作系统调用mutliprocessing是执行以下代码。

![image-20200201195918615](C:\Users\davidlu\AppData\Roaming\Typora\typora-user-images\image-20200201195918615.png)

##### 3.2 ios/linux操作创建进程

​	ios/linux操作系统执行开启进程代码，直接copy 全局变量 函数等内存地址，并不执行代码。

![image-20200201214500275](C:\Users\davidlu\AppData\Roaming\Typora\typora-user-images\image-20200201214500275.png)



主进程如何知道子进程执行结束？？

![image-20200201222452711](C:\Users\davidlu\AppData\Roaming\Typora\typora-user-images\image-20200201222452711.png)



##### 3.3 join阻塞

```
from multiprocessing import Process
import time,os

def func():
	print('start',os.getpid)
	time.sleep(5)
	print('end',os.getpid)

if __name__=='__main__':
	p=Process(target=func)
	p.start()	#异步非阻塞
	p.jion()	#同步 阻塞 直到p对应的进程结束之后才结束阻塞
	print(os.getpid)
```

```
from multiprocessing import Process
import os
import random

def func(a):
    random.random()
    print('start',a)

if __name__=='__main__':
    l=[]
    for i in range(10):
        p=Process(target=func,args=(i,))
        p.start()
        l.append(p)
    for p in l:
        p.join()
    print('hahhahaha')

```



##### 3.4守护进程daemon

- 守护进程是随着主进程的代码结束而结束的
  - 生产者消费者模型
  - 线程守护对比

- 所有的子进程必须在主进程结束之前结束，由主进程来负责回收资源

```
from multiprocessing import Process
import time

def son1():
    while True:
        print('son1 alive')
        time.sleep(0.5)

def son2():
    for i in range(5):
        print('son2222')
        time.sleep(1)

if __name__=='__main__':
    p=Process(target=son1)
    p.daemon=True		#设置为守护进程，守护进程在主进程代码结束
    p.start()
    p2=Process(target=son2)
    p2.start()
    time.sleep(2)
```

##### 3.5 p.is_alive()

```
#判断子进程是否还在执行
def son1():
    while True:
        print('son1 alive')
        time.sleep(0.5)

if __name__=='__main__':
    p=Process(target=son1)
    p.start()
    print(p.is_alive()) #判断子进程是否还在执行
    time.sleep(2)
```

##### 3.6 p.terminate()

```
#强制结束一个子进程
from multiprocessing import Process
import time

def son1():
    while True:
        print('son1 alive')
        time.sleep(0.5)

if __name__=='__main__':
    p=Process(target=son1)
    p.start()
    print(p.is_alive())
    time.sleep(2)
    p.terminate()		#	强制结束一个子进程，异步非阻塞
    print(p.is_alive())	 #	这里会显示True由于代码执行速度太快，操作系统还来不及关闭进程
    time.sleep(2)
    print(p.is_alive())	#这里显示False ，操作系统以及响应我们的关闭进程请求
```

#什么是异步非阻塞？

​	典型就是terminate

##### 3.7 使用面向对象创建子进程

```
from multiprocessing import  Process
import time

class MYserver1(Process):
    def run(self):
        while True:
            time.sleep(1)
            print('MYserver1')

class MYserver2(Process):
    def run(self):
        for i in range(5):
            time.sleep(1)
            print('MYserver2222')

if __name__=='__main__':
    a=time.time()
    cp1=MYserver1()
    cp1.daemon=True
    cp1.start()
    time.sleep(2)
    cp2=MYserver2()
    cp2.start()
    time.sleep(4)
    c=time.time()-a
    print(c)
```

传参：

```
from multiprocessing import  Process
import time

class MYserver1(Process):
    def __init__(self,a,b):
        super().__init__()	#不要忘记super的init，传参数
        self.x=a
        self.y=b

    def run(self):
        while True:
            time.sleep(1)
            print('MYserver1')

class MYserver2(Process):
    def run(self):		#子进程执行的代码要下载run方法内
        for i in range(5):			
            time.sleep(1)
            print('MYserver2222')

if __name__=='__main__':
    a=time.time()
    cp1=MYserver1(1,2)
    cp1.daemon=True
    cp1.start()			#start 调用run方法
    time.sleep(2)
    cp2=MYserver2()
    cp2.start()
    time.sleep(4)
    c=time.time()-a
    print(c)
```

##### 3.8 lock

with lock 等于 lock.acquire()  。。。lock.release()

```
#1.如果在一个并发的环境下，涉及到某部分的内容
	#是需要修改一些所有进程都共享数据资源
	#需要加锁来维护数据的安全
#2.在数据安全的基础上，才考虑效率问题
#3.同步存在的意义
	#数据的安全性
#在主进程下实例化lock=Lock()对象
#把这把锁传递给子进程
#在子进程中 对需要加锁的代码 进行with lock：
	#with lock 相当于lock.acquire()和lock.release()
#在进程中需要加锁的场景
	#共享的数据源（文件，数据库）
	#对资源进行修改、删除操作
#加锁之后能够保证数据的安全性，但是也降低了程序的执行效率
```



```
from  multiprocessing import Process,Lock
import time,os
import json


def serach_tick(user):
    with open('aaa','r')  as f:
        dic=json.load(f)
        print('%s查询结果:%s张余票'%(user,dic['count']))

def buy_tick(user,lock):
    # lock.acquire()
    with lock:
        time.sleep(0.2)
        with open('aaa','r')  as f:
            dic=json.load(f)
            if dic['count']>0:
                print('%s买到票了'%(user))
                dic['count'] -= 1
            else:
                print('%s没买到票了' % (user))
            time.sleep(0.2)
            with open('aaa','w') as f:
                json.dump(dic,f)
    # lock.release()


def task(user,lock):
   serach_tick(user)
   # with lock:
   buy_tick(user,lock)


if __name__=='__main__':
    lock = Lock()
    for i in range(10):
        p=Process(target=task,args=('user%s'%i,lock))
        p.start()
#
```





##### 3.9进程间通信-IPC机制

IPC（inter process communication） 进程间通信。

###### 	1.queue 

###### 	2.pip管道

- Queue基于 天生就是数据安全的
  - 文件家族的socket pickle lock
- pip管道（不安全）=文件家族的socket pickle

- 队列=管道+锁

```
from multiprocessing import Process,queues

n=1000
def func():
    global n
    n-=1
    print(n)

if __name__=='__main__':
    p_l=[]
    for i in range(10):
        p=Process(target=func)
        p.start()
        p_l.append(p)
    for i in p_l:i.join()
    print('___>>>',n)#1000
 #由于windows操作系统在创建子进程时，是将主进程python代码全部import到子进程，所以n也会copy到每个子进程，进程间数据独立 所以子进程输出的n都为999，主进程输出
```

```
##Queue 先进先出
def func(exp,q):
    ret=eval(exp)
    q.put({ret,1,2})
    q.put(2*ret)
    q.put(3*ret)
    q.put(4*ret)
    
if __name__=='__main__':
    q = Queue()
    Process(target = func, args = ('1+2+3', q)).start()
    print(q.get())
    print(q.get())
    print(q.get())
    print(q.get())
```

Queue()

```
q=Queue(3)   # 设置队列长度
q.put(1)     # 放入数据
q.put(2)
q.put(3)
print(123)
q.put(4)    #当队列为满的时候再向队列中放数据 队列会阻塞
print(12345)
q.put(5)
```

q.put_nowait

```
import queue
q=Queue(3)   # 设置队列长度
q.put(1)     # 放入数据
q.put(2)
q.put(3)
print(123)          #当队列为满的时候再向队列中放数据 队列会阻塞
try:
    q.put_nowait(4) # 当队列为满的时候再向队列中放数据 会报错并且会丢失数据
except queue.Full:
    pass
print(12345)
```

q.get_noewait

```
print(q.get())
print(q.get())
print(q.get())
try:
    print(q.get_nowait())   # 在队列为空的时候 直接报错
except queue.Empty:         #报错类型在queue模块中，所以要import queue
    pass
print(q.get())   # 在队列为空的时候会发生阻塞
print(q.get())   # 在队列为空的时候会发生阻塞

```

