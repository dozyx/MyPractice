一个很奇怪的问题，Android Studio 运行程序，提示安装成功，却无法启动应用，提示 activity 不存在，launcher 也没有该应用图标。

最后，通过命令行 `adb uninstall <package> ` 卸载后重新运行解决。



参考：

[Error type 3 Error: Activity class {} does not exist](https://stackoverflow.com/questions/20915266/error-type-3-error-activity-class-does-not-exist)