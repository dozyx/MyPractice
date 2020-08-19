### 使用 quick document 时，长时间处于 “fetching documentation”

[参考](https://stackoverflow.com/questions/23378610/android-studio-quick-documentation-always-fetching-documentation)

Android Studio 默认使用了远程的文档而不是本地，具体修改看参考。



### 代码文件乱码

描述：

* 显示乱码，不止是中文
* 也不是完全的乱码，可以看到一些非本工程的内容

解决：

* 重启电脑之后正常，所以怀疑是访问文件系统出错



### restart 之后，有的项目没有打开，重新 open 也打不开

> 感觉是项目被启动了，但是没有成功打开

删除 `~/.android/cache` 之后，重启正常

以下方法无效：

* Android Studio 里启动 Edit Custom VM options，添加 `-Dide.mac.file.chooser.native=false`
* mac 系统设置里给 Android Sudio 授予完全访问权限

