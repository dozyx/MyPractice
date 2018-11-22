Oh My Zsh 是个管理 zsh 配置的框架，而 zsh 专为交互式使用的 shell。

[地址](https://github.com/robbyrussell/oh-my-zsh/)



### 功能

> 20181031 久仰 zsh 大名，但却不知它的强大在何处，于是装上再慢慢探索。

+ cd 自动补全 - 如，输入 cd，点击 tab，自动提示补全
+ git 别名 - omz 默认安装了 git 插件，提供了大量的 alias，如果想要查看某个 alias 表示的完整命令，可以使用如 `alias gaa` 查看，其中的 gaa 为一个 alias，如果想要查看哪些 alias 包含了某个命令，则可以使用类似 `alias |grep add`，add 表示想要查找的命令 。
+ 路径展开 - 如输入 `cd /u/lo/b`，点击 tab 后将自动补全为 `cd /usr/local/bin/`。



### 自定义 alias

`alias cdgit=[输入命令]`



### 主题

### 随机主题

编辑 `~/.zshrc`

```shell
ZSH_THEME="random"
```

### 输入当前使用主题

指定的主题 `echo $ZSH_THEME`

随机主题 `print $RANDOM_THEME`

