### URLEncoder

URLEncoder 是用于 HTML form 编码的工具类，该类包含了将 String 转为 `application/x-www-form-urlencoded ` MIME 格式的静态方法。

在对一个 String 进行编码时，应用了以下规则：

+ "a - z"、"A - Z"、"0 - 9" 保持不变
+ 特殊字符 "."、"-"、"*" 、"_"保持不变
+ 空格" " 转为 "+"
+ 其他都是不安全字符，将使用其他编码方案转为一个或多个字节，每一个字节都是用  "%xy" 形式的 3 个字符来表示，其中 xy 为该字节的两位十六进制表示。推荐的编码方案是 UTF-8。

如：

"The string ü@foo-bar"  编码后为 "The+string+%C3%BC%40foo-bar" 。



### URLDecoder

与 URLEncoder  相反





参考：

[URLEncoder](https://developer.android.com/reference/java/net/URLEncoder)

[URLDecoder](https://developer.android.com/reference/java/net/URLDecoder)