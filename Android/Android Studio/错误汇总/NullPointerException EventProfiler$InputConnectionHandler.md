在使用 EditText 时突然发生了以下异常：

```
05-03 18:24:44.838 8850-8902/com.XXX.android.XXX E/AndroidRuntime: FATAL EXCEPTION: Thread-4
    Process: com.XXX.android.XXXX, PID: 8850
    java.lang.NullPointerException: Attempt to invoke virtual method 'java.lang.Class java.lang.Object.getClass()' on a null object reference
        at com.android.tools.profiler.support.profilers.EventProfiler$InputConnectionHandler.run(EventProfiler.java:285)
        at java.lang.Thread.run(Thread.java:760)
```

这个问题的出现与开启了 Run Configuration 中 “Enable advanced profilling” 有关，关闭后没有再出现此问题。



参考：

[focus on editText result in crash](https://stackoverflow.com/questions/47440771/focus-on-edittext-result-in-crash)