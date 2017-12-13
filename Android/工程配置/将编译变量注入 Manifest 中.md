`build.gradle`

```groovy
android {
    defaultConfig {
        manifestPlaceholders = [hostName:"www.example.com"]
    }
    ...
}
```

`AndroidManifest.xml`

```groovy
<intent-filter ... >
    <data android:scheme="http" android:host="${hostName}" ... />
    ...
</intent-filter>
```

默认地，编译工具使用  `${applicationId}`  占位符来提供应用的 ID。比如，在 `build.gradle` 中

```groovy
android {
    defaultConfig {
        applicationId "com.example.myapp"
    }
    productFlavors {
        free {
            applicationIdSuffix ".free"
        }
        pro {
            applicationIdSuffix ".pro"
        }
    }
}
```

然后，在 manifest 中使用：

```xml
<intent-filter ... >
    <action android:name="${applicationId}.TRANSMOGRIFY" />
    ...
</intent-filter>
```

当我们编译一个 "free" 版本时，manifest 实际的效果为：

```xml
<intent-filter ... >
   <action android:name="com.example.myapp.free.TRANSMOGRIFY" />
    ...
</intent-filter>
```



参考：

[Inject Build Variables into the Manifest](https://developer.android.com/studio/build/manifest-build-variables.html)