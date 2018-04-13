比如，我们需要链接：https://www.example.com/articles?title=XX#section-name，其中 title 和 section-name 的值都是动态的。

显然，如果我们不知道 Uri 这个类，我们可以通过 StringBuilder 进行拼接得到，但这样需要我们自己添加诸如 ？、&、#等连接符，而且当链接比较长，参数比较多的时候，显得很冗长。

如果是通过 Uri 类来拼接的话，我们需要先得到一个 Uri.Builder 类，而获取 Uri.Builder 实例有两种方式：

```java
new Uri.Builder()
 	.scheme("https")
    .authority("www.example.com")
    .appendPath("articles")
    .appendQueryParameter("title","张三")
    .fragment("first")
    .toString();
// 我们也可以基于一个基本的 uri 来进行拼接
Uri.parse("https://www.example.com/articles")
    .buildUpon()
    .appendQueryParameter("title", "张三")
    .fragment("first")
    .toString()
// 打印结果都是：
// https://www.example.com/articles?title=张三#first
```









参考：

[Use URI builder in Android or create URL with variables](https://stackoverflow.com/questions/19167954/use-uri-builder-in-android-or-create-url-with-variables)