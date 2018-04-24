### 选择 jniLib 文件夹

[为何 Twitter 区别于微信、淘宝，只使用了 armeabi-v7a？](https://www.diycode.cc/topics/691)

详看上述链接。摘要：

+ so 加载顺序：

  其下有armeabi-v7a，armeabi ；armeabi-v7a向下兼容armeabi。对于一个cpu是arm64-v8a架构的手机，它运行app时，进入jnilibs去读取库文件时，先看有没有arm64-v8a文件夹，如果没有该文件夹，去找armeabi-v7a文件夹，如果没有，再去找armeabi文件夹，如果连这个文件夹也没有，就抛出异常； 如果有arm64-v8a文件夹，那么就去找特定名称的.so文件。如果有arm64-v8a文件夹，那么就去找特定名称的.so文件，注意：如果没有找到，不会再往下（armeabi-v7a文件夹）找了，而是直接抛出异常。

+ 如果第三方库支持了不同于应用的 abi，会发生 crash，所以最好添加 ndk.abiFilters

  ```
  defaultConfig {  
      ndk {  
          abiFilters "armeabi"// 指定ndk需要兼容的ABI(这样其他依赖包里x86,armeabi,arm-v8之类的so会被过滤掉) 
      }  
  }  
  ```

+ 如果希望 apk 体积小一些，可以只保留 armeabi 或 armeabi-v7a 文件夹。可以动态检查系统环境，加载其他架构的 so 库。