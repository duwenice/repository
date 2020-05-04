# 基础理论

## 四种隔离级别

|隔离级别|脏读(Dirty Read)|不可重复读(NonRepeatable Read)|幻读(Phantom Read)|
|---|---|---|---|
|读未提交(Read uncommitted)|Y|Y|Y|
|读已提交(Read committed)|N|Y|Y|
|可重复读(Repeatable Read)|N|N|Y|
|串行(Serializable)|N|N|N|

- RU:允许脏读，也就是可能读取其他会话中未提交的事务修改的数据
- RC:只能读取到已经提交的数据
- RR:InnoDB默认级别
- Serializable:每次读都需要获取表级共享锁，读写相互都会阻塞

## 锁

Mysql中锁按粒度可以分为表级锁和行级锁：
- 表级锁对当前操作的整张表都加锁，实现简单，加锁快，不会出现死锁，但是粒度大，锁冲突的概率高，并发度低。
- 行级锁只对当前操作行进行加锁，并发度高，但是加锁开销也大，加锁慢，会出现死锁。

Mysql中锁按分类可以分为共享锁(S)和排他锁(X)：
- 共享锁(Share Lock):读锁，S锁和S锁不冲突，因此可以支持并发读取数据，但是S锁和X锁冲突，如果需要加X锁，必须等记录上的S锁释放。
- 排他锁(Exclusive Lock):写锁，若事务T对数据对象A加上X锁，则只允许T读取和修改A，其它任何事务都不能再对A加任何类型的锁，直到T释放A上的锁。它防止任何其它事务获取资源上的锁，直到在事务的末尾将资源上的原始锁释放为止。在更新操作(INSERT、UPDATE 或 DELETE)过程中始终应用X锁。

在 InnoDB 事务中，行锁是在需要的时候才加上的，但并不是不需要了就立刻
释放，而是要等到事务结束时才释放。这个就是两阶段锁协议。也就是说事务会有两个阶段：加锁阶段和解锁阶段。

# 实战

## 基本命令
查看隔离级别
```mysql
select @@tx_isolation
```
设置隔离级别
```mysql
SET [GLOBAL/SESSION] TRANSACTION ISOLATION LEVEL READ UNCOMMITTED
```
查看事务和锁
```mysql
SELECT
	r.trx_id waiting_trx_id,
	r.trx_mysql_thread_id waiting_thread,
	r.trx_query waiting_query,
	b.trx_id blocking_trx_id,
	b.trx_mysql_thread_id blocking_thread,
	b.trx_query blocking_query 
FROM
	information_schema.INNODB_LOCK_WAITS w
	INNER JOIN information_schema.INNODB_TRX b ON b.trx_id = w.blocking_trx_id
	INNER JOIN information_schema.INNODB_TRX r ON r.trx_id = w.requesting_trx_id
```
## 通用表结构和数据
table：user
|id|name|age|
|--|--|--|
|1|张三|18|

## RU与脏读

|Session1|Session2|
|---|---|
|begin|begin|
|select * from user where name = "张三"||
||update user set age = 19 where name = "张三"|
|select * from user where name = "张三"||
|commit||

因为在RU级别下可以读取到其他未提交事务的记录，所以在Session1中两次select查询出来的记录发生了变更，这就是脏读。

## RC与不可重复读
|Session1|Session2|
|---|---|
|begin|begin|
|select * from user where name = "张三"||
||update user set age = 19 where name = "张三"|
||commit|
|select * from user where name = "张三"||
|commit||

在RC级别下只能读取到其他已提交事务的记录(解决了脏读)，但是由于Session2中的事务先提交导致Session1中的两次查询结果不一致，这就是不可重复读。

在RC级别中，数据的读取都是不加锁的，但是数据的写入、修改和删除是需要加锁的。
|Session1|Session2|
|---|---|
|begin|begin|
|update user set age = 17 where name = "张三"||
||update user set age = 19 where name = "张三"|
|commit||
如果Session1中的事务一直不commit,那么Session2中的事务也就会一直拿不到该行锁，直到超时。
如果where条件的字段是有索引的，会根据索引对相关行进行加行锁，但是如果没有索引，就会对整个表的所有数据行都加上行锁。但是在实际过程中MySQL做了一些改进，在MySQL Server过滤条件，发现不满足后，会调用unlock_row方法，把不满足条件的记录释放锁 (违背了二段锁协议的约束)。这样做，保证了最后只会持有满足条件记录上的锁，但是每条记录的加锁操作还是不能省略的。

这种情况同样适用于MySQL的默认隔离级别RR。所以对一个数据量很大的表做批量修改的时候，如果无法使用相应的索引，MySQL Server过滤数据的的时候特别慢，就会出现虽然没有修改某些行的数据，但是它们还是被锁住了的现象。

## RR与幻读
|Session1|Session2|
|---|---|
|begin|begin|
|select * from user where age = 18||
||insert into user (name,age) value ("李四",18)|
||commit|
|select * from user where age = 18||
|commit||

在RR级别下通过加X锁和S锁(在一个事务操作记录时，其他事务需等待锁释放)解决了不可重复读。
上面这种情况是很多网上博客说的可能出现幻读的情况，但我在实际测试的时候，发现两次查询结果其实是一样的。原因呢？
首先说说不可重复读和幻读：
- 不可重复读重点在于update和delete，而幻读的重点在于insert。
- 如果使用锁机制来实现这两种隔离级别，在可重复读中，该sql第一次读取到数据后，就将这些数据加锁，其它事务无法修改这些数据，就可以实现可重复读了。但这种方法却无法锁住insert的数据，所以当事务A先前读取了数据，或者修改了全部数据，事务B还是可以insert数据提交，这时事务A就会发现莫名其妙多了一条之前没有的数据，这就是幻读，不能通过行锁来避免。需要Serializable隔离级别 ，读用读锁，写用写锁，读锁和写锁互斥，这么做可以有效的避免幻读、不可重复读、脏读等问题，但会极大的降低数据库的并发能力。

上文说的都是采用悲观锁来处理这两种问题，但是MySQL、ORACLE、PostgreSQL等成熟的数据库，出于性能考虑，都是使用了以乐观锁为理论基础的MVCC（多版本并发控制）来避免这两种问题，这也是在RR级别下两次查询结果一致的原因。

## 悲观锁和乐观锁

### 悲观锁

正如其名，它指的是对数据被外界（包括本系统当前的其他事务，以及来自外部系统的事务处理）修改持保守态度，因此，在整个数据处理过程中，将数据处于锁定状态。悲观锁的实现，往往依靠数据库提供的锁机制（也只有数据库层提供的锁机制才能真正保证数据访问的排他性，否则，即使在本系统中实现了加锁机制，也无法保证外部系统不会修改数据）。

在悲观锁的情况下，为了保证事务的隔离性，就需要一致性锁定读。读取数据时给加锁，其它事务无法修改这些数据。修改删除数据时也要加锁，其它事务无法读取这些数据。

### 乐观锁

相对悲观锁而言，乐观锁机制采取了更加宽松的加锁机制。悲观锁大多数情况下依靠数据库的锁机制实现，以保证操作最大程度的独占性。但随之而来的就是数据库性能的大量开销，特别是对长事务而言，这样的开销往往无法承受。

而乐观锁机制在一定程度上解决了这个问题。乐观锁，大多是基于数据版本（ Version ）记录机制实现。何谓数据版本？即为数据增加一个版本标识，在基于数据库表的版本解决方案中，一般是通过为数据库表增加一个 “version” 字段来实现。读取出数据时，将此版本号一同读出，之后更新时，对此版本号加一。此时，将提交数据的版本数据与数据库表对应记录的当前版本信息进行比对，如果提交的数据版本号大于数据库表当前版本号，则予以更新，否则认为是过期数据。

### InnoDB中的MVCC
在InnoDB中，会在每行数据后添加两个额外的隐藏的值来实现MVCC，这两个值一个记录这行数据何时被创建，另外一个记录这行数据何时过期（或者被删除）。 在实际操作中，存储的并不是时间，而是事务的版本号，每开启一个新事务，事务的版本号就会递增。 在可重读Repeatable read事务隔离级别下：

- SELECT时，读取创建版本号<=当前事务版本号，删除版本号为空或>当前事务版本号。
- INSERT时，保存当前事务版本号为行的创建版本号
- DELETE时，保存当前事务版本号为行的删除版本号
- UPDATE时，插入一条新纪录，保存当前事务版本号为行创建版本号，同时保存当前事务版本号到原来删除的行

在MySQL的RR级别中，通过MVCC是解决了幻读的读问题的。虽然让数据变得可以重复读，但是可能读到的数据是历史数据。对于这种读取历史数据的方式，叫做快照读，而读取数据库当前版本数据的方式叫做当前读。

在MVCC中
- 快照读就是select
  - select * from t ...
- 当前读：特殊的读操作，插入/更新/删除操作，属于当前读，处理的都是当前的数据，需要加锁。
   - select * from table where ? lock in share mode;
   - select * from table where ? for update;
   - insert;
   - update;
   - delete;

## Next-Key锁
> Next-Key锁是行锁和GAP（间隙锁）的合并
> 
接下来看这样一种情况:
|Session1|Session2|
|---|---|
|begin|begin|
|select * from user where age = 18||
|update user set name = "王五" where age = 18||
||insert into user (name,age) value ("李四",18)|
||commit|
|select * from user where age = 18||
|commit||

在RC级别下，最后age为18的会有李四和王五，在RR级别下Session2的insert会尝试获取锁，这个锁就是Gap锁。
总结一下：RR级别中，事务A在update后加锁，事务B无法插入新数据，这样事务A在update前后读的数据保持一致，避免了幻读。这个锁，就是Gap锁。
如果使用的是有索引的字段会锁住相应的数据行，以及两边的区间，如果是非索引字段，就会锁住全表，同时，它不能像行锁一样经过MySQL Server过滤自动解除不满足条件的锁，因为没有索引，则这些字段也就没有排序，也就没有区间。除非该事务提交，否则其它事务无法插入任何数据。


相关文章:
- https://tech.meituan.com/2014/08/20/innodb-lock.html