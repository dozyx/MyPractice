> 在看源码时注意到了这个方法，在此做下记录，不过没有遇到过实际需要使用该方法的情况，所以也并不是十分理解。

```java
After a FragmentTransaction is committed with FragmentTransaction.commit(), it is scheduled to be executed asynchronously on the process's main thread. If you want to immediately executing any such pending operations, you can call this function (only from the main thread) to do so. Note that all callbacks and other related behavior will be done from within this call, so be careful about where this is called from.

This also forces the start of any postponed Transactions where Fragment.postponeEnterTransition() has been called.
```

在调用 FragmentTransaction.commit() 来提交一个事务时，该事务将在主线程上异步执行，如果需要立即执行，则调用此方法。



参考：

[executePendingTransactions](https://developer.android.com/reference/android/app/FragmentManager#executePendingTransactions%28%29)