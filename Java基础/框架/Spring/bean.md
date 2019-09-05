## Bean
Spring核心其实是一个bean容器，什么是bean？可以简单的理解为在Java面向对象的世界里类的一个代言人。Java是面向对象的，对象拥有属性和方法，但是需要一个对象实例来调用属性和方法，这个对象实例就是bean。在spring内部使用BeanDefinition这一数据结构来对应bean。

```java
public interface BeanDefinition extends AttributeAccessor, BeanMetadataElement {

	/**
	 * bean在容器中是单例的
	 */
	String SCOPE_SINGLETON = ConfigurableBeanFactory.SCOPE_SINGLETON;

	/**
	 * 多例，每次对bean的请求都会创建一个新的bean实例，试用于有状态的bean
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
BeanDefinition中定义的规则默认由AbstractBeanDefinition实现，AbstractBeanDefinition有三个重要的子类:RootBeanDefinition，ChildBeanDefinition，GenericBeanDefinition


## BeanDefinitionHolder
```java
	private final BeanDefinition beanDefinition;

	private final String beanName;

	@Nullable
	private final String[] aliases;
```
BeanDefinitionHolder类里面主要包含三个属性，beanDefinition,beanName,aliases;从名称就可以看出，这个类主要是用来持有一个beanDefinition的，通过BeanDefinitionHolder来操作beanDefinition。

## BeanRegister
```java
public interface BeanDefinitionRegistry extends AliasRegistry {

	void registerBeanDefinition(String beanName, BeanDefinition beanDefinition)
			throws BeanDefinitionStoreException;

	void removeBeanDefinition(String beanName) throws NoSuchBeanDefinitionException;

	BeanDefinition getBeanDefinition(String beanName) throws NoSuchBeanDefinitionException;

	boolean containsBeanDefinition(String beanName);

	String[] getBeanDefinitionNames();

	int getBeanDefinitionCount();

	boolean isBeanNameInUse(String beanName);
}
```
BeanDefinitionRegistry继承自AliasRegistry，AliasRegistry定义了beanName和alias之间的关系，而BeanDefinition则定义了beanName和beanDefintion之间的关系。
其中registerBeanDefinition方法默认实现如下:
```java
@Override
	public void registerBeanDefinition(String beanName, BeanDefinition beanDefinition)
			throws BeanDefinitionStoreException {

		Assert.hasText(beanName, "Bean name must not be empty");
		Assert.notNull(beanDefinition, "BeanDefinition must not be null");
		// 对beanDefinition进行验证
		if (beanDefinition instanceof AbstractBeanDefinition) {
			try {
				((AbstractBeanDefinition) beanDefinition).validate();
			}
			catch (BeanDefinitionValidationException ex) {
				throw new BeanDefinitionStoreException(beanDefinition.getResourceDescription(), beanName,
						"Validation of bean definition failed", ex);
			}
		}

		BeanDefinition existingDefinition = this.beanDefinitionMap.get(beanName);
		if (existingDefinition != null) {
			// 如果已经存在并且不允许覆盖，抛出异常
			if (!isAllowBeanDefinitionOverriding()) {
				throw new BeanDefinitionOverrideException(beanName, beanDefinition, existingDefinition);
			}
			// 如果用户自定义的bean可以覆盖配置中定义的bean，这两者都可以覆盖spring内部的bean，反之则不行
			else if (existingDefinition.getRole() < beanDefinition.getRole()) {
				// e.g. was ROLE_APPLICATION, now overriding with ROLE_SUPPORT or ROLE_INFRASTRUCTURE
				if (logger.isInfoEnabled()) {
					logger.info("Overriding user-defined bean definition for bean '" + beanName +
							"' with a framework-generated bean definition: replacing [" +
							existingDefinition + "] with [" + beanDefinition + "]");
				}
			}
			// 如果已存在的bean和新的bean类型不一致，输出日志
			else if (!beanDefinition.equals(existingDefinition)) {
				if (logger.isDebugEnabled()) {
					logger.debug("Overriding bean definition for bean '" + beanName +
							"' with a different definition: replacing [" + existingDefinition +
							"] with [" + beanDefinition + "]");
				}
			}
			else {
				if (logger.isTraceEnabled()) {
					logger.trace("Overriding bean definition for bean '" + beanName +
							"' with an equivalent definition: replacing [" + existingDefinition +
							"] with [" + beanDefinition + "]");
				}
			}
			// 默认是可以覆盖的
			this.beanDefinitionMap.put(beanName, beanDefinition);
		}
		else {
			// 判断工厂是否开始创建bean这个过程，如果已经开始，需要进行并发控制，因为都是注册到beanDefinitionMap里面去，可能会出现并发问题
			if (hasBeanCreationStarted()) {
				synchronized (this.beanDefinitionMap) {
					this.beanDefinitionMap.put(beanName, beanDefinition);
					List<String> updatedDefinitions = new ArrayList<>(this.beanDefinitionNames.size() + 1);
					updatedDefinitions.addAll(this.beanDefinitionNames);
					updatedDefinitions.add(beanName);
					this.beanDefinitionNames = updatedDefinitions;
					removeManualSingletonName(beanName);
				}
			}
			else {
				this.beanDefinitionMap.put(beanName, beanDefinition);
				this.beanDefinitionNames.add(beanName);
				removeManualSingletonName(beanName);
			}
			this.frozenBeanDefinitionNames = null;
		}

		if (existingDefinition != null || containsSingleton(beanName)) {
			//  更新缓存
			resetBeanDefinition(beanName);
		}
	}
```
从这个注册过程其实就可以看出spring bean容器的本质了，其实就是一个key值为beanName，value为BeanDefinition的map。
registerAlias的过程其实很类似，代码如下:
```java
public void registerAlias(String name, String alias) {
		Assert.hasText(name, "'name' must not be empty");
		Assert.hasText(alias, "'alias' must not be empty");
		synchronized (this.aliasMap) {
			if (alias.equals(name)) {
				// name和alias相同则remove
				this.aliasMap.remove(alias);
				if (logger.isDebugEnabled()) {
					logger.debug("Alias definition '" + alias + "' ignored since it points to same name");
				}
			}
			else {
				String registeredName = this.aliasMap.get(alias);
				if (registeredName != null) {
					if (registeredName.equals(name)) {
						// An existing alias - no need to re-register
						return;
					}
					if (!allowAliasOverriding()) {
						throw new IllegalStateException("Cannot define alias '" + alias + "' for name '" +
								name + "': It is already registered for name '" + registeredName + "'.");
					}
					if (logger.isDebugEnabled()) {
						logger.debug("Overriding alias '" + alias + "' definition for registered name '" +
								registeredName + "' with new target name '" + name + "'");
					}
				}
				checkForAliasCircle(name, alias);
				this.aliasMap.put(alias, name);
				if (logger.isTraceEnabled()) {
					logger.trace("Alias definition '" + alias + "' registered for name '" + name + "'");
				}
			}
		}
	}
```
## 一些概念
* DTD : Document Type Definition,文档类型定义。属于xml文件中的一部分，用来验证xml文件中的格式是否正确。
* XSD : XML Schemas Definition,xsd是针对dtd的缺陷而提出的，dtd的缺陷在于本身不是使用的xml格式，因此解析起来需要重新定义一套解析器，同时dtd相较于xsd更难于解析。xsd本省就是使用xml格式编写的，因此可以直接同一个解析器进行解析。
