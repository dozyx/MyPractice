疑问：

> 在一个工程中，有两个 module，一个作为 app，另一个是一个 library module，在 library 中声明了一个 service，它的 `Android:process=":remote"`，两个 module 清单的 package 属性是不同的，而且 library 不能有 applicationId，也就是只有 app 才能设置 applicationId（这个不难理解，因为applicationId 本身就是用来标识 app 的）。那么，“:remote” 的完整进程名应该是哪个呢？实际运行结果表明，它的进程名是相对于 app 的 applicationId，也就是说与 library 的 package 属性无关，难道，相对的是启动它的应用的进程名？

答案：

> 相对于程序的主进程。

分析：

> 估计最完美的解释应该在源码中吧，但目前水平限制，也没时间研究，只能间接地进行一些分析。
>
> 冒号表示新的进程是 application 私有的。[If the name assigned to this attribute begins with a colon (':'), a new process, private to the application, is created when it's needed and the service runs in that process. ]
>
> 在网上没找到明确的解释，不过我验证后发现，的确与 package  以及启动它的进程无关，而且从冒号的意思来看，因为它是属于 application 的一个私有进程，所以其名称应该也是相对于 application （即 app 模块）的。
>
> 解释也牵强，但代码验证的结果表明的确如此。以后看了源码再进一步分析吧。
>
> 其实，这个问题可能有点钻牛角尖了。换一个方式看待这个问题，假如 `:remote` 与 application 的主进程无关，那么 library 中其他没有重写 process 的组件的进程名也会是无关的，也就是说整个库的组件都运行在与主进程不同的进程中，这个想想就不可能。。。



参考：    

[service](https://developer.android.com/guide/topics/manifest/service-element.html#proc) 