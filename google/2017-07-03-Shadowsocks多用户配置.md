---
title: Shadowsocks 多用户配置
tags:
  - shadowsocks
date: 2017-07-03 15:37:22
categories: 工具
---

[Configure Multiple Users](https://github.com/shadowsocks/shadowsocks/wiki/Configure-Multiple-Users)

[shadowsocks 多用户配置失败原因及解决方法](http://blog.csdn.net/helinlin007/article/details/51469656)

[How to Start and Enable Firewalld on CentOS 7](https://www.liquidweb.com/kb/how-to-start-and-enable-firewalld-on-centos-7/)

​	Shadowsocks 支持多用户使用不同的端口和密码进行登陆使用。

​	如果需要添加多用户，只需要编辑 /etc/shadowsocks.json 文件，然后在 port_password 字段配置用户端口和密码，如：

```json
{
    "server": "0.0.0.0",
    "port_password": {
        "8381": "foobar1",
        "8382": "foobar2",
        "8383": "foobar3",
        "8384": "foobar4"
    },
    "timeout": 300,
    "method": "aes-256-cfb"
}
```

在编辑完成后保存退出，重启Shadowsocks

```shell
# /etc/init.d/shadowsocks restart
```



### CentOS配置后无效

​	按照上面添加了多用户后，在 Shadowsocks 客户端仍不能使用其他端口进行登陆（CentOS 7）。原因在于centos 默认的防火墙机制，阻隔了我们的多端口配置。

​	这里有两种方法（第二种测试有效，第一种没验证）：

+ 第一种

  ```shell
  # iptables -A INPUT -p tcp –dport 443 -j ACCEPT
  ```

  （其中，443为示例端口，需修改为多用户配置的端口）

  重启防火墙

  ```shell
  # service iptables restart
  ```

+ 第二种

  打开 firewalled 配置端口文件

  ```shell
  # vi /etc/firewalld/zones/public.xml
  ```

  按以下形式添加端口到 public.xml 文件中

  ```xml
  <zone>
    ...
    <port protocol="udp" port="8080"/>
    <port protocol="tcp" port="8080"/>
    ...
  </zone>
  ```

  wq 保存退出后，重启防火墙

  ```shell
  # systemctl restart firewalld
  ```