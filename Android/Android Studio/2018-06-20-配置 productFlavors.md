通过 productFlavors，我们可以在一个工程中生成有差异的 apk。

比如：demo 版本和 full 版本

```groovy
android {
    ...
    defaultConfig {...}
    buildTypes {...}
    productFlavors {
        demo {
            applicationIdSuffix ".demo"
            versionNameSuffix "-demo"
        }
        full {
            applicationIdSuffix ".full"
            versionNameSuffix "-full"
        }
    }
}
```



#### 组合 productFlavors

如果需要组合更多种维度，可以设置  flavorDimensions

如：基于不同最小 api 的 demo 和 full 版本

```
android {
  ...
  buildTypes {
    debug {...}
    release {...}
  }

  // Specifies the flavor dimensions you want to use. The order in which you
  // list each dimension determines its priority, from highest to lowest,
  // when Gradle merges variant sources and configurations. You must assign
  // each product flavor you configure to one of the flavor dimensions.
  flavorDimensions "api", "mode"

  productFlavors {
    demo {
      // Assigns this product flavor to the "mode" flavor dimension.
      dimension "mode"
      ...
    }

    full {
      dimension "mode"
      ...
    }

    // Configurations in the "api" product flavors override those in "mode"
    // flavors and the defaultConfig {} block. Gradle determines the priority
    // between flavor dimensions based on the order in which they appear next
    // to the flavorDimensions property above--the first dimension has a higher
    // priority than the second, and so on.
    minApi24 {
      dimension "api"
      minSdkVersion '24'
      // To ensure the target device receives the version of the app with
      // the highest compatible API level, assign version codes in increasing
      // value with API level. To learn more about assigning version codes to
      // support app updates and uploading to Google Play, read Multiple APK Support
      versionCode 30000 + android.defaultConfig.versionCode
      versionNameSuffix "-minApi24"
      ...
    }

    minApi23 {
      dimension "api"
      minSdkVersion '23'
      versionCode 20000  + android.defaultConfig.versionCode
      versionNameSuffix "-minApi23"
      ...
    }

    minApi21 {
      dimension "api"
      minSdkVersion '21'
      versionCode 10000  + android.defaultConfig.versionCode
      versionNameSuffix "-minApi21"
      ...
    }
  }
}
...
```

通过上面的配置可以构建 3 * 2 * 2 = 12 个不同 apk，对应

`app-[minApi24, minApi23, minApi21]-[demo, full]-[debug, release].apk `

我们可以为不同 product flavor 的 apk 使用不同的源码集，如 app-minApi24-demo-debug.apk 源码放在 `src/demoMinApi24/java/ `目录。

> 添加 product flavor 并不会自动生成对应的源码目录，如果不确定源集目录，可以执行 gradle -> 应用 -> Tasks -> android -> sourceSets，该 task 将列出所有组合的源码目录。或者在 project 窗口选择 Project 视图，右键 src，选择 New -> Folder -> javaFolder，选择 target source set 后，将自动生成对应的源码目录。



#### 过滤 productFlavors

有时候，我们并不需要同时使用所有的 product flavor，比如 demo 下不需要 minApi21，这是我们可以使用 variantFilter 进行过滤。

```groovy
android {
  ...
  buildTypes {...}

  flavorDimensions "api", "mode"
  productFlavors {
    demo {...}
    full {...}
    minApi24 {...}
    minApi23 {...}
    minApi21 {...}
  }

  variantFilter { variant ->
      def names = variant.flavors*.name
      // To check for a certain build type, use variant.buildType.name == "<buildType>"
      if (names.contains("minApi21") && names.contains("demo")) {
          // Gradle ignores any variants that satisfy the conditions above.
          setIgnore(true)
      }
  }
}
...
```























参考：

[build-variants](https://developer.android.com/studio/build/build-variants)