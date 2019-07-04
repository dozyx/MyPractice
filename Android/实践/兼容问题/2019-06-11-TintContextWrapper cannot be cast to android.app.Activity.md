异常系统版本：Android 4.4

日志：

```shell
Caused by: java.lang.ClassCastException: android.support.v7.widget.TintContextWrapper cannot be cast to android.app.Activity
06-11 19:50:19.404 10308-10308/xxx.debug W/System.err:     at com.bigkoo.pickerview.view.BasePickerView.initViews(BasePickerView.java:84)
06-11 19:50:19.404 10308-10308/xxx.debug W/System.err:     at com.bigkoo.pickerview.view.TimePickerView.initView(TimePickerView.java:39)
06-11 19:50:19.404 10308-10308/xxx.debug W/System.err:     at com.bigkoo.pickerview.view.TimePickerView.<init>(TimePickerView.java:34)
06-11 19:50:19.404 10308-10308/xxx.debug W/System.err:     at com.bigkoo.pickerview.builder.TimePickerBuilder.build(TimePickerBuilder.java:292)
...
```

分析：跟踪代码可以看到 BasePickerView 中将传入的 context 强转为 Activity，而这个传入 context 是在 view 中通过 getContext() 得到的，这个 view 是继承 AppcompatButton 的自定义 View。而 AppCompatButton 的一个构造函数实现为：

```java
public AppCompatButton(Context context, AttributeSet attrs, int defStyleAttr) {
        super(TintContextWrapper.wrap(context), attrs, defStyleAttr);
        ...
    }
```

TintContextWrapper.wrap(context) 方法：

```java
public static Context wrap(@NonNull Context context) {
        if (shouldWrap(context)) {
            synchronized(CACHE_LOCK) {
                ...

                TintContextWrapper wrapper = new TintContextWrapper(context);
                sCache.add(new WeakReference(wrapper));
                return wrapper;
            }
        } else {
            return context;
        }
    }
private static boolean shouldWrap(@NonNull Context context) {
        if (!(context instanceof TintContextWrapper) && !(context.getResources() instanceof TintResources) && !(context.getResources() instanceof VectorEnabledTintResources)) {
            return VERSION.SDK_INT < 21 || VectorEnabledTintResources.shouldBeUsed();
        } else {
            return false;
        }
    }
```

可以看到，在低于 21 的版本，传给 view 的 context 被包装成了 TintContextWrapper，这样就导致强转出现异常。



我本以来 View#getContext() 得到的一定是 Activity 的 context，但这个问题让我意识到了这是一个错误。所以，如果需要确保 context 正确，还是自己维护一个变量并传入比较好。