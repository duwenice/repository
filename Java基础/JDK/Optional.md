# Optional

> Optional: A container object which may or may not contain a non-null value.

## 起源

程序员在写代码的时候经常遇到的一个错误就是NullPointerException（以下简称为NPE），所以在使用的时候经常就要进行是否为null的判断，像下面这样：

```java
if(null != user){
   if(null != user.getName()){
      user.getName().toUpperCase();
 }
}
```
当需要做很多次null值判断时，往往需要很多if-else语句，这在一定程度上影响了代码的可读性，因此在java8中引进了Optional。Optional是一个容器，在容器的内部有对于null值的判断来防止可能出现的NPE问题。

## 源码分析

```java

    //默认的空容器
    private static final Optional<?> EMPTY = new Optional<>();

    //容器中存储的对象
    private final T value;

    //默认构造一个空实例
    private Optional() {
        this.value = null;
    }

    //返回一个空的Optional容器
    public static<T> Optional<T> empty() {
        @SuppressWarnings("unchecked")
        Optional<T> t = (Optional<T>) EMPTY;
        return t;
    }

    //私有构造函数，使用non-null值构造一个Optional容器
    private Optional(T value) {
        this.value = Objects.requireNonNull(value);
    }

    //提供的初始化接口,of接口只能接收non-null值，否则会报NPE
    public static <T> Optional<T> of(T value) {
        return new Optional<>(value);
    }

    //另外一个初始化接口,ofNullable接口可以接收null值
    public static <T> Optional<T> ofNullable(T value) {
        return value == null ? empty() : of(value);
    }

    //从Optional容器中取出value值
    public T get() {
        if (value == null) {
            throw new NoSuchElementException("No value present");
        }
        return value;
    }

    //判断容器里面的value是否为null
    public boolean isPresent() {
        return value != null;
    }

    //如果容器中的value不为null，使用函数式接口Consumer消费value，可以用lambda来具体实现
    public void ifPresent(Consumer<? super T> consumer) {
        if (value != null)
            consumer.accept(value);
    }

    //如果容器内的对象满足过滤条件，则返回过滤后的结果（可以用lambda具体实现test的过滤过程）
    //如果不满足过滤条件，则返回空的容器对象
    //如果容器内对象是null，返回null
    public Optional<T> filter(Predicate<? super T> predicate) {
        Objects.requireNonNull(predicate);
        if (!isPresent())
            return this;
        else
            return predicate.test(value) ? this : empty();
    }

    //如果Optional内的对象存在，则返回对象执行mapping之后的结果
    //如果Optional内的对象不存在，返回empty()
    public<U> Optional<U> map(Function<? super T, ? extends U> mapper) {
        Objects.requireNonNull(mapper);
        if (!isPresent())
            return empty();
        else {
            return Optional.ofNullable(mapper.apply(value));
        }
    }

    //和map的区别在于Function里面的参数必须有一个是Optional容器
    public<U> Optional<U> flatMap(Function<? super T, Optional<U>> mapper) {
        Objects.requireNonNull(mapper);
        if (!isPresent())
            return empty();
        else {
            return Objects.requireNonNull(mapper.apply(value));
        }
    }

    //如果容器内的value值是null的话返回自定义的other，不是null的时候返回value值
    public T orElse(T other) {
        return value != null ? value : other;
    }

    //和orElse的区别在于传入的是一个函数式接口
    public T orElseGet(Supplier<? extends T> other) {
        return value != null ? value : other.get();
    }

    //如果容器内的value不为null返回value值，为null的时候抛出异常
    public <X extends Throwable> T orElseThrow(Supplier<? extends X> exceptionSupplier) throws X {
        if (value != null) {
            return value;
        } else {
            throw exceptionSupplier.get();
        }
    }

```

## 案例
现在回过头来看最开始的那段代码，我们可以通过Optional将其改写如下：

```java
Optional.ofNullable(user).map(u -> user.getName())
                         .map(name -> name.toUpperCase())
                         .orElse(null);
```

