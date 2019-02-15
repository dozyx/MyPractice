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



参考：

[What does 'chrome' mean?](https://stackoverflow.com/questions/5071905/what-does-chrome-mean)

[Why is Chrome called Chrome?](https://www.quora.com/Google-Chrome/Why-is-Chrome-called-Chrome) 

[Google Chrome 为什么取名 Chrome?](https://www.zhihu.com/question/19826456)