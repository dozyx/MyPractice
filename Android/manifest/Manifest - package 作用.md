- 生成 R.java
- 声明 manifest中的相关类名称，如 <activity android:name=".MainActivity"> 的 Activity 将解析为 com.example.myapp.MainActivity

> 尽管清单 package 和 Gradle applicationId 可以具有不同的名称，但构建工具会在构建结束时将应用 ID 复制到 APK 的最终清单文件中。

