---
title: windowSoftInputMode 属性
tags:
  - android
  - 输入法
date: 2017-05-02 15:37:22
categories: 笔记
---

​	windowSoftInputMode 定义了当window显示时的软输入状态。对应于`android.view.WindowManager.LayoutParams#softInputMode`。

​	stateXXX为当前的window设置软输入区域（软键盘）的可见性状态；adjustXXX 定义window如何调整以适应软输入的窗口。

+ stateUnspecified

+ stateUnchanged

  不改变软输入区域的状态（保持之前的状态）

+ stateHidden

  在适当的时候隐藏软输入区域（用户导航到你的window）

+ stateAlwaysHidden

  当window获取到焦点时，总是使软输入区域处于隐藏状态

+ stateVisible

  在适当的时候显示软输入区域（用户导航到你的windows）

+ stateAlwaysVisible

  当window接收到输入焦点时，总是使软输入区域处于显示状态

+ adjustUnspecified

  没有指定，系统将根据 window 的内容选择。

+ adjustResize

  当输入法显示时，允许 window 重新调整大小，以使其内容不被输入法覆盖。该选项无法与 adjustPan 共同使用，如果它们两个都没设置，则系统将根据 window 的内容自行选择一个。如果 window 的layout 参数标记包括了 FLAG_FULLSCREEN，这个值将被忽略，window 将不会重新调整大小，而是保持全屏。

+ adjustPan

  当输入法显示时，将存在一个 window pan （窗口面板？），这样就不需要重新处理大小，而是由 framework 将window 进行 pan 从而保证输入焦点可见。

+ adjustNothing



#### stateHidden 和 stateAlwaysHidden

参考：https://developer.android.com/guide/topics/manifest/activity-element.html#wsoft

* stateHidden - 用户明确选择跳转到该 Activity 的情况（不是因为离开了另一个 Activity 而返回），隐藏软键盘
* stateAlwaysHidden - 当 Activity 的主窗口有输入焦点时始终隐藏软键盘。

#### adjustPan 和 adjustResize的区别

​	adjustPan 将导致整个 window 的上移（如一个Activity，上移后上面部分将被遮挡）。一般adjustResize显示效果更好。

adjustResize：（EditText和TextView原本均在底部居中）

![adjustResize](https://ws2.sinaimg.cn/large/006tKfTcgy1finvgjv4mkj309d0gqaah.jpg)

adjustPan：

![adjustPan](https://ws4.sinaimg.cn/large/006tKfTcgy1finvgkam3fj309e0grjrs.jpg)