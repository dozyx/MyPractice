---
title: 网络开源库使用-volley、okhttp、retrofit
tags:
  - android
  - 网络
date: 2017-08-28 16:04:38
categories: 开源
---



> HTTP 客户端的工作就是接收一个 request，然后得到它的 response。

## Volley

[Github 地址](https://github.com/google/volley)

Volley 是 Google 官方的一个网络库，它具有了以下优点：

+ 自动调度网络请求
+ 多并发网络连接
+ 使用标准 HTTP [cache coherence](http://en.wikipedia.org/wiki/Cache_coherence) （缓存一致性）的透明磁盘和内存响应缓存
+ 支持请求优先级
+ 有取消请求 API
+ 易于定制，如实现重试和回退
+ 强排序，使网络异步获取的数据可以很轻易的转移到 UI 中
+ 提供调试和跟踪工具

> 需要注意，Volley 不适合大型下载或者流操作，因为 Volley 会在解析过程中将所有的响应保留在内存中。

将 Volley 导入项目最简单的方式是使用 gradle：

```groovy
dependencies {
    ...
    compile 'com.android.volley:volley:1.0.0'
}
```



### Google Traning

#### 发送简单请求

通常，我们通过创建一个 RequestQueue 并传入多个 Request 对象来使用 Volley。使用Volley，需要具有 `android.permission.INTERNET ` 权限。



##### 使用 newRequestQueue

Volley 提供了 Volley.newRequestQueue 来设置一个使用默认值的 RequestQueue。

```java
final TextView mTextView = (TextView) findViewById(R.id.text);
...

// Instantiate the RequestQueue.
RequestQueue queue = Volley.newRequestQueue(this);
String url ="http://www.google.com";

// Request a string response from the provided URL.
StringRequest stringRequest = new StringRequest(Request.Method.GET, url,
            new Response.Listener<String>() {
    @Override
    public void onResponse(String response) {
        // Display the first 500 characters of the response string.
        mTextView.setText("Response is: "+ response.substring(0,500));
    }
}, new Response.ErrorListener() {
    @Override
    public void onErrorResponse(VolleyError error) {
        mTextView.setText("That didn't work!");
    }
});
// Add the request to the RequestQueue.
queue.add(stringRequest);
```



##### 发送 Request

发送一个请求，只需要构建一个 Request 并通过 RequestQueue 的 add() 方法添加即可。添加后，该请求将被通过管道移动，并得到服务，然后获取它的原始响应解析和传递。

一个请求的生命周期如下（蓝色表示主线程，绿色表示缓存线程，黄色表示网络线程）：

![volley-request](../../OneDrive/markdown/photo/volley-request.png)

##### 取消 Request

通过调用 Request 对象的 cancel() 方法即可取消请求，一旦请求，已设置的响应处理器将不会被调用。我们也可以为每一个请求关联一个标签对象，然后利用这个标签来取消一片的请求。

如：

1. 定义一个 tag，并加到请求中

   ```java
   public static final String TAG = "MyTag";
   StringRequest stringRequest; // Assume this exists.
   RequestQueue mRequestQueue;  // Assume this exists.

   // Set the tag on the request.
   stringRequest.setTag(TAG);

   // Add the request to the RequestQueue.
   mRequestQueue.add(stringRequest);
   ```

2. 在 Activity 的 onStop() 方法中取消带有该 tag 的请求

   ```java
   @Override
   protected void onStop () {
       super.onStop();
       if (mRequestQueue != null) {
           mRequestQueue.cancelAll(TAG);
       }
   }
   ```




### 配置 RequestQueue

#### 配置网络和缓存

在 Volley 的 toolbox 中，有 RequestQueue 网络和缓存的标准实现：DiskBasedCache 提供了一个 one-file-per-response 的索引；BasicNetwork 提供了基于偏好的 HTTP 客户端的网络传输。

BasicNetwork 必须使用我们 app 连接网络的 HTTP 客户端进行初始化，通常使用的是一个 `HttpURLConnection`（即 HurlStack）。

以下代码展示了配置一个 RequestQueue 的步骤：

```java
RequestQueue mRequestQueue;

// Instantiate the cache
Cache cache = new DiskBasedCache(getCacheDir(), 1024 * 1024); // 1MB cap

// Set up the network to use HttpURLConnection as the HTTP client.
Network network = new BasicNetwork(new HurlStack());

// Instantiate the RequestQueue with the cache and network.
mRequestQueue = new RequestQueue(cache, network);

// Start the queue
mRequestQueue.start();

String url ="http://www.example.com";

// Formulate the request and handle the response.
StringRequest stringRequest = new StringRequest(Request.Method.GET, url,
        new Response.Listener<String>() {
    @Override
    public void onResponse(String response) {
        // Do something with the response
    }
},
    new Response.ErrorListener() {
        @Override
        public void onErrorResponse(VolleyError error) {
            // Handle error
    }
});

// Add the request to the RequestQueue.
mRequestQueue.add(stringRequest);

// ...
```

如果只是需要进行一次请求并且不希望保留它的线程池，那么可以在需要的时候创建，并在返回响应或失败后调用 RequestQueue 的 stop() 。不过，更常用的做法是创建一个单例的 RequestQueue 以保证它在整个生命周期中存活。



#### 使用单例模式

推荐做法是实现一个封装 RequestQueue 和其它 Volley 功能的单例类。另一种方法是子类化 Application，并在 Application.onCreate() 中配置 RequestQueue，但不提倡这种方式。

一个关键的地方在于，RequestQueue 必须使用 Application 的 context 来实例化，而不是 Activity 的 context。

如：

```java
public class MySingleton {
    private static MySingleton mInstance;
    private RequestQueue mRequestQueue;
    private ImageLoader mImageLoader;
    private static Context mCtx;

    private MySingleton(Context context) {
        mCtx = context;
        mRequestQueue = getRequestQueue();

        mImageLoader = new ImageLoader(mRequestQueue,
                new ImageLoader.ImageCache() {
            private final LruCache<String, Bitmap>
                    cache = new LruCache<String, Bitmap>(20);

            @Override
            public Bitmap getBitmap(String url) {
                return cache.get(url);
            }

            @Override
            public void putBitmap(String url, Bitmap bitmap) {
                cache.put(url, bitmap);
            }
        });
    }

    public static synchronized MySingleton getInstance(Context context) {
        if (mInstance == null) {
            mInstance = new MySingleton(context);
        }
        return mInstance;
    }

    public RequestQueue getRequestQueue() {
        if (mRequestQueue == null) {
            // getApplicationContext() is key, it keeps you from leaking the
            // Activity or BroadcastReceiver if someone passes one in.
            mRequestQueue = Volley.newRequestQueue(mCtx.getApplicationContext());
        }
        return mRequestQueue;
    }

    public <T> void addToRequestQueue(Request<T> req) {
        getRequestQueue().add(req);
    }

    public ImageLoader getImageLoader() {
        return mImageLoader;
    }
}
```



### 制作一个标准的 Request

Volley 支持的常见的请求类型有：

+ StringRequest：指定一个 URL，然后在响应时获得一个原生字符串。
+ JsonObjectRequest 和 JsonArrayRequest：指定一个URL，然后在响应时获得一个 JSON 对象或数组。



#### 请求 JSON

JsonObjectRequest 和 JsonArrayRequest 的基类均为 JsonRequest。

示例：

```java
TextView mTxtDisplay;
ImageView mImageView;
mTxtDisplay = (TextView) findViewById(R.id.txtDisplay);
String url = "http://my-json-feed";

JsonObjectRequest jsObjRequest = new JsonObjectRequest
        (Request.Method.GET, url, null, new Response.Listener<JSONObject>() {

    @Override
    public void onResponse(JSONObject response) {
        mTxtDisplay.setText("Response: " + response.toString());
    }
}, new Response.ErrorListener() {

    @Override
    public void onErrorResponse(VolleyError error) {
        // TODO Auto-generated method stub

    }
});

// Access the RequestQueue through your singleton class.
MySingleton.getInstance(this).addToRequestQueue(jsObjRequest);
```



### 实现一个自定义的 Request

Volley 中已经实现了 string、image 和 JSON 的请求。

#### 编写一个自定义的 Request

实现一个自定义的请求，需要：

+ 继承 Request\<T> 类，\<T> 表示的是请求所希望得到的被解析响应的类型。比如，响应被解析后是一个字符串，那么在创建自定义请求时需要继承 Request\<String>。
+ 实现抽象方法 parseNetworkResponse() 和 deliverResponse()。



##### parseNetworkResponse

`Response` 为指定类型（如 string、image 或 JSON）封装了用于传递的已被解析的响应。

如：

```java
@Override
protected Response<T> parseNetworkResponse(
        NetworkResponse response) {
    try {
        String json = new String(response.data,
        HttpHeaderParser.parseCharset(response.headers));
    return Response.success(gson.fromJson(json, clazz),
    HttpHeaderParser.parseCacheHeaders(response));
    }
    // handle errors
...
}
```

需要注意：

+ parseNetworkResponse() 以一个 NetworkResponse 作为参数，它包含了响应的有效载荷（如 byte[]、HTTP 状态码、响应头）。
+ 响应必须返回一个 Response\<T>，它包含了响应类型对象和缓存元数据或者 error。

如果协议中没有标准缓存规定，那么可以自行创建一个 Cache.Entry，但大部分会类似于下面的格式：

```java
return Response.success(myDecodedObject,
        HttpHeaderParser.parseCacheHeaders(response));
```



##### deliverResponse

Volley 将 parseNetworkResponse() 中返回的对象回传到主线程中，大部分请求会在此处调用一个回调接口，如：

```java
protected void deliverResponse(T response) {
        listener.onResponse(response);
```



#### 例子：GsonRequest

使用 Gson 解析的完整实现：

T 表示的是 Gson 反射后得到的类。

```java
public class GsonRequest<T> extends Request<T> {
    private final Gson gson = new Gson();
    private final Class<T> clazz;
    private final Map<String, String> headers;
    private final Listener<T> listener;

    /**
     * Make a GET request and return a parsed object from JSON.
     *
     * @param url URL of the request to make
     * @param clazz Relevant class object, for Gson's reflection
     * @param headers Map of request headers
     */
    public GsonRequest(String url, Class<T> clazz, Map<String, String> headers,
            Listener<T> listener, ErrorListener errorListener) {
        super(Method.GET, url, errorListener);
        this.clazz = clazz;
        this.headers = headers;
        this.listener = listener;
    }

    @Override
    public Map<String, String> getHeaders() throws AuthFailureError {
        return headers != null ? headers : super.getHeaders();
    }

    @Override
    protected void deliverResponse(T response) {
        listener.onResponse(response);
    }

    @Override
    protected Response<T> parseNetworkResponse(NetworkResponse response) {
        try {
            String json = new String(
                    response.data,
                    HttpHeaderParser.parseCharset(response.headers));
            return Response.success(
                    gson.fromJson(json, clazz),
                    HttpHeaderParser.parseCacheHeaders(response));
        } catch (UnsupportedEncodingException e) {
            return Response.error(new ParseError(e));
        } catch (JsonSyntaxException e) {
            return Response.error(new ParseError(e));
        }
    }
}
```



## OkHttp

[okhttp](http://square.github.io/okhttp/)

[github](https://github.com/square/okhttp)

[wiki](https://github.com/square/okhttp/wiki)

### 引入项目

OkHttp 是用于 Android 和 Java 程序的一个 HTTP 和 HTTP/2 客户端，可以直接通过 gradle 引入项目中。

```groovy
compile 'com.squareup.okhttp3:okhttp:3.8.1'
```

与 OkHttp 耦合的 MockWebServer 对于 HTTP/2 的正确测试至关重要，这样代码才能被共享。（不是很理解）

使用 gradle 引入 MockWebServer ：

```groovy
testCompile 'com.squareup.okhttp3:mockwebserver:3.8.1'
```

需要注意，在混淆时可能需要添加以下选项：

```shell
-dontwarn okio.**
-dontwarn javax.annotation.Nullable
-dontwarn javax.annotation.ParametersAreNonnullByDefault
```



### 简单示例

+ GET 

  ```java
  OkHttpClient client = new OkHttpClient();

  String run(String url) throws IOException {
    Request request = new Request.Builder()
        .url(url)
        .build();

    Response response = client.newCall(request).execute();
    return response.body().string();
  }
  ```

+ POST 

  ```java
  public static final MediaType JSON
      = MediaType.parse("application/json; charset=utf-8");

  OkHttpClient client = new OkHttpClient();

  String post(String url, String json) throws IOException {
    RequestBody body = RequestBody.create(JSON, json);
    Request request = new Request.Builder()
        .url(url)
        .post(body)
        .build();
    Response response = client.newCall(request).execute();
    return response.body().string();
  }
  ```


### 详细说明(wiki)

#### Calls

> Call 拨号？

**Request**

每一个 HTTP 请求都会包含

+ 一个 URL 
+ 一个方法（如 GET、POST）
+ 一系列的 header

请求还可能包含一个 body：特定类型的数据流。

**Response**

响应用一个 code （如200表示成功或者404表示没找到）、多个 header以及可选的 body 来对请求做出应答。



##### 重写请求

当你向 OkHttp 提供 HTTP 请求时，将在高级别描述该请求，就像是『使用这些 header 来 fetch 这个 URL』。为了正确和效率，OkHttp 将在传输之前对你的请求进行重写。

OkHttp 可能会添加原始请求中缺少的 header，包括 `Content-Length`、 `Transfer-Encoding`、 `User-Agent`、 `Host`、 `Connection`、  `Content-Type` 。它将为透明响应压缩添加一个 `Accept-Encoding`，除非该 header 已存在。如果有 cookies，OkHttp 还会添加一个 `Cookie` 的header。

有些请求会有一个缓存的响应，当该缓存不是最新的时候，OkHttp 将进行一次有条件的 GET 来下载一个比缓存更新的响应。



##### 重写响应

如果使用了透明压缩，OkHttp 将舍弃相应的响应头 `Content-Encoding` 和 `Content-Length`，因为它们不会用于解压响应 body。

如果一个有条件的 GET 成功了，那么来自网络和缓存的响应将按规范合并。



##### 跟进（Follow-up）请求

当你的请求 URL 已经被移动，web 服务器将返回一个响应码如 302 来指示文档的新 URL，OkHttp 将进行重定向来获得最终的响应。

如果响应发起授权认证，OkHttp 将询问 `Authenticator` （如果已配置）来满足认证；如果authenticator 提供了提供了凭证，那么请求将使用该凭证进行重试。



##### 请求重试

有时候连接会失败，如池连接过时并断开连接 或者 web 服务器本身无法被访问，OkHttp 将使用不同的路由（如果有）进行请求的重试。



##### Calls

通过重写、重定向、跟进和重试，一个简单地请求可能产生大量的请求和响应。OkHttp使用 `Call` 来建立满足你的请求的任务，但这需要经过许多必要的中间请求和响应。通常这不会很多。。。（无力）

Call 可以以两种方式来执行：

+ 同步
+ 异步

Call 可以从任意线程进行取消。



##### 调度（dispatch）

对于同步调用，你需要携带自己的线程并负责管理请求的并发数量（不是很懂，指的是多个请求还是多个连接？）。太多的并发连接将浪费资源，太少的话将对延迟产生危害。

> 可能解释得有问题，保留原文：
>
> For synchronous calls, you bring your own thread and are responsible for managing how many simultaneous requests you make. Too many simultaneous connections wastes resources; too few harms latency.

对于异步调用， `Dispatcher` 实现了最大并发请求数量的策略，你可以设置每个 web 服务器（默认为 5）和整体（默认为 64）的最大值。





## Retrofit

[retrofit](http://square.github.io/retrofit/)

[github 地址](https://github.com/square/retrofit)

### 引入项目

gradle 引入

```groovy
compile 'com.squareup.retrofit2:retrofit:2.3.0'
```

需要在混淆中加入

```shell
-dontwarn okio.**
-dontwarn javax.annotation.**
```



### 官方说明

#### 介绍

Retrofit 将 HTTP API 转为 Java 接口：

```java
public interface GitHubService {
  @GET("users/{user}/repos")
  Call<List<Repo>> listRepos(@Path("user") String user);
}
```

Retrofit 类生成一个 GitHubService 接口的实现：

```java
Retrofit retrofit = new Retrofit.Builder()
    .baseUrl("https://api.github.com/")
    .build();

GitHubService service = retrofit.create(GitHubService.class);
```

GitHubService 中的每个 Call 都会向远程 web 服务器发出同步或异步的 HTTP 请求：

```java
Call<List<Repo>> repos = service.listRepos("octocat");
```

使用注解描述 HTTP 请求：

+ URL 参数替换并支持查询参数
+ 对象转换为请求 body（如 JSON、协议缓冲区）
+ multipart 请求 body 和文件上传



### API 声明

接口方法和它的参数的注解指示了请求如何被处理。



#### 请求方法

每个方法必须有一个提供请求方法和相对 URL 的 HTTP 注解。

这里有五种内置注解：GET、POST、PUT、DELETE 和 HEAD。

```java
@GET("users/list")
```

还可以在 URL 中指定查询参数

```java
@GET("users/list?sort=desc")
```



#### URL 操作

请求 URL 可以使用替换块和方法上的参数来动态更新。一个替换块是一个使用 {and} 包裹的字母字符串，相应的参数必须使用带有相同字符串的 @Path 进行注解。

```java
@GET("group/{id}/users")
Call<List<User>> groupList(@Path("id") int groupId);
```

添加查询参数：

```java
@GET("group/{id}/users")
Call<List<User>> groupList(@Path("id") int groupId, @Query("sort") String sort);
```

使用 Map 来处理复杂的查询参数

```java
@GET("group/{id}/users")
Call<List<User>> groupList(@Path("id") int groupId, @QueryMap Map<String, String> options);
```



#### 请求体

```java
@POST("users/new")
Call<User> createUser(@Body User user);
```



#### FORM ENCODED 和 MULTIPART

> form 表单，form encoded 和 multipart 是 post 请求提交数据的格式。

当方法带有 @FormUrlEncoded Form-encoded 时，发送的是 form-encoded 数据，每一个键值对使用 @Filed 进行注解。

```java
@FormUrlEncoded
@POST("user/edit")
Call<User> updateUser(@Field("first_name") String first, @Field("last_name") String last);
```

当方法带有 @Multipart 时，使用的是 multipart 请求，part 使用 @Part 来注解。

```java
@Multipart
@PUT("user/photo")
Call<User> updateUser(@Part("photo") RequestBody photo, @Part("description") RequestBody description);
```



#### Header 操作

使用 @Headers 注解来为方法设置静态 header

```java
@Headers("Cache-Control: max-age=640000")
@GET("widget/list")
Call<List<Widget>> widgetList();
```

```java
@Headers({
    "Accept: application/vnd.github.v3.full+json",
    "User-Agent: Retrofit-Sample-App"
})
@GET("users/{username}")
Call<User> getUser(@Path("username") String username);
```

注意：header 不会被彼此覆盖，所有相同名称的 header 都会包含在请求中。

请求 header 也可以使用 @Header 注解来动态更新。

```java
@GET("user")
Call<User> getUser(@Header("Authorization") String authorization)
```



#### 同步 VS 异步

Call 实例可以以同步或者异步方式执行，每个实例都只能使用一次，但调用 clone() 将创建一个可被使用的新实例。

在 Android 中，回调将执行在主线程，而在 JVM 中，回调将执行在于 HTTP 请求相同的线程。



### Retrofit 配置



