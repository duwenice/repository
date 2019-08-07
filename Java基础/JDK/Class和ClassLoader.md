java中在获取资源的时候，Class和ClassLoader都提供了方法来实现，首先看Class类里面的实现:
```java
     /**
      * 返回资源的InputStream
      */
     public InputStream getResourceAsStream(String name) {
        name = resolveName(name);
        ClassLoader cl = getClassLoader0();
        if (cl==null) {
            // A system class.
            return ClassLoader.getSystemResourceAsStream(name);
        }
        return cl.getResourceAsStream(name);
    }

    /**
     * 返回资源的URL
     */
    public java.net.URL getResource(String name) {
        name = resolveName(name);
        ClassLoader cl = getClassLoader0();
        if (cl==null) {
            // A system class.
            return ClassLoader.getSystemResource(name);
        }
        return cl.getResource(name);
    }

    /**
     * 如果路径以'/'开头，去掉'/'
     * 如果路径不以'/'开头，则加上包路径
     */
    private String resolveName(String name) {
        if (name == null) {
            return name;
        }
        if (!name.startsWith("/")) {
            Class<?> c = this;
            while (c.isArray()) {
                c = c.getComponentType();
            }
            String baseName = c.getName();
            int index = baseName.lastIndexOf('.');
            if (index != -1) {
                name = baseName.substring(0, index).replace('.', '/')
                    +"/"+name;
            }
        } else {
            name = name.substring(1);
        }
        return name;
    }
```
然后是ClassLoader里面的实现:
```java
    /**
     * 返回资源的InputStream
     */
    public InputStream getResourceAsStream(String name) {
        URL url = getResource(name);
        try {
            return url != null ? url.openStream() : null;
        } catch (IOException e) {
            return null;
        }
    }

    /**
     * 返回资源的URL
     */
    public URL getResource(String name) {
        URL url;
        if (parent != null) {
            url = parent.getResource(name);
        } else {
            url = getBootstrapResource(name);
        }
        if (url == null) {
            url = findResource(name);
        }
        return url;
    }
```
对比发现，Class类中的资源加载其实是通过调用ClassLoader实现的，核心主要有两个方法：getResource返回资源的url路径，getResourceAsStream返回资源的InputStream流。

|   |path|寻找路径|
|---|---|---|
|Class|不以'/'开头|当前类所在包|
|Class|以'/'开头|ClassPath路径下|
|ClassLoader|不以'/'开头|ClassPath路径下|
|ClassLoader|以'/'开头|null|

可以看出class.getResource("/") == class.getClassLoader().getResource(""),从源码上看也可以看出这一点，Class类中的getResource方法首先通过resolveName方法如果有'/'则去掉。