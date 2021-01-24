# Mybatis 动态sql遇到的一个小bug

首先从一段xml文件说起

```xml
<sql id="conditions">
    <trim prefix="where" prefixOverrides="and |or">
        <if test="ids != null and ids.size() > 0">and
         id in
            <foreach collection="ids" open="(" separator="," close=")" item="id">
                #{id}
            </foreach>
        </if>
    </trim>
</sql>
```

就是上面这坨，看上去似乎没有任何问题，但是一执行就报异常:sql语法错误，debug之后发现where 后面多跟了一个and，此时就令人疑惑了，prefixOverrides这个标签不就是用来移除开头的字符吗？按理说and应该被移除掉呀。

在程序世界里，debug能解决一切问题。于是，带着疑惑，开始了对这个标签解析的追踪，直到看到了下面这段代码：

```java
private void applyPrefix(StringBuilder sql, String trimmedUppercaseSql) {
  if (!prefixApplied) {
    prefixApplied = true;
    if (prefixesToOverride != null) {
      for (String toRemove : prefixesToOverride) {
        if (trimmedUppercaseSql.startsWith(toRemove)) {
          sql.delete(0, toRemove.trim().length());
          break;
        }
      }
    }
    if (prefix != null) {
      sql.insert(0, " ");
      sql.insert(0, prefix);
    }
  }
}
```

![image-20201026184514219](https://repositoryimage.oss-cn-shanghai.aliyuncs.com/img/image-20201026184514219.png)

**原来是没注意空格和换行导致的！！！！！！！！！**

顺带总结一下mybatis动态sql中常用的一些标签:

| 标签        | 作用                                                         |
| ----------- | ------------------------------------------------------------ |
| if标签      | 主要用于实现某些简单的条件判断                               |
| where标签   | 标签会自动判断如果后面的标签中有返回值的话，就在sql中插入一个where |
| trim标签    | 去除特殊的字符串，prefix/suffix属性代表前/后缀覆盖并增加其内容，prefixOverrides/suffixOverrides属性代表前/后缀需要去除的哪些特殊字符串 |
| foreach标签 | 遍历集合，其中item：表示循环中当前的元素，index：表示当前元素在集合的位置下标， collection：配置list的属性名等，open和close：配置的是以什么符号将这些集合元素包装起来， separator：配置的是各个元素的间隔符。 |

