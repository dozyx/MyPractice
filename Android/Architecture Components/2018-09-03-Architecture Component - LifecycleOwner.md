

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



Lifecycle 的实现类是 LifecycleRegistry，在 arch 库中提供了 4 个 LifecycleOwner 接口的实现类，它们返回的 Lifecycle 实例都是 LifecycleRegistry 类型，这 4 个实现类分别是

+ LifecycleService：Service 的子类
+ ProcessLifecycleOwner：为整个进程提供生命周期
+ Fragment
+ SupportActivity





