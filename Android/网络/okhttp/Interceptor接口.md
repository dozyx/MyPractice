对发出的请求以及对应的响应进行监察、修改以及缩短。通常，拦截器用于添加、移除、改变请求或响应的 header。个人理解，interceptor 可以对 “发起请求 - 连接处理 - 响应” 的整个过程就行拦截。

### Interceptors wiki 学习

如下的拦截器用于打印发出的请求以及返回的响应：

```java
class LoggingInterceptor implements Interceptor {
  @Override public Response intercept(Interceptor.Chain chain) throws IOException {
    Request request = chain.request();// request() 方法获取请求对象

    long t1 = System.nanoTime();
    logger.info(String.format("Sending request %s on %s%n%s",
        request.url(), chain.connection(), request.headers()));// connection() 方法用于获取请求执行的连接

    Response response = chain.proceed(request);// proceed(...) 方法进行 http 工作，并产生 response

    long t2 = System.nanoTime();
    logger.info(String.format("Received response for %s in %.1fms%n%s",
        response.request().url(), (t2 - t1) / 1e6d, response.headers()));

    return response;
  }
}
```







源码：

```java
/**
 * Observes, modifies, and potentially short-circuits requests going out and the corresponding
 * responses coming back in. Typically interceptors add, remove, or transform headers on the request
 * or response.
 */
public interface Interceptor {
  Response intercept(Chain chain) throws IOException;

  interface Chain {
    Request request();

    Response proceed(Request request) throws IOException;

    /**
     * Returns the connection the request will be executed on. This is only available in the chains
     * of network interceptors; for application interceptors this is always null.
     */
    @Nullable Connection connection();
  }
}
```





参考：

[Interceptors](https://github.com/square/okhttp/wiki/Interceptors)