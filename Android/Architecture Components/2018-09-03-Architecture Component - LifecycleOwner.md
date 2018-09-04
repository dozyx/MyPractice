

通过 LiveData#observe 方法可以为数据绑定一个生命周期：

```java
public void observe(@NonNull LifecycleOwner owner, @NonNull Observer<T> observer) {
        ...
    }
```

可以看到 LiefcycleOwner 表示的就是一个带有生命周期的对象。

LifecycleOwner 是一个 interface，它仅有一个方法：

```java
public interface LifecycleOwner {
    @NonNull
    Lifecycle getLifecycle();
}
```

所以，只要能提供一个 Lifecycle 实例，这个对象就具有了生命周期。Lifecycle 是一个抽象类：

```java
public abstract class Lifecycle {
    @MainThread
    public abstract void addObserver(@NonNull LifecycleObserver observer);
    
    @MainThread
    public abstract void removeObserver(@NonNull LifecycleObserver observer);

    @MainThread
    @NonNull
    public abstract State getCurrentState();

    @SuppressWarnings("WeakerAccess")
    public enum Event {
        ON_CREATE,
        ON_START,
        ON_RESUME,
        ON_PAUSE,
        ON_STOP,
        ON_DESTROY,
        /**
         * An {@link Event Event} constant that can be used to match all events.
         */
        ON_ANY
    }

    /**
     * Lifecycle states. You can consider the states as the nodes in a graph and
     * {@link Event}s as the edges between these nodes.
     */
    @SuppressWarnings("WeakerAccess")
    public enum State {
        /**
         * Destroyed state for a LifecycleOwner. After this event, this Lifecycle will not dispatch
         * any more events. For instance, for an {@link android.app.Activity}, this state is reached
         * <b>right before</b> Activity's {@link android.app.Activity#onDestroy() onDestroy} call.
         */
        DESTROYED,

        /**
         * Initialized state for a LifecycleOwner. For an {@link android.app.Activity}, this is
         * the state when it is constructed but has not received
         * {@link android.app.Activity#onCreate(android.os.Bundle) onCreate} yet.
         */
        INITIALIZED,

        /**
         * Created state for a LifecycleOwner. For an {@link android.app.Activity}, this state
         * is reached in two cases:
         * <ul>
         *     <li>after {@link android.app.Activity#onCreate(android.os.Bundle) onCreate} call;
         *     <li><b>right before</b> {@link android.app.Activity#onStop() onStop} call.
         * </ul>
         */
        CREATED,

        /**
         * Started state for a LifecycleOwner. For an {@link android.app.Activity}, this state
         * is reached in two cases:
         * <ul>
         *     <li>after {@link android.app.Activity#onStart() onStart} call;
         *     <li><b>right before</b> {@link android.app.Activity#onPause() onPause} call.
         * </ul>
         */
        STARTED,

        /**
         * Resumed state for a LifecycleOwner. For an {@link android.app.Activity}, this state
         * is reached after {@link android.app.Activity#onResume() onResume} is called.
         */
        RESUMED;

        /**
         * Compares if this State is greater or equal to the given {@code state}.
         *
         * @param state State to compare with
         * @return true if this State is greater or equal to the given {@code state}
         */
        public boolean isAtLeast(@NonNull State state) {
            return compareTo(state) >= 0;
        }
    }
}
```

Lifecycle 主要包括了：

+ 三个抽象方法：添加 observer、移除 observer、获取当前生命周期状态
+ 枚举 Event：生命周期事件
+ 枚举 State：生命周期状态

所以，Lifecycle 的主要职责是实现观察者模式、维护生命周期状态、分发生命周期事件。



Lifecycle 的实现类是 LifecycleRegistry，在 arch 库中提供了 4 个 LifecycleOwner 接口的实现类，它们返回的 Lifecycle 实例都是 LifecycleRegistry 类型，这 4 个实现类分别是

+ LifecycleService：Service 的子类

+ ProcessLifecycleOwner：为整个进程提供生命周期

  更确切的说，ProcessLifecycleOwner 表示的是所有 Activity 整体的生命周期，而不是进程的生命周期，不过，`Lifecycle.Event#ON_CREATE` 只会发送一次，并且 `Lifecycle.Event#ON_DESTROY` 永远不会被发送。其他的生命周期事件将按以下规则发送：

  - `Lifecycle.Event#ON_START` 和 `Lifecycle.Event#ON_RESUME` 在第一个 activity 经历这些生命周期时发送
  - `Lifecycle.Event#ON_PAUSE` 和 `Lifecycle.Event#ON_STOP` 在最后一个 activity 经历这些生命周期并经过一定延时后发送。这个延时可以确保 ProcessLifecycleOwner  不会在 activity 配置变更而重建时发送任何事件。

  ProcessLifecycleOwner 适用于某些需要判断 app 前后台的情形。

+ Fragment

+ SupportActivity



## 源码分析

### LifecycleOwner 实现

#### SupportActivity

SupportActivity 的生命周期实现是通过一个名为 ReportFragment 的 Fragment 的生命周期来实现的（感觉这种设计十分巧妙，因为这样就把生命周期相关代码与 Activity 进行了分离）。

ReportFragement 注入：

```java
// ReportFragment.java
public static void injectIfNeededIn(Activity activity) {
        // ProcessLifecycleOwner should always correctly work and some activities may not extend
        // FragmentActivity from support lib, so we use framework fragments for activities
        android.app.FragmentManager manager = activity.getFragmentManager();
        if (manager.findFragmentByTag(REPORT_FRAGMENT_TAG) == null) {
            manager.beginTransaction().add(new ReportFragment(), REPORT_FRAGMENT_TAG).commit();
            // Hopefully, we are the first to make a transaction.
            manager.executePendingTransactions();
        }
    }
```

然后在 ReportFragment 的生命周期方法中分发事件给 Lifecycle

```java
private void dispatch(Lifecycle.Event event) {
        Activity activity = getActivity();
        if (activity instanceof LifecycleRegistryOwner) {
            ((LifecycleRegistryOwner) activity).getLifecycle().handleLifecycleEvent(event);
            return;
        }

        if (activity instanceof LifecycleOwner) {
            Lifecycle lifecycle = ((LifecycleOwner) activity).getLifecycle();
            if (lifecycle instanceof LifecycleRegistry) {
                ((LifecycleRegistry) lifecycle).handleLifecycleEvent(event);
            }
        }
    }
```

> 注：LifecycleRegistryOwner 已被标记为 deprecated



#### ProcessLifecycleOwner

ProcessLifecycleOwner 是一个单例，通过静态方法 `get()` 可以获得它的实例。ProcessLifecycleOwner 中有一个 init(context) 初始化方法：

```java
    static void init(Context context) {
        sInstance.attach(context);
    }
```

这个初始化是通过 ProcessLifecycleOwnerInitializer 类来实现的，ProcessLifecycleOwnerInitializer 是 ContentProvider 的一个子类，它通过 AndroidManifest 来注册的（如果通过 Android Studio 查看合并后的 manifest，可以看到引入了该 provider），然后当应用启动时，onCreate 方法就会被调用。

```java
@RestrictTo(RestrictTo.Scope.LIBRARY_GROUP)
public class ProcessLifecycleOwnerInitializer extends ContentProvider {
    @Override
    public boolean onCreate() {
        LifecycleDispatcher.init(getContext());
        ProcessLifecycleOwner.init(getContext());
        return true;
    }
    ...
}
```

至于 ContentProvider 的其他抽象方法，ProcessLifecycleOwnerInitializer 都只是提供了空的实现。ProcessLifecycleOwnerInitializer 的这种方式避免了手动在 Application 中调用 init()，这种技巧感觉也十分巧妙，只是不知过多的使用 ContentProvider 的话，对程序的影响会不会很大。

再来看 attach(context) 方法：

```java
    void attach(Context context) {
        mHandler = new Handler();
        mRegistry.handleLifecycleEvent(Lifecycle.Event.ON_CREATE);
        Application app = (Application) context.getApplicationContext();
        app.registerActivityLifecycleCallbacks(new EmptyActivityLifecycleCallbacks() {
            @Override
            public void onActivityCreated(Activity activity, Bundle savedInstanceState) {
                ReportFragment.get(activity).setProcessListener(mInitializationListener);
            }

            @Override
            public void onActivityPaused(Activity activity) {
                activityPaused();
            }

            @Override
            public void onActivityStopped(Activity activity) {
                activityStopped();
            }
        });
    }
```

生命周期的处理主要通过 ActivityLifecycleCallbacks 进行处理，首先，通过 ReportFragment 为每个 activity 设置一个 ActivityInitializationListener 来处理 started 和 resumed 事件

```java
private ActivityInitializationListener mInitializationListener =
            new ActivityInitializationListener() {
                @Override
                public void onCreate() {
                }

                @Override
                public void onStart() {
                    activityStarted();
                }

                @Override
                public void onResume() {
                    activityResumed();
                }
            };
```

而 paused 和 stopped 事件仍在 ActivityLifecycleCallbacks 处理。

> ps：这里不是很明白为什么要特意通过 fragment 来处理 started 和 resumed 状态。

当 activity 状态变化时，判断分发生命周期事件

```java
 void activityStarted() {
        mStartedCounter++;
        if (mStartedCounter == 1 && mStopSent) {
            mRegistry.handleLifecycleEvent(Lifecycle.Event.ON_START);
            mStopSent = false;
        }
    }

    void activityResumed() {
        mResumedCounter++;
        if (mResumedCounter == 1) {
            if (mPauseSent) {
                mRegistry.handleLifecycleEvent(Lifecycle.Event.ON_RESUME);
                mPauseSent = false;
            } else {
                mHandler.removeCallbacks(mDelayedPauseRunnable);
            }
        }
    }

    void activityPaused() {
        mResumedCounter--;
        if (mResumedCounter == 0) {
            mHandler.postDelayed(mDelayedPauseRunnable, TIMEOUT_MS);
        }
    }

    void activityStopped() {
        mStartedCounter--;
        dispatchStopIfNeeded();
    }

    private void dispatchPauseIfNeeded() {
        if (mResumedCounter == 0) {
            mPauseSent = true;
            mRegistry.handleLifecycleEvent(Lifecycle.Event.ON_PAUSE);
        }
    }

    private void dispatchStopIfNeeded() {
        if (mStartedCounter == 0 && mPauseSent) {
            mRegistry.handleLifecycleEvent(Lifecycle.Event.ON_STOP);
            mStopSent = true;
        }
    }
```



### Fragment

Fragment 的 LifecycleOwner 实现原理主要就是返回一个 LifecycleRegistry 实例，并将自身的生命周期传递给 LifecycleRegistry。



#### LifecycleService

通过 ServiceLifecycleDispatcher 代理类来处理，





## 疑问

+ 假如 app 中没有全部使用 AppCompatActivity 的话，ProcessLifecycleOwner 是否会正常

