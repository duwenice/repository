# ELK
> Elasticsearch + Logstash + Kibana

## Elasticsearch
分布式的搜索引擎
在输入查询关键字之后，通过命中结果的匹配度有序返回结果集，就像是google搜索和百度搜索一样
在ELK中主要的作用是存储数据，索引和提供查询接口

## Logstash
内容转存站，主要用来数据收集和解析
input配置读取
filter配置解析，转化为k，v对
out配置输出

## Kibana
对es中的数据进行可视化的展示

