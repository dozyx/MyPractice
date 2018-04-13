[The Difference Between URLs and URIs](https://danielmiessler.com/study/url-uri/)

通过以上参考链接查看具体的区分，这里只记下大概的理解：

+ URL (Uniform Resource Locator) 是 URI (Uniform Resource Identifier)的一个子集
+ URL 比 URI 更具体

![URI vs. URL](https://danielmiessler.com/images/URI-vs.-URL-e1464829000786.png)

举例：

一个文件位于`files.hp.com` ，这时候我们可以称它为 URI，但通过 `http://files.hp.com` 和 `ftp://files.hp.com`，我们可能得到完全不同的内容。