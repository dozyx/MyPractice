> 在经过下面的配置后，如果使用 Android Studio 3.0 版本还是会有其他问题，[Android studio 3.0 butterknife error](https://github.com/JakeWharton/butterknife/issues/963)，链接里给出了解决方案，不过我没细看，因为我决定不在库 module 中引入 Butter Knife 的依赖了。

这个问题是在库 module 中使用 Butter Knife 时出现的。在库中使用 Butter Knife，需要在编译脚本中添加 plugin：

(AS 中为 工程目录的 build.gradle)

```groovy
buildscript {
  repositories {
    mavenCentral()
   }
  dependencies {
    classpath 'com.jakewharton:butterknife-gradle-plugin:8.8.1'
  }
}
```

然后在 module 中添加：

```
apply plugin: 'com.android.library'
apply plugin: 'com.jakewharton.butterknife'
```

最后，在 Butter Knife 注解中使用 R2 替代 R：

```java
class ExampleActivity extends Activity {
  @BindView(R2.id.user) EditText username;
  @BindView(R2.id.pass) EditText password;
...
}
```



参考：    

[butterknife library-projects](https://github.com/JakeWharton/butterknife#library-projects)