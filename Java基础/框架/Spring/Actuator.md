# Actuator
> 本文基于spring-boot 2.2.6官方文档：https://docs.spring.io/spring-boot/docs/2.2.6.RELEASE/reference/html/production-ready-features.html#production-ready

## EndPoint
> Actuator endpoints let you monitor and interact with your application. Spring Boot includes a number of built-in endpoints and lets you add your own. For example, the health endpoint provides basic application health information.
> 
> Each individual endpoint can be enabled or disabled. This controls whether or not the endpoint is created and its bean exists in the application context. To be remotely accessible an endpoint also has to be exposed via JMX or HTTP. Most applications choose HTTP, where the ID of the endpoint along with a prefix of /actuator is mapped to a URL. For example, by default, the health endpoint is mapped to /actuator/health.

Actuator中的EndPoint是用来监控应用的，Spring Boot已经内置了许多endPoint，同时也可以自定义Endpoint。EndPoint大部分默认是不暴露的，其暴露的方式分为两种，JMX和HTTP，大部分的应用会选择通过HTTP方式暴露相应的EndPoint。

以下是一些内置的Endpoint：
|id|说明|默认开启|默认http可访问|默认jmx可访问|
|--|--|--|--|--|
|beans|显示容器中的bean列表|Y|N|Y|
|caches|显示应用中的缓存|Y|N|Y|
|conditions|显示配置条件的计算情况|Y|N|Y|
|configprops|显示@ConfigurationProperties的信息|Y|N|Y|
|env|显示ConfigurableEnvironment中的属性|Y|N|Y|
|health|显示健康检查信息|Y|Y|Y|
|httptrace|显示HTTP TRACE 信息|Y|N|Y|
|info|显示设置好的应用信息|Y|Y|Y|
|loggers|显示并更新日志配置|Y|N|Y|
|metrics|显示应用的度量信息|Y|N|Y|
|mappings|显示所有的@RequestMapping信息|Y|N|Y|
|scheduledtasks|显示应用的调度任务信息|Y|N|Y|
|shutdown|优雅的关闭用用程序|N|N|Y|
|threaddump|执行Thread Dump|Y|N|Y|
|heapdump|返回Heap Dump文件，格式为HPROF|Y|N|N/A|
|prometheus|返回可以供Prometheus抓取的信息|Y|N|N/A|

## Micrometer
> https://www.ibm.com/developerworks/cn/java/j-using-micrometer-to-record-java-metric/index.html

>http://ylzheng.com/2018/01/24/use-prometheus-monitor-your-spring-boot-application/

MicroMeter中有两个核心概念：Meter(计量器)和MeterRegistry(计量器注册表)，计量器指的是需要收集的性能指标数据，而计量器注册表是用来维护计量器的。
常用的计量器有以下四种:Counter,Gauge,Timer,Distribution Summary.

### Counter
只增不减的计量器：比如说记录请求总数

### Gauge
可增可减的计量器：用于反应应用的当前状态，比如说当前机器可用内存

### Timer
计时器：用来记录事件的持续时间。

### Distribution Summary
分布概要：用来记录事件的分布情况，比如说百分比和直方图。

## Note
> http://www.heartthinkdo.com/?p=2457


![20200426160537](https://repositoryimage.oss-cn-shanghai.aliyuncs.com/img/20200426160537.png)
![20200426160600](https://repositoryimage.oss-cn-shanghai.aliyuncs.com/img/20200426160600.png)