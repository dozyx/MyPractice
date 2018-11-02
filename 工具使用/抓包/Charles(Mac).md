使用：

- 勾选 Proxy -> MacOS Proxy
- 抓取chrome数据：将chrome代理设为使用系统代理；如果chrome使用了扩展插件进行代理，如Proxy SwitchyOmega，需要添加并使用代理127.0.0.1:8888(注意：如果使用了shadowsocks，需要将其关闭)
- 抓取 https 信息：“Help” –> “SSL Proxying” –> “Install Charles Root Certificate”；安装完后，charles默认不会拦截https信息，需要在右键该网络，勾选enable ssl proxying
- 过滤：Proxy->Recording Settings->inclue->Add,Port填*;还有一种过滤方法是选择Sequence视图，在 Filter 中输入

一些概念：

- Throttling 模拟网络速度
- 

问题：

- 无数据：系统偏好设置 -> 网络 -> 高级 -> 代理，查看是否为 http 代理并且代理服务器为127.0.0.1:8888;如果系统有其它代理软件，如shadowsocks，需要将其关闭，然后再次开启 charles 的 MacOS Proxy开关，这样软件将自动修改代理。
- 没有 Request 和 Response 视图：Preference -> Viewers -> 取消combine request and response；需要注意，要当前url有Request和Response才会显示
- Request和Response乱码：安装完证书后，Proxy -> SSL Proxying Settings -> SSL Proxying -> Add;Host 填 *，Port 填443。设置完后可取消 enable ssl proxying