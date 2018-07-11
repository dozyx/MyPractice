+ 引入

  `implementation 'com.squareup.retrofit2:adapter-rxjava2:latest.version'`

+ 配置 Retrofit

  ```java
  Retrofit retrofit = new Retrofit.Builder()
      .baseUrl("https://example.com/")
      .addCallAdapterFactory(RxJava2CallAdapterFactory.create())
      .build();
  ```

+ service 方法使用 RxJava2 中的类型作为返回类型

  ```java
  interface MyService {
    @GET("/user")
    Observable<User> getUser();
  }
  ```



service 方法支持的返回类型有：

- `Observable<T>`, `Observable<Response<T>>`, and `Observable<Result<T>>` where `T` is the body type.
- `Flowable<T>`, `Flowable<Response<T>>` and `Flowable<Result<T>>` where `T` is the body type.
- `Single<T>`, `Single<Response<T>>`, and `Single<Result<T>>` where `T` is the body type.
- `Maybe<T>`, `Maybe<Response<T>>`, and `Maybe<Result<T>>` where `T` is the body type.
- `Completable` where response bodies are discarded.



所有的响应类型默认都是同步执行它们的请求，存在多种方式来控制请求发生的线程：

+ 对响应类型调用 subscribeOn 来设置 Scheduler 
+ 在创建一个使用 OkHttp 内部线程池的 factory 时，使用 createAsync() 
+ 使用 createWithScheduler(Scheduler)  来提供一个默认的订阅 Scheduler 



参考：

[retrofit-adapters](https://github.com/square/retrofit/tree/master/retrofit-adapters/rxjava2)