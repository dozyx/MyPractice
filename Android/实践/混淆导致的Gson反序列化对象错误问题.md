> Gson 官方文档中没提到混淆问题，但想想，用于反序列的类经过混淆后肯定会出问题啊。我所遇到的问题是，Gson 在序列化一个 Bean 对象为 Json 字符串时，相应字段变成了 a、b、c，然后另一边使用 Gson 进行反序列化，这时候 Bean 相应变量的值变为了 null 或其他初始值。

其实，官方提供了 Gson 的混淆配置例子的，它放在了 [android-proguard-example](https://github.com/google/gson/tree/master/examples/android-proguard-example) 里。 `proguard.cfg` 文件配置了该示例在使用 Gson 时需要做的混淆处理，文件内容如下：

```
##---------------Begin: proguard configuration for Gson  ----------
# Gson uses generic type information stored in a class file when working with fields. Proguard
# removes such information by default, so configure it to keep all of it.
-keepattributes Signature

# For using GSON @Expose annotation
-keepattributes *Annotation*

# Gson specific classes
-dontwarn sun.misc.**
#-keep class com.google.gson.stream.** { *; }

# Application classes that will be serialized/deserialized over Gson
-keep class com.google.gson.examples.android.model.** { *; }

# Prevent proguard from stripping interface information from TypeAdapterFactory,
# JsonSerializer, JsonDeserializer instances (so they can be used in @JsonAdapter)
-keep class * implements com.google.gson.TypeAdapterFactory
-keep class * implements com.google.gson.JsonSerializer
-keep class * implements com.google.gson.JsonDeserializer

##---------------End: proguard configuration for Gson  ----------
```

可以看到， `-keep class com.google.gson.examples.android.model.** { *; }` 表明了不对用于反序列化类进行混淆处理。   

所以，为了方便处理，最好将用于反序列化的 Bean 类放到一起。   

> 除了混淆配置，也可以通过使用 @SerializedName 注解来防止名称因为混淆改变而导致错误的问题，不过暂时还没对这种方式进行验证。



参考：

[android-proguard-example](https://github.com/google/gson/tree/master/examples/android-proguard-example)    

[Gson 混淆不正确导致的 bug](http://www.jianshu.com/p/2b9b15a79639)    

[google gson 使用proguard混淆代码注意事项](http://blog.csdn.net/yuxiaohui78/article/details/46885337)