SharedPreferences 的使用随处可见，我们通过 context 的 getSharedPreferences  来得到一个 SharedPreferences 实例，然后就可以使用该实例进行数据读写。随着使用的地方越来越多，每一次都通过各自的 Context 来获取 SharedPreferences 实例，这样冗余代码越来越多。那么，如果我直接在 Applicantion 中初始化一个 SharedPreference 实例，然后其余地方均使用此实例可不可行呢？

事实上，仅通过 Applicantion 的 context 来获取 SharedPreferences 实例是没有问题的，因为在同一进程中 SharedPreferences 实例以单例的形式存在，每个实例都会保存在一个 static 的 map 中，而每个文件名对应一个实例。











参考：

[SharedPreferences application context vs activity context](https://stackoverflow.com/questions/11567134/sharedpreferences-application-context-vs-activity-context)