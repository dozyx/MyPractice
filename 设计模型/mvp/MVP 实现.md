tips：

+ 为 presenter 添加 attach(View) 和 detach() 方法
+ view 的实现通过 presenter 的构造函数传入，则可以只用一个 onDestroy 来替代 attach 和 detach
+ 对于 fragment 的 view 接口，可以实现 isActived 方法，这样 presenter 可以避免 null 检测，而使用该方法来判断，这样的另一个好处是，不需要添加 detach 或 onDestroy 方法。





参考：

[android-architecture](https://github.com/googlesamples/android-architecture) 