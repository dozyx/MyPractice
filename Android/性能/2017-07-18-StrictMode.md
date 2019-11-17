---
title: StrictMode 严格模式
tags:
  - android
  - 性能
date: 2017-07-18 15:37:22
categories: 笔记
---

[StrictMode](https://developer.android.com/reference/android/os/StrictMode.html)

[Android性能调优利器StrictMode](http://droidyue.com/blog/2015/09/26/android-tuning-tool-strictmode/)

[walk-through-hell-with-android-strictmode](https://medium.com/@elye.project/walk-through-hell-with-android-strictmode-7e8605168032)

java.lang.Object
   ↳	android.os.StrictMode

------

​	StrictMode 是一个开发者工具，用于检测不经意事件并将它们暴露出来。StrictMode 最常用的地方是检测主线程中的**磁盘和网络访问**。

示例：

(**在 Application 、Activity或其他组件的 onCreate() 中启用 StrictMode**)

```java
 public void onCreate() {
     if (DEVELOPER_MODE) {
         StrictMode.setThreadPolicy(new StrictMode.ThreadPolicy.Builder()
                 .detectDiskReads()
                 .detectDiskWrites()
                 .detectNetwork()   // or .detectAll() for all detectable problems
                 .penaltyLog()
                 .build());
         StrictMode.setVmPolicy(new StrictMode.VmPolicy.Builder()
                 .detectLeakedSqlLiteObjects()
                 .detectLeakedClosableObjects()
                 .penaltyLog()
                 .penaltyDeath()
                 .build());
     }
     super.onCreate();
 }
```

​	在某些情况下，从普通的 activity 生命周期中访问磁盘是必须的，StrictMode 只是为了避免不经意的一些操作，并且**不应该在 release 版本中启用**。通过 penaltyXX() 方法可以确定出现违反情况时的反应，如 penaltyLog() 将输出 log。

> ​	StrictMode 不是一种安全机制并且不能确保找出所有的磁盘和网络访问。通过 JNI 调用的磁盘和网络访问也不会触发 StrictMode。



### 可检测问题

​	StrictMode 主要检测两大问题：TreadPolicy (policy：策略)和 VmPolicy。而 ThreadPolicy 检测的具体内容包括：

- 自定义的耗时调用 使用**detectCustomSlowCalls()**开启
- 磁盘读取操作 使用**detectDiskReads()**开启
- 磁盘写入操作 使用**detectDiskWrites()**开启
- 网络操作 使用**detectNetwork()**开启



​	VmPolicy 检测的具体内容：

- Activity泄露 使用**detectActivityLeaks()**开启
- 未关闭的Closable对象泄露 使用**detectLeakedClosableObjects()**开启
- 泄露的Sqlite对象 使用**detectLeakedSqlLiteObjects()**开启
- 检测实例数量 使用**setClassInstanceLimit()**开启





