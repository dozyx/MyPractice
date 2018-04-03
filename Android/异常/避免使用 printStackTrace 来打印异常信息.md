printStackTrace() 会将 stack trace 打印到标准的错误流中，我们应该使用 framework 的打印系统，如 Log，可以更加方便灵活的查看打印（可以添加 tag 和 level）。如果希望使用 Log 打印 stack trace，可以调用 Log.e(String tag, String msg, Throwable tr) 方法。



附一个 printStackTrace 的打印：

```shell
03-11 23:42:26.796 30077-30077/? W/System.err: java.lang.NullPointerException: Attempt to invoke virtual method 'void android.app.Dialog.show()' on a null object reference
03-11 23:42:26.797 30077-30077/? W/System.err:     at com.zerofate.template.justfortest.HelloActivity.onBtnHello(HelloActivity.java:58)
03-11 23:42:26.797 30077-30077/? W/System.err:     at com.zerofate.template.justfortest.HelloActivity_ViewBinding$1.doClick(HelloActivity_ViewBinding.java:37)
03-11 23:42:26.797 30077-30077/? W/System.err:     at butterknife.internal.DebouncingOnClickListener.onClick(DebouncingOnClickListener.java:22)
03-11 23:42:26.797 30077-30077/? W/System.err:     at android.view.View.performClick(View.java:6256)
03-11 23:42:26.797 30077-30077/? W/System.err:     at android.view.View$PerformClick.run(View.java:24697)
03-11 23:42:26.797 30077-30077/? W/System.err:     at android.os.Handler.handleCallback(Handler.java:789)
03-11 23:42:26.797 30077-30077/? W/System.err:     at android.os.Handler.dispatchMessage(Handler.java:98)
03-11 23:42:26.797 30077-30077/? W/System.err:     at android.os.Looper.loop(Looper.java:164)
03-11 23:42:26.797 30077-30077/? W/System.err:     at android.app.ActivityThread.main(ActivityThread.java:6541)
03-11 23:42:26.797 30077-30077/? W/System.err:     at java.lang.reflect.Method.invoke(Native Method)
03-11 23:42:26.797 30077-30077/? W/System.err:     at com.android.internal.os.Zygote$MethodAndArgsCaller.run(Zygote.java:240)
03-11 23:42:26.797 30077-30077/? W/System.err:     at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:767)
```









参考：

[Why is exception.printStackTrace() considered bad practice?](https://stackoverflow.com/questions/7469316/why-is-exception-printstacktrace-considered-bad-practice)

[Is it a bad idea to use printStackTrace() in Android Exceptions?](https://stackoverflow.com/questions/3855187/is-it-a-bad-idea-to-use-printstacktrace-in-android-exceptions)