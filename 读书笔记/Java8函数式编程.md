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

从原理上看，for其实是一个封装了迭代的语法糖（一种更优雅便捷的等价实现，在字节码中实际并不存在该简便实现），上面那段代码的迭代实现如下:

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
  
tip：

* 使用为基本类型定制的 Lambda 表达式和 Stream，如 IntStream 可以显著提升系统性能。
* 每个用作函数接口作用的接口都需要添加@FunctionalInterface注解，函数接口是为了提高stream流对象的可操作性，需要使用lambda表达式来实现，它们所存在的意义就是为了能将代码块像数据一样打包起来。
* 在Java 8之前，接口都是面向抽象编程而不是面向具体编程，这样带来了一个问题，当需要修改接口的时候就需要接口的所有实现类来达到二进制兼容（不影响之前的版本）。因此在Java 8中，提出了默认方法，可以在接口中默认实现，从而解决了接口的修改与现有的实现的兼容问题。默认方法使用default关键字作为前缀。
* 在一个值可能为空的建模情况下，使用 Optional 对象能替代使用 null 值。
* 方法引用是一种引用方法的轻量级语法，形如：ClassName::methodName。 
* 收集器可用来计算流的最终值，是 reduce 方法的模拟。 
* Java 8 提供了收集多种容器类型的方式，同时允许用户自定义收集器。
* 重构遗留代码时考虑如何使用 Lambda 表达式，有一些通用的模式。 
* 如果想要对复杂一点的 Lambda 表达式编写单元测试，将其抽取成一个常规的方法。
* peek 方法能记录中间值，在调试时非常有用。

### 数据并行化

> 并行和并发的区别：并发是指同一个cpu给不同的任务分配了不同的时间片，此时说这些任务并发执行；而并行指的是多个任务同一时间在不同cpu上执行。

数据并行化指的是在大数据量的情况下，将数据分为段，分别分配给不同的执行单元同时执行后汇总，从而提高数据处理效率。

stream提供了parallel()和parallelStream()方法来实现数据并行化操作，但是在使用的时候有几个限制。
- 在使用reduce函数的时候，为了保证数据并行化之后结果正确，初始值必须为恒等值（比如组合函数是加法，初始值只能为0），以及组合函数必须满足结合律（比如说加法和乘法）。
  ```java
        // 该组合函数为乘法，如果初始值不为1，在并行处理的过程中，初始值会
        // 在每一个处理单元里面处理一次，从而造成结果错误。
        list.parallelStream().reduce(2, (acc, x) -> x * acc);

        // 正确写法如下：
        2 * list.parallelStream().reduce(1, (acc, x) -> x * acc);
  ````
- stream在数据并行化操作的时候自己会处理同步操作，因此不需要加锁。

tip:

影响数据并行化性能的五要素是：数据大小、源数据结构、值是否装箱、可用的 CPU 核数量，以及处理每个元素所花的时间。

## 设计与架构

设计模式就是软件架构中解决通用问题的模板。
