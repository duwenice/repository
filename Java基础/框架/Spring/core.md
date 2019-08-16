## 加载资源 


在开发中，往往有需要去读取资源的情况出现，这些资源包括文件系统中的文件资源，网络资源，之前可以用jdk原生的URL类去读取资源，但是在Spring中提供的一个Resource接口，用来表示资源，它有许多实现类，比如UrlResource和ClassPathResource等等。
对Resource出现的解释:
![20190812092134.png](https://repositoryimage.oss-cn-shanghai.aliyuncs.com/img/20190812092134.png)
![20190807092115.png](https://repositoryimage.oss-cn-shanghai.aliyuncs.com/img/20190807092115.png)

作为spring中所有资源的统一抽象，Resource定义了一些通用的方法，并由AbstractResource提供了默认实现。
Resource中定义的方法如下：
```java
	/**
	 * 资源是否存在
	 */
	boolean exists();

	 /**
	  * 资源是否可读
	  */
	default boolean isReadable() {
		return exists();
	}

	 /**
	  * 资源的流是否开启
	  */
	default boolean isOpen() {
		return false;
	}

	 /**
	  * 判断资源是不是文件
	  */
	default boolean isFile() {
		return false;
	}

	 /**
	  * 返回资源的URL句柄
	  */
	URL getURL() throws IOException;

	 /**
	  * 返回资源的URI句柄
	  */
	URI getURI() throws IOException;

	 /**
	  * 返回资源的文件句柄
	  */
	File getFile() throws IOException;


	default ReadableByteChannel readableChannel() throws IOException {
		return Channels.newChannel(getInputStream());
	}

	/**
	 * 返回资源内容的长度
	 */
	long contentLength() throws IOException;

	/**
	 * 返回资源上一次修改的时间
	 */
	long lastModified() throws IOException;


	 /**
	  * 根据相对路径创建资源
	  */
	Resource createRelative(String relativePath) throws IOException;

    /**
	 * 返回资源的文件名
	 */
	@Nullable
	String getFilename();

	/**
	 * 返回资源的描述
	 */
	String getDescription();
```

既然有这么多的实现类，如果是由开发者在使用的时候来决定使用什么类的话，那么就体现不出Resource接口在这里的作用了。Spring提供了另一个接口叫ResourceLoader，用来加载资源返回对应的Resource实例，这是一种典型的策略模式，在调度器中根据不同的对象返回不同的策略（在ResourceLoader中根据不同的地址路径返回不同的Resource实例）。其默认实现为
DefaultResourceLoader，核心是getResource函数,如下所示：
```java
	public Resource getResource(String location) {
		Assert.notNull(location, "Location must not be null");

		for (ProtocolResolver protocolResolver : this.protocolResolvers) {
			Resource resource = protocolResolver.resolve(location, this);
			if (resource != null) {
				return resource;
			}
		}

		if (location.startsWith("/")) {
			return getResourceByPath(location);
		}
		else if (location.startsWith(CLASSPATH_URL_PREFIX)) {
			return new ClassPathResource(location.substring(CLASSPATH_URL_PREFIX.length()), getClassLoader());
		}
		else {
			try {
				// Try to parse the location as a URL...
				URL url = new URL(location);
				return (ResourceUtils.isFileURL(url) ? new FileUrlResource(url) : new UrlResource(url));
			}
			catch (MalformedURLException ex) {
				// No URL -> resolve as resource path.
				return getResourceByPath(location);
			}
		}
```
最后返回一个Resource，其中比较重要的是ClassPathResource：
![20190802173452.png](https://repositoryimage.oss-cn-shanghai.aliyuncs.com/img/20190802173452.png)

Resource
```java
	public InputStream getInputStream() throws IOException {
		InputStream is;
		if (this.clazz != null) {
			is = this.clazz.getResourceAsStream(this.path);
		}
		else if (this.classLoader != null) {
			is = this.classLoader.getResourceAsStream(this.path);
		}
		else {
			is = ClassLoader.getSystemResourceAsStream(this.path);
		}
		if (is == null) {
			throw new FileNotFoundException(getDescription() + " cannot be opened because it does not exist");
		}
		return is;
	}
```
## 加载.properties配置文件
> https://blog.csdn.net/andy_zhang2007/article/details/86749301


PropertiesLoaderSupport类是用来加载JavaBean风格配置的基础类，Spirng将属性分为两种：localProperties（本地缺省属性）和environmentProperties（外部环境属性），同时默认外部环境属性优先级高于本地缺省属性，PropertiesLoaderSupport主要包括三个属性:Properties（java.util包里面的一个类，将配置文件中的属性变成kv对）,Resource（Spring中定义的资源）以及PropertiesPersister（用来覆盖重写Properties类中方法的接口类）。
PropertiesLoaderSupport类的核心代码是其中的loadProperties方法：

```java
	protected void loadProperties(Properties props) throws IOException {
		if (this.locations != null) {
			for (Resource location : this.locations) {
				if (logger.isTraceEnabled()) {
					logger.trace("Loading properties file from " + location);
				}
				try {
					PropertiesLoaderUtils.fillProperties(
							props, new EncodedResource(location, this.fileEncoding), this.propertiesPersister);
				}
				catch (FileNotFoundException | UnknownHostException ex) {
					if (this.ignoreResourceNotFound) {
						if (logger.isDebugEnabled()) {
							logger.debug("Properties resource not found: " + ex.getMessage());
						}
					}
					else {
						throw ex;
					}
				}
			}
		}
	}
```
可以看到，此处通过PropertiesLoaderUtils工具类实现将Resource资源中的配置属性加载填充进入Properties中，接下来看PropertiesLoaderUtils方法中的fillProperties方法：
```java
	static void fillProperties(Properties props, EncodedResource resource, PropertiesPersister persister)
			throws IOException {
		InputStream stream = null;
		Reader reader = null;
		try {
			String filename = resource.getResource().getFilename();
			if (filename != null && filename.endsWith(XML_FILE_EXTENSION)) {
				stream = resource.getInputStream();
				persister.loadFromXml(props, stream);
			}
			else if (resource.requiresReader()) {
				reader = resource.getReader();
				persister.load(props, reader);
			}
			else {
				stream = resource.getInputStream();
				persister.load(props, stream);
			}
		}
		finally {
			if (stream != null) {
				stream.close();
			}
			if (reader != null) {
				reader.close();
			}
		}
	}
```
可以看出，这个方法其实就起到了一个调用的工作，传入的三个参数，props是资源加载返回的结果，resource是资源，persister是加载资源的方法。


## Bean
Spring核心其实是一个bean容器，什么是bean？可以简单的理解为在Java面向对象的世界里类的一个代言人。Java是面向对象的，对象拥有属性和方法，但是需要一个对象实例来调用属性和方法，这个对象实例就是bean。在spring内部使用BeanDefinition这一数据结构来对应bean。

```java
public interface BeanDefinition extends AttributeAccessor, BeanMetadataElement {

	/**
	 * Scope identifier for the standard singleton scope: "singleton".
	 * <p>Note that extended bean factories might support further scopes.
	 * @see #setScope
	 */
	String SCOPE_SINGLETON = ConfigurableBeanFactory.SCOPE_SINGLETON;

	/**
	 * Scope identifier for the standard prototype scope: "prototype".
	 * <p>Note that extended bean factories might support further scopes.
	 * @see #setScope
	 */
	String SCOPE_PROTOTYPE = ConfigurableBeanFactory.SCOPE_PROTOTYPE;


	/**
	 * 此类占据了程序中的大多数，是用户自定义的bean
	 */
	int ROLE_APPLICATION = 0;

	/**
	 * 此类表示的是从配置文件中得到的bean
	 */
	int ROLE_SUPPORT = 1;

	/**
	 * 此类表示的是spring内部的bean
	 */
	int ROLE_INFRASTRUCTURE = 2;


	// Modifiable attributes

	/**
	 * Set the name of the parent definition of this bean definition, if any.
	 */
	void setParentName(@Nullable String parentName);

	/**
	 * Return the name of the parent definition of this bean definition, if any.
	 */
	@Nullable
	String getParentName();

	/**
	 * Specify the bean class name of this bean definition.
	 * <p>The class name can be modified during bean factory post-processing,
	 * typically replacing the original class name with a parsed variant of it.
	 * @see #setParentName
	 * @see #setFactoryBeanName
	 * @see #setFactoryMethodName
	 */
	void setBeanClassName(@Nullable String beanClassName);

	/**
	 * Return the current bean class name of this bean definition.
	 * <p>Note that this does not have to be the actual class name used at runtime, in
	 * case of a child definition overriding/inheriting the class name from its parent.
	 * Also, this may just be the class that a factory method is called on, or it may
	 * even be empty in case of a factory bean reference that a method is called on.
	 * Hence, do <i>not</i> consider this to be the definitive bean type at runtime but
	 * rather only use it for parsing purposes at the individual bean definition level.
	 * @see #getParentName()
	 * @see #getFactoryBeanName()
	 * @see #getFactoryMethodName()
	 */
	@Nullable
	String getBeanClassName();

	/**
	 * Override the target scope of this bean, specifying a new scope name.
	 * @see #SCOPE_SINGLETON
	 * @see #SCOPE_PROTOTYPE
	 */
	void setScope(@Nullable String scope);

	/**
	 * Return the name of the current target scope for this bean,
	 * or {@code null} if not known yet.
	 */
	@Nullable
	String getScope();

	/**
	 * 设置是否采取lazy init，如果是false，这个bean将会在启动的时候由工厂实* 例化
	 */
	void setLazyInit(boolean lazyInit);

	
	boolean isLazyInit();

	/**
	 * 设置这个bean在被实例化的时候依赖的其他bean
	 */
	void setDependsOn(@Nullable String... dependsOn);

	@Nullable
	String[] getDependsOn();

	/**
	 * 设置当这个bean需要被注入的时候是否是其中的候选人 
	 * 这个针对于@autowired （基于类型的装配）有效
	 * 当使用@Resource（基于名称的装配）的时候不管该属性是true还是false还是* 会被匹配到的
	 */
	void setAutowireCandidate(boolean autowireCandidate);

	boolean isAutowireCandidate();

	/**
	 * 是否为主候选bean
	 */
	void setPrimary(boolean primary);

	boolean isPrimary();

	/**
	 * 设置加载这个bean的工厂名
	 */
	void setFactoryBeanName(@Nullable String factoryBeanName);

	@Nullable
	String getFactoryBeanName();

	/**
	 * 设置加载的时候的工厂方法。
     * 这个方法先将通过调用构造函数，或者如果没有参数，将调用该方法的无参数构* 造。
     * 方法将在指定的工厂bean（如果有的话）上被调用，或者作为本地bean类的静* 态方法被调用。
	 */
	void setFactoryMethodName(@Nullable String factoryMethodName);

	 */
	@Nullable
	String getFactoryMethodName();

	/**
	 * 返回构造函数参数
	 */
	ConstructorArgumentValues getConstructorArgumentValues();

	/**
	 * Return if there are constructor argument values defined for this bean.
	 * @since 5.0.2
	 */
	default boolean hasConstructorArgumentValues() {
		return !getConstructorArgumentValues().isEmpty();
	}

	/**
	 * 返回属性值
	 */
	MutablePropertyValues getPropertyValues();

	/**
	 * Return if there are property values values defined for this bean.
	 * @since 5.0.2
	 */
	default boolean hasPropertyValues() {
		return !getPropertyValues().isEmpty();
	}

	/**
	 * Set the name of the initializer method.
	 * @since 5.1
	 */
	void setInitMethodName(@Nullable String initMethodName);

	/**
	 * Return the name of the initializer method.
	 * @since 5.1
	 */
	@Nullable
	String getInitMethodName();

	/**
	 * Set the name of the destroy method.
	 * @since 5.1
	 */
	void setDestroyMethodName(@Nullable String destroyMethodName);

	/**
	 * Return the name of the destroy method.
	 * @since 5.1
	 */
	@Nullable
	String getDestroyMethodName();

	/**
	 * Set the role hint for this {@code BeanDefinition}. The role hint
	 * provides the frameworks as well as tools with an indication of
	 * the role and importance of a particular {@code BeanDefinition}.
	 * @since 5.1
	 * @see #ROLE_APPLICATION
	 * @see #ROLE_SUPPORT
	 * @see #ROLE_INFRASTRUCTURE
	 */
	void setRole(int role);

	/**
	 * Get the role hint for this {@code BeanDefinition}. The role hint
	 * provides the frameworks as well as tools with an indication of
	 * the role and importance of a particular {@code BeanDefinition}.
	 * @see #ROLE_APPLICATION
	 * @see #ROLE_SUPPORT
	 * @see #ROLE_INFRASTRUCTURE
	 */
	int getRole();

	/**
	 * Set a human-readable description of this bean definition.
	 * @since 5.1
	 */
	void setDescription(@Nullable String description);

	/**
	 * Return a human-readable description of this bean definition.
	 */
	@Nullable
	String getDescription();


	// Read-only attributes

	/**
	 * Return whether this a <b>Singleton</b>, with a single, shared instance
	 * returned on all calls.
	 * @see #SCOPE_SINGLETON
	 */
	boolean isSingleton();

	/**
	 * Return whether this a <b>Prototype</b>, with an independent instance
	 * returned for each call.
	 * @since 3.0
	 * @see #SCOPE_PROTOTYPE
	 */
	boolean isPrototype();

	/**
	 * Return whether this bean is "abstract", that is, not meant to be instantiated.
	 */
	boolean isAbstract();

	/**
	 * Return a description of the resource that this bean definition
	 * came from (for the purpose of showing context in case of errors).
	 */
	@Nullable
	String getResourceDescription();

	/**
	 * Return the originating BeanDefinition, or {@code null} if none.
	 * Allows for retrieving the decorated bean definition, if any.
	 * <p>Note that this method returns the immediate originator. Iterate through the
	 * originator chain to find the original BeanDefinition as defined by the user.
	 */
	@Nullable
	BeanDefinition getOriginatingBeanDefinition();

}
```

## 加载指定路径下的特定类

![20190805170212.png](https://repositoryimage.oss-cn-shanghai.aliyuncs.com/img/20190805170212.png)

