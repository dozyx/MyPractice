> 前言：想要实现一个悬浮窗用于测试一些功能，因为悬浮窗是在服务中创建启动，所以不需要有 Activity。
1. 在启动 Activity 使用的主题设置属性 "android:windowIsTranslucent" 为 true （也可以直接使用该属性为 true 的主题，如 Theme.Translucent.NoTitleBar）
2. 在启动 Activity 的 onCreate() 方法中启动服务，该 Activity 不需要调用 setContentView()
3. 调用 finish() 将启动 Activity 结束掉

参考：    
[Launch Android application without main Activity and start Service on launching application](https://stackoverflow.com/questions/10909683/launch-android-application-without-main-activity-and-start-service-on-launching)
