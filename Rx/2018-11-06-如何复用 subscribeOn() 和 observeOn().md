下面是 [Don't break the chain: use RxJava's compose() operator](https://blog.danlew.net/2015/03/02/dont-break-the-chain/) 文中提到的解决方案，但感觉并不是一种完美的解决方案，特别是如果使用的是 Java7。

#### 问题

大量的重复代码：

```java
Observable.from(someSource)
    .map(data -> manipulate(data))
    .subscribeOn(Schedulers.io())
    .observeOn(AndroidSchedulers.mainThread())
    .subscribe(data -> doSomething(data));
```



#### 方案

+ 一种丑陋的方式

  ```java
  <T> Observable<T> applySchedulers(Observable<T> observable) {
      return observable.subscribeOn(Schedulers.io())
          .observeOn(AndroidSchedulers.mainThread());
  }
  ```

  调用

  ```java
  applySchedulers(
      Observable.from(someSource)
          .map(data -> manipulate(data))
      )
      .subscribe(data -> doSomething(data));
  ```

+ 使用 Transformers 方式

  ```java
  <T> Transformer<T, T> applySchedulers() {
      return new Transformer<T, T>() {
          @Override
          public Observable<T> call(Observable<T> observable) {
              return observable.subscribeOn(Schedulers.io())
                  .observeOn(AndroidSchedulers.mainThread());
          }
      };
  }
  // Java8 是这样的
  <T> Transformer<T, T> applySchedulers() {
      return observable -> observable.subscribeOn(Schedulers.io())
          .observeOn(AndroidSchedulers.mainThread());
  }
  ```

  调用

  ```java
  Observable.from(someSource)
      .map(data -> manipulate(data))
      .compose(applySchedulers())
      .subscribe(data -> doSomething(data));
  // 如果是 Java7，需要强转类型，丑陋。。。
  Observable.from(someSource)
      .map(data -> manipulate(data))
      .compose(this.<YourType>applySchedulers())
      .subscribe(data -> doSomething(data));
  ```

  复用 Transformers

  ```java
  final Transformer schedulersTransformer =
      observable -> observable.subscribeOn(Schedulers.io())
          .observeOn(AndroidSchedulers.mainThread());
  
  @SuppressWarnings("unchecked")
  <T> Transformer<T, T> applySchedulers() {
      return (Transformer<T, T>) schedulersTransformer;
  }
  ```
