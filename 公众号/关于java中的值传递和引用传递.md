# Java中的值传递和引用传递

## 缘起
bug，bug，bug！！！
大致代码如下：
~~~java
    ThreadFactory namedThreadFactory = new ThreadFactoryBuilder()
            .setNameFormat("demo-pool-%d").build();

    ExecutorService pool = new ThreadPoolExecutor(5, 200,
            0L, TimeUnit.MILLISECONDS,
            new LinkedBlockingQueue<Runnable>(1024), namedThreadFactory, new ThreadPoolExecutor.AbortPolicy());

    public void outFunction() {
        Map<String, Object> map = new HashMap<>(4);
        List<Integer> list = Arrays.asList(1, 2, 3, 4);
        list.forEach(i -> {
            map.put("id", i);
            pool.execute(() -> {
                try {
                    innerFunction(map);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            });
        });
    }

    public void innerFunction(Map<String, Object> map) throws InterruptedException {
        Thread.sleep(1 * 1000);
        // 具体业务以控制台输出代替
        System.out.println("id:" + map.get("id"));
    }

~~~
这段代码最初的本意是想遍历一个id的list，根据每个id去进行具体的业务操作，可是结果竟然是：
![20200223220742.png](https://repositoryimage.oss-cn-shanghai.aliyuncs.com/img/20200223220742.png)

## 分析&&解决
看到这个结果，我第一反应就感觉是因为线程池而导致的问题，顿时就想把整个方法改成同步的，果不其然就没有出现这个问题。但是细细想来，顿时发现了问题所在，原来是给每个线程传入的是同一个对象实例（map）。于是上述代码就可以如下解决:
![20200223230028.png](https://repositoryimage.oss-cn-shanghai.aliyuncs.com/img/20200223230028.png)

## 思考
经过这个小小的插曲，我意识到自己对于Java的参数传递这块并没有从原理上理解，于是花了点时间开始了自己的整理:

### 方法与参数
Java是一门面向对象的语言，对于Java类中的方法，我是这么理解的，方法决定了一个对象能够接收什么样的消息(参数),采取何种方式(方法体),来返回相应的结果(返回值)。其中的参数，传递的类型就是Java的数据类型。
OK，那么Java有哪些数据类型呢？基本上可以分为两类：
1. 基本类型：byte，short，int，long，float，double，char，boolean
2. 引用类型：引用也叫句柄，引用类型，其实可以看做是一个数据结构，句柄中存放着实际对象内容的地址。

所以Java中方法的参数传递基本上就是这两大类(String其实可以看做是基本类型，其处理方式和基本类型相似)，所以这也带出了一个令很多人迷惑的问题，那Java中的传递是值传递还是引用传递呢？

这里可以首先通过《Java编程思想》中对于引用的描述来进一步深入说明什么是引用：
> 每种编程语言都有自己的操纵内存中元素的方式，在Java中，一切都被视为对象，因此可以采用单一固定的语法，尽管一切都看做是对象，但是操纵的标识符实际上是对象的一个引用。

通过上面这段话，加上一个具体的例子就可以彻底明白什么是引用了，比如我想创建一个String对象，这时可以在内存中new 一个对象，然后我想操纵这个String对象，则可以创建一个引用String s，这里的s就是引用，并将这个引用指向之前new的对象，于是就实现了通过引用操纵内存中元素。

### 值传递or引用传递
那么回到正题，为什么对于Java中的传递是值传递还是引用传递会模糊不清呢？首先看下面两段代码:
~~~java
    public static void main(String[] args) {
        ReferenceSample1 referenceSample1 = new ReferenceSample1();
        int i = 0;
        referenceSample1.function(i);
        System.out.println("i:" + i);
    }

    private void function(int i) {
        i = 1;
    }
~~~

~~~java
    public static void main(String[] args) {
        ReferenceSample1 referenceSample1 = new ReferenceSample1();
        User user = new User();
        user.setAge(0);
        referenceSample1.function(user);
        System.out.println("age:"+ user.getAge());
    }

    private void function(User user) {
        user.setAge(1);
    }
~~~

第一段代码输出的结果是
![20200223234107.png](https://repositoryimage.oss-cn-shanghai.aliyuncs.com/img/20200223234107.png)

第二段代码输出的结果是
![20200223234223.png](https://repositoryimage.oss-cn-shanghai.aliyuncs.com/img/20200223234223.png)

OK，现在开始分析，第一段代码将int值传递给function，但经过function的作用，int值并没有发生改变，这似乎证明了Java中的传递时值传递，从该例来说，传递给function方法的只是int值i的一份拷贝，原先的int值i并不会随着function的作用而变化，但是这个推论到了第二段代码里面就出现了相反的结果，彷佛又是引用传递导致的原先的user对象的age随着function的作用而发生了变化。

那么结论到底是是什么呢？可以先把结论放在这里，java中的传递都是值传递，也就是每次传递的其实是原先值的一份拷贝。为了解释第二段代码中看上去不一致的原因，我们需要更深入了解Java对象到底存储在哪？

### Java对象的存储
《深入理解Java虚拟机》对于JVM内存结构的描述如下图所示：
![20200223235526.png](https://repositoryimage.oss-cn-shanghai.aliyuncs.com/img/20200223235526.png)

那么，对于Java对象的存储，重点关注堆和虚拟机栈就行啦。结论如下:
1. 虚拟机栈是由若干个栈帧组成，在虚拟机栈中会存放编译期可知的各种基本数据类型和对象引用。
2. 堆的作用是存放所有的Java对象。

### 结论
Java中的传递都是值传递，也就是每次传递的其实是原先值的一份拷贝。
* 对于基本数据类型，因为Java中是不用new来创建变量，而是创建一个并非是引用的“自动”变量，这个变量直接存储“值”，并且置于虚拟机栈中,所以原始内容和副本都是存储的实际值，而且是处于不同的栈区，所以互不影响。
* 对于引用类型，每次传递的其实是指向对象的地址的拷贝（这是个具体的值），而通过function的作用可能使所指向的对象发生改变，也就是原来的地址指向了一个作用过的新的对象，所以出现了第二段代码看似是引用传递导致的结果，而其本质还是值传递(传递的是地址的拷贝)。
  

参考：
* https://juejin.im/post/5bce68226fb9a05ce46a0476#heading-11
