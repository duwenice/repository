# Java泛型

> 泛型在jdk1.5之后引入，其本质是将形参类型作为参数传入，在之前，比如说我们需要对int和double类型的数组进行排序，只能通过都传入Object而后强制转换来实现，即Object的任意化，对于强制转换，编译的时候可能不会发现错误，但是运行的时候可能会引发错误，这是潜在的安全隐患。而引入泛型，就能在编译的时候就进行类型的检查，从而提前发现错误。

## 泛型类
我们先定义一个DataHolder类：

```java
public class DataHolder{
     private String data;
  
     public void setData(String data){
       this.data = data;
     }
  
     public String getData(){
        return this.data;
     }
}
```
显然这个类只能接受String类型的变量，如果我们需要传入int类型的呢？那可能就需要重写了。而如果我们使用泛型就可以解决这个问题。

```java
public class DataHolder<T> {
        T t;

        public void setT(T t) {
            this.t = t;
        }

        public T getT() {
            return this.t;
        }
    }
```
此时我们就能传入我们想传入的类型了，比如像下面这样：

```java
DataHolder<String> stringDataHolder = new DataHolder<String>();
DataHolder<Integer> integerDataHolder = new DataHolder<Integer>();
```

## 泛型接口
泛型接口的使用与泛型类基本相同。但是有一点需要注意：在实现泛型接口的时候如果已经传入了泛型参数类型，实现类里面需要全部替换。比如：

```java
public interface IGeneric<T> {
    T next();
}
```
现在有一个类Generic实现这个接口：

```java
public class Generic implements IGeneric<String> {
    @Override
    public String next() {
        return null;
    }
}
```

## 泛型方法
举例如下:

```java
public<E> void show(E e){
            System.out.println(e);
        }
```

## PECS原则（待完善）
> PECS原则即：Producer Extends, Consumer Super.

这里主要说的是<? extends T> 和<? super T>的区别，举个例子就很好懂了，比如说现在有一个Fruit类，它有两个子类Apple和Banana，当我使用List<? extends Fruit>的时候,可以使用其中的get方法，无论是Apple还是Banana。可是使用add方法想要添加一个元素的时候就会报错了，因为list可能指向多个。就像下面这样

```java
List<? extends Fruit> list = new ArrayList<Fruit>();
List<? extends Fruit> list = new ArrayList<Apple>();
List<? extends Fruit> list = new ArrayList<Banana>();
```
所以当你使用list.add(new Apple())的时候，list并不知道该指向哪个，从而报错。<br />而使用<? super Fruit>的时候就相反啦，可以往其中添加元素，但是坏处是不能get其中的元素了。

## 类型擦除（待完善）

java泛型因为是1.5之后才引入的，为了保证与之前项目的兼容性，所以在编译之后会进行类型擦除。先看下面这段代码：

```java
        Class class1 = new ArrayList<String>().getClass();
        Class class2 = new ArrayList<Integer>().getClass();
        System.out.println(class1);
        System.out.println(class2);
        System.out.println(Arrays.toString(class1.getTypeParameters()));
        System.out.println(Arrays.toString(class2.getTypeParameters()));
        System.out.println(class1.equals(class2));
```

输出如下：

![20190729164043.png](https://repositoryimage.oss-cn-shanghai.aliyuncs.com/img/20190729164043.png)

可以看出不管ArrayList里面的传入的泛型形参类型是Integer还是String，编译之后的结果都是一样的，这也从原理上解释了PECS原则。





















