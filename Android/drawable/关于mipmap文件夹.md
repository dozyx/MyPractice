结论：将应用图标（即 ic_launcher.png）放在 mipmap 文件夹，其它图片资源仍然放置在 drawable 文件夹。

> 之所以使用 mipmap 是因为 launcher 可能会使用比设备密度更大的图标，比如，在 xxhdpi 设备上使用 xxxhdpi 的图标（通常 app 打包的 ic_lacuncher 大小为 48 * 48，但 launcher 可能不使用该大小）。不过，感觉还是未能完全理解 mipmap 的处理，本来有个想法：是不是在安装应用时，drawable 只会保留匹配密度的图片？但谷歌后，似乎也并不会这样。
>
> 而且，如果 drawable 与 mipmap 混用会有什么影响？

> [JellyBean MR2](https://developer.android.com/about/versions/android-4.3.html#Graphics) 中提到，mipmap 用于高质量或者不同缩放尺寸的图片。



参考：

[Mipmap drawables for icons](https://stackoverflow.com/questions/23935810/mipmap-drawables-for-icons)

[Mipmaps vs. drawable folders](https://stackoverflow.com/questions/28065267/mipmaps-vs-drawable-folders?rq=1)

[Does Android only install device size's resources?](https://stackoverflow.com/questions/9657399/does-android-only-install-device-sizes-resources/9657423#9657423)

[Goodbye launcher drawables, hello mipmaps!](https://androidbycode.wordpress.com/2015/02/14/goodbye-launcher-drawables-hello-mipmaps/)

[JellyBean MR2](https://developer.android.com/about/versions/android-4.3.html#Graphics)