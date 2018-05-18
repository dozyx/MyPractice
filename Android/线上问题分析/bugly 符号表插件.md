使用插件可以实现符号表上传功能。

+ 添加依赖：在项目的 build.gradle 的 dependencies （buildscript 部分）中

  `classpath 'com.tencent.bugly:symtabfileuploader:latest.release'`

+ 添加依赖和配置：在 module 的 build.gradle 中

  ```
  apply plugin: 'bugly'

  bugly {
      appId = '<APP_ID>' // 注册时分配的App ID
      appKey = '<APP_KEY>' // 注册时分配的App Key
  }
  ```

上面的 appId 和 appKey 为必填项，除此之外还有其他可选属性配置，我们也可以为每一个 flavor 配置不同的 id 和 key，具体看参考。



### 插件其他配置属性说明

仅记录自己注意的属性

+ debug：调试模式开关，默认关。开启插件调试模式之后，将打印更详细日志，并在**Debug编译打包**的时候自动执行符号表文件上传任务。



### 注意事项

+ 默认只在**Release编译打包**的时候自动执行符号表文件上传任务，调试模式下**Debug编译打包**也会自动执行符号表文件上传任务；
+ 如果项目使用了代码混淆（Proguard），插件将自动上传Proguard生成的Mapping文件；



参考：

[Bugly符号表插件使用指南](https://bugly.qq.com/docs/utility-tools/plugin-gradle-bugly/?v=20170912151050)