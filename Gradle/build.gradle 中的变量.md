>  编译相关的信息感觉还是放在 build.gradle 中比较好，如果是创建一个类来保存此类配置的话，别人接手代码会不方便查找。





### 代码获取 build.gradle 的配置信息

我们可以在 build.gradle 通过 buildConfigField() 方法添加字段，resValue() 添加资源值，然后在我们的代码中读取出来。

```groovy
android {
  ...
  buildTypes {
    release {
      // These values are defined only for the release build, which
      // is typically used for full builds and continuous builds.
      buildConfigField("String", "BUILD_TIME", "\"${minutesSinceEpoch}\"")
      resValue("string", "build_time", "${minutesSinceEpoch}")
      ...
    }
    debug {
      // Use static values for incremental builds to ensure that
      // resource files and BuildConfig aren't rebuilt with each run.
      // If they were dynamic, they would prevent certain benefits of
      // Instant Run as well as Gradle UP-TO-DATE checks.
      buildConfigField("String", "BUILD_TIME", "\"0\"")
      resValue("string", "build_time", "0")
    }
  }
}
...
```

> 需要注意添加 String 变量时加上双引号

访问：

```java
...
Log.i(TAG, BuildConfig.BUILD_TIME);
Log.i(TAG, getString(R.string.build_time));
```

如果想要为每一个 build type 都声明同一个字段，可以在 buildTypes 中添加

```groovy
buildTypes.each{
            it.buildConfigField("int","ENV","1")
        }
```









