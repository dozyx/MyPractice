Android Studio 代码风格文件：    
[官方AndroidStyle](https://github.com/aosp-mirror/platform_development/blob/master/ide/intellij/codestyles/AndroidStyle.xml)    
个人基于此风格使用 AS 并做下列修改：

- AndroidStyle 中的 XML 格式不是标准的 Android 风格，需要改成内置的：Android Studio -> Settings -> Editor -> Code Style -> XML -> Set from... -> Android
- 全局变量前不加 m（《代码整洁之道》中提及，细想的确是多余的，完全可以依靠IDE与局部变量进行区分）：Android Studio -> Settings -> Editor -> Code Style -> Java -> Code Generation -> Naming -> 去掉 Field 的 m 前缀

### 包与类


+ 将通用的基类放于 common 包中，如 adapter、activity
+ 考虑以 Helper 而不是 Util 作为后缀



### 代码

+ 使用 Objects.equals 判断是否逻辑相等

  ​

### 资源文件

#### drawable 文件

| 类型           | 前缀              | 示例                         |
| ------------ | --------------- | -------------------------- |
| Action bar   | `ab_`           | `ab_stacked.9.png`         |
| Button       | `btn_`          | `btn_send_pressed.9.png`   |
| Dialog       | `dialog_`       | `dialog_top.9.png`         |
| Divider      | `divider_`      | `divider_horizontal.9.png` |
| Icon         | `ic_`           | `ic_star.png`              |
| Menu         | `menu_`         | `menu_submenu_bg.9.png`    |
| Notification | `notification_` | `notification_bg.9.png`    |
| Tabs         | `tab_`          | `tab_pressed.9.png`        |



#### icon 图标命名

icon 指的是非 xml 文件的图片资源

| 类型                              | 前缀               | 示例                         |
| ------------------------------- | ---------------- | -------------------------- |
| Icons                           | `ic_`            | `ic_star.png`              |
| Launcher icons                  | `ic_launcher`    | `ic_launcher_calendar.png` |
| Menu icons and Action Bar icons | `ic_menu`        | `ic_menu_archive.png`      |
| Status bar icons                | `ic_stat_notify` | `ic_stat_notify_msg.png`   |
| Tab icons                       | `ic_tab`         | `ic_tab_recent.png`        |
| Dialog icons                    | `ic_dialog`      | `ic_dialog_info.png`       |



#### selector 状态

| 状态       | 后缀          | 示例                         |
| -------- | ----------- | -------------------------- |
| Normal   | `_normal`   | `btn_order_normal.9.png`   |
| Pressed  | `_pressed`  | `btn_order_pressed.9.png`  |
| Focused  | `_focused`  | `btn_order_focused.9.png`  |
| Disabled | `_disabled` | `btn_order_disabled.9.png` |
| Selected | `_selected` | `btn_order_selected.9.png` |



### XML 风格

资源 id 采用`小写+下划线`命名。

#### ID 名称

| 元素          | 前缀        |
| ----------- | --------- |
| `TextView`  | `text_`   |
| `ImageView` | `image_`  |
| `Button`    | `button_` |
| `Menu`      | `menu_`   |

> 遵循此规则的话，在声明变量时，也需要将元素名作为前缀，如 textXXX。

#### 字符串

String 的名称前缀表明它们所属的功能块，如`registration_email_hint` 和 `registration_name_hint`。如果不属于任何功能块，遵循以下规则：

| 前缀        | 描述                                   |
| --------- | ------------------------------------ |
| `error_`  | An error message                     |
| `msg_`    | A regular information message        |
| `title_`  | A title, i.e. a dialog title         |
| `action_` | An action such as "Save" or "Create" |



#### Styles 和 Themes

按 **UpperCamelCase** 大驼峰命名。



### 参考 

[android-guidelines](https://github.com/ribot/android-guidelines/blob/master/project_and_code_guidelines.md) 这里面给出的很多命名的前缀都比较符合我的想法    




[阿里巴巴Java开发手册](https://github.com/alibaba/p3c/blob/master/%E9%98%BF%E9%87%8C%E5%B7%B4%E5%B7%B4Java%E5%BC%80%E5%8F%91%E6%89%8B%E5%86%8C%EF%BC%88%E7%BB%88%E6%9E%81%E7%89%88%EF%BC%89.pdf)    
【强制】构造方法里面禁止加入任何业务逻辑，如果有初始化逻辑，请放在 init 方法中。      
【强制】POJO 类必须写 toString 方法。    
【推荐】setter 方法中，参数名称与类成员变量名称一致，this.成员名 = 参数名。在 getter/setter 方法中，不要增加业务逻辑，增加排查问题的难度。    
【强制】创建线程或线程池时请指定有意义的线程名称，方便出错时回溯。    
【强制】线程资源必须通过线程池提供，不允许在应用中自行显式创建线程。    
【强制】线程池不允许使用 Executors 去创建，而是通过 ThreadPoolExecutor 的方式，这样的处理方式让写的同学更加明确线程池的运行规则，规避资源耗尽的风险。    
【强制】高并发时，同步调用应该去考量锁的性能损耗。能用无锁数据结构，就不要用锁；能锁区块，就不要锁整个方法体；能用对象锁，就不要用类锁。    
【参考】谨慎注释掉代码。在上方详细说明，而不是简单地注释掉。如果无用，则删除。    

【推荐】及时清理不再使用的代码段或配置信息。    
说明：对于垃圾代码或过时配置，坚决清理干净，避免程序过度臃肿，代码冗余。    
正例：对于暂时被注释掉，后续可能恢复使用的代码片断，在注释代码上方，统一规定使用三个斜杠(///)来说明注释掉代码的理由。     
【强制】对大段代码进行 try-catch，这是不负责任的表现。catch 时请分清稳定代码和非稳定代码，稳定代码指的是无论如何不会出错的代码。对于非稳定代码的 catch 尽可能进行区分异常类型，再做对应的异常处理。    
【强制】捕获异常是为了处理它，不要捕获了却什么都不处理而抛弃之，如果不想处理它，请将该异常抛给它的调用者。    
【推荐】方法的返回值可以为 null，不强制返回空集合，或者空对象等，必须添加注释充分说明什么情况下会返回 null 值。调用方需要进行 null 判断防止 NPE 问题。    
说明：本手册明确防止 NPE 是调用者的责任。即使被调用方法返回空集合或者空对象，对调用者来说，也并非高枕无忧，必须考虑到远程调用失败、序列化失败、运行时异常等场景返回null 的情况。    
【参考】在代码中使用“抛异常”还是“返回错误码”，对于公司外的 http/api 开放接口必须使用“错误码”；而应用内部推荐异常抛出；跨应用间 RPC 调用优先考虑使用 Result 方式，封装 isSuccess()方法、“错误码”、“错误简短信息”。

【强制】应用中不可直接使用日志系统（Log4j、Logback）中的 API，而应依赖使用日志框架 SLF4J 中的 API，使用门面模式的日志框架，有利于维护和各个类的日志处理方式统一。    
    import org.slf4j.Logger;    
    import org.slf4j.LoggerFactory;    
    private static final Logger logger = LoggerFactory.getLogger(Abc.class);     



关于基本数据类型与包装数据类型的使用标准如下：

1. 【强制】所有的 POJO 类属性必须使用包装数据类型。
2. 【强制】RPC 方法的返回值和参数必须使用包装数据类型。
3. 【推荐】所有的局部变量使用基本数据类型。    
  说明：POJO 类属性没有初值是提醒使用者在需要使用时，必须自己显式地进行赋值，任何 NPE 问题，或者入库检查，都由使用者来保证。    
  正例：数据库的查询结果可能是 null，因为自动拆箱，用基本数据类型接收有 NPE 风险。    
  反例：比如显示成交总额涨跌情况，即正负 x%，x 为基本数据类型，调用的 RPC 服务，调用不成功时，返回的是默认值，页面显示为 0%，这是不合理的，应该显示成中划线。所以包装数据类型的 null 值，能够表示额外的信息，如：远程调用失败，异常退出。     

共享常量位置：
1. 跨应用共享常量：放置在二方库中，通常是 client.jar 中的 constant 目录下。
2. 应用内共享常量：放置在一方库中，通常是 modules 中的 constant 目录下。    
  反例：易懂变量也要统一定义成应用内共享常量，两位攻城师在两个类中分别定义了表示“是”的变量：    
  类 A 中：public static final String YES = "yes";    
  类 B 中：public static final String YES = "y";    
  A.YES.equals(B.YES)，预期是 true，但实际返回为 false，导致线上问题。
3. 子工程内部共享常量：即在当前子工程的 constant 目录下。
4. 包内共享常量：即在当前包下单独的 constant 目录下。
5. 类内共享常量：直接在类内部 private static final 定义。



