### 别名 alias

1. 编写一个别名文件， 按以下方式将文件引入 .gitconfig 中。[文件地址](https://github.com/GitAlias/gitalias/blob/master/gitalias.txt)

   ```
   [include]
       path = gitalias.txt
   ```

2. 命令行设置

   ```
   $ git config --global alias.co checkout
   $ git config --global alias.unstage 'reset HEAD --'
   ```

#### 查看已配置的别名

`git config --get-regexp alias`

> 如果引入了上面的 gitalias 文件，则可以使用别名来查看 git aliases

如果想要查看某个缩写代表的指令：

`git config alias.[缩写]`

删除某个别名：

`git config --global --unset alias.trololo`

> 好像对自定义文件定义的别名无效。

参考：

[List Git aliases](https://stackoverflow.com/questions/7066325/list-git-aliases)



#### alias 里的 !

 在 gitalias.txt 中有的别名对应的指令带有 !，表示该指令将作为 shell 命令执行。

参考：

[What does the exclamation mark mean in git config alias?](https://stackoverflow.com/questions/21083933/what-does-the-exclamation-mark-mean-in-git-config-alias)

### 修改 git bash 启动路径

+ 右键属性
+ 删除 “目标” 末尾的 `--cd-to-home`
+ 将起始位置改为启动路径



### git status 中文乱码

乱码：

`"\346\265\213\350\257\225.txt"`

解决方法：

`git config --global core.quotepath false`



参考：    

[Git实用小技巧：git status 中文文件名编码问题解决](http://blog.csdn.net/mlq8087/article/details/52174834)

### 