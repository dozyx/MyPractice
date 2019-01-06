

[FileProvider][] 是 ContentProvider 的一个子类，它可以通过创建 `content://` 而不是  `file://` 的 Uri 来实现更加安全的 app 文件共享。

content URI 允许授予临时的读写权限，这些权限只在接收带 URI 的 Intent 的 Activity 或 Service 存活的时间内有效。相对的，`file://` Uri  必须修改文件的系统权限来控制访问。



## 使用步骤

### 定义一个 FileProvider

```xml
<manifest>
    ...
    <application>
        ...
        <provider
            android:name="android.support.v4.content.FileProvider"
            android:authorities="com.mydomain.fileprovider"
            android:exported="false"
            android:grantUriPermissions="true">
            ...
        </provider>
        ...
    </application>
</manifest>
```



### 指定对哪些文件生效

FileProvider 只能对预先声明的目录的文件生成 content URI。

1. 创建一个 xml 文件：

   ```xml
   <paths xmlns:android="http://schemas.android.com/apk/res/android">
       <files-path name="my_images" path="images/"/>
       ...
   </paths>
   ```

   <paths> 元素必须包括一个或多个子元素：

   * `<files-path name="name" path="path" />` 表示的是 app 内部存储区域 `files/` 子目录的文件，该子目录所在的根目录是 `Context.getFilesDir()` 返回的目录。
   * `<cache-path name="name" path="path" />` 对应于 `Context.getCacheDir()`
   * `<external-path name="name" path="path" />` 对应于 `Environment.getExternalStorageDirectory()`
   * `<external-files-path name="name" path="path" />` 对应于 `Context#getExternalFilesDir(String) `
   * `<external-cache-path name="name" path="path" />` 对应于 `Context.getExternalCacheDir()`
   * `<external-media-path name="name" path="path" />` 对应于 `Context.getExternalMediaDirs()`（该目录在 API21+ 有效）

   `name` 作为 URI 路径的一个部分，可以隐藏它所表示的子目录，子目录将包含在 path 属性中。

   `path` 表示要分享的子目录。

2. 将 xml 文件链接到 FileProvider

   ```xml
   <provider
       android:name="android.support.v4.content.FileProvider"
       android:authorities="com.mydomain.fileprovider"
       android:exported="false"
       android:grantUriPermissions="true">
       <meta-data
           android:name="android.support.FILE_PROVIDER_PATHS"
           android:resource="@xml/file_paths" />
   </provider>
   ```



### 为一个文件生成 Content URI

```java
File imagePath = new File(Context.getFilesDir(), "images");
File newFile = new File(imagePath, "default_image.jpg");
Uri contentUri = getUriForFile(getContext(), "com.mydomain.fileprovider", newFile);
// 返回的 uri 为 content://com.mydomain.fileprovider/my_images/default_image.jpg
```

得到 content uri 后，可以通过 Intent 将 uri 分享给第三方 app，第三方 app 通过 [ContentResolver.openFileDescriptor](https://developer.android.com/reference/android/content/ContentResolver.html#openFileDescriptor(android.net.Uri,%20java.lang.String)) 返回的 [ParcelFileDescriptor](https://developer.android.com/reference/android/os/ParcelFileDescriptor.html) 来访问 uri 的内容。



### 给 URI 授予临时权限

可以选择以下的其中一种方式：

+ 调用 `Context.grantUriPermission(package, Uri, mode_flags)`，mode_flags 可以使用以下值： FLAG_GRANT_READ_URI_PERMISSION、FLAG_GRANT_WRITE_URI_PERMISSION。权限将一直有效，知道调用 ` revokeUriPermission()` 收回或者重启设备。
+ 调用 Intent 的 `setData()` 将 content URI 设置进去，接着，可以调用  `Intent.setFlags()` 来设置 FLAG_GRANT_READ_URI_PERMISSION 和 FLAG_GRANT_WRITE_URI_PERMISSION，最后，将 Intent 发送给另一个 app。Intent 中的权限将持续到 Activity 存活期间。授予一个 Activity 的权限会同时被该 app 的其他组件继承。

### 将 Content URI 提供给另一个 app

一个常用的方式是 chient app 使用 `startActivityResult()`  通过 Intent 打开你的 app，然后你的 app 通过 setResult 返回一个 content URI。











参考：

[FileProvider]:https://developer.android.com/reference/android/support/v4/content/FileProvider