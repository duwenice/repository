# CompletableFuture

## 异步计算
异步调用就是无需等待调用函数的返回结果而可以继续执行操作，异步计算说的是使用另一个线程来完成调用中的计算部分，使调用继续运行或者返回，而不需要等待计算结果。

## 回调函数
通过函数指针调用的函数，把函数的指针作为参数传递给另一个函数，当这个指针被用为调用它所指向的函数的时候，就说这是回调函数。回调函数是在特定的事件或者条件发生时由另外一方调用的，用于表示对该事件或者条件进行响应。

定义回调函数 --> 函数实现方初始化后将函数指针传递给调用者 --> 调用者在特定的事件下调用函数

## Callable和Future
Runnable是一个没有参数，没有返回的异步封装接口，当需要返回值的时候，就可以使用Callable了。Callable接口是一个参数化的类型，只有一个方法call()，返回值类型就是参数的类型。例如Callable<String>就表示将返回一个String类型的值。

通常线程都是通过实现Runnable接口来创建，但是run()方法没有返回，因此如果需要异步计算，并且获取计算的返回结果的时候，显然是不能够的，因此Future就被设计出来了。Future的核心模式就是当异步计算的时候，马上返回一个Future实例，通过这个实例来控制该异步线程，获取执行返回结果。

FutureTask实现了Future和Runnable接口。

```java
    /**
    * 通过callable构建一个既是Future又是Runnable的对象
    */
    public FutureTask(Callable<V> callable) {
        if (callable == null)
            throw new NullPointerException();
        this.callable = callable;
        this.state = NEW;       // ensure visibility of callable
    }
    /**
    * 通过runnable构建一个既是Future又是Runnable的对象
    */
    public FutureTask(Runnable runnable, V result) {
        this.callable = Executors.callable(runnable, result);
        this.state = NEW;       // ensure visibility of callable
    }
```

## 与Future的联系
JDK5 新增的Future接口用于描述异步计算的结果，但是对于结果的获取不方便，只能通过阻塞或者轮询的方式得到任务的结果


有结果的同步行为 Callable句柄
无结果的同步行为 Runnable句柄
异步行为         Future句柄
异步回调行为     CompletableFuture句柄

## CompletableFuture的API
- 创建类型：创建CompletableFuture
   1. completedFuture
   2. runAsync
   3. supplyAsync
   4. anyOf
   5. allOf
- 状态相关
   1. join
   2. get
   3. getNow
   4. isCancelled
   5. isCompletedExceptionally
   6. isDone
 - 行为相关
    1. complete
    2. completeExceptionally
    3. cancel
- 回调相关：对计算结果做下一步处理，行为接续
    1. thenApply , thenApplyAsync
    2. thenAccept , thenAcceptAsync
    3. thenRun , thenRunAsync
    4. thenCombine , thenCombineAsync
    5. thenAcceptBoth , thenAcceptBothAsync
    6. runAfterBoth , runAfterBothAsync
    7. applyToEither , applyToEitherAsync
    8. thenCompose , thenComposeAsync
    9. whenComplete , whenCompleteAsync
    10. handle , handleAsync
    11. exceptionally

 规律： 
  * 带Async的是异步方法，不带的则为同步方法
  * 带run的方法，其方法入参的lambda表达式一定是无参数，并且无返回，对应Runnable
  * 带supply的方法，其方法入参的lambda表达式一定是无参数，并且有返回，对应Supplier
  * 带Accept的方法，其方法入参的lambda表达式一定是有参数，并且无返回，对应Consumer
  * 带Apply的方法，其方法入参的lambda表达式一定是有参数，并且有返回，对应Function
  * 

接续即是CompletableFuture存在的核心价值。接续分为以下几种：

CompletableFuture + (Runnable,Consumer,Function)
CompletableFuture + CompletableFuture
CompletableFuture + 结果处理