#Java 8 函数式编程

## 什么是函数式编程
  
我们习惯的Java是面向对象编程，即需要对数据进行抽象；而函数式编程则是对行为进行抽象，即面向对象编程传递的是一个包含各种方法和数据的对象，而函数式编程传递的是方法体。

## Lambda表达式

什么是Lambda表达式，Lambda表达式是一个匿名方法，将行为像数据一样传递。

Lambda表达式的几个核心概念:函数式接口，类型推断。函数式接口指的是只有一个方法的接口，Lambda表达式与函数式接口的关系是：Lambda表达式的类型是所实现的函数式接口的类型,也就是说Lambda表达式是函数式接口的一个实例。常用的函数式接口如下：


![20190729134156.png](https://repositoryimage.oss-cn-shanghai.aliyuncs.com/img/20190729134156.png)

而至于类型推断，在Java 7中就开始使用菱形操作符来实现目标类型推断，比如说下面这样:
```java
Map<String, Object> map = new HashMap<>();
```
到了Java 8之后，对其进行了扩展，使得javac可以根据上下文（方法的签名）来推断出Lambda表达式中的参数类型。

一个简单的Lambda表达式如下所示:
```java
        Predicate<Integer> lambdaTest = i -> i > 3;
        lambdaTest.test(5);  // true
```
i -> i > 3这个表达式实现了Predicate中的test接口。

tip：

在Lambda表达式中引用变量的时候必须引用的final修饰的变量或者是实际上的final变量，实际上的final变量指的是只能给该变量赋值一次。如果多次给变量赋值，就会编译不通过，并且报错：Variable used in lambda expression should be final or effectively final.

## stream

在Java 8之前，如果需要对集合中的元素进行处理，一般需要对集合进行迭代，比如说找到一个list中的所有偶数的个数如下所示:

```java
        List<Integer> list = Lists.newArrayList(1, 2, 3, 4, 5, 6);
        int count = 0;
        for (Integer integer : list) {
            if (integer % 2 == 0){
                count ++;
            }
        }
```

从原理上看，for其实是一个封装了迭代的语法糖（一种更优雅便捷的等价实现），上面那段代码的迭代实现如下:

```java
        int count = 0;
        Iterator<Integer> iterator = list.iterator();
        while (iterator.hasNext()) {
            Integer i = iterator.next();
            if (i % 2 == 0) {
                count++;
            }
        }
```

外部迭代的流程图如下：

![20190729150838.png](https://repositoryimage.oss-cn-shanghai.aliyuncs.com/img/20190729150838.png)

在Java 8之后，可以通过使用stream来进行内部迭代从而实现该操作，代码如下：

```java
        list.stream().filter(integer -> integer % 2 == 0).count();
```

其内部迭代的流程图如下：

![20190729151250.png](https://repositoryimage.oss-cn-shanghai.aliyuncs.com/img/20190729151250.png)

对比其内部迭代和外部迭代，使用内部迭代将迭代这个过程和实际的构建操作给分离了，如此一来在构建操作比较复杂的情况下，就不用去考虑迭代的过程，而只需专心于构建操作。

stream是使用函数式编程在集合类上进行复杂操作的工具。它提供了许多操作，比如上面的filter和count，这些操作可以分为两类:
- 惰性求值方法: 只对stream进行描述，并不返回新的集合，比如说filter。
- 及早求值方法：会在stream的基础上返回新的集合，比如说count。

整个stream的复杂操作应该是一系列惰性求值的方法链，最后使用一个及早求值来返回新的结果。这和建造者模式有共通的地方，首先通过一系列操作设置属性和配置，最后通过一个build操作来创建对象。

常用的流操作如下：
- collect
- map 
- filter:接收的lambda表达式的函数接口（或者说lambda表达式的类型）是Predicate
- flatMap
- reduce：接收的lambda表达式的类型是BinaryOperator
  