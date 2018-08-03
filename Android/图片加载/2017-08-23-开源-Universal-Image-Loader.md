---
title: 开源-Universal Image Loader 用法
tags:
  - android
  - 开源
date: 2017-08-23 11:04:48
categories: 开源
---

> [Android-Universal-Image-Loader](https://github.com/nostra13/Android-Universal-Image-Loader) 是目前 Github 排名第一的库，尽管它在15年已经停止维护。不过，因为之前工作没涉及，所以一直没有使用过，在此，想要对它的用法和原理进行一次完整的梳理。

首先，我会先回顾一下一般 Bitmap 的使用策略，然后再对 UIL 进行分析。



## Android 中对 Bitmap 的处理

由于 Bitmap 会占用较多的内存，很容易触发 OOM 异常，所以，我们通常会在使用 Bitmap 时采用以下手段：

+ 缩放
+ 内存缓存：使用 LrcCache
+ 磁盘缓存：使用 DiskLrcCache

（LRU ，Least Recently Used，近期最少使用算法）

除此之外，还可以通过一些小技巧提升用户体验：

+ 未加载完成时使用默认图片
+ 滑动过程中停止加载

### 缩放图片

加载 Bitmap 需要 BitmapFactory 类，它提供了多个 decodeXX() 方法来从不同的源中加载出一个 Bitmap 对象，如果需要提高加载性能，首先可以做的就是在 decode 时利用 BitmapFactory.Options 参数对图片进行缩放。

这里，主要用到的是 BitmapFactory.Options 的 inSampleSize 变量，它表示的是 Bitmap 的采样率（即缩放比例），我们通常按照以下步骤来获取一个适当的 inSampleSize 的值：

+ 获取 Bitmap 原始宽高（将 BitmapFactory.Options 的 inJustDecodeBounds 设为 true，这时调用 decodeXX()方法将不会直接将 Bitmap 加载到内存中，但却能提取到 Bitmap 的信息）
+ 结合目标 View 的大小来计算 inSampleSize
+ 将 inJustDecodeBounds 设为 false，再次调用 decodeXX() 方法将得到缩放后的 Bitmap

一个完整的代码片段如下：

```java
public static Bitmap decodeSampledBitmap(Resources res, int resId, int reqWidth,
            int reqHeight) {
        final BitmapFactory.Options options = new BitmapFactory.Options();
        options.inJustDecodeBounds = true;
        BitmapFactory.decodeResource(res, resId, options);

        options.inSampleSize = calculateInSampleSize(options, reqWidth, reqHeight);

        options.inJustDecodeBounds = false;
        return BitmapFactory.decodeResource(res, resId, options);
    }

    private static int calculateInSampleSize(BitmapFactory.Options options, int reqWidth,
            int reqHeight) {
        final int width = options.outWidth;
        final int height = options.outHeight;
        int inSampleSize = 1;// 采样率
        if (width > reqWidth || height > reqHeight) {
            final int halfWidth = width / 2;
            final int halfHeight = height / 2;
            while ((halfWidth / inSampleSize) >= reqWidth
                    && (halfHeight / inSampleSize) >= reqHeight) {
                inSampleSize *= 2;
            }
        }
        return inSampleSize;
    }
```



### 使用 LruCache 实现内存缓存

LruCache 继承于 LinkedHashMap，在超过最大容量后，它可以根据访问时间来移除元素。

在用来实现 Bitmap 容量缓存时，需要传入一个最大容量值（如果没有重写 sizeOf的话，该值表示的是缓存的数目），并重写它的 sizeOf 方法来计算缓存对象的大小。如果需要在移除缓存时进行一些资源的回收，可以重写 entryRemoved() 方法。

LruCache 的初始化过程如下：

```java
        int maxMemory = (int) (Runtime.getRuntime().maxMemory());// KB
        int cacheSize = maxMemory / 8;
        mMemoryCache = new LruCache<String, Bitmap>(cacheSize) {
            @Override
            protected int sizeOf(String key, Bitmap value) {
                return value.getRowBytes() * value.getHeight() / 1024;
            }
        };
```

添加和获取缓存对象时，分别调用 put 和 get 方法即可。



### 使用 DiskLruCache 实现磁盘缓存

DiskLruCache 通过将缓存对象写入文件系统来实现缓存效果。不过，DiskLruCache 需要得到 Google 官方推荐，但却不是 SDK 的一部分，它的源码可以在[这个地址](https://android.googlesource.com/platform/libcore/+/android-4.1.1_r1/luni/src/main/java/libcore/io/DiskLruCache.java)得到。

#### 创建

DiskLruCache 的创建需要通过它的 open 方法

```java
public static DiskLruCache open(File directory, int appVersion, int valueCount, long maxSize)
```

directory：缓存目录

appVersion：一般设为 1 即可，当版本号发生变化时，DiskLruCache 将清空之前所有的缓存文件。

valueCount：单个节点所对应的数据个数，一般设为 1。（javac：the number of values per cache entry）

maxSize：缓存的总大小

 常见创建代码如下：

```java
private static final long DISK_CACHE_SIZE = 1024 * 1024 * 50;// 50MB
		...
		File diskCacheDir = getDiskCacheDir(mContext, "bitmap");
        if (!diskCacheDir.exists()) {
            diskCacheDir.mkdirs();
        }
        mDiskLruCache = DiskLruCache.open(diskCacheDir, 1, 1, DISK_CACHE_SIZE);
```



#### 添加缓存

客户端需要调用 edit() 方法来创建或更新值，edit() 将返回一个 Editor 对象，每一次的 edit() 都需要有一个对应的 Editor.commit() 或 Editor.abort()。需要注意的是，同一时间只能有一个 Editor 在编译同一个缓存，所以如果在该缓存被其他 Editor 编辑时，再次调用 edit() 将返回 null。

以图片缓存为例：

一般将 url 的 md5 作为 key

```java
    /**
     *  将字符串如 URL 转换为 hash 值，该值将作为文件名。(因为图片的 url 中可能含有无法在 Android 中
     *  使用的特殊编码)
     */
    public static String hashKeyForDisk(String key) {
        String cacheKey;
        try {
            final MessageDigest mDigest = MessageDigest.getInstance("MD5");
            mDigest.update(key.getBytes());
            cacheKey = bytesToHexString(mDigest.digest());
        } catch (NoSuchAlgorithmException e) {
            cacheKey = String.valueOf(key.hashCode());
        }
        return cacheKey;
    }
    private static String bytesToHexString(byte[] bytes) {
        // http://stackoverflow.com/questions/332079
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < bytes.length; i++) {
            String hex = Integer.toHexString(0xFF & bytes[i]);
            if (hex.length() == 1) {
                sb.append('0');
            }
            sb.append(hex);
        }
        return sb.toString();
    }
```

将 url 转为 key 后，获取 Editor 对象，

```java
key = hashKeyForDisk(url);
DiskLruCache.Editor editor = mDiskLruCache.edit(key);
                        if (editor != null) {
                            OutputStream out = editor.newOutputStream(DISK_CACHE_INDEX);
                        }
// 因为前面把每个节点值得数量设为了1，所以 DISK_CACHE_INDEX 设为 0 即可
```

然后，我们可以通过得到的输出流将网络上下载的图片写入到文件系统中

```java
    public boolean downloadUrlToStream(String urlString, OutputStream outputStream) {
        HttpURLConnection urlConnection = null;
        BufferedOutputStream out = null;
        BufferedInputStream in = null;

        try {
            final URL url = new URL(urlString);
            urlConnection = (HttpURLConnection) url.openConnection();
            in = new BufferedInputStream(urlConnection.getInputStream(),IO_BUFFER_SIZE);
            out = new BufferedOutputStream(outputStream,IO_BUFFER_SIZE);

            int b;
             while ((b = in.read()) != -1) {
                 out.write(b);
             }
             return true;
        } catch (IOException e) {
            Log.e(TAG, "downloadUrlToStream: failed ", e);
        } finally {
            if (urlConnection != null) {
                urlConnection.disconnect();
            }
            try {
                out.close();
                in.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        return false;
    }
```

最后，真正将图片写入文件系统的是 commit 操作，如果下载中出现异常，可以使用 abort 方法回退操作

```java
            OutputStream outputStream = editor.newOutputStream(DISK_CACHE_INDEX);
            if (downloadUrlToStream(url, outputStream)) {
                editor.commit();
            } else {
                editor.abort();
            }
```

整理一下整个添加图片缓存过程：

+ edit() 方法需要传入一个 key，所以需要将图片的 URL 进行转化
+ 调用 edit() 获得 Editor 对象，通过 Editor 的 newOutputStream 方法可以获得一个用于写入文件的输出流
+ 通过网络下载图片，得到图片的输入流，然后输入流的内容写入输出流中
+ 最后通过 commit() 来进行文件写入



#### 缓存查找

查找过程同样需要对 key 进行转换，然后利用 key 来获得一个 Snapshot （快照）对象，接着利用 Snapshot 对象可以得到缓存的文件输入流，通过输入流就可以很容易的得到 Bitmap。

```java
Bitmap bitmap = null;
        String key = hashKeyFormUrl(url);
        DiskLruCache.Snapshot snapShot = mDiskLruCache.get(key);
        if (snapShot != null) {
            FileInputStream fileInputStream = (FileInputStream)snapShot.getInputStream(DISK_CACHE_INDEX);
            FileDescriptor fileDescriptor = fileInputStream.getFD();
            bitmap = mImageResizer.decodeSampledBitmapFromFileDescriptor(fileDescriptor,
                    reqWidth, reqHeight);
            if (bitmap != null) {
                addBitmapToMemoryCache(key, bitmap);
            }
        }
```





# Universal Image Loader 开源库

[Github 地址](https://github.com/nostra13/Android-Universal-Image-Loader)

### 用法

#### 快速使用

+ 添加库（gradle）

  ```groovy
  compile 'com.nostra13.universalimageloader:universal-image-loader:1.9.5'
  ```

+ 配置权限

  ```xml
  <manifest>
  	<!-- Include following permission if you load images from Internet -->
  	<uses-permission android:name="android.permission.INTERNET" />
  	<!-- Include following permission if you want to cache images on SD card -->
  	<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
  	...
  </manifest>
  ```

+ 在第一次使用 ImageLoader 之前需要配置（Application 或 Activity 中）

  ```java
  public class MyActivity extends Activity {
  	@Override
  	public void onCreate() {
  		super.onCreate();

  		// Create global configuration and initialize ImageLoader with this config
  		ImageLoaderConfiguration config = new ImageLoaderConfiguration.Builder(this)
  			...
  			.build();
  		ImageLoader.getInstance().init(config);// ImageLoader 是一个单例
  		...
  	}
  }
  ```




#### Loader 配置

从上面一节可以发现，我们可以在第一次使用时传入一个 ImageLoaderConfiguration 对象来对 ImageLoader 进行配置，这个配置是对整个 Application 有效的，应当只进行一次的设置。

所有的配置项（均是可选的）包括：

```java
// DON'T COPY THIS CODE TO YOUR PROJECT! This is just example of ALL options using.
// See the sample project how to use ImageLoader correctly.
File cacheDir = StorageUtils.getCacheDirectory(context);
ImageLoaderConfiguration config = new ImageLoaderConfiguration.Builder(context)
		.memoryCacheExtraOptions(480, 800) // default = device screen dimensions
		.diskCacheExtraOptions(480, 800, null)
		.taskExecutor(...) // 自定义加载和显示的 Executor
		.taskExecutorForCachedImages(...)
		.threadPoolSize(3) // default
		.threadPriority(Thread.NORM_PRIORITY - 2) // default
		.tasksProcessingOrder(QueueProcessingType.FIFO) // default
		.denyCacheImageMultipleSizesInMemory() // 不允许在内存中为图片的多个尺寸进行缓存
		.memoryCache(new LruMemoryCache(2 * 1024 * 1024)) // 为 bitmap 设置内存缓存
		.memoryCacheSize(2 * 1024 * 1024)
		.memoryCacheSizePercentage(13) // default，即八分之一
		.diskCache(new UnlimitedDiskCache(cacheDir)) // default
		.diskCacheSize(50 * 1024 * 1024)
		.diskCacheFileCount(100)
		.diskCacheFileNameGenerator(new HashCodeFileNameGenerator()) // default，文件名生成
		.imageDownloader(new BaseImageDownloader(context)) // default，图片下载器得到输入流
		.imageDecoder(new BaseImageDecoder()) // default，解码器得到 bitmap
		.defaultDisplayImageOptions(DisplayImageOptions.createSimple()) // default 图片显示过程中的一些配置
		.writeDebugLogs()
		.build();
```



#### 显示配置

在使用 ImageLoader 的displayImage() 方法时，可以传入一个 DisplayImageOptions 对象来配置显示时的一些特性，如果没有传入，那么将使用用 ImageLoaderConfiguration 所提供的默认 DisplayImageOptions 对象。所有的配置包括：

```java
// DON'T COPY THIS CODE TO YOUR PROJECT! This is just example of ALL options using.
// See the sample project how to use ImageLoader correctly.
DisplayImageOptions options = new DisplayImageOptions.Builder()
		.showImageOnLoading(R.drawable.ic_stub) // resource or drawable
		.showImageForEmptyUri(R.drawable.ic_empty) // resource or drawable
		.showImageOnFail(R.drawable.ic_error) // resource or drawable
		.resetViewBeforeLoading(false)  // default
		.delayBeforeLoading(1000)
		.cacheInMemory(false) // default
		.cacheOnDisk(false) // default
		.preProcessor(...) // 设置在 bitmap 缓存到内存之前进行预处理的处理器
		.postProcessor(...) // 设置用于显示之前，内存缓存之后的处理器
		.extraForDownloader(...) // 传给下载器的额外对象
		.considerExifParams(false) // default，为 JEPG 图片插入 EXIF 信息
		.imageScaleType(ImageScaleType.IN_SAMPLE_POWER_OF_2) // default
		.bitmapConfig(Bitmap.Config.ARGB_8888) // default
		.decodingOptions(...)// 传入的是 BitmapFactory.Options 对象
		.displayer(new SimpleBitmapDisplayer()) // default，用于图片加载任务，可以在显示前对图片进行处理
		.handler(new Handler()) // default，用于传递 ImageLoadingListener 事件的 Handler
		.build();
```



#### 实际用例

完整例子源码可以查看 UIL 库的 [sample](https://github.com/nostra13/Android-Universal-Image-Loader/tree/master/sample)，apk 可以从 Google Play [下载](https://play.google.com/store/apps/details?id=com.nostra13.universalimageloader.sample)（sample 里的图片需要代理才能下载。。。）。

sample 中提供了以下几种使用场景：

+ ListView
+ GridView
+ ViewPager
+ Gallery
+ ViewPager（ListView + GridView）



UIL 的使用很简单，配置好后，只要调用 `ImageLoader.getInstance().displayImage(...)` 即可，displayImage(…) 有多个重载方法，提供了许多定制化的特性，十分方便。





### 注意事项

[Useful Info](https://github.com/nostra13/Android-Universal-Image-Loader/wiki/Useful-Info)

+ **缓存默认是没有开启的**，如果需要启用，需要创建一个 DisplayImageOptions 对象，并在ImageLoaderConfiguration 配置时设为默认选项。如果不需要全局设置，也可以在加载时单独设置。
+ 如果在 list 控件中使用，可以考虑使用 PauseOnScrollListener
+ 通过 ImageLoaderConfiguration.memoryCache(…) 可以配置不同的内存缓存实现，UIL 提供了多种实现，如LruMemoryCache（默认）、UsingFreqLimitedMemoryCache 等，它们对 bitmap 的引用方式会有所不同。
+ 通过 ImageLoaderConfiguration.diskCache(…) 可以配置不同的磁盘缓存实现
+ 通过 DisplayImageOptions.displayer(…) 可以使用不同的显示，内置实现由：RoundedBitmapDisplayer 、FadeInBitmapDisplayer。
+ ImageLoader 中有个 stop() 方法可以用来取消运行中或计划中的图片显示任务，但此方法并不会主动设置的 Executor。
+ 默认下载器在使用网络下载时用的是 HttpURLConnection，如果需要修改，可以继承 BaseImageDownloader 然后重写 getStreamFromNetwork() 方法。



## 最后

本以为 UIL 的原理与 Android 官网上演示的差不多，结果一看 UIL 源码发现东西好多！暂时没什么时间深入看 UIL 源码了，但从 UIL 的用例来看使用上却是出奇的简单。可以说，UIL 提供的功能基本可以满足绝大部分的图片需求，不过我很好奇哪些公司会将 UIL 应用到自己项目中，感觉 UIL 的许多功能是否对特定项目有点多余，当然，对于一般项目倒是可以加快开发速度。




参考

《Android 开发艺术探索》第 12 章

[UIL 官方文档](https://github.com/nostra13/Android-Universal-Image-Loader)

