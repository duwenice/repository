# Mybatis的缓存机制

## 一级缓存

1. mybatis的一级缓存是默认开启的，本质是个hashMap，只能修改作用域:session/statement 前者表现为在同一个session中连续两次相同查询第二次查询是不查表的，但是要注意的是如果两次查询中间有insert/update/delete等会导致session提交。statement作用域表现为每一个statement都是直接查表。
2. 一级缓存的实现其实是BaseExecutor的query方法会先去localCache中查找，而update方法会更新localCache

## 二级缓存

1. mybatis的二级缓存可以在多个sqlSession之间共享缓存，粒度为namespace
2. 如果开启二级缓存使用的Executor为CachingExecutor，缓存取值顺序为二级缓存 -> 一级缓存 -> db
3. 二级缓存也有缺陷，如果是不同的namespace(即不同的mapper)，如果有关联查询也会有脏数据，情景如下：

| Session1                                                     | Session2                                  |
| :----------------------------------------------------------- | ----------------------------------------- |
| Select a.id,b.name from A a left join B b on a.id = b.aId （结果为1 name1） |                                           |
|                                                              | Update b set name = 'name2' where aId = 1 |
| Select a.id,b.name from A a left join B b on a.id = b.aId （结果还是为1 name1出现了脏数据） |                                           |



