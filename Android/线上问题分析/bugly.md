> 公司项目中使用了 bugly，我自己也看了 bugly 返回的线上问题，不过对返回的堆栈信息的未能完全理解，因此打算汇总一下 bugly 的相关内容。



### 集成

+ 引入库

  Bugly 包括 SDK 和 NDK 两个独立库，分别用于捕获 java crash 和 native crash。使用 gradle 集成：

  ```
  android {
      defaultConfig {
          ndk {
              // 设置支持的SO库架构
              abiFilters 'armeabi' //, 'x86', 'armeabi-v7a', 'x86_64', 'arm64-v8a'
          }
      }
  }

  dependencies {
      compile 'com.tencent.bugly:crashreport:latest.release' //其中latest.release指代最新Bugly SDK版本号，也可以指定明确的版本号，例如2.1.9
      compile 'com.tencent.bugly:nativecrashreport:latest.release' //其中latest.release指代最新Bugly NDK版本号，也可以指定明确的版本号，例如3.0
  }
  ```

  ​

+ 配置

  AndroidManifest.xml 添加权限：

  ```xml
  <uses-permission android:name="android.permission.READ_PHONE_STATE" />
  <uses-permission android:name="android.permission.INTERNET" />
  <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
  <uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />
  <uses-permission android:name="android.permission.READ_LOGS" />
  ```

  Proguard 混淆文件中添加：

  ```
  -dontwarn com.tencent.bugly.**
  -keep public class com.tencent.bugly.**{*;}
  ```

+ 初始化

  在自定义的 Applicantion 类的 onCreate() 中：

  ```java
  CrashReport.initCrashReport(getApplicationContext(), "注册时申请的APPID", false); 
  // 除了在代码中配置 APP 信息，也可以在 AndroidManifest 中配置。
  ```

  第三个参数为 SDK 调试模式开关，调试模式的行为特性如下：

  - 输出详细的Bugly SDK的Log；
  - 每一条Crash都会被立即上报；
  - 自定义日志将会在Logcat中输出。

  建议在测试阶段设置为 true，发布时设置为 false。

+ 测试

  ```java
  CrashReport.testJavaCrash();
  // 执行此代码将触发一次crash
  ```

  ​

### 配置用户策略

```java
UserStrategy strategy = new UserStrategy(appContext);
//...在这里设置strategy的属性，在bugly初始化时传入
//...
CrashReport.initCrashReport(appContext, APPID, true, strategy);
```

+ 设置 App 版本、渠道、包名

  ```java
  strategy.setAppChannel("myChannel");  //设置渠道
  strategy.setAppVersion("1.0.1");      //App的版本
  strategy.setAppPackageName("com.tencent.xx");  //App的包名
  ```

+ 设置Bugly初始化延迟

  ```java
  strategy.setAppReportDelay(20000);   //改为20s (默认在 10s 后联网同步数据)
  ```

+ 设置标签：表明该 crash 所发生的场景，以最后设置的标签为准

  ```java
  CrashReport.setUserSceneTag(context, 9527); // 上报后的Crash会显示该标签
  ```

+ 设置自定义 Map 参数：保存 crash 发生时的一些自定义的环境信息

  ```java
  CrashReport.putUserData(context, "userkey", "uservalue");
  ```

+ 设置开发设备：在开发测试阶段，把调试设备设置为"开发设备"

  ```java
  CrashReport.setIsDevelopmentDevice(context, BuildConfig.DEBUG);
  ```

+ 设置Crash回调：通过用户策略设置一个 CrashHandleCallback，在上报时提供额外的信息。（暂时不太清楚有多大作用，所以简单记录下）

+ Javascript的异常捕获功能

+ 更多的Bugly日志附加信息

  ```java
  // 用户 id
  CrashReport.setUserId("9527");
  // 主动上报开发者 catch 的异常
  try {
      //...
  } catch (Throwable thr) {
      CrashReport.postCatchedException(thr);  // bugly会将这个throwable上报
  }
  // 自定义日志功能，与 Log 类似。BuglyLog 会先将日志缓存在内存中，到达一定阈值再持久化到文件中，
  // 该阈值可通过 BuglyLog.setCache 修改
  BuglyLog.v(tag, log)
  BuglyLog.d(tag, log)
  BuglyLog.i(tag, log)
  BuglyLog.w(tag, log)
  BuglyLog.e(tag, log)
  ```

+ 添加额外的SO文件信息

  + SO文件的版本号
  + 添加SO文件的UUID





### 注意

#### 增加上报进程控制

多进程中初始化 bugly，则每个进程都会上报，为此，可以增加一个上报进程的策略配置：

```java
Context context = getApplicationContext();
// 获取当前包名
String packageName = context.getPackageName();
// 获取当前进程名
String processName = getProcessName(android.os.Process.myPid());
// 设置是否为上报进程
UserStrategy strategy = new UserStrategy(context);
strategy.setUploadProcess(processName == null || processName.equals(packageName));
// 初始化Bugly
CrashReport.initCrashReport(context, "注册时申请的APPID", isDebug, strategy);
// 如果通过“AndroidManifest.xml”来配置APP信息，初始化方法如下
// CrashReport.initCrashReport(context, strategy);

/**
 * 获取进程号对应的进程名
 * 
 * @param pid 进程号
 * @return 进程名
 */
private static String getProcessName(int pid) {
    BufferedReader reader = null;
    try {
        reader = new BufferedReader(new FileReader("/proc/" + pid + "/cmdline"));
        String processName = reader.readLine();
        if (!TextUtils.isEmpty(processName)) {
            processName = processName.trim();
        }
        return processName;
    } catch (Throwable throwable) {
        throwable.printStackTrace();
    } finally {
        try {
            if (reader != null) {
                reader.close();
            }
        } catch (IOException exception) {
            exception.printStackTrace();
        }
    }
    return null;
}
```





#### 提高 App crash 堆栈的可读性

为了使APP Crash堆栈的可读性更高，需要配置符号表文件：

+ 纯Java代码的工程：只需要配置混淆后生成的Mapping文件即可；
+ 含有Native代码的工程：建议配置符号表工具从Debug SO中提取的Symbol符号表文件。

> 为了方便追查问题，建议为每个 release 版本保留一份 mapping

为了更好的定位 crash，可以在混淆中保留源文件名和行号：

```java
-keepattributes SourceFile,LineNumberTable 
```

不过，这样是否存在泄漏源码风险？







参考：

[Duang~ Android堆栈慘遭毁容？精神哥揭露毁容真相！](http://blog.csdn.net/tencent_bugly/article/details/46275685)

[Bugly Android SDK 使用指南](https://bugly.qq.com/docs/user-guide/instruction-manual-android/?v=20170912151050)