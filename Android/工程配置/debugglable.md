Manifest 中的 android:debugglable 表示是否允许调试（即使安装为非开发版的系统），可以通过 ApplicationInfo

的 flags 读取。这个与BuildConfig.debug 是不同的，BuildCongig.debug 判断的是build type 是否为 debug 版本，每个 module 都有自己的 BuildConfig。

在旧版本的 Gradle 中存在一个问题：每个 module 的 BuildConfig 可能不一样。这个问题已经在 Gradle 3.0 中修复。

> 在一些旧的代码中可能会看到使用 debugglable 进行的判断，因此在此做下记录。



参考：

[BuildConfig.DEBUG always false when building library projects with gradle](https://stackoverflow.com/questions/20176284/buildconfig-debug-always-false-when-building-library-projects-with-gradle)