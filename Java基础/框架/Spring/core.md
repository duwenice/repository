## 加载配置文件 

在开发中，往往有需要去读取资源的情况出现，这些资源包括文件系统中的文件资源，网络资源，之前可以用jdk原生的URL类去读取资源，但是在Spring中提供的一个Resource接口，用来表示资源，它有许多实现类，比如UrlResource和ClassPathResource等等。
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

## 加载指定路径下的特定类

![20190805170212.png](https://repositoryimage.oss-cn-shanghai.aliyuncs.com/img/20190805170212.png)

