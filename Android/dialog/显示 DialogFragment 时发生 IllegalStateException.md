todo：

- [ ] IllegalStateException 发生源码分析
- [ ] commit 和 commitAllowingStateLoss 区别分析



在调用 DialogFragment#show 时，发生异常：java.lang.IllegalStateException: Can not perform this action after onSaveInstanceState。原因是在 onSaveInstanceState 状态，不能进行 Fragment 的 commit 操作。比如，有一个延迟显示的 DialogFragment，如果在显示之前，我们点击最近任务，那么它的宿主 Fragment 将进入 onSaveInstanceState，这时延时时间结束显示 DialogFragment 将发生异常。如下面的代码在点击按钮后，进入最近任务，过一会将发生异常：

```
@OnClick(R.id.btn_hello)
    void onBtnHello() {
        btnHello.postDelayed(new Runnable() {
            @Override
            public void run() {
                IllegalStateExceptionTestDialogFragment.newInstance().show(getFragmentManager(),
                        "dailog");
            }
        }, 3000);
    }
```

DialogFragment#show 源码：

```java
public void show(FragmentManager manager, String tag) {
        mDismissed = false;
        mShownByMe = true;
        FragmentTransaction ft = manager.beginTransaction();
        ft.add(this, tag);
        ft.commit();
    }
```

可以看到，show 方法是采用了 commit 方法。

如果我们想要规避该异常，可以采用 commitAllowingStateLoss 方法，不过该方法将可能导致状态丢失（具体差别也还不是很清楚）。



参考：

[commitAllowingStateLoss on DialogFragment](https://stackoverflow.com/questions/30424319/commitallowingstateloss-on-dialogfragment)

[FragmentTransaction的commit和commitAllowingStateLoss的区别](http://blog.csdn.net/stoppig/article/details/31776607)

