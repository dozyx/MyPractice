# 重新认识 targetSdkVersion
> 在新公司代码中碰到了一个 bug，两个几乎完全相同的 Activity，在 WebView 中加载相同内容时，其中一个页面的内容分割线被拉宽，在花了大半天的时间排查掉代码原因后，直接在该 app 中启动一个新的 Activity 来加载网页才意识到问题在工程配置上，然后很快地发现 targetSdkVersion 的差异，修改为 19+ 以后正常。  
> 问题解决后，虽然一开始觉得这个问题很坑，但后面想了想，觉得还是自己一开始的思路有了问题，相同机器、相同 WebView 配置，我本应该能更快地得到答案。  

配置 Android 工程时，会涉及三种的版本设置：
+ compileSdkVersion：编译时采用的版本，就是编写代码时使用的源码版本，这个版本是「不会改变运行时行为」的，因为它不会被编译进 APK 中，**建议使用最新的 SDK 进行编译**。
+ minSdkVersion：兼容的最小版本，在使用更高版本 API 时会做出警告。（应用的 minSdkVersion 一般需要 大于使用的库的minSdkVersion，如果仍然希望使用该库，那么可以通过在清单的 <uses-sdk> 中添加  tools:overrideLibrary 属性来使用）
+ targetSdkVersion：希望运行的目标版本

前面两个版本其实都比较好理解，所以下面主要说下 targetSdkVersion。  

「targetSdkVersion 是 Android 提供向前兼容的主要依据，在应用的 targetSdkVersion 没有更新之前系统不会应用最新的行为变化。」在新的 Android 版本中，原有的 API 行为可能做出了变更，但如果我们的 targetSdkVersion 没有更改，那么 API 的行为将维持旧的逻辑，这样就可以确保 app 的功能在新的 SDK 中也可以保持相同的行为。所以，关于文章开头说的 bug，虽然没有深入细究它的原理，但个人猜测（很不严谨。。。）是由于 API 19 的 WebView 行为更改导致的。  

如果希望确定新 SDK 版本的行为变更，可以在 [VERSION_CODES](http://developer.android.com/reference/android/os/Build.VERSION_CODES.html?utm_campaign=adp_series_sdkversion_010616&utm_source=medium&utm_medium=blog) 和 [API Level](http://developer.android.com/guide/topics/manifest/uses-sdk-element.html?utm_campaign=adp_series_sdkversion_010616&utm_source=medium&utm_medium=blog#ApiLevels) 中查看，这将有助于我们适配新的 SDK。  

最后，引用一下关于上面三个版本之间的理想关系：
`minSdkVersion (lowest possible) <= targetSdkVersion == compileSdkVersion (latest SDK)`







参考：

[如何选择 compileSdkVersion, minSdkVersion 和 targetSdkVersion](https://chinagdg.org/2016/01/picking-your-compilesdkversion-minsdkversion-targetsdkversion/)

 [tools:overrideLibrary 标记](https://developer.android.com/studio/build/manifest-merge.html?#wzxhzdk49uses-sdk)
 
[当前的 Android 分布统计](http://developer.android.com/about/dashboards/index.html)
