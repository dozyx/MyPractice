cherry-pick：应用一个或多个 commit 里的变更，并为每一条 commit 创建新的 commit。

### 语法

```shell
git cherry-pick [--edit] [-n] [-m parent-number] [-s] [-x] [--ff] [-S[<keyid>]] <commit>…
git cherry-pick --continue
git cherry-pick --quit
git cherry-pick --abort
```

* -x

  创建新的 commit 时，为原始的 commit 信息拼接一行 "(cherry picked from commit …)" 。如果是从私有的分支进行 cherry-picking，则不需要这样做。



### 示例

* `git cherry-pick <commit-hash>`

  应用某个 commit

* `git cherry-pick master`

  应用 master 最顶端的 commit



参考：

[cherry-pick](https://git-scm.com/docs/git-cherry-pick)