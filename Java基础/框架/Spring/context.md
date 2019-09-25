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


![20190906153048.png](https://repositoryimage.oss-cn-shanghai.aliyuncs.com/img/20190906153048.png)

DefaultSingletonBeanRegistry中的几个map如下：
* Map<String, Object> singletonObjects spring中的bean大部分是单例的，singletonObjects就是缓存单例对象的位置。
* Map<String, ObjectFactory<?>> singletonFactories 用于存储在spring内部所使用的beanName->对象工厂的引用，一旦最终对象被创建(通过objectFactory.getObject())，此引用信息将删除
* Map<String, Object> earlySingletonObjects 用于存储在创建Bean早期对创建的原始bean的一个引用，注意这里是原始bean，即使用工厂方法或构造方法创建出来的对象，一旦对象最终创建好，此引用信息将删除
* Set<String> registeredSingletons
* Set<String> singletonsCurrentlyInCreation

beanName其实对应的是xml文件中定义的beanId xml文件中定义的name对应的是bean AliasName

### bean的实例化
bean的实例化核心代码如下:
```java
sharedInstance = getSingleton(beanName, () -> {
                        try {
                            return createBean(beanName, mbd, args);
                        } catch (BeansException ex) {
                            destroySingleton(beanName);
                            throw ex;
                        }
```
就是这么一行代码首先实例化bean而后将实例化后的bean获取出来。
getSingleton传入的参数有两个，beanName和一个ObjectFactory<?>对象，其中ObjectFactory是一个典型的函数式接口，其定义如下：
```java
/**
 * Defines a factory which can return an Object instance
 * (possibly shared or independent) when invoked.
 */
@FunctionalInterface
public interface ObjectFactory<T> {
	T getObject() throws BeansException;
}
```
至于createBean方法是在AbstractBeanFactory中定义，在其子类AbstractAutowireCapableBeanFactory中实现。该子类中的核心方法就是这个方法，用来创建一个实例。


```java
public interface FactoryBean<T> {
	@Nullable
	T getObject() throws Exception;

	@Nullable
	Class<?> getObjectType();

	default boolean isSingleton() {
		return true;
	}
}
```

一般情况下，Spring是通过反射机制来实现bean的实例化的，但是在某些情况下，实例化bean比较复杂，此时就通过实现FactoryBean接口来定制实例化bean的逻辑（通过实现getObject方法可以在其中定制实例化bean的逻辑）。

### FactoryBean和ObjectFactory的理解
FactoryBean和ObjectFactory是bean实例化过程中非常重要的两个概念，这里说一下自己的理解：FactoryBean是spring中的一个SPI(Service Provider Interface)设计，Spring提供了定义，但是由用户自定义实现，因此FactoryBean是用来提供给用户定制怎么实例化bean的接口，接下来说ObjectFactory，这是一个典型的函数式接口，由上面实例化的核心代码可知：bean的实例化过程是通过实现ObjectFactory的函数接口来实现的，因此ObjectFactory正如其名是一个工厂方法。但是ObjectFactory还有一个重要的作用，就是在下面这两段代码中：
```java
        Object singletonObject = singletonObjects.get(beanName);
        if (singletonObject == null && isSingletonCurrentlyInCreation(beanName)) {
            synchronized (singletonObjects) {
                singletonObject = earlySingletonObjects.get(beanName);
                if (singletonObject == null && allowEarlyReference) {
                    ObjectFactory<?> singletonFactory = singletonFactories.get(beanName);
                    if (singletonFactory != null) {
                        singletonObject = singletonFactory.getObject();
                        earlySingletonObjects.put(beanName, singletonObject);
                        singletonFactories.remove(beanName);
                    }
                }
            }
        }
        return singletonObject;
```
上面这段代码有两个临时map：singletonFactories和earlySingletonObjects，前者是beanName到ObjectFactory的映射，后者是beanName到原始bean的映射。这里又涉及了另外一个过程，Spring在bean的实例化过程中，并不是完整的原子操作，而是先根据构造函数实例化一个原始bean，而后通过populate()这个函数进行属性的注入填充。一旦对象最终实例化成功，这两个临时map都会清空，现在开始看这段代码，主要有以下几步：
1. 首先从缓存中获取bean，如果缓存中不存在bean并且bean正在被创建，此时就说明出现了循环依赖的问题（Bean在实例化的过程中会先加入一个正在创建的池，当创建的过程中发现自己已经在池中，就说明出现了循环依赖），接下来解决循环依赖的问题。
2. 如果原始bean不存在，并且allowEarlyReference为true，这个属性代表的是在依赖注入的过程中，在A依赖于B的情况下，允许对A注入B的原始Bean（即一个ObjectFactory对象）。
3. 根据beanName从singletonFactories中获取到对应的beanFactory，即原始bean。
4. 建立从beanName到原始bean的映射。
5. 移除beanName到beanFactory的映射。
总结一下，这段代码的意义在于getBean的时候如果缓存中存在则返回缓存中的bean实例，如果缓存中不存在，并且正在被创建，说明发生了循环依赖，此时原始bean存在，会返回原始bean。
另一段代码如下：
```java
        boolean earlySingletonExposure =
            (mbd.isSingleton() && allowCircularReferences && isSingletonCurrentlyInCreation(beanName));
        if (earlySingletonExposure) {
            if (logger.isTraceEnabled()) {
                logger.trace(
                    "Eagerly caching bean '" + beanName + "' to allow for resolving potential circular references");
            }
            addSingletonFactory(beanName, () -> getEarlyBeanReference(beanName, mbd, bean));
        }
```
这段代码的位置在于调用构造函数得到原始bean和属性填充的中间，说的是在bean实例化的过程中，如果是单例对象，允许循环依赖并且此时这个bean正在被创建，其实就是出现了循环依赖的问题，此时会中断属性填充，将原始bean加入singletonFactories这个临时map。因此可以得到以下过程（发生循环依赖）：
![20190910194626.png](https://repositoryimage.oss-cn-shanghai.aliyuncs.com/img/20190910194626.png)
又因为是将正在实例化的原始beanA提供给B注入，因此当beanA属性填充完成之后，beanB所依赖的就是完整的beanA（同一个地址的beanA）.


tip:
* 如果在依赖注入的过程中采取的是构造器注入的方式，这种方式造成的循环依赖是没法解决的，只能抛出异常。

### bean的属性填充
bean的属性填充是通过下面这一行代码：
```java
        populateBean(beanName, mbd, instanceWrapper);
```
属性填充的具体代码如下:
```java
        PropertyValues pvs = (mbd.hasPropertyValues() ? mbd.getPropertyValues() : null);

        if (mbd.getResolvedAutowireMode() == AUTOWIRE_BY_NAME || mbd.getResolvedAutowireMode() == AUTOWIRE_BY_TYPE) {
            MutablePropertyValues newPvs = new MutablePropertyValues(pvs);
            // Add property values based on autowire by name if applicable.
            if (mbd.getResolvedAutowireMode() == AUTOWIRE_BY_NAME) {
                autowireByName(beanName, mbd, bw, newPvs);
            }
            // Add property values based on autowire by type if applicable.
            if (mbd.getResolvedAutowireMode() == AUTOWIRE_BY_TYPE) {
                autowireByType(beanName, mbd, bw, newPvs);
            }
            pvs = newPvs;
        }
		……
		if (needsDepCheck) {
            if (filteredPds == null) {
                filteredPds = filterPropertyDescriptorsForDependencyCheck(bw, mbd.allowCaching);
            }
            checkDependencies(beanName, mbd, filteredPds, pvs);
        }

        if (pvs != null) {
            applyPropertyValues(beanName, mbd, bw, pvs);
        }
```
可以看到上面这段代码说的是获取属性值pvs，检查属性的依赖，然后填充pvs的过程。首先现在获取属性值pvs的模式有以下几种:
```java
public static final int AUTOWIRE_NO = AutowireCapableBeanFactory.AUTOWIRE_NO;

public static final int AUTOWIRE_BY_NAME =
	AutowireCapableBeanFactory.AUTOWIRE_BY_NAME;

public static final int AUTOWIRE_BY_TYPE = AutowireCapableBeanFactory.AUTOWIRE_BY_TYPE;

public static final int AUTOWIRE_CONSTRUCTOR = AutowireCapableBeanFactory.AUTOWIRE_CONSTRUCTOR;
```
从名字就能看出来，分别是不进行注入填充，根据名称进行填充，根据类型进行填充，使用构造器进行填充。
其中第二个和第三个对应的就是我们常用的注解@Autowired和@Resource，那我们接下来看看它们分别怎么实现的。

@Autowired的实现如下：
```java
    protected void autowireByName(String beanName, AbstractBeanDefinition mbd, BeanWrapper bw,
        MutablePropertyValues pvs) {

        String[] propertyNames = unsatisfiedNonSimpleProperties(mbd, bw);
        for (String propertyName : propertyNames) {
            if (containsBean(propertyName)) {
                Object bean = getBean(propertyName);
                pvs.add(propertyName, bean);
                registerDependentBean(propertyName, beanName);
				……
                }
            } else {
				……
            }
        }
    }
```
很简单的逻辑，根据属性值名称对应的beanName去bean容器中取，然后与本实例关联。

@Resource的实现如下:
```java
    protected void autowireByType(String beanName, AbstractBeanDefinition mbd, BeanWrapper bw,
        MutablePropertyValues pvs) {

        TypeConverter converter = getCustomTypeConverter();
        if (converter == null) {
            converter = bw;
        }

        Set<String> autowiredBeanNames = new LinkedHashSet<>(4);
        String[] propertyNames = unsatisfiedNonSimpleProperties(mbd, bw);
        for (String propertyName : propertyNames) {
            try {
                PropertyDescriptor pd = bw.getPropertyDescriptor(propertyName);
                if (Object.class != pd.getPropertyType()) {
                    MethodParameter methodParam = BeanUtils.getWriteMethodParameter(pd);
                    boolean eager = !PriorityOrdered.class.isInstance(bw.getWrappedInstance());
                    DependencyDescriptor desc = new AutowireByTypeDependencyDescriptor(methodParam, eager);
                    Object autowiredArgument = resolveDependency(desc, beanName, autowiredBeanNames, converter);
                    if (autowiredArgument != null) {
                        pvs.add(propertyName, autowiredArgument);
                    }
                    for (String autowiredBeanName : autowiredBeanNames) {
                        registerDependentBean(autowiredBeanName, beanName);
						……
                    }
                    autowiredBeanNames.clear();
                }
            } catch (BeansException ex) {
                throw new UnsatisfiedDependencyException(mbd.getResourceDescription(), beanName, propertyName, ex);
            }
        }
    }
```
根据type注入的时候也是遍历各个属性名，然后根据每个属性的类型的描述符来进行判断注入。
接下来看具体得到了pvs之后，怎么将pvs填充到本实例的过程:
```java
    protected void applyPropertyValues(String beanName, BeanDefinition mbd, BeanWrapper bw, PropertyValues pvs) {
        if (pvs.isEmpty()) {
            return;
        }

        if (System.getSecurityManager() != null && bw instanceof BeanWrapperImpl) {
            ((BeanWrapperImpl)bw).setSecurityContext(getAccessControlContext());
        }

        MutablePropertyValues mpvs = null;
        List<PropertyValue> original;

        if (pvs instanceof MutablePropertyValues) {
            mpvs = (MutablePropertyValues)pvs;
            if (mpvs.isConverted()) {
                try {
                    bw.setPropertyValues(mpvs);
                    return;
                } catch (BeansException ex) {
                    throw new BeanCreationException(mbd.getResourceDescription(), beanName,
                        "Error setting property values", ex);
                }
            }
            original = mpvs.getPropertyValueList();
        } else {
            original = Arrays.asList(pvs.getPropertyValues());
        }

        TypeConverter converter = getCustomTypeConverter();
        if (converter == null) {
            converter = bw;
        }
        BeanDefinitionValueResolver valueResolver = new BeanDefinitionValueResolver(this, beanName, mbd, converter);

        List<PropertyValue> deepCopy = new ArrayList<>(original.size());
        boolean resolveNecessary = false;
        for (PropertyValue pv : original) {
            if (pv.isConverted()) {
                deepCopy.add(pv);
            } else {
                String propertyName = pv.getName();
                Object originalValue = pv.getValue();
                Object resolvedValue = valueResolver.resolveValueIfNecessary(pv, originalValue);
                Object convertedValue = resolvedValue;
                boolean convertible = bw.isWritableProperty(propertyName)
                    && !PropertyAccessorUtils.isNestedOrIndexedProperty(propertyName);
                if (convertible) {
                    convertedValue = convertForProperty(resolvedValue, propertyName, bw, converter);
                }
                if (resolvedValue == originalValue) {
                    if (convertible) {
                        pv.setConvertedValue(convertedValue);
                    }
                    deepCopy.add(pv);
                } else if (convertible && originalValue instanceof TypedStringValue
                    && !((TypedStringValue)originalValue).isDynamic()
                    && !(convertedValue instanceof Collection || ObjectUtils.isArray(convertedValue))) {
                    pv.setConvertedValue(convertedValue);
                    deepCopy.add(pv);
                } else {
                    resolveNecessary = true;
                    deepCopy.add(new PropertyValue(pv, convertedValue));
                }
            }
        }
        if (mpvs != null && !resolveNecessary) {
            mpvs.setConverted();
        }

        try {
            bw.setPropertyValues(new MutablePropertyValues(deepCopy));
        } catch (BeansException ex) {
            throw new BeanCreationException(mbd.getResourceDescription(), beanName, "Error setting property values",
                ex);
        }
    }
```

## 初始化（init）Bean
```java
        populateBean(beanName, mbd, instanceWrapper);
        exposedObject = initializeBean(beanName, exposedObject, mbd);
```
可以看到，在进行属性填充之后，紧接着就是对Bean的初始化。
```java
    protected Object initializeBean(final String beanName, final Object bean, @Nullable RootBeanDefinition mbd) {
        if (System.getSecurityManager() != null) {
            AccessController.doPrivileged((PrivilegedAction<Object>)() -> {
                invokeAwareMethods(beanName, bean);
                return null;
            }, getAccessControlContext());
        } else {
            invokeAwareMethods(beanName, bean);
        }

        Object wrappedBean = bean;
        if (mbd == null || !mbd.isSynthetic()) {
            wrappedBean = applyBeanPostProcessorsBeforeInitialization(wrappedBean, beanName);
        }

        try {
            invokeInitMethods(beanName, wrappedBean, mbd);
        } catch (Throwable ex) {
            throw new BeanCreationException((mbd != null ? mbd.getResourceDescription() : null), beanName,
                "Invocation of init method failed", ex);
        }
        if (mbd == null || !mbd.isSynthetic()) {
            wrappedBean = applyBeanPostProcessorsAfterInitialization(wrappedBean, beanName);
        }

        return wrappedBean;
    }
```
大概分为以下几步:
* 调用相应的Aware接口方法
* 调用相应的BeanPostProcessor的postProcessBeforeInitialization方法
* 调用初始化方法
* 调用相应的BeanPostProcessor的postProcessAfterInitialization方法

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
