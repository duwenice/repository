# Aop

## 代理模式

代理，在生活中其实是无处不在的。交易需要找中介，明星会有经纪人，科学上网需要找梯子，上述提到的中介，经纪人，梯子其实就是一种代理。在Java中的代理模式，往往就是因为对象不方便被直接访问或者不想直接访问对象，所以需要创建一个该对象的代理。

具体实现的话，主要有三部分: 真实对象，代理对象以及真实对象和代理对象共同实现的接口或者抽象类。

代理可以分为两种，一种就是上面说的三个组成的模式，称为静态代理，但是在这个过程中，需要自己定义许多代理对象，那么可不可以自己动态生成代理对象呢，答案是可以，这种代理就是动态代理，常用的动态代理有jdk中的动态代理和cglib中的代理。

## Spring中的Aop

Spring中的aop实现是依赖于ioc的，其中的一个关键类就是AbstractAutoProxyCreator，我们来看看它的继承关系：

![20191009193141.png](https://repositoryimage.oss-cn-shanghai.aliyuncs.com/img/20191009193141.png)

可以看出其本质上是一个BeanPostProcessor，还记得在ioc实例化bean的过程中，会在bean的初始化前后加载BeanPostProcessor里面的两个方法吗？因此说Spring的aop是依赖于ioc来实现的。那么我们就来重点关注这两个方法:

```java
	@Override
	public Object postProcessBeforeInitialization(Object bean, String beanName) {
		return bean;
	}

	@Override
	public Object postProcessAfterInitialization(@Nullable Object bean, String beanName) {
		if (bean != null) {
			Object cacheKey = getCacheKey(bean.getClass(), beanName);
			if (earlyProxyReferences.remove(cacheKey) != bean) {
				return wrapIfNecessary(bean, beanName, cacheKey);
			}
		}
		return bean;
	}
```
继续看wrapIfNecessary这个方法:
```java
	protected Object wrapIfNecessary(Object bean, String beanName, Object cacheKey) {
        ……
		// Create proxy if we have advice.
		Object[] specificInterceptors = getAdvicesAndAdvisorsForBean(bean.getClass(), beanName, null);
		if (specificInterceptors != DO_NOT_PROXY) {
			advisedBeans.put(cacheKey, Boolean.TRUE);
			Object proxy = createProxy(
					bean.getClass(), beanName, specificInterceptors, new SingletonTargetSource(bean));
			proxyTypes.put(cacheKey, proxy.getClass());
			return proxy;
		}
        ……
	}
```
这里主要说两个方法：
- getAdvicesAndAdvisorsForBean这个方法会找到所有的Advisor。(Advice是通知，即代理对象对真实对象的功能增强点的功能实现，Advisor是切面，切面往往包含两个主要部分切入点与增强功能实现，所以可以把Advisor看做是Advice的更高层的封装)
- createProxy方法会具体生成代理对象。

接下来继续看createProxy方法的具体实现:
```java
	protected Object createProxy(Class<?> beanClass, @Nullable String beanName,
								 @Nullable Object[] specificInterceptors, TargetSource targetSource) {

		if (beanFactory instanceof ConfigurableListableBeanFactory) {
			AutoProxyUtils.exposeTargetClass((ConfigurableListableBeanFactory) beanFactory, beanName, beanClass);
		}

		ProxyFactory proxyFactory = new ProxyFactory();
		proxyFactory.copyFrom(this);

		if (!proxyFactory.isProxyTargetClass()) {
			if (shouldProxyTargetClass(beanClass, beanName)) {
				proxyFactory.setProxyTargetClass(true);
			} else {
				evaluateProxyInterfaces(beanClass, proxyFactory);
			}
		}

		Advisor[] advisors = buildAdvisors(beanName, specificInterceptors);
		proxyFactory.addAdvisors(advisors);
		proxyFactory.setTargetSource(targetSource);
		customizeProxyFactory(proxyFactory);

		proxyFactory.setFrozen(freezeProxy);
		if (advisorsPreFiltered()) {
			proxyFactory.setPreFiltered(true);
		}

		return proxyFactory.getProxy(getProxyClassLoader());
	}
```

可以看出其主要是生成了一个ProxyFactory实例，并且对其注入了相应的属性，那么什么是ProxyFactory呢？从名称就可以大概猜出来，这是代理类的生成工厂。

```java
public class ProxyFactory extends ProxyCreatorSupport {
    ……
	public Object getProxy() {
		return createAopProxy().getProxy();
	}
    ……
}
```

其核心方法就是getProxy，那么怎么生成具体的代理呢？首先是createAopProxy():

```java
	protected final synchronized AopProxy createAopProxy() {
		if (!this.active) {
			activate();
		}
		return getAopProxyFactory().createAopProxy(this);
	}
```

又是先需要创建AopProxy的工厂，其默认实现如下:

```java
public ProxyCreatorSupport() {
		this.aopProxyFactory = new DefaultAopProxyFactory();
	}
```

于是在DefaultAopProxyFactory类里面终于可以创建AopProxy了，代码如下:

```java
	public AopProxy createAopProxy(AdvisedSupport config) throws AopConfigException {
		if (config.isOptimize() || config.isProxyTargetClass() || hasNoUserSuppliedProxyInterfaces(config)) {
			Class<?> targetClass = config.getTargetClass();
			if (targetClass == null) {
				throw new AopConfigException("TargetSource cannot determine target class: " +
						"Either an interface or a target is required for proxy creation.");
			}
			// 如果目标类是接口或者是Proxy的子类，采用jdk动态代理，其他情况采取cglib代理
			if (targetClass.isInterface() || Proxy.isProxyClass(targetClass)) {
				return new JdkDynamicAopProxy(config);
			}
			return new ObjenesisCglibAopProxy(config);
		} else {
			return new JdkDynamicAopProxy(config);
		}
	}
```

可以看到Spring中的代理生成是通过jdk动态代理或者cglib代理生成的。

![20191009200811.png](https://repositoryimage.oss-cn-shanghai.aliyuncs.com/img/20191009200811.png)

下面可以稍微看看jdk动态代理生成代理的过程:

```java
	public Object getProxy(@Nullable ClassLoader classLoader) {
		if (logger.isTraceEnabled()) {
			logger.trace("Creating JDK dynamic proxy: " + this.advised.getTargetSource());
		}
		Class<?>[] proxiedInterfaces = AopProxyUtils.completeProxiedInterfaces(this.advised, true);
		findDefinedEqualsAndHashCodeMethods(proxiedInterfaces);
		return Proxy.newProxyInstance(classLoader, proxiedInterfaces, this);
	}
```
Java.lang.reflect.Proxy.newProxyInstance(…) 方法需要三个参数，第一个是 ClassLoader，第二个参数代表需要实现哪些接口，第三个参数最重要，是 InvocationHandler 实例，我们看到这里传了 this，因为 JdkDynamicAopProxy 本身实现了 InvocationHandler 接口。

InvocationHandler 只有一个方法，当生成的代理类对外提供服务的时候，都会导到这个方法中：

```java
public interface InvocationHandler {
    public Object invoke(Object proxy, Method method, Object[] args)
        throws Throwable;
}
```

JdkDynamicAopProxy 对其的实现如下:

```java
	public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
            ……
			// 创建一个 chain，包含所有要执行的 advice
			List<Object> chain = this.advised.getInterceptorsAndDynamicInterceptionAdvice(method, targetClass);
			if (chain.isEmpty()) {
				Object[] argsToUse = AopProxyUtils.adaptArgumentsIfNecessary(method, args);
				retVal = AopUtils.invokeJoinpointUsingReflection(target, method, argsToUse);
			}
			else {
				MethodInvocation invocation =
						new ReflectiveMethodInvocation(proxy, target, method, args, targetClass, chain);
				// Proceed to the joinpoint through the interceptor chain.
				retVal = invocation.proceed();
			}
            ……
		}
	}
```

简单地说，就是在执行每个方法的时候，判断下该方法是否需要被一次或多次增强（执行一个或多个 advice）。