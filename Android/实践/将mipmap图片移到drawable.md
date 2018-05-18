> 旧的工程里所有图片都放在了 mipmap 文件夹，虽然没看出什么大的影响，但总看着不顺眼，所以打算将除 ic_launcher 外的所有图片移回 drawable。在此做下简单记录。

+ Ctrl + Shift + R，将 @mipmap 替换为 @drawable，R.mipmap 替换为 R.drawable

+ 将 manifest 中的 ic_launcher 引用改回 @mipmap

+ Ctrl + Shift + F，搜索 mipmap，一般除了 manifest 中的 ic_launcher，其他地方都不会用到 mipmap。

  ​