

## 使用

在调用 observe 时，会接收到上一次的数据，即上一次 setValue 的值，即使是 null，如果 observer 前没有值，则不会触发。如，旋转屏幕时，将可能一直触发上一次的数据。如果不希望有这种问题，可以参考 googlesample 的 [SingleLiveEvent](https://github.com/googlesamples/android-architecture/blob/dev-todo-mvvm-live/todoapp/app/src/main/java/com/example/android/architecture/blueprints/todoapp/SingleLiveEvent.java) 类。

SingleLiveEvent 设置了一个标记位，每一次 setValue 时置为 true，然后事件被消耗时置为 false。需要注意的一点是，仅有一个 observer 可以接受到值，因为值被第一个 observer 消耗后，标记位就变成了 false。



### MutableLiveData 与 LiveData 

唯一区别： posValue 和 setValue 两个方法在 MutableLiveData 中是 public 的，而 LiveData 中是 protect 的。



### MediatorLiveData

observe 其他的 LiveData。

示例代码：

```java
LiveData liveData1 = ...;
LiveData liveData2 = ...;

MediatorLiveData liveDataMerger = new MediatorLiveData<>();
liveDataMerger.addSource(liveData1, value -> liveDataMerger.setValue(value));
liveDataMerger.addSource(liveData2, value -> liveDataMerger.setValue(value));
```

MediatorLiveData 会响应任何一个 source 的变化。



## Transformations

LiveData 变换方法。



### switchMap

观察输入的变化，根据输入应用一个 Function，将该输入转换为一个 LiveData。将最后一个输入的返回的 LiveData 的值作为输出。

源码分析：

```java
    @MainThread
    public static <X, Y> LiveData<Y> switchMap(
            @NonNull LiveData<X> source,
            @NonNull final Function<X, LiveData<Y>> switchMapFunction) {
        final MediatorLiveData<Y> result = new MediatorLiveData<>();
        // 观察输入变化
        result.addSource(source, new Observer<X>() {
            LiveData<Y> mSource;

            @Override
            public void onChanged(@Nullable X x) {
                // 输入发生变化，应用 Function 变换得到一个 LiveData
                LiveData<Y> newLiveData = switchMapFunction.apply(x);
                if (mSource == newLiveData) {
                    return;
                }
                if (mSource != null) {
                    // 已经不关心旧的输入产生的数据，所以移除
                    result.removeSource(mSource);
                }
                mSource = newLiveData;
                if (mSource != null) {
                    result.addSource(mSource, new Observer<Y>() {
                        @Override
                        public void onChanged(@Nullable Y y) {
                            // 将数据透传返回，得到最新的输入产生的数据
                            result.setValue(y);
                        }
                    });
                }
            }
        });
        return result;
    }
```







## 分析

### LiveData 是什么

* 持有 data 的类

* 具有生命周期感知
* 在生命周期内，data 的变化能被 observe

注意：一个 liveData 实例可以被多个不同的具有生命周期的 observer 观察。

### 生命周期

LiveData 用来感知生命周期的对象为 `LifecycleOwner` ，该接口只有一个方法来提供一个 `Lifecycle` 对象。`Lifecycle`  源码：

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
        ON_ANY
    }

    @SuppressWarnings("WeakerAccess")
    public enum State {
        DESTROYED,
        INITIALIZED,
        CREATED,
        STARTED,
        RESUMED;
        public boolean isAtLeast(@NonNull State state) {
            return compareTo(state) >= 0;
        }
    }
}
```

`Lifecycle` 主要提供了两种方式来感知生命周期状态：

* addObserver 和 removeObserver，生命周期状态改变时，LifecycleOwner 进行通知
* getCurrentState，主动获取 LifecycleOwner 的生命周期状态

> 注意：addObserver 和 removeObserver 参数里的 LifecycleObserver 是一个 interface，实现该接口的类需要使用 `@OnLifecycleEvent` 注解来声明哪些方法需要接收生命周期变化，被注解的方法最多可以有两个参数，第一个是类型为 LifecycleOwner，第二个类型为 Lifecycle.Event（Lifecycle.Event 有一个值为 ON_ANY，所以注解里的 Event 和参数的 Event 可能不一样）。其实，除了使用注解来声明生命周期回调方法外，还可以使用 LifecycleEventObserver 和 FullLifecycleObserver 两个接口，这两个接口都继承于 LifecycleObserver，但他们声明了具体的回调方法。

对于 LiveData，关注的生命周期只有两种状态：是否 active。

### observe

```java
@MainThread
    public void observe(@NonNull LifecycleOwner owner, @NonNull Observer<? super T> observer) {
        assertMainThread("observe");
        if (owner.getLifecycle().getCurrentState() == DESTROYED) {
            // ignore
            // owner 已销毁，不进行 observe
            return;
        }
        // LifecycleBoundObserver 响应生命周期，并分发数据
        LifecycleBoundObserver wrapper = new LifecycleBoundObserver(owner, observer);
        ObserverWrapper existing = mObservers.putIfAbsent(observer, wrapper);
        // 一个 observer 只能关联到一个 owner，并且只能关联一次
        if (existing != null && !existing.isAttachedTo(owner)) {
            throw new IllegalArgumentException("Cannot add the same observer"
                    + " with different lifecycles");
        }
        if (existing != null) {
            return;
        }
        // 监听 owner 生命周期
        owner.getLifecycle().addObserver(wrapper);
    }
```

LifecycleBoundObserver 主要用于处理于 owner 相关的事物，它实现了 LifecycleEventObserver 接口，并继承 ObserverWrapper，当生命周期的 active 状态改变时，调用 ObserverWrapper#activeStateChanged 方法。

```java
private abstract class ObserverWrapper {
        final Observer<? super T> mObserver;
        boolean mActive;
        int mLastVersion = START_VERSION;

        ObserverWrapper(Observer<? super T> observer) {
            mObserver = observer;
        }

        abstract boolean shouldBeActive();

        boolean isAttachedTo(LifecycleOwner owner) {
            return false;
        }

        void detachObserver() {
        }

        void activeStateChanged(boolean newActive) {
            // active 状态有变化才处理
            if (newActive == mActive) {
                return;
            }
            // immediately set active state, so we'd never dispatch anything to inactive
            // owner
            mActive = newActive;
            // liveData 可能有多个 observer，所以 mActiveCount > 0 表示有 owner 处于 active
            // 而 mActive 表示的是该 observer 对应的 owner 的状态
            boolean wasInactive = LiveData.this.mActiveCount == 0;
            LiveData.this.mActiveCount += mActive ? 1 : -1;
            if (wasInactive && mActive) {
                onActive();
            }
            if (LiveData.this.mActiveCount == 0 && !mActive) {
                onInactive();
            }
            if (mActive) {
                dispatchingValue(this);
            }
        }
    }
```

LiveData#dispatchingValue

```java
    void dispatchingValue(@Nullable ObserverWrapper initiator) {
        if (mDispatchingValue) {
            mDispatchInvalidated = true;
            return;
        }
        mDispatchingValue = true;
        do {
            mDispatchInvalidated = false;
            // 如果 initiator 不为空，则只分发给 initiator。否则分发给所有的 observer
            if (initiator != null) {
                considerNotify(initiator);
                initiator = null;
            } else {
                for (Iterator<Map.Entry<Observer<? super T>, ObserverWrapper>> iterator =
                        mObservers.iteratorWithAdditions(); iterator.hasNext(); ) {
                    considerNotify(iterator.next().getValue());
                    if (mDispatchInvalidated) {
                        break;
                    }
                }
            }
        } while (mDispatchInvalidated);
        mDispatchingValue = false;
    }
    private void considerNotify(ObserverWrapper observer) {
        if (!observer.mActive) {
            return;
        }
        // Check latest state b4 dispatch. Maybe it changed state but we didn't get the event yet.
        //
        // we still first check observer.active to keep it as the entrance for events. So even if
        // the observer moved to an active state, if we've not received that event, we better not
        // notify for a more predictable notification order.
        if (!observer.shouldBeActive()) {
            observer.activeStateChanged(false);
            return;
        }
        // 如果是最新数据则不需要更新
        // mLastVersion 记录的是 observer 的数据版本，mVersion 即使的是 LiveData 的数据版本
        // mLastVersion 和 mVersion 初始值都是 -1，mVersion 在 LiveData#setValue 中增加，所以在第一次调用 LiveData#observe 时，如果 LiveData 有setValue 过，都会触发 observer 的回调，即类似于粘性事件。
        if (observer.mLastVersion >= mVersion) {
            return;
        }
        observer.mLastVersion = mVersion;
        //noinspection unchecked
        observer.mObserver.onChanged((T) mData);
    }
```

### 关于 mLastVersion

上面的分析可以看到，observer 是可以收到注册之前的数据的，如果需要改变这个特性，可以通过反射修改 mLastVersion。参考：[Android消息总线的演进之路：用LiveDataBus替代RxBus、EventBus](https://tech.meituan.com/2018/07/26/android-livedatabus.html)







参考：

[LiveData](https://developer.android.com/topic/libraries/architecture/livedata.html)