### 在当前目录打开

系统偏好设置 -> 键盘 -> 快捷键 -> 服务 -> 新建位于文件夹位置的终端窗口

设置完后，在文件夹右键 -> 服务中启动终端 



### 设置大小不敏感

> 终端在输入时默认会区分大小写，这样导致 tab 自动补全时不太方便

[Case insensitive tab completion in Bash](https://superuser.com/questions/90196/case-insensitive-tab-completion-in-bash)

在 `~/.inputrc` 中添加

`set completion-ignore-case on`，重新启动终端生效