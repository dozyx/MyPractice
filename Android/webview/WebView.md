## 术语

### chrome

在化学里表示铬，在专业术语里，chrome 指的是浏览器接口的非网页部分——工具栏、标签、按钮，也可以理解为框架 frame。





shouldOverrideUrlLoading 不拦截 post 请求，比如 form 里的 post 方法  



## 功能实现

### 选取图片（拍照或相册选取）

> Android 的 WebView 无法直接调用系统功能选取图片和拍照，需要开发者在方法回调中自行实现，并在获取到图片 Uri 后主动回传。

[深坑之Webview,解决H5调用android相机拍照和录像](https://blog.csdn.net/villa_mou/article/details/78728417)

#### 流程

1. Manifest 中添加相机权限，设置 WebView 文件读取相关功能
2. 复写 WebChromeClient 的 `onShowFileChooser(WebView webView, ValueCallback<Uri[]> filePathCallback, FileChooserParams fileChooserParams) ` 方法（5.0 +）和 `openFileChooser(ValueCallback<Uri> uploadMsg, String acceptType, String capture)` 方法（4.1~4.4），在这两个方法中添加图片获取逻辑
3. 通过 ValueCallback 将图片的 Uri 返回给 H5



#### 注意

* 每一次回调 onShowFileChooser 或 openFileChooser 之后，都需要调用 ValueCallback#onReceiveValue 否则无法触发下一次回调



### 电话拨打

在 H5 页面拨打电话跳转的是一个 `tel:` 地址，WebView 需要在 [shouldOverrideUrlLoading](https://developer.android.com/reference/android/webkit/WebViewClient#shouldOverrideUrlLoading(android.webkit.WebView,%20android.webkit.WebResourceRequest)) 方法中判断处理。

下面是[Android WebView “tel:” links show web page not found](https://stackoverflow.com/questions/4338305/android-webview-tel-links-show-web-page-not-found)中的代码：

```java
    @SuppressWarnings("deprecation")
    @Override
    public boolean shouldOverrideUrlLoading(WebView view, String url) {
        if (url.startsWith("mailto:")) {  
            //Handle mail Urls
            startActivity(new Intent(Intent.ACTION_SENDTO, Uri.parse(url)));
        } else if (url.startsWith("tel:")) {
            //Handle telephony Urls
            startActivity(new Intent(Intent.ACTION_DIAL, Uri.parse(url)));
        } else {
            view.loadUrl(url);
        }
        return true;
    }

    @TargetApi(Build.VERSION_CODES.N)
    @Override
    public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
        final Uri uri = request.getUrl();
        if (uri.toString().startsWith("mailto:")) {
            //Handle mail Urls
            startActivity(new Intent(Intent.ACTION_SENDTO, uri));
        } else if (uri.toString().startsWith("tel:")) {
            //Handle telephony Urls
            startActivity(new Intent(Intent.ACTION_DIAL, uri));
        } else {
            //Handle Web Urls
            view.loadUrl(uri.toString());
        }
        return true;
    }
```

* 上面复写了两个 shouldOverrideUrlLoading 来确保兼容
* `Intent.ACTION_DIAL` 会调起电话的拨号页面而不是直接拨打，所以不需要权限。



### 重定向问题

开发中遇到一个问题，H5 页面 A 发起支付宝网页支付，按返回键，又重复发起了支付，无法回到第一个页面。概括起来就是，H5 页 A 发起支付，跳到 B，B 重定向到支付宝网页支付页面，返回，回到 B，B 又重定向到了支付页面。

解决：

这个问题出现的原因在于 shouldOverrideUrlLoading 方法的处理，下面是我一开始有重复重定向的代码（这个代码跟上一个电话拨打部分的差不多）：

```java
public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
    Uri uri = request.getUrl();
    if (uri.toString().startsWith("http://") || uri.toString().startsWith("https://")) {
        view.loadUrl(uri.toString());
        return true;
    }
    ...
    return true;
}
```

这段代码里我犯了两个错误：

1. 返回值没理解好
2. 调用了 loadUrl

首先，看下 [shouldOverrideUrlLoading](https://developer.android.com/reference/android/webkit/WebViewClient#shouldOverrideUrlLoading(android.webkit.WebView,%20android.webkit.WebResourceRequest)) 返回值的说明：

true - WebView 放弃加载该 URL（跟方法名一样，可以理解为 app 拦截了该 URL 自行处理）；

false - WebView 正常加载该 URL。

上面犯的错误就是返回 true 选择了自行处理，却又执行了 loadUrl。shouldOverrideUrlLoading 文档里也对此进行了特别注明：

> **Note:** Do not call `WebView.loadUrl(String)` with the request's URL and then return `true`. This unnecessarily cancels the current load and starts a new load with the same URL. The correct way to continue loading a given URL is to simply return `false`, without calling `WebView.loadUrl(String)`.

按个人的理解，应该对 重定向 URL 进行 loadUrl 破坏了 WebView 对该 URL 重定向的处理，无法区分它是否为真实的目的页面。

最后，代码进行修改后返回正常：

```java
public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
    Uri uri = request.getUrl();
    if (uri.toString().startsWith("http://") || uri.toString().startsWith("https://")) {
        return false;
    }
    ...
    return true;
}
```

参考：

[Android 解决WebView重定向问题](https://www.jianshu.com/p/c01769ababfa)



#### 记一个奇怪的重定向问题

> 本以为上面的写法可以处理好重定向问题，直到我遇到了测试反馈的一个问题。。。

问题描述：启动一个 H5 页面，点击返回会一直刷新，无法退出页面

原因分析：测试人员在后台配置的是一个电脑版的 url 地址 `http://www.yeahka.com`，WebView 加载后会重定向到手机版页面。点击返回会再次发生重定向。使用手机微信加载该 url 存在类似问题。

奇怪的点：

* 在我的手机（小米8，Android10）不存在该问题。猜测是手机上的 WebView 版本经过更新，新版本已修复该问题。
* 修改配置为 `setJavaScriptEnabled(false)` 也可以解决该问题。猜测跟 H5 本身有关系？



## WebView 优化

### 安全

#### addJavascriptInterface 接口引起远程代码执行漏洞

Android 4.2 要求 js 调用的函数需要有 @JavascriptInterface 注解，所以此问题可以忽略



#### 密码明文存储漏洞

密码会被明文保到 /data/data/com.package.name/databases/webview.db 中

解决：

```java
WebSettings.setSavePassword(false)
```



#### 域控制不严格漏洞

描述：A 应用启动 B 应用的 Activity 加载一个恶意的 file 协议 url，然后通过该网页获取 B 应用的内部私有文件。

优化：

* 不需要使用 file 协议的网页禁用
* 对于

> 理解：如果一个应用声明可以打开加载 url，那么其他应用就可能提交恶意的 url，然后在加载的页面中进行恶意操作。



[WebView的优化--处理WebView的容易忽略的漏洞](https://blog.csdn.net/li15225271052/article/details/73730321)



参考：

[What does 'chrome' mean?](https://stackoverflow.com/questions/5071905/what-does-chrome-mean)

[Why is Chrome called Chrome?](https://www.quora.com/Google-Chrome/Why-is-Chrome-called-Chrome) 

[Google Chrome 为什么取名 Chrome?](https://www.zhihu.com/question/19826456)