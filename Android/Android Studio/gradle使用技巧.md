### 配置 project 范围属性

在 project 的 build.gradle 中添加一个 ext 块，并添加属性

```groovy
buildscript {...}
allprojects {...}

// This block encapsulates custom properties and makes them available to all
// modules in the project.
ext {
    // The following are only a few examples of the types of properties you can define.
    compileSdkVersion = 26
    // You can also use this to specify versions for dependencies. Having consistent
    // versions between modules can avoid behavior conflicts.
    supportLibVersion = "27.0.0"
    ...
}
...
```

在module中通过如下方式访问

```groovy
android {
  // Use the following syntax to access properties you define at the project level:
  // rootProject.ext.property_name
  compileSdkVersion rootProject.ext.compileSdkVersion
  ...
}
...
dependencies {
    compile "com.android.support:appcompat-v7:${rootProject.ext.supportLibVersion}"
    ...
}
```





参考：

[Configure project-wide properties](https://developer.android.com/studio/build/gradle-tips.html#configure-project-wide-properties)