## 术语

### chrome

在化学里表示铬，在专业术语里，chrome 指的是浏览器接口的非网页部分——工具栏、标签、按钮，也可以理解为框架 frame。





shouldOverrideUrlLoading 不拦截 post 请求，比如 form 里的 post 方法  



## 功能实现

### 选取图片（拍照或相册选取）

> Android 的 WebView 无法直接调用系统功能选取图片和拍照，需要开发者在方法回调中自行实现，并在获取到图片 Uri 后主动回传。

[深坑之Webview,解决H5调用android相机拍照和录像](https://blog.csdn.net/villa_mou/article/details/78728417)

流程：

1. Manifest 中添加相机权限，设置 WebView 文件读取相关功能
2. 复写 WebChromeClient 的 `onShowFileChooser(WebView webView, ValueCallback<Uri[]> filePathCallback, FileChooserParams fileChooserParams) ` 方法（5.0 +）和 `openFileChooser(ValueCallback<Uri> uploadMsg, String acceptType, String capture)` 方法



参考：

[What does 'chrome' mean?](https://stackoverflow.com/questions/5071905/what-does-chrome-mean)

[Why is Chrome called Chrome?](https://www.quora.com/Google-Chrome/Why-is-Chrome-called-Chrome) 

[Google Chrome 为什么取名 Chrome?](https://www.zhihu.com/question/19826456)