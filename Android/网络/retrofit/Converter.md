作用：将 Java 类型转为 HTTP 表示；将 HTTP 实体转回 Java 类型。

使用：通过 Retrofit.Builder 的 addConverterFactory(Factory) 方法进行安装。

Retrofit 提供的一些第一方模块包括：

- [Gson](https://github.com/google/gson) - `com.squareup.retrofit2:converter-gson`
- [Jackson](https://github.com/FasterXML/jackson-dataformat-xml) - `com.squareup.retrofit2:converter-jackson`
- [Moshi](https://github.com/square/moshi) - `com.squareup.retrofit2:converter-moshi`
- [Protobuf](https://developers.google.com/protocol-buffers/) - `com.squareup.retrofit2:converter-protobuf`
- [Wire](https://github.com/square/wire) - `com.squareup.retrofit2:converter-wire`
- [Simple Framework](http://simple.sourceforge.net/) - `com.squareup.retrofit2:converter-simplexml`
- Scalars - `com.squareup.retrofit2:converter-scalars`

还包括两个代理转换器：

- Guava's `Optional<T>` - `com.squareup.retrofit2:converter-guava`
- Java 8's `Optional<T>` - `com.squareup.retrofit2:converter-java8`




#### 分析

Converter\<T, F\> 是一个 interface，它的唯一方法是

`T convert(F value) throws IOException;`

除此之外，它还包含一个抽象内部类 Factory，在使用时，我们使用 Converter.Factory 的实现类来间接提供 Converter 实现。

Converter.Factory 包括以下五个方法（该抽象类并没有抽象方法）：

+ Converter\<ResponseBody, ?> responseBodyConverter(...)

  返回一个将 HTTP 响应体转换为 type 的 Converter，如果无法处理，则返回 null。

+ Converter<?, RequestBody> requestBodyConverter (...)

  返回一个将 type 转为 HTTP 请求体的 Converter，如果无法处理，则返回 null。

+ Converter<?, String> stringConverter(...)

  返回一个将 type 转为 String 的 Converter，如果无法处理，则返回 null。

+ Type getParameterUpperBound(int index, ParameterizedType type)

  从 type 中提取第 index 个泛型参数的最高类型。比如，Map\<String, ? extends Runnable> ，index 为 1，得到的是 Runnable。

+ Class<?> getRawType(Type type)

  从 type 中提取原始类型，如 List<? extends Runnable> 返回 List.class。

  ​



#### 源码

```java
/**
 * Convert objects to and from their representation in HTTP. Instances are created by {@linkplain
 * Factory a factory} which is {@linkplain Retrofit.Builder#addConverterFactory(Factory) installed}
 * into the {@link Retrofit} instance.
 */
public interface Converter<F, T> {
  T convert(F value) throws IOException;

  /** Creates {@link Converter} instances based on a type and target usage. */
  abstract class Factory {
    /**
     * Returns a {@link Converter} for converting an HTTP response body to {@code type}, or null if
     * {@code type} cannot be handled by this factory. This is used to create converters for
     * response types such as {@code SimpleResponse} from a {@code Call<SimpleResponse>}
     * declaration.
     */
    public @Nullable Converter<ResponseBody, ?> responseBodyConverter(Type type,
        Annotation[] annotations, Retrofit retrofit) {
      return null;
    }

    /**
     * Returns a {@link Converter} for converting {@code type} to an HTTP request body, or null if
     * {@code type} cannot be handled by this factory. This is used to create converters for types
     * specified by {@link Body @Body}, {@link Part @Part}, and {@link PartMap @PartMap}
     * values.
     */
    public @Nullable Converter<?, RequestBody> requestBodyConverter(Type type,
        Annotation[] parameterAnnotations, Annotation[] methodAnnotations, Retrofit retrofit) {
      return null;
    }

    /**
     * Returns a {@link Converter} for converting {@code type} to a {@link String}, or null if
     * {@code type} cannot be handled by this factory. This is used to create converters for types
     * specified by {@link Field @Field}, {@link FieldMap @FieldMap} values,
     * {@link Header @Header}, {@link HeaderMap @HeaderMap}, {@link Path @Path},
     * {@link Query @Query}, and {@link QueryMap @QueryMap} values.
     */
    public @Nullable Converter<?, String> stringConverter(Type type, Annotation[] annotations,
        Retrofit retrofit) {
      return null;
    }

    /**
     * Extract the upper bound of the generic parameter at {@code index} from {@code type}. For
     * example, index 1 of {@code Map<String, ? extends Runnable>} returns {@code Runnable}.
     */
    protected static Type getParameterUpperBound(int index, ParameterizedType type) {
      return Utils.getParameterUpperBound(index, type);
    }

    /**
     * Extract the raw class type from {@code type}. For example, the type representing
     * {@code List<? extends Runnable>} returns {@code List.class}.
     */
    protected static Class<?> getRawType(Type type) {
      return Utils.getRawType(type);
    }
  }
}

```




参考：

[Wiki Converters](https://github.com/square/retrofit/wiki/Converters)