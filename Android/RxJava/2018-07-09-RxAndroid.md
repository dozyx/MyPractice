RxAndroid 并不是 RxJava 的替代，它只是 RxJava 的一个补充，使其更适用于 Android。

> RxAndroid 源码只有几个很简单的类。。。

引入：

```
implementation 'io.reactivex.rxjava2:rxandroid:2.0.2'
// Because RxAndroid releases are few and far between, it is recommended you also
// explicitly depend on RxJava's latest version for bug fixes and new features.
// (see https://github.com/ReactiveX/RxJava/releases for latest 2.x.x version)
implementation 'io.reactivex.rxjava2:rxjava:2.x.x'
```

 用法：

+ 在主线程进行 observe

  ```java
  Observable.just("one", "two", "three", "four", "five")
          .subscribeOn(Schedulers.newThread())
          .observeOn(AndroidSchedulers.mainThread())
          .subscribe(/* an Observer */);
  ```

+ 在任意 looper 上 observe

  ```java
  Looper backgroundLooper = // ...
  Observable.just("one", "two", "three", "four", "five")
          .observeOn(AndroidSchedulers.from(backgroundLooper))
          .subscribe(/* an Observer */)
  ```

  





参考：

[RxAndroid](https://github.com/ReactiveX/RxAndroid)











