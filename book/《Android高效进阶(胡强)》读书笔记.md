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