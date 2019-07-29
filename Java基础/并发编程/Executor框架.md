## Executor框架
> 参考 https://juejin.im/entry/59b232ee6fb9a0248d25139a

创建一个线程是有代价，需要和操作系统进行交互，管理一个线程也是需要牺牲额外的性能的。因此一般不显式的创建线程，而是通过线程池来创建管理线程。Executors工具类有许多静态方法来创建线程池。Executor框架主要包括**Executor**接口，**ExecutorService**接口和**Executors**工具类。

> Executor接口： This interface provides a way of decoupling task submission from the mechanics of how each task will be run, including details of thread use, scheduling, etc.( 此接口提供了一种将任务提交与每个任务的运行机制分离的方法，包括线程使用，调度等的详细信息。)

> ExecutorService接口： 继承自Executor接口，**submit()**方法提交任务之后会返回一个Future对象，同时提供了关闭线程池的方法，**shutDown()**会在关闭线程池之前执行完当前等待队列中的任务，**shutdownNow()**会取消所有任务并关闭线程。**invokeAny()**和**invokeAll()**会阻塞等待任意一个或者所有的任务执行完。

> Executors是Executor,ExecutorService等的工厂方法。
![20190722183643.png](https://repositoryimage.oss-cn-shanghai.aliyuncs.com/img/20190722183643.png)

![20190724133929.png](https://repositoryimage.oss-cn-shanghai.aliyuncs.com/img/20190724133929.png)

Executor 接口只有一个方法execute,ExecutorService扩展了Executor，添加了操控线程池生命周期的方法，如shutDown()，shutDownNow()等，以及扩展了可异步跟踪执行任务生成返回值Future的方法，如submit()等方法。ThreadPoolExecutor继承自AbstractExecutorService，同时实现了ExecutorService接口，也是Executor框架默认的线程池实现类，一般我们使用线程池，如没有特殊要求，直接创建ThreadPoolExecutor，初始化一个线程池，如果需要特殊的线程池，则直接继承ThreadPoolExecutor，并实现特定的功能，如ScheduledThreadPoolExecutor，它是一个具有定时执行任务的线程池。



### ThreadPoolExecutor

 * <li> If fewer than corePoolSize threads are running, the Executor
 * always prefers adding a new thread
 * rather than queuing.</li>
 *
 * <li> If corePoolSize or more threads are running, the Executor
 * always prefers queuing a request rather than adding a new
 * thread.</li>
 *
 * <li> If a request cannot be queued, a new thread is created unless
 * this would exceed maximumPoolSize, in which case, the task will be
 * rejected.</li>
 
 当新的任务被提交的时候，首先判断线程池中活跃线程的数目，如果小于corePoolSize，即使其他线程是空闲的，也会新建一个线程去执行该任务；如果大于corePoolSize但是小于maximumPoolSize，线程池优先将任务加入工作队列；如果队列已满，线程数大于maximumPoolSize，线程池会采用相应的拒绝策略拒绝这个任务。

创建一个新的线程池需要的几个核心参数：

- corePoolSize 核心线程池数目
- maximumPoolSize 线程池最大线程数
- keepAliveTime 空闲线程多久会被回收
- unit keepAliveTime的单位
- workQueue 工作队列，用来存放任务
- threadFactory 新建线程的工厂方法
- handler 拒绝任务的策略

接下来开始看线程池的工作流程，在开始之前，需要先知道几个概念：
* ctl 是一个32位的整数，用来存放线程池的状态和当前线程池的线程数，其中高3位用来存放线程池状态，低29位表示线程数。线程池主要有以下状态：RUNNING，SHUTDOWN，STOP，TIDYING,TERMINATED.
    - RUNNING：接受新的任务，处理等待队列中的任务
    - SHUTDOWN：不接受新的任务提交，但是会继续处理等待队列中的任务
    - STOP：不接受新的任务提交，不再处理等待队列中的任务，中断正在执行任务的线程
    - TIDYING：所有的任务都销毁了，workCount 为 0。线程池的状态在转换为TIDYING 状态时，会执行terminated()
    - TERMINATED：terminated() 方法结束后线程池的状态
* 在线程池中使用使用worker来包装线程，每一个工作的线程就是一个worker，线程池通过一个set来保存所有的worker。

接下来就可以开始分析啦。
从execute开始
```java
    public void execute(Runnable command) {
        if (command == null)
            throw new NullPointerException();\
        // 获取ctl值
        int c = ctl.get();

        // 如果当前活跃线程数目小于corePoolSize
        if (workerCountOf(c) < corePoolSize) {
            // 添加一个worker（线程）来开始工作
            if (addWorker(command, true))
                return;
            c = ctl.get();
        }
        // 如果线程池处于running状态，将任务加入到工作队列里面
        if (isRunning(c) && workQueue.offer(command)) {
            // 加入之前再检查一次状态
            int recheck = ctl.get();
            // 如果线程池不再是running状态并且移除入队的任务，执行拒绝策略
            if (! isRunning(recheck) && remove(command))
                reject(command);
            // 如果线程池处于running状态但是活跃线程为0，而此时工作队列里
            // 还有刚刚入队的任务，新建worker（线程）来执行刚刚入队的任务
            else if (workerCountOf(recheck) == 0)
                addWorker(null, false);
        }
        // 如果添加新的worker（线程）失败，说明此时已经超过最大线程数，执行
        // 拒绝策略
        else if (!addWorker(command, false))
            reject(command);
    }
```

可以看出，execute方法的核心是addWorker，因此接下来看addWorker方法：

```java
private boolean addWorker(Runnable firstTask, boolean core) {
      ……
        boolean workerStarted = false;
        boolean workerAdded = false;
        Worker w = null;
        try {
        // 新建一个worker与任务相关联
            w = new Worker(firstTask);
            final Thread t = w.thread;
            if (t != null) {
                final ReentrantLock mainLock = this.mainLock;
                mainLock.lock();
                try {
                    int rs = runStateOf(ctl.get());
                    if (rs < SHUTDOWN ||
                        (rs == SHUTDOWN && firstTask == null)) {
                        if (t.isAlive()) // precheck that t is startable
                            throw new IllegalThreadStateException();
                        // 将新增的worker加入线程池的worker队列中
                        workers.add(w);
                        int s = workers.size();
                        if (s > largestPoolSize)
                            largestPoolSize = s;
                        workerAdded = true;
                    }
                } finally {
                    mainLock.unlock();
                }
                if (workerAdded) {
                    t.start();
                    workerStarted = true;
                }
            }
        } finally {
            if (! workerStarted)
                addWorkerFailed(w);
        }
        return workerStarted;
    }
```

加入worker成功之后，会调用start方法，于是接下来就进入了worker的run方法：

```java
        public void run() {
            runWorker(this);
        }

        final void runWorker(Worker w) {
        Thread wt = Thread.currentThread();
        Runnable task = w.firstTask;
        w.firstTask = null;
        w.unlock(); // allow interrupts
        boolean completedAbruptly = true;
        try {
            // 循环获取任务或者循环从工作队列里面获取任务
            while (task != null || (task = getTask()) != null) {
                w.lock();
                // 如果线程池状态大于等于 STOP，那么意味着该线程也要中断
                if ((runStateAtLeast(ctl.get(), STOP) ||
                     (Thread.interrupted() &&
                      runStateAtLeast(ctl.get(), STOP))) &&
                    !wt.isInterrupted())
                    wt.interrupt();
                try {
                    beforeExecute(wt, task);
                    Throwable thrown = null;
                    try {
                        // 执行任务
                        task.run();
                    } catch (RuntimeException x) {
                        thrown = x; throw x;
                    } catch (Error x) {
                        thrown = x; throw x;
                    } catch (Throwable x) {
                        thrown = x; throw new Error(x);
                    } finally {
                        afterExecute(task, thrown);
                    }
                } finally {
                    task = null;
                    w.completedTasks++;
                    w.unlock();
                }
            }
            completedAbruptly = false;
        } finally {
            processWorkerExit(w, completedAbruptly);
        }
    }
```

![20190724143503.png](https://repositoryimage.oss-cn-shanghai.aliyuncs.com/img/20190724143503.png)