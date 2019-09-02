# Java中的Holder

## 值传递&&引用传递
首先Java中的传递都是值传递，从底层原理来看，java中的基本类型和对象引用都是放在栈内存中的，而引用指向的值却是放在堆内存里面的。可以先看一个简单的例子：
```java
    @Test
    public void test() {
        int a = 1;
        change(a);
        assertEquals(a, 2);
    }

    void change(int b) {
        b = 2;
    }
```
输出结果如下：

![20190829193841.png](https://repositoryimage.oss-cn-shanghai.aliyuncs.com/img/20190829193841.png)

在上面这个过程中，其实内部的过程如下所示：
![20190829200732.png](https://repositoryimage.oss-cn-shanghai.aliyuncs.com/img/20190829200732.png)

所以其实在调用change方法的时候，并没有将原来的引用传递过去，传过去的只是原引用的一个copy，因此对该copy的操作导致的变化是不会提现在原引用的身上的。

## Holder
> holder可以译为持有者，其实就可以看出它的作用就是持有一个对象，因为java中的传递都是值传递，那么如果我们需要改变原引用指向的值的时候，就需要使用holder了。

