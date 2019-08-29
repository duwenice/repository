## 数学函数
* ABS()
* CEILING(x) 返回大于x的最小整数
* FLOOR(x) 返回小于x的最大整数
* GREATEST(x1,x2,...) 返回集合中最大的值
* LEAST(x1,x2,...) 返回集合中最小的值
* RAND() 返回0到1内的随机值
* ROUND(x,y) 返回参数x的四舍五入的有y位小数的值
* TRUNCATE(x,y) 返回数字x截短为y为小数的值
* MOD(x,y) 取模
* LN(x) 自然对数
* LOG(x,y)
* SQRT(x) 

## 聚合函数
* AVG
* COUNT
* MIN
* MAX
* SUM
* GROUP_CONCAT 返回由属于一组的列值连接组合而成的结果

## 字符串函数
* ASCII
* CONCAT
* CONCAT(sep,s1,s2..) 将s1,s2...连接成字符串，并用sep字符间隔
* INSERT(str,x,y,instr) 将字符串str从第x位置开始，y个字符长的子字符串替换成instr
* LCASE() LOWER() 小写
* LEFT(str,x) 返回str最左边x个字符
* LENGTH() 返回字符数
* LTRIM() 去掉开头的空格
* POSITION(substr,str) 返回substr在str中第一次出现的位置
* QUOTE() 反斜杠转义单引号
* REVERSE() 反转字符串
* RIGHT(str,x) 返回字符串str最右边的x个字符
* RTRIM() 去掉尾部的空格
* TRIM() 去掉所有空格
* STRCMP(s1,s2) 比较字符串
* UCASE() UPPER() 大写

## 时间日期函数
* CURDATE()     CURRENT_DATE()
* CURTIME()     CURRENT_TIME()
* DATE_ADD(date,INTERVAL INT Keyword) date加上int间隔时间  eg: DATE_ADD(CURRENT_DATE,INTERVAL 6 MONTH)
* DATE_SUB(date,INTERVAL INT Keyword) date减去int间隔时间  eg: DATE_SUB(CURRENT_DATE,INTERVAL 6 MONTH)
* DATE_FORMAT(date,fmt) 格式化
* DAYORWEEK() 一周的第几天
* DAYOFMONTH() 一个月的第几天
* DAYOFYEAR() 一年的第几天
* DAYNAME() 周几 
* MONTHNAME()
* FROM_UNIXTIME(ts,fmt) 根据fmt格式化ts
* MINUTE()
* HOUR()
* NOW()
* WEEK() 一年中的第几周
* MONTH()
* QUARTER() 第几季度
* YEAR()

## 控制流函数
* CASE WHEN ... THEN ... ELSE ... END
* CASE ... WHEN ... THEN ... ELSE ... END
* IF(test,t,f) 如果test是真，返回t,否则返回f
* IFNULL(arg1,arg2) 如果arg1非空，返回arg1，否则返回arg2
* NULLIF(arg1,arg2) 如果arg1=arg2 返回null，否则返回arg1

## 加密函数