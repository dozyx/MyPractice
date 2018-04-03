官方地址：[XX-Net](https://github.com/XX-net/XX-Net/)





## 注意

+ Xx-net 中有的 X-Tunnel 使用的端口与 shadowsocks 冲突，默认都是 1080。（网上说修改 client.json 文件，但 3.11.1 版本没找到，所以如果真的有需要可以修改 shadowsocks 的端口）



## 问题解决

### Mac 10.13.3 系统无法启动

#### 描述

xx-net 版本：3.11.1

点击 start 文件后桌面没有生成图标，终端显示以下内容

```shell
MrdeMacBook-Pro:~ zero$ /Users/.../XX-Net/start ; exit;
XX-Net version:default
logout
Saving session...
...copying shared history...
...saving history...truncating history files...
...completed.
```

127.0.0.1:8085 地址也打不开。

#### 解决

> 尝试使用 3.10.8 版本也不行。暂时不折腾了，shadowsocks用着挺好的。