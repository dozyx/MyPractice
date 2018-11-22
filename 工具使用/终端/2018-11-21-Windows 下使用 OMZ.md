> 20181121：经过一上午折腾，最终放弃了在 Windows 下使用 omz，因为有些问题比较困扰： cmder 无法记忆上一次 babun 窗口的状态；有的项目 push 失败。一开始想要使用 omz 主要是为了统一 mac 与 windows 作业时的 alias，所以改为将 omz 的 alias 移到 cmder 的方式。omz 的 alias 文件位置 C:\Users\Administrator\.babun\cygwin\home\Administrator\.oh-my-zsh\plugins\git。

环境：Windows + Babun + Cmder



[让 Windows 用上 OMZ 的神器 Babun](https://www.hi-linux.com/posts/57246.html)



注：

+ Windows 下使用 omz 可能会比较卡，所以个人改用了 babun 自带的 mintty
+ 个人使用主题为 kolo



### 使用问题整理

#### 执行 git status 显示所有问题状态都是 modified

解决：`git config --global core.autocrlf=true`

原因：不同系统的行尾换行不统一