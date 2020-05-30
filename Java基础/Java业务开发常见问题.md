# 判等问题

## equals 和 == 的区别
Java中的数据分为两种类型，基本类型和引用类型。对于基本类型，比如int其值存的就是真实的值，因此只能使用==进行比较；对于引用类型，比如Integer，如果判等，需要使用equals进行内容判等，引用类型存储等是指针（对象在内存中的地址）如果使用==就是比较两个对象在内存中的地址，即比较两个引用是不是指向同一个对象，而不是比较对象的内容。

```java
    Integer i1 = 127; // Integer.valueOf(127)
    Integer i2 = 127; // Integer.valueOf(127)
    System.out.println(i1 == i2); // true
    Integer i3 = 128; // Integer.valueOf(128)
    Integer i4 = 128; // Integer.valueOf(128)
    System.out.println(i3 == i4); // false
```
有一点值得注意的是在Integer i1 = 127; 这个自动装箱的过程中，默认情况下会缓存-128到127的数值，所以上面例子中的第一个判断结果是true。

总结：基本类型判等用==，其他尽量都用equals

# 数值计算：精度问题

## 危险的double

```java
    double d1 = 0.2;
    double d2 = 0.1;
    System.out.println(d1 + d2); //0.30000000000000004
```
出现这种情况的主要原因是计算机是以二进制存储数值的。比如0.1 的二进制表示为 0.0 0011 0011 0011… （0011 无限循环)，再转换为十进制就是 0.1000000000000000055511151231257827021181583404541015625。

## BigDecimal的几个坑

```java
    System.out.println(new BigDecimal(0.1).add(new BigDecimal(0.2))); // 0.3000000000000000166533453693773481063544750213623046875
    System.out.println(new BigDecimal("0.1").add(new BigDecimal("0.2"))); // 0.3

    System.out.println(new BigDecimal("1.0").equals(new BigDecimal("1"))); // false
    System.out.println(new BigDecimal("1.0").compareTo(new BigDecimal("1"))); // 0
```

总结：精确计算不要使用double，使用BigDecimal表示和计算浮点数的时候，务必使用字符串的构造方法来初始化，比较BigDecimal如果用equals会不仅比较数值还会比较小数位，因此BigDecimal的比较都用compareTo。
