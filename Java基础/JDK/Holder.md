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

所以其实在调用change