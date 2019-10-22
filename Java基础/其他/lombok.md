## @NonNull
> 作用在成员方法或者构造函数的参数前，用来做对成员变量的非空判断

## @Cleanup
> 作用在变量前，默认调用变量的close方法，也可以自定义方法。

## @Getter/@Setter
> 作用在成员变量上，用来生成成员变量的get和set方法。

## @ToString/@EqualsAndHashCode
> 作用在类上，生成类的toString，equals和hashcode方法。

## @NoArgsConstructor/@RequiredArgsConstructor/@AllArgsConstructor
> 作用在类上，分别表示生成无参构造函数，带有@NonNull或者final的变量的构造函数，全参构造函数。

## @Data/@Value
> 作用在类上，@Data和@Getter @Setter @RequiredArgsConstructor @ToString @EqualsAndHashCode一起等效，@Value和@Getter @FieldDefaults(makeFinal=true, level=AccessLevel.PRIVATE) @AllArgsConstructor @ToString @EqualsAndHashCode等效，会将所有成员变量变成private final。

## @SneakyThrows
> 作用在方法上，用于抛出指定异常。



