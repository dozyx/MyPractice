用于 form-encoded 类型请求的键值对。



示例 1：

```java
@FormUrlEncoded
 @POST("/")
 Call<ResponseBody> example(
     @Field("name") String name,
     @Field("occupation") String occupation);
```

foo.example("Bob Smith", "President") 生成的请求体为 name=Bob+Smith&occupation=President



示例 2：

```java
 @FormUrlEncoded
 @POST("/list")
 Call<ResponseBody> example(@Field("name") String... names);
```

 foo.example("Bob Smith", "Jane Doe") 生成的请求体为  name=Bob+Smith&name=Jane+Doe









参考：

[Filed API](https://square.github.io/retrofit/2.x/retrofit/retrofit2/http/Field.html)