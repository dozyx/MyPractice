

### 源码分析

首先查看 `RxActivity` 代码

```java
public abstract class RxActivity extends Activity implements LifecycleProvider<ActivityEvent> {

    private final BehaviorSubject<ActivityEvent> lifecycleSubject = BehaviorSubject.create();

    @Override
    @NonNull
    @CheckResult
    public final Observable<ActivityEvent> lifecycle() {
        return lifecycleSubject.hide();
    }

    @Override
    @NonNull
    @CheckResult
    public final <T> LifecycleTransformer<T> bindUntilEvent(@NonNull ActivityEvent event) {
        return RxLifecycle.bindUntilEvent(lifecycleSubject, event);
    }

    @Override
    @NonNull
    @CheckResult
    public final <T> LifecycleTransformer<T> bindToLifecycle() {
        return RxLifecycleAndroid.bindActivity(lifecycleSubject);
    }
    // 省略了 lifecycleSubject 发送生命周期 event 的代码，如 lifecycleSubject.onNext(...);
}
```

上面 override 的三个方法来自 LifecycleProvider

```java
public interface LifecycleProvider<E> {
    
    @Nonnull
    @CheckReturnValue
    Observable<E> lifecycle();

    @Nonnull
    @CheckReturnValue
    <T> LifecycleTransformer<T> bindUntilEvent(@Nonnull E event);

    @Nonnull
    @CheckReturnValue
    <T> LifecycleTransformer<T> bindToLifecycle();
}
```

从 RxActivity 的实现里可以知道，`Observable<E> lifecycle()` 返回的是一个发送生命周期 event 的 source。



#### bindUntilEvent

首先分析 bindUntilEvent 方法，它调用的是 `RxLifecycle.bindUntilEvent(lifecycleSubject, event)`

```java
public static <T, R> LifecycleTransformer<T> bindUntilEvent(@Nonnull final Observable<R> lifecycle,
                                                            @Nonnull final R event) {
    checkNotNull(lifecycle, "lifecycle == null");
    checkNotNull(event, "event == null");
    return bind(takeUntilEvent(lifecycle, event));
}
```

* `takeUntilEvent(lifecycle, event)`

  ```java
      private static <R> Observable<R> takeUntilEvent(final Observable<R> lifecycle, final R event) {
          return lifecycle.filter(new Predicate<R>() {
              @Override
              public boolean test(R lifecycleEvent) throws Exception {
                  return lifecycleEvent.equals(event);
              }
          });
      }
  ```

  对生命周期 event 进行了过滤，只发送指定的 event。也就是将一开始会把每个生命周期 event 都发送的 lifecycle 变成了只发送单个 event。

* `bind(takeUntilEvent(lifecycle, event))`

  ```java
      public static <T, R> LifecycleTransformer<T> bind(@Nonnull final Observable<R> lifecycle) {
          return new LifecycleTransformer<>(lifecycle);
      }
  ```

  直接返回一个 `LifecycleTransformer`

  ```java
  @ParametersAreNonnullByDefault
  public final class LifecycleTransformer<T> implements ObservableTransformer<T, T>,
                                                        FlowableTransformer<T, T>,
                                                        SingleTransformer<T, T>,
                                                        MaybeTransformer<T, T>,
                                                        CompletableTransformer
  {
      final Observable<?> observable;
  
      LifecycleTransformer(Observable<?> observable) {
          checkNotNull(observable, "observable == null");
          this.observable = observable;
      }
  
      @Override
      public ObservableSource<T> apply(Observable<T> upstream) {
          return upstream.takeUntil(observable);
      }
      ...
      // 省略的代码是其他 apply 实现，都是类似的操作
  }
  ```

  `upstream.takeUntil(observable)` 中，upstream 是一开始上游的 observable，即实际发送数据的 source，使用 `takeUntil` 操作符之后，当 observable 发送 item 时，upstream 将停止发送。

  这样，就实现了只在某个生命周期事件之前才发送数据的功能，比如在 `Activity#onDestory()` 之前。



#### bindToLifecycle

bindToLifecycle 实现里调用的是 `RxLifecycleAndroid.bindActivity(lifecycleSubject)` 方法。

```java
    public static <T> LifecycleTransformer<T> bindActivity(@NonNull final Observable<ActivityEvent> lifecycle) {
        // ACTIVITY_LIFECYCLE 对 Activity 的生命周期一一映射，比如 onCreate 映射到 onDestory
        return bind(lifecycle, ACTIVITY_LIFECYCLE);
    }
```

上面调用的 bind(...) 是 RxLifecycle 里的方法：

```java
    public static <T, R> LifecycleTransformer<T> bind(@Nonnull Observable<R> lifecycle,
                                                      @Nonnull final Function<R, R> correspondingEvents) {
        return bind(takeUntilCorrespondingEvent(lifecycle.share(), correspondingEvents));
    }
    private static <R> Observable<Boolean> takeUntilCorrespondingEvent(final Observable<R> lifecycle,
                                                                       final Function<R, R> correspondingEvents) {
        return Observable.combineLatest(
            lifecycle.take(1).map(correspondingEvents),
            lifecycle.skip(1),
            new BiFunction<R, R, Boolean>() {
                @Override
                public Boolean apply(R bindUntilEvent, R lifecycleEvent) throws Exception {
                    return lifecycleEvent.equals(bindUntilEvent);
                }
            })
            .onErrorReturn(Functions.RESUME_FUNCTION)
            .filter(Functions.SHOULD_COMPLETE);
    }
```

未完待续



#### 总结

创建一个 subject 用来发送生命周期 event，当接收到某个生命周期 event 时，停止上游 source 的发送。





