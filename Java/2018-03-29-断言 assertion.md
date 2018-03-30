assertion 是一种语句，它允许你测试你关于程序的设想。每个 assertion 包含了一条你确信在 assertion 执行时为 true 的 boolean 表达式，如果不是 true，那么系统将抛出错误。

assertion 是检查和更正 bug 最快速、最有效的方式之一。



#### 格式

assertion 有两种格式：

+ `assert Expression1 ;`
+ `assert Expression1 : Expression2 ;`

Expression1 是一个 boolean 表达式，当它的结果为 false 时，将抛出 AssertionError。Expression2 是一个有返回值的表达式，该值被系统用来作为 AssertionError 的详细信息。

> assertion 在运行时默认是禁用的，此时的 assertion 语句相当于空语句。

（ps：暂时没感觉有什么地方需要使用到断言，特别是 android 里，所以先了解断言的含义算了）

















参考：

[oracle: Programming With Assertions](https://docs.oracle.com/javase/8/docs/technotes/guides/language/assert.html)