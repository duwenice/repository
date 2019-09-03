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