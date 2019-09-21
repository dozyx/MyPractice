[Android解析ClassLoader（二）Android中的ClassLoader](http://liuwangshu.cn/application/classloader/2-android-classloader.html)



Android 的 ClassLoader 加载的是 dex 文件，Java 是 class 和 jar（本质也是 class 文件）。

系统 ClassLoader：

* BootClassLoader：系统启动时预加载常用类。为 ClassLoader 的内部类，一般的用户程序无法调用。
* DexClassLoader：加载 dex 文件及 dex 的压缩文件（apk 和 jar）。
* PathClassLoader：加载系统类和应用程序的类。