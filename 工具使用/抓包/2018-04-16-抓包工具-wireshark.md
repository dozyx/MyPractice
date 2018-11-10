> 20180416:
>
> 尽管今天加班到了九点半，而且问题没有解决，眼睛也有点疼，但今天心情感觉还不错，因为今天接触到了一个新的抓包工具——wireshark，并看到了 tcp 通讯的完整过程。
>
> 很久之前就已经用过 Fiddler 进行抓包，不过今天要抓到数据是 Android 手机上的 Socket 数据，而 Fiddler 只能捕获 http 的数据，折腾了很长时间才顺利地将数据捕获到。但不足的是没能实现实时的数据抓取。



### 一些皮毛

wireshark 支持多中系统，尽管刚开始使用，但我却已经感觉到它的强大。

这次使用是在 win7 环境下使用的，本想实现实时抓包，不过有些命令没有运行起来，所以暂时先实现的是通过 adb 抓包保存到手机文件，再取出来使用 wireshark 分析。

环境：win7、android（已 root）

软件：wireshark（pc）、es 文件浏览器（android，方便操作文件）、终端模拟器（android，电脑直接通过 adb 没能进行 root 操作，但通过手机端模拟器输入 su 后得到 root 权限）

+ 下载 [tcpdump](http://www.androidtcpdump.com/)

+ 将 tcpdump 放置在 /system/xbin 目录，并修改权限（我是直接通过 es 浏览器操作的，简单粗暴）

  `http://www.androidtcpdump.com/`

  `chmod 777 /system/xbin/tcpdump`

+ 下载 [wireshark](https://www.wireshark.org/#download)

+ 抓包，执行下面命令后操作应用即可，Ctrl + C 结束抓包

  `adb shell tcpdump -i any -p -vv -s 0 -w /sdcard/capture.pcap`

+ 将文件 pull 到电脑中用 wireshark 打开进行分析（我是直接 es 浏览器分享到微信获取的。。）



### 用法

#### 过滤

+ 右键某一行数据，右键将该列的条件作为过滤条件。「作为过滤器应用」会立即将该条件应用为一个过滤器，「准备过滤器」会将该条件作为过滤器的条件之一，然后在 Filter 栏点击「应用此过滤器字符串进行显示」时应用新的过滤器。



### 分析

+ 图表：统计 -> 流量图。更直观地查看通讯过程

### 抓取实时数据

> 最简单的方式应该是 pc 提供一个热点，然后手机连接热点，wireshark 监听热点网络即可。



### 注意

+ 包中的 seq/ack 为相对序列号/相对确认号

参考：

[利用tcpdump+wireshark对android进行抓包分析](https://blog.csdn.net/shan987/article/details/47667073)