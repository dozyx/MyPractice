[SDK 下载](http://xg.qq.com/ctr_index/download)

[Android SDK 集成指南](http://docs.developer.qq.com/xg/android_access/jcenter.html)

### 自动集成

app 级 build.gradle 的 defaultConfig 中添加

```groovy
android {
    ......
    defaultConfig {

        //信鸽官网上注册的包名.注意application ID 和当前的应用包名以及 信鸽官网上注册应用的包名必须一致。
        applicationId "你的包名" 
        ......

        ndk {
            //根据需要 自行选择添加的对应cpu类型的.so库。 
            abiFilters 'armeabi', 'armeabi-v7a', 'arm64-v8a' 
            // 还可以添加 'x86', 'x86_64', 'mips', 'mips64'
        }

        manifestPlaceholders = [

            XG_ACCESS_ID:"注册应用的accessid",
            XG_ACCESS_KEY : "注册应用的accesskey",
        ]
        ......
    }
    ......
}

dependencies {
//信鸽jar
compile 'com.tencent.xinge:xinge:3.2.3-release'
//wup包
compile 'com.tencent.wup:wup:1.0.0.E-release'
//mid包
compile 'com.tencent.mid:mid:4.0.6-release'
}
```

> 只要使用了相同的 accessid，不同包名的应用也能收到推送。



### 监听消息

实现 XGBaseReceiver 并在 manifest 中注册

```xml
  <receiver android:name="完整的类名如:com.qq.xgdemo.receiver.MessageReceiver"
      android:exported="true" >
      <intent-filter>
          <!-- 接收消息透传 -->
          <action android:name="com.tencent.android.tpush.action.PUSH_MESSAGE" />
          <!-- 监听注册、反注册、设置/删除标签、通知被点击等处理结果 -->
          <action android:name="com.tencent.android.tpush.action.FEEDBACK" />
      </intent-filter>
  </receiver>
```



### 其他功能

#### 日志

```java
XGPushConfig.enableDebug(this,true);
```



#### token 注册

注册后才能接收推送，并且管理后台也可以向 token 发送单独的消息。

```java
XGPushManager.registerPush(this, new XGIOperateCallback() {
@Override
public void onSuccess(Object data, int flag) {
//token在设备卸载重装的时候有可能会变
Log.d("TPush", "注册成功，设备token为：" + data);
}
@Override
public void onFail(Object data, int errCode, String msg) {
Log.d("TPush", "注册失败，错误码：" + errCode + ",错误信息：" + msg);
}
})
```



#### 设置账号

标识登录的用户，这里的账号指的是 app 自身的账户体系

```java
XGPushManager.bindAccount(getApplicationContext(), "XINGE");
```



#### 设置标签

```java
XGPushManager.setTag(this,"XINGE");
```



### 代码混淆

```
-keep public class * extends android.app.Service
-keep public class * extends android.content.BroadcastReceiver
-keep class com.tencent.android.tpush.** {* ;}
-keep class com.tencent.mid.** {* ;}
-keep class com.qq.taf.jce.** {*;}
```

