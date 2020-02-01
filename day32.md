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

​		

#### 3.multiprocessing

#注意：主进程负责子进程创建并且负责子进程资源回收。

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

