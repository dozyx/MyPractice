

+ [commit](https://developer.android.com/reference/android/app/FragmentTransaction#commit%28%29)

+ [commitAllowingStateLoss](https://developer.android.com/reference/android/app/FragmentTransaction#commitAllowingStateLoss%28%29)
+ [commitNow](https://developer.android.com/reference/android/app/FragmentTransaction#commitNow%28%29)
+ [commitNowAllowingStateLoss](https://developer.android.com/reference/android/app/FragmentTransaction.html#commitNowAllowingStateLoss%28%29)
+ [FragmentManager#executePendingTransactions](https://developer.android.com/reference/android/app/FragmentManager#executePendingTransactions%28%29)



### commit() vs commitAllowingStateLoss()

如果在 `Activity#onSaveInstanceState()` 后调用 `commit()`，有可能会发生下面的异常：

```java
java.lang.IllegalStateException: Can not perform this action after onSaveInstanceState
    at android.support.v4.app.FragmentManagerImpl.checkStateLoss(FragmentManager.java:1341)
    at android.support.v4.app.FragmentManagerImpl.enqueueAction(FragmentManager.java:1352)
    at android.support.v4.app.BackStackRecord.commitInternal(BackStackRecord.java:595)
    at android.support.v4.app.BackStackRecord.commit(BackStackRecord.java:574)
```

这是因为 commit() 会检查 state 是否已保存，是的话将直接抛出异常。如果想要在这种情况下避免该异常，可以使用 commitAllowingStateLoss()，但可能出现状态丢失的情况。

例子：

(出自[Fragment Transactions & Activity State Loss](https://www.androiddesignpatterns.com/2013/08/fragment-transaction-commit-state-loss.html))

1. Activity 在前台，显示的是 FragmentA
2. Activity 进入后台（调用了 onStop()和onSaveInstanceState()）
3. 调用 commitAllowingStateLoss()，将 FragmentA 替换为 FragmentB

当用户重新返回该 App 时，可能发生：

+ 如果系统在后台回收杀死了该 App，系统将重建 App，并恢复到第 2 步的状态，FragmentB 不会显示
+ 如果系统没有杀死该 App，App 将回到前台，FragmentB 会被显示，然后下一次 Actvitiy 进入 stop 时，包括 FragmentB 的状态也会被保存。

**选择 commit() 还是 commitAllowingStateLoss() 取决于你 commit 的内容以及丢失该 commit 是否可接受。**



### commit(), commitNow(), and executePendingTransactions()

commit() 后，提交的 transaction 并不是立即执行的，而是在主线程下一次空闲时执行，如果希望立即执行，旧的开发方式是在 commit() 后使用 executePendingTransactions()，而在 support24.0.0 之后，commitNow() 是更好的选择。因为 commitNow() 只会同步执行当前的 transactions，而 executePendingTransactions() 会执行所有已经 commited 并且处于等待中的 transactions（也就是有多次的 commit）。

但有一个需要注意的地方是，**不能对添加到 back stack 的 transaction 使用  commitNow()**。因为这样可能导致 back stack 混乱，想象一下，先调用了 commit() 把 transaction1 加到 back stack，在用 commitNow() 添加 transaction2 到 back stack。



**如何选择**：

+ 需要同步并且不需要 back stack，使用 commitNow()。一般，只要不是添加到 back stack 的 transaction，都可以使用 commitNow()
+ 如果需要执行多个 transations，并且不需要同步或者需要添加到 back stack，应使用 commit()
+ 如果需要确保一系列的 transation 在某个时刻发生，则使用 executePendingTransactions()



### 避免 IllegalStateException

+ 在 Activity 的生命周期内提交 transaction 要十分注意。`onCreate()` 是安全的，但其他生命周期方法如 `onActivityResult()`, `onStart()`, 和 `onResume()`，可能出出现问题。比如，不应该在 `FragmentActivity#onResume()` 里 commit transaction，因为此时 Activity 的 state 可能还没有恢复。如果需要在 `onCreate()` 外进行 commit，可以在 `FragmentActivity#onResumeFragments()` 或者`Activity#onPostResume()` 中处理，这两个方法可以确保 Activity 已经还原到原始的 state。
+ 避免在异步的回调方法中执行 transaction。如果真的要这样做的话，考虑使用 `commitAllowingStateLoss()`。
+ 使用 `commitAllowingStateLoss()` 是最后的手段。







资料：

[Fragment Transactions & Activity State Loss](https://www.androiddesignpatterns.com/2013/08/fragment-transaction-commit-state-loss.html)

[The many flavors of commit()](https://medium.com/@bherbst/the-many-flavors-of-commit-186608a015b1)