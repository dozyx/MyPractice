## 第 1 章 Android 数据技术

* 数据采集：关键页面或关键动作。

  在数据采集前期，进行定义设计时，指定数据采集规范至关重要。

  * 数据格式：

    流式格式表达结构例子：

    ```
    version||chient_ip||imei||imsi|brand||cpu||device_id||device_model||resolution||carrier||access||access_subtype||channel||app_key||app_version||usernick||phone_number||language||os||os_version||sdk_type||sdk_version||reserve||local_time||server_time||page||eventid||arg1||arg2||arg3||args
    ```

  * 多端协同技巧

    参与人员：产品经理、开发人员、测试人员、数据分析师

  * 数据分级方案

    * 基础常规事件
      * 页面访问
      * 控件点击
      * 控件曝光
    * 业务核心事件：不同类型的产品有各自关注的核心业务。如应用下载平台：
      * 下载开始
      * 下载完成
    * 特殊自定义事件：指除基础常规事件和业务核心事件外的所有自定义事件。

  * 多进程解决方案

    * 数据采集 SDK 独立子进程

      进程间通信推荐广播或 AIDL

    * SDK 多进程实例化

* 数据绑定

  * 控件数据绑定
    * MVVM：双向绑定。DataBinding 解决了数据和控件绑定的耦合问题，实现了数据和表现的分离。
  * 内容曝光框架
    * 存在问题：
      * 定义复杂，比如，用户看到才算曝光，曝光之后不能重复曝光
      * 测试难
      * 自定义组件
    * 自动化曝光的规则
      * 曝光定义：元素曝光时长超过 500ms 且元素曝光面积大于 50%
      * 当前页面元素已经曝光，如果元素希望被再次展现，只有当前业务消失过或业务方主动调用刷新接口，才能算曝光。
      * 当前页面元素的曝光会在页面退出时或同一区块数据累积大小超过一定的设定值（如 30KB）时产生（即多条曝光日志合并成一条上报，需要后期解析处理）。

* 数据存储和上报

  * 数据加密方案：通常采用流式加密的方式，使用对称密钥加密数据日志，并存储到本地。同时在上传数据日志时，使用非对称密钥对对称密钥 Key 做加密上传，防止密钥 Key 被破解，从而在网络层保证日志上报安全。

    * 密钥管理：
      * 密钥不能为常量，应随机、定期更换。常量难防止字典攻击。
      * 开发时要规避密钥硬编码。

  * 数据储存策略

    * SharedPreferences：不支持多进程

    * 内部存储：卸载时，会被移除

    * 外部存储：全局可读

      存储方式分两种

      * 卸载后，会被删除：context.getExternalFilesDir(null).getPath() 私有存储目录，null 指定的是根目录

        > 从 Android4.4 开始，读取或写入应用私有目录中的文件不再需要 READ_EXTERNAL_STORAGE 或 WRITE_EXTERNAL_STORAGE 权限

      * 永久存储：Environment.getExternalStorageDirectory().getAbsolutePath()

    * SQLite

    * 网络连接

  * 数据上报策略

    策略配置：

    * INSTANT
    * ONLY_WIFI
    * BATCH：批量，默认达到 30 条发送一次
    * APP_LAUNCH
    * DEVELOPER：开发者模式，调用方法发送，否则缓存到本地
    * PERIOD：间隔发送

* 前端埋点

  技术要求：

  * 数据的准确性和及时性
  * 埋点的效率
  * 动态部署与修复埋点的能力

  三类：

  * 代码埋点：友盟、百度统计等第三方数据统计服务商

  * 可视化埋点：通过可视化工具配置采集节点，“无痕埋点”，代表方案 Mixpanel

  * “无埋点”：前端自动采集全部事件并上报埋点数据，在后端进行数据计算时过滤出有用数据，代表方案 GrowingIO。

    实现 onClick 统计参考方案要点：

    * 通过 Hook LayoutInflater 的方式，遍历所有的 View 并且将 ID 一一设置到 Tag 里面
    * 通过 Javassist （AOP）将统计代码注入 onClick 方法里，获取 View 的 ID，并且上传统计
    * 手动将 View ID 与对应的 View 事件的描述对应起来



## 第 2 章 Android 下的工具基建进阶

### 带有反劫持功能的下载 SDK

#### 分段式多线程网络通信

如何分割文件：

* HTTP 请求头通知目标服务器本次网络请求的文件目标范围



多线程阻塞优化：分段 1 下载完成时，如果分段 2 还没开始下载，则负责下载分段 1 的线程继续下载分段 2，同时移除原先负责下载分段 2 的线程。

* 优化后的分段为：每一段的起始位置都处于自己的等分点，而结束位置都是文件尾部。一个分段线程下载到当前分段下载量的位置时，先判断下一分段是否已启动下载，如果未启动，则移除负责下载下一分段的线程，并由下载当前分段的线程负责下载，同时更新当前分段的下载量为增加下一个分段的下载量。如果已启动，则停止当前分段。
  * 解决因线程阻塞导致分段等待下载的问题
  * 减少发起网络请求



#### 常见的下载劫持

主要发生在网络层，细分：

* DNS 解析劫持
* 篡改 HTTP 请求头
* 篡改 HTTP 请求体等

具体劫持实现方式中，最常见的是运营商劫持。



#### 下载劫持监控

* 验证下载后**文件大小**是否与预设值一致。（下载文件前，是可以提前知道目标文件的大小的）
* 下载完成后，解析下载完成的 App 的**包名、版本号**。

如果只是某个区分渠道来源的标识改变了，上面两种方案还是会一样。这样在下载后，如果用户使用该文件，可能相关的收费统计都会被归于实施劫持的那个渠道。

* 计算整个文件的  **MD5** 值。（最耗时但最准确）

### 

#### 在下载中实现反劫持

上一节介绍的是监控下载劫持，但我们的目标是下载正确的资源文件。（如果监控到劫持但却啥也做不了，也是个问题）

最主要手段：使用 HTTPS 协议访问



### 沉浸式交互组件

沉浸式可以分为 3 个阶段：

* 19~21：可以实现沉浸式，但表现一般
  * 实现方式：通过 FLAG_TRANSLUCENT_STATUS 设置状态栏为透明和全屏模式，添加一个与 StatusBar 一样尺寸的 View，通过设置该 view 颜色实现沉浸式
* 21+：`android:statusBarColor` 属性
* 23+：可以改变状态栏字体和图标颜色



适配主流厂商：

* MIUI 适配：在 Android6.0 之前，MIUI 使用的是自定义方法，需要通过反射对状态栏颜色进行设置

* OPPO 适配：在 Android5.0 之前是系统方法，之后的 Color OS 版本需要适配

  > ImmersionBar 库没看到有适配 OPPO。

* 魅族：Android 6.0 之前需要适配



### 基于信息流的图片加载框架

负载、渲染、多线程、内存处理等技术。

* 图片加载库选择考虑
  * 图片的加载速度
  * 占用的内存缓存大小
  * 是否支持 JPG、PNG、GIF 和 SVG 等图片格式
  * 库代码的大小
  * 列表图片是否可以高复用
* 图片缓存机制
  * 三层缓存
    * Bitmap 内存缓存
      * 存储 Bitmap 对象
      * Android 5.0 以下位于 ashmem（匿名共享内存区域，此内存区域可无限扩大，不受 APP 限制），这样 Bitmap 对象的创建和释放将不会引发 GC。
      * Android 5.0 及以上，Bitmap 内存缓存直接位于 Java heap 上
    * 未解码图片内存缓存
      * 存储原始压缩格式的图片，需要先解码再使用
    * 磁盘缓存
  * 减少内存占用大小的方案
    * 根据控件尺寸获得对应大小的 Bitmap
    * 使用 RGB_565 显示，缺点是清晰度不高
  * Bitmap 回收机制
    * Android 2.3.3 及以下：Bitmap 的像素数据存储在 native 内存，但其依然会计算在一个进程的内存上限中
    * Android 3.0~4.4 版本：Bitmap 像素存储在 Java 堆，解码 Bitmap 时可以通过 Options#inBitmap 复用不再使用的 Bitmap，从而减少系统 GC 操作。但要求被复用的 Bitmap 和新的 Bitmap 的像素数据一样大。
    * Android 5.0 及以上：对于复用的 Bitmap，不再严格要求其像素数据与新 Bitmap 的一样大，只要求复用的 Bitmap 的像素数据不小于新 Bitmap 的像素数据即可。
  * 图片加载的流程
    * Bitmap 内存缓存是否存在图片；未解码图片内存缓存是否存在；磁盘缓存是否存在；网络下载
* 图片加载过程中遇到的问题
  * 通过 APK 路径获取 icon 图片的 Bitmap
  * 通过应用包名获取 icon 图片的 Bitmap
  * 加载超大图 OOM
    * 获取图片的宽和高 inJustDecodeBounds = true
    * 根据图片的宽度和高度计算缩放比 inSampleSize
    * 根据缩放比将图片加载到内存中
  * 列表图片很多时，快速来回滑动会卡顿
    * 原因：滑动导致 item 项频繁重用和销毁，进而导致图片中的 Bitmap 被频繁地创建和销毁
    * 解决方案：滚动时，暂停加载；停止滚动时，恢复加载任务
      * ListView#setOnScrollListener(...)
      * RecyclerView#addOnScrollListener(...)
  * 列表图片显示错位、出现闪烁问题
    * 原因：列表的复用机制
    * 解决：getView 时给对象提供一个标识，在异步加载完成时比对标识与当前行 item 的标识是否一致，一致则显示，否则不做处理
  * 加载图片时只显示了一部分
    * 原因：ImageView 的高度被设置为 WRAP_CONTENT，在加载图片时，会先设置一个 loading 的展位图，这就导致 item 在计算显示高度时开始只能计算占位图的高度
    * 两个解决方案：
      * WRAP_CONTENT 改为准确值
      * 图片下载成功的监听回调中，通知 ImageView 父布局做一次重绘操作，即调用 requestLayout 方法
  * 加载图片变绿的问题
    * 原因：图片压缩，在使用 WebP 图片时出现可能性较大
    * 解决：将默认的 Bitmap 编码格式 RGB565 更改成 ARGB_8888
* 基于信息流的图片加载设计
  * API 使用层
  * 核心层：图片下载的请求分发处理
  * 缓存层：解码后的 Bitmap 内存缓存、原始未解码的 Bitmap 内存缓存以及磁盘缓存
* 进程保活



### Android 文件系统扫描

### 高可用前置通道

前置通道包括：常驻通知栏、消息推送、桌面悬浮窗等。



## 第 3 章 Android 下的效能进阶

### Android 性能监测实现

启动速度、内存监测、页面卡顿等

* BlockCanary：利用 Looper 队列在处理主线程消息之前和之后提供的日志打印接口

  * 缺点是粒度不够细

* 启动速度

  * Activity：registerActivityLifecycleCallbacks
  * Fragment：Lifecycle 框架

* 内存监测系统

  * 原理：在 Activity 和 Fragment onDestroy 的时候，将对象用 WeakReference 引用起来，监听对象是否发生内存泄露，通过 WeakReference 和 ReferenceQueue<Object> 配合使用，如果弱引用引用的对象被 GC（垃圾回收），则 Java 虚拟机就会把这个弱引用加入与之关联的引用队列，然后主动执行 GC，触发 WeakReference 被 GC，同时检测 GC 前后 ReferenceQueue 是否包含被监听对象，如果不包含，则说明该对象没有被 GC，一定存在到 GC Roots 的强引用链，也就是发生了内存泄露。

* 页面卡顿解决方案

  * 原理：通过设置主线程 Looper 日志，在主线程接收到消息并开始执行时，延时 500ms 新建子线程记录当前的堆栈信息，如果主线程在 500ms 内执行完则取消子线程，如果主线程超过 2s 才执行完则获取子线程保存的堆栈信息上报。

* 处理 App 性能问题的经验

  * 合理使用 static 成员
  * merge、include
  * 延迟加载 View；使用 ViewStub
  * 动态注册的广播要记得反注册
  * ListView 性能优化
    * item 布局
    * 背景色与 cacheColorHint 设置相同颜色
    * getView 重用 View
    * 考虑分页加载
  * 注意使用线程的同步（synchronized）机制，防止多个线程同时访问一个对象时发生异常
  * 合理使用 StringBuffer、StringBuilder、String
  * 执行后 IO 操作，记得关闭
  * 使用 IntentService 代替 Service
  * 使用 Application Context 代替 Activity 中的 Context
  * 及时清理集合中的对象
  * Bitmap 的使用
    * 较大 Bitmap 压缩后使用；加载高清大图考虑使用 BitmapRegionDecoder；使用完调用 recycle
  * 巧妙运用 SoftReference
  * 尽量不要使用整张大图作为资源文件，尽量使用 9patch

  

### App 真机检测系统

* 真机控制服务器、真机连接 Hub 等
* monkey 检测
* 自动化敏感权限检测



### APK 信息一站式修改

* APK 文件构成
* APK 签名校验流程
* V1 与 V2 签名
* 如何打造渠道包
  * V1原理：在 APK 文件的注释字段中添加动态信息
  * V2：在 APK 签名块中添加一个 ID-Value 并赋值。



## 第 4 章 Android 工具应用进阶

### 游戏加速器

### 近场传输

### 微信清理

### Google 安装器



## 第 5 章 Android 工程构建进阶























