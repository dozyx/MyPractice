# Gradle——构建的基本知识
> 本文是官网的个人简略版。  

## 构建过程
官网上的图：

![img](https://ws2.sinaimg.cn/large/006tNc79gy1fyvwr4i9dqj30qe0togmu.jpg)

> 在生成最终的 APK 之前，packager 还会用 zipalign 来对 app 进行优化以减少运行时的占用内存。  

## 自定义构建配置
利用 Gradle 和 Android 插件，可以从以下几方面对编译进行配置：
+ Build Types
通常用于不同开发周期的配置，Android Studio 默认会创建 debug 和 release 两种编译类型。
+ Product Flavors
用于为用户提供不同的 app 版本，如免费和收费版。
+ Build Variants
Gradle 用于编译 app 的配置，build variant 由 build type 和 product flavor 共同产生。我们不直接配置 build variant，但通过 build type 和 product flavor 将生成 build variant。
+ Manifest Entries
我们可以在 build variant 配置（也就是 build type 和 product flavor 的配置）中指定 manifest 文件某些属性的值，如应用名、最小 SDK、target SDK 等。
+ Dependencies
本地或远程依赖。
+ Signing
在编译配置中指定签名设置并在构建过程中自动为 apk 签名。
+ ProGuard
可以为不同的 build variant 指定不同的混淆规则。
+ Multiple APK Support
编译不同的 apk，这些 apk 只包含特定屏幕尺寸或 abi 所需要的代码和资源。

## 编译配置文件
一个 Android Studio 工程目录如下：
![](Gradle%20%E6%9E%84%E5%BB%BA%E7%9A%84%E5%9F%BA%E6%9C%AC%E7%9F%A5%E8%AF%86/4357026F-D607-470F-98EC-F7F30EB697EB.png)
在编译配置文件中，普通文本文件使用 DSL(Domain Specific Language)  来描述配置，而操作编译逻辑使用的 Groovy。

### Gradle 设置文件
工程根目录的 `settings.gradle` 用于告诉 Gradle 编译时需要包含哪些 module。如：
```
include ‘:app’
```

### 顶层的编译文件
工程根目录的 `build.gradle` 文件，定义了应用于工程中所有 module 的编译配置。默认的，它使用 `buildscript ` 块来确定所有 module 的 Gradle 仓库和依赖。
如：
```groovy
/**
 * buildscript 块用于配置 Gradle 自身的仓库和依赖。
 * 如它依赖的 Android plugin 将为 Gradle 提供编译 Android app 模块所需的额外指令。
 */

buildscript {

    /**
     * Gradle 搜索和下载依赖所用的仓库。Gradle 预配置的有 JCenter、MavenCentral、Ivy。
     */

    repositories {
        jcenter()
    }

    /**
     * Gradle 编译工程所需要的依赖。
     */

    dependencies {
        classpath 'com.android.tools.build:gradle:2.3.3'
    }
}

/**
 * allprojects 块用来配置所用 module 使用的仓库和依赖。
 */

allprojects {
   repositories {
       jcenter()
   }
}
```

#### 配置工程范围的属性
我们可以在顶层的 `build.gradle` 中添加一个 `ext` 块来配置额外属性，这些属性将在所有 module 中共享。
如：
```groovy
buildscript {...}

allprojects {...}

// ext 块包含自定义属性并对所有 module 可用。
ext {
    // The following are only a few examples of the types of properties you can define.
    compileSdkVersion = 26
    buildToolsVersion = "26.0.1"
    // You can also create properties to specify versions for dependencies.
    // Having consistent versions between modules can avoid conflicts with behavior.
    supportLibVersion = "26.1.0"
    ...
}
...
```

在 module 的 `build.gradle` 文件中可以使用以下语法来访问这些属性：

```
android {
  // Use the following syntax to access properties you defined at the project level:
  // rootProject.ext.property_name
  compileSdkVersion rootProject.ext.compileSdkVersion
  buildToolsVersion rootProject.ext.buildToolsVersion
  ...
}
...
dependencies {
    compile "com.android.support:appcompat-v7:${rootProject.ext.supportLibVersion}"
    ...
}
```
> 注意：应避免这种用法，因为它将导致使用这些属性的 module 耦合在一起。  

### Module 层的编译文件
每一个 module 目录的 `build.gradle` 文件。
如：
```
/**
 * 第一行将 Android plugin 应用到编译该 module 的 Gradle，这样 android 块才可用于指定 Android特定的编译项。
 */

apply plugin: 'com.android.application'

/**
 * android 块用于配置所有的 Android 特定编译项。
 */

android {

  /**
   * buildToolsVersion：SDK build tools 的版本。
   */

  compileSdkVersion 26
  buildToolsVersion "26.0.1"

  /**
   * The defaultConfig 块包含了所有 build variant 的默认配置，编译系统可以动态
	 * 覆盖 main/AndroidManifest.xml 的默写属性。我们也可以在 product flavors 中为不同版本的 app 重写这些值。 
   */

  defaultConfig {

    /**
     * 发布的包的唯一标识，但源码仍会引用定义在 main/AndroidManifest.xml 文件中的包名。
     */

    applicationId 'com.example.myapp'

    minSdkVersion 15

    targetSdkVersion 26

    versionCode 1

    versionName "1.0"
  }

  /**
   * buildTypes 块用于配置多种 build type。
   * 编译系统默认会定义两种 build type：debug和release。debug 版本不会显式地显示在默认的编译配置中，但
   * 它包含了调试工具并会使用 debug 密钥进行签名。
   * release 版本会使用混淆设置并且默认没有签名。
	 * （这里指的是默认生成的文件内容，实际中往往会做修改，如为 release 配置签名）
   */

  buildTypes {

    release {
        minifyEnabled true // Enables code shrinking for the release build type.
        proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
    }
  }

  /**
   * productFlavors 块用于配置多种的 product flavors。编译系统默认生成的文件没有创建这部分。
   */

  productFlavors {
    free {
      applicationId 'com.example.myapp.free'
    }

    paid {
      applicationId 'com.example.myapp.paid'
    }
  }

  /**
   * splits 块配置不同的 apk 编译，每一个将只包含所支持的屏幕尺寸或 abi 的源码和资源。
   */

  splits {
    // 设置基于屏幕尺寸的 multiple apk
    density {

      // 是否编译 multiple apk
      enable false

      // 在编译 multiple apk 时排除这些密度
      exclude "ldpi", "tvdpi", "xxxhdpi", "400dpi", "560dpi"
    }
  }
}

/**
 * module 级别依赖
 */

dependencies {
    compile project(":lib")
    compile 'com.android.support:appcompat-v7:26.1.0'
    compile fileTree(dir: 'libs', include: ['*.jar'])
}
```


### Gradle 属性文件

`gradle.properties`
配置工程范围的 Gradle 设置，如 Gradle 进程的最大堆大小。

`local.properties`
为编译系统配置本地环境变量，如 SDK 安装目录。该目录内容一般由 Android Studio 自动生成，所以通常不应该手动修改或者引入版本控制系统（不过因为没必要引入 VCS 中，所以我们可以在这里配置签名信息）。


### Source Sets 源集
Android Studio将每一个 module 的代码和资源归到一个源集中，一个 module 的 `main/` 源集包含了所有 build variant 共用的代码和资源。
我们可以为不同的 build variant 添加额外的源集目录：
+ `src/main/` 
+ `src/buildType/` 
+ `src/productFlavor/`
+ `src/productFlavorBuildType/`

例如，在生成一个「fullDebug」版本应用时，编译系统将从以下目录合并代码、设置、资源
+ `src/fullDebug/`  (build variant 源集)
+ `src/debug/`  (build type 源集)
+ `src/full/`  (product flavor 源集)
+ `src/main/`  (main 源集)

如果不同源集中包含了同一文件的不同版本，Gradle 将采用以下的优先级顺序：
build variant > build type > product flavor > main source set > library dependencies




参考：
[build process](https://developer.android.com/studio/build/index.html#build-process)