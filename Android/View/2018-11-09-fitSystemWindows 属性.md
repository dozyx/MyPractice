fitsSystemWindows 用于避免布局被系统级的 UI （如状态栏）遮挡，常用于实现沉浸式布局。

在使用这一属性时，需要谨记以下几点：

+ `fitsSystemWindows` 是深度优先的，第一个 view 会消耗它
+ Inset 通常是与全屏相关的
+ view 的 padding 会被覆盖，即无效











资料：

[Why would I want to fitsSystemWindows?](https://medium.com/androiddevelopers/why-would-i-want-to-fitssystemwindows-4e26d9ce1eec?linkId=19685562)