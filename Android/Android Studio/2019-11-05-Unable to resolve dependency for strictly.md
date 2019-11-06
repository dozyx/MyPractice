遇到一个很奇怪的依赖下载失败问题，下载的库是 com.tencent.wup:wup:1.0.0.E-release，我这边使用大写开头的 Release 才能下载成功，另一个同事却要使用 release 才能下载成功，而在 Jenkins 种也要 Release 才能成功。

错误提示：

```shell
ERROR: Unable to resolve dependency for ':app@MerchantPreDebug/compileClasspath': Could not resolve com.tencent.wup:wup:1.0.0.E-release.

ERROR: Unable to resolve dependency for ':app@MerchantPreDebug/compileClasspath': Could not resolve com.tencent.wup:wup:{strictly 1.0.0.E-Release}.
```

经过一轮尝试发现：

`jcenter() { url 'http://jcenter.bintray.com/' }` 库下载下来的是 release，而 `jcenter()` 下载下来的是 Release。