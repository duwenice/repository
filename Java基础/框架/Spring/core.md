## 加载配置文件 

在开发中，往往有需要去读取资源的情况出现，这些资源包括文件系统中的文件资源，网络资源，之前可以用jdk原生的URL类去读取资源，但是在Spring中提供的一个Resource接口，用来表示资源，它有许多实现类，比如UrlResource和ClassPathResource等等。既然有这么多的实现类，如果是由开发者在使用的时候来决定使用什么类的话，那么就体现不出Resource接口在这里的作用了。Spring提供了另一个接口叫ResourceLoader，用来加载资源返回对应的Resource实例。其默认实现为
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

