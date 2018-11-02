### 为 product flavor 配置不同 Id

[application-id](https://developer.android.com/studio/build/application-id.html) 变体的id

```
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

根据构建类型buildtype

```
android {
    ...
    buildTypes {
        debug {
            applicationIdSuffix ".debug"
        }
    }
}
```

free 的 debug 的应用ID 为 com.example.myapp.free.debug



### AndroidManifest 引用 applicationId

`${applicationId}`

