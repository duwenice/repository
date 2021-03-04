# 索引&文档

## 文档

1. es是面向文档的，文档是所有可搜索数据的最小单元(对应关系型数据的一条记录)。
2. 文档会被序列化成json格式，保存在es中。
3. 每个文档都有一个unique id(可以自己指定，也可以es自动生成)
4. 文档的元数据
   - _index ：文档所属的索引名
   - _type ：文档所属的类型名(7.0开始已经被废弃，一个索引只能创建一个type: "__doc")
   - _id：文档的id
   - _source：文档的原始json数据
   - -version：版本号
   - _score：相关性打分

## 索引

索引时一类文档的集合，索引的Mapping是定义文档字段的类型，Setting定义不同的数据分布(shard)

## 基本API

方法 + type + 其他

首先方法动词:

```
POST /uri 创建
DELETE /uri/xxx 删除
PUT /uri/xxx 更新或创建
GET /uri/xxx 查看
```

POST不用加具体的id，它是作用在一个集合资源之上的（/uri），而PUT操作是作用在一个具体资源之上的（/uri/xxx）。

在ES中，如果不确定document的ID，那么直接POST对应uri（ “POST /website/blog” ），ES可以自己生成不会发生碰撞的UUID；

type:

- _doc:index文档:如果文档不存在则新增，否则现有文档会被删除，新的文档被索引
- _create:新增文档，如果使用put指定了id，id已经存在会报错
- _update：更新文档

示例:

// 删除索引
DELETE user

// 新增文档，自动生成id
POST user/_doc
{
  "name":"zhangsan",
  "age":18,
  "city":"nanjing"
}

// 新增文档，指定id
PUT user/_create/1
{
  "name":"zhangsan",
  "age":28
}

// 查询id为1的文档
GET user/_doc/1

// 重新index，会删除之前的文档
PUT user/_doc/1
{
  "name":"lisi"
}

// 更新文档
POST user/_update/1
{
  "doc":{
    "age":18,
    "city":"nanjing"
  }
}

参考连接:

https://blog.csdn.net/sinat_36005594/article/details/90449781

# ES查询

1. URI查询
2. Request Body 查询