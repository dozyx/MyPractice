> 注意：Git 中没有 shelve，只有 stash。shelve 是 IDE 自带功能。

git stash 用于将改动保存到一个 dirty 的工作目录。这样我们就可以得到一个干净的工作目录来进行修改，而不必受已修改代码的影响。

「Use `git stash` when you want to record the current state of the working directory and the index, but want to go back to a clean working directory.  The command saves your local modifications away and reverts the working directory to match the `HEAD` commit.」

语法：

```shell
git stash list [<options>]
git stash show [<stash>]
git stash drop [-q|--quiet] [<stash>]
git stash ( pop | apply ) [--index] [-q|--quiet] [<stash>]
git stash branch <branchname> [<stash>]
git stash [push [-p|--patch] [-k|--[no-]keep-index] [-q|--quiet]
	     [-u|--include-untracked] [-a|--all] [-m|--message <message>]
	     [--] [<pathspec>…]]
git stash clear
git stash create [<message>]
git stash store [-m|--message <message>] [-q|--quiet] <commit>
```



### 常用指令

+ `git stash` - 同 `git stash push`，保存修改并还原。可以使用 `-m` 添加说明信息，不过此时需要带上 push 才能实现保存。
+ `git stash list` - 列出保存条目
+ `git stash show` - 查看修改 stash 内容
+ `git stash apply` - 还原
+ `git stash pop` - 还原上一个条目，与 apply 的一个区别在于 pop 还原后不会保留 stash 记录。
+ `git stash drop` - 丢弃某一条目
+ `git stash clear` - 清空所有 stash 记录
+ `git stash branch <branchname> [<stash>]` - 将 stash 中的修改放到一个新分支中。

> 还有基本不会用到的 create 和 store，create 会创建一个 stash 条目并返回名称（类似于 commit），并且不会保存到 ref 空间，然后使用 store 可以保存到 ref 中。这两个指令一般用于脚本中。



### git shelve

git shelve 是 IDEA 的一项特性，它不会将修改保存到 Git 版本控制中，而是使用 IDE 自身的保存。

> 以前 shelve 与 stash 的一个区别在于，shelve 可以对单个修改文件进行保存，不过最新版本的 Git 也实现了使用 stash 来保存单个修改文件。
>
> 那 shelve 与 stash 的区别就只在于存放位置的区别了？google 后，好像的确是这样。。。

### 总结

+ 保存并还原的是本地所做的更改，不会对没有在版本控制系统中的内容造成影响。
+ 通过 stash，我们可以创建一个基于 HEAD 版本的工作空间来进行临时的工作并不会丢失已做修改。



参考：

[git stash](https://git-scm.com/docs/git-stash)

[Git Shelve vs Stash](https://stackoverflow.com/questions/28008139/git-shelve-vs-stash)