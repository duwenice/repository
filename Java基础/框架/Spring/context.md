# Spring的入口类

![20190903154859.png](https://repositoryimage.oss-cn-shanghai.aliyuncs.com/img/20190903154859.png)

WebApplicationInitializer接口定义了Spring的入口方法:onStartup(ServletContext servletContext),AbstractContextLoaderInitializer默认实现了该方法，代码如下:
```java
	public void onStartup(ServletContext servletContext) throws ServletException {
		registerContextLoaderListener(servletContext);
	}

    protected void registerContextLoaderListener(ServletContext servletContext) {
		WebApplicationContext rootAppContext = createRootApplicationContext();
		if (rootAppContext != null) {
			ContextLoaderListener listener = new ContextLoaderListener(rootAppContext);
			listener.setContextInitializers(getRootApplicationContextInitializers());
			servletContext.addListener(listener);
		}
		else {
			logger.debug("No ContextLoaderListener registered, as " +
					"createRootApplicationContext() did not return an application context");
		}
	}
```
Spring的核心功能其实就是对于bean对象的创建管理，可以把bean类比于手机，制造生产手机的地方是工厂，那么创建管理bean的场所就是容器。spring中的容器大致可以分为两类，一种是BeanFactory，只提供了容器的最基本功能，创建管理对象，对象的依赖注入等；另外一种就是面向企业的应用上下文了，在基础功能之上还可以解析配置等企业级的功能。

## BeanFactory
```java
/**
 * The root interface for accessing a Spring bean container.
 * This is the basic client view of a bean container;
 * further interfaces such as {@link ListableBeanFactory} and
 * {@link org.springframework.beans.factory.config.ConfigurableBeanFactory}
 * are available for specific purposes.
 *
 * <p>This interface is implemented by objects that hold a number of bean definitions,
 * each uniquely identified by a String name. Depending on the bean definition,
 * the factory will return either an independent instance of a contained object
 * (the Prototype design pattern), or a single shared instance (a superior
 * alternative to the Singleton design pattern, in which the instance is a
 * singleton in the scope of the factory). Which type of instance will be returned
 * depends on the bean factory configuration: the API is the same. Since Spring
 * 2.0, further scopes are available depending on the concrete application
 * context (e.g. "request" and "session" scopes in a web environment).
 *
 * <p>The point of this approach is that the BeanFactory is a central registry
 * of application components, and centralizes configuration of application
 * components (no more do individual objects need to read properties files,
 * for example). See chapters 4 and 11 of "Expert One-on-One J2EE Design and
 * Development" for a discussion of the benefits of this approach.
 *
 * <p>Note that it is generally better to rely on Dependency Injection
 * ("push" configuration) to configure application objects through setters
 * or constructors, rather than use any form of "pull" configuration like a
 * BeanFactory lookup. Spring's Dependency Injection functionality is
 * implemented using this BeanFactory interface and its subinterfaces.
 *
 * <p>Normally a BeanFactory will load bean definitions stored in a configuration
 * source (such as an XML document), and use the {@code org.springframework.beans}
 * package to configure the beans. However, an implementation could simply return
 * Java objects it creates as necessary directly in Java code. There are no
 * constraints on how the definitions could be stored: LDAP, RDBMS, XML,
 * properties file, etc. Implementations are encouraged to support references
 * amongst beans (Dependency Injection).
 *
 * <p>In contrast to the methods in {@link ListableBeanFactory}, all of the
 * operations in this interface will also check parent factories if this is a
 * {@link HierarchicalBeanFactory}. If a bean is not found in this factory instance,
 * the immediate parent factory will be asked. Beans in this factory instance
 * are supposed to override beans of the same name in any parent factory.
 *
 * <p>Bean factory implementations should support the standard bean lifecycle interfaces
 * as far as possible. The full set of initialization methods and their standard order is:
 * <ol>
 * <li>BeanNameAware's {@code setBeanName}
 * <li>BeanClassLoaderAware's {@code setBeanClassLoader}
 * <li>BeanFactoryAware's {@code setBeanFactory}
 * <li>EnvironmentAware's {@code setEnvironment}
 * <li>EmbeddedValueResolverAware's {@code setEmbeddedValueResolver}
 * <li>ResourceLoaderAware's {@code setResourceLoader}
 * (only applicable when running in an application context)
 * <li>ApplicationEventPublisherAware's {@code setApplicationEventPublisher}
 * (only applicable when running in an application context)
 * <li>MessageSourceAware's {@code setMessageSource}
 * (only applicable when running in an application context)
 * <li>ApplicationContextAware's {@code setApplicationContext}
 * (only applicable when running in an application context)
 * <li>ServletContextAware's {@code setServletContext}
 * (only applicable when running in a web application context)
 * <li>{@code postProcessBeforeInitialization} methods of BeanPostProcessors
 * <li>InitializingBean's {@code afterPropertiesSet}
 * <li>a custom init-method definition
 * <li>{@code postProcessAfterInitialization} methods of BeanPostProcessors
 * </ol>
 *
 * <p>On shutdown of a bean factory, the following lifecycle methods apply:
 * <ol>
 * <li>{@code postProcessBeforeDestruction} methods of DestructionAwareBeanPostProcessors
 * <li>DisposableBean's {@code destroy}
 * <li>a custom destroy-method definition
 * </ol>
 *
 */
public interface BeanFactory {

	String FACTORY_BEAN_PREFIX = "&";

	Object getBean(String name) throws BeansException;

	<T> T getBean(String name, Class<T> requiredType) throws BeansException;

	Object getBean(String name, Object... args) throws BeansException;

	<T> T getBean(Class<T> requiredType) throws BeansException;

	<T> T getBean(Class<T> requiredType, Object... args) throws BeansException;

	<T> ObjectProvider<T> getBeanProvider(Class<T> requiredType);

	<T> ObjectProvider<T> getBeanProvider(ResolvableType requiredType);

	boolean containsBean(String name);

	boolean isSingleton(String name) throws NoSuchBeanDefinitionException;

	boolean isPrototype(String name) throws NoSuchBeanDefinitionException;

	boolean isTypeMatch(String name, ResolvableType typeToMatch) throws NoSuchBeanDefinitionException;

	boolean isTypeMatch(String name, Class<?> typeToMatch) throws NoSuchBeanDefinitionException;

	@Nullable
	Class<?> getType(String name) throws NoSuchBeanDefinitionException;

	String[] getAliases(String name);

}
```
在Spring官方给出的BeanFactory注解中，已经将其解释得很清楚了，这里翻译一下:
  BeanFactory是访问Spring bean容器的元接口，是bean容器的客户端页面（这意味着我们所有对于spring bean容器的操作都是通过BeanFactory来实现的），其子接口像ListableBeanFactory，ConfigurableBeanFactory等可以用来实现特定的功能。
  这个接口由包含许多BeanDefinition的对象来实现，每个BeanDefinition由一个String类型的name唯一标识。当需要从容器中获取到bean实例的时候，会根据BeanDefinition的scope，如果是单例的就返回bean容器的保存的单例共享对象，如果是Prototype，就从容器中返回一个新的实例。
  BeanFactory的关键在于是应用程序组件的注册中心并且集中了应用程序的组件配置。
  通过setter方法和构造器对对象进行依赖注入可以比作为push，而对象需要依赖的时候来BeanFactory查找可以比作pull，往往使用push比pull好。而Spring的依赖注入功能就是通过BeanFactory接口和它的子接口来实现的。
  BeanFactory有许多实现，HierarchicalBeanFactory就是其中一种，这个接口的所有方法会检查它的parent factory。如果需要的bean在该实例中没有找到，就会去它的 parent factory里面查找，该实例中的bean应该覆盖其parent factory里面相同name的bean。
  一个bean的初始化过程如下：
  1. setBeanName
  2. setBeanClassLoader
  3. setBeanFactory
  4. setEnvironment
  5. setEmbeddedValueResolver
  6. setResourceLoader
  
  以下为在application context中才执行的过程

  7. setApplicationEventPublisher
  8. setMessageSource
  9. setApplicationContext
  10. setServletContext
  11. postProcessBeforeInitialization
  12. postProcessAfterInitialization

![20190904140432.png](https://repositoryimage.oss-cn-shanghai.aliyuncs.com/img/20190904140432.png)

这张图基本上包含了常见的BeanFactory子接口：
* ListableBeanFactory: 拓展了BeanFactory，可以罗列出此时容器中的所有实例，定义了返回所有实例name的方法。
* HierarchicalBeanFactory: 拓展了BeanFactory的一个重要思想，对其分层。定义了获取其parent factory的方法。
* AutowireCapableBeanFactory: 在BeanFactory的基础上实现了对于存在实例的管理，可以使用这个接口集成其他框架，捆绑并填充并不由spring管理但已经存在的实例。
* ConfigurableBeanFactory: 定义了BeanFactory的配置，比如类加载器，类型转换等等。
* ConfigurableListableBeanFactory: 集大成者,提供解析,修改bean定义,并初始化单例


几个核心map
- Map<String, Object> singletonObjects key为beanName，value为对应的单例实例
- Map<String, String> aliasMap key为别名，value为beanName
- Map<String, BeanDefinition> beanDefinitionMap key为beanName，value为BeanDefinition


Spring 中大量使用反射，需要获取泛型的具体类型，为此专门提供了一个工具类解析泛型 - ResolvalbeType。ResolvableType 是对 Class，Field，Method 获取 Type 的抽象

## Context
Spring中的Context的始祖是ApplicationContext，代码如下：
```java
public interface ApplicationContext extends EnvironmentCapable, ListableBeanFactory, HierarchicalBeanFactory,
		MessageSource, ApplicationEventPublisher, ResourcePatternResolver {

	@Nullable
	String getId();

	String getApplicationName();

	String getDisplayName();

	long getStartupDate();

	@Nullable
	ApplicationContext getParent();

	AutowireCapableBeanFactory getAutowireCapableBeanFactory() throws IllegalStateException;
}
```
