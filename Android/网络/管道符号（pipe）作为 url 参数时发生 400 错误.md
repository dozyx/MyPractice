> 在使用 Retrofit 时出现一个 400 错误，而且蛋疼的是 “iOS 没问题，android 有问题”，经过查找发现是 @Query 的参数中有一个 | 符号，而 Retrofit 说是 okhttp 的问题。。。okhttp 在对参数中的 | 不会重新进行编码，然后就发生了 400 错误，我也不知道 web 那端发生了什么鬼。

如果服务端不肯修改，那就只能 app 改咯。

retrofit 开发者提供的一个解决方案就是增加一个 Interceptor，将 URL 作为 URI 返回，因为 URI 的规则更为严格，它将把 | 转为 %7c，这样就能使请求成功。

```java
Interceptor interceptor = new Interceptor() {
      @Override public Response intercept(Chain chain) throws IOException {
        Request request = chain.request();
        request.newBuilder()
            .url(request.url().uri().toString())
            .build();
        return chain.proceed(chain.request());
      }
    };
```

感觉好狗血。。。







参考：

[Query parameters with pipes (\|) result in invalid calls](https://github.com/square/okhttp/issues/3393)

[url 转码规则](https://docs.google.com/spreadsheets/d/1BgGAhJ5WE3JBsATeudamiBzxmgEhwkfcFqQmPx8qrkc/edit#gid=0)