在分支上 push 时发生以下错误：

>warning: redirecting to http://xxxxxxxxxxxxxxxxxxxxx
>To http://gitlab.xxxxxxxxxxxxxx
>! [rejected]        pos_bound -> pos_bound (non-fast-forward)
>error: failed to push some refs to 'http://gitlab.xxxxxxxxxxxxxxxx'
>hint: Updates were rejected because the tip of your current branch is behind
>hint: its remote counterpart. Integrate the remote changes (e.g.
>hint: 'git pull ...') before pushing again.
>hint: See the 'Note about fast-forwards' in 'git push --help' for details.

并且出现了一堆的冲突，不过那些文件只在分支上有 commit 过。具体流程是：

1. 分支开发
2. commit A 没有进行 push
3. rebase master
4. commit B 并进行 push，失败并出现冲突文件

首先要解决冲突文件并恢复 commit 前修改文件，我通过执行下面的命令来取消了 commit，并保留了 commit 前的文件修改

`git reset --soft HEAD~1`

接着经过一番搜索，发现使用 `git push -f` 后能 push 成功。





参考：

[How do I delete unpushed git commits?](https://stackoverflow.com/questions/3197413/how-do-i-delete-unpushed-git-commits)

[Git push rejected after feature branch rebase](https://stackoverflow.com/questions/8939977/git-push-rejected-after-feature-branch-rebase)

[Updates were rejected because the tip of your current branch is behind](https://stackoverflow.com/questions/39399804/updates-were-rejected-because-the-tip-of-your-current-branch-is-behind)

