







### 问题记录

#### NoClassDefFoundError

在使用过程中有时会打印一大堆信息

```bash
 Rejecting re-init on previously-failed class java.lang.Class<org.greenrobot.greendao.database.DatabaseOpenHelper$EncryptedHelper>: java.lang.NoClassDefFoundError: Failed resolution of: Lnet/sqlcipher/database/SQLiteOpenHelper;
 ...
 ...
```

这些打印的 level 为 info，所以不会对程序运行带来什么影响，只是看着感觉不安，所以想找出问题在哪。经过一番所搜，发现这个问题跟 instant run 有关，关闭 instant run 后正常。

> 虽然没有找到为什么 instant run 会导致此问题，但至少心安了一点。





参考：

[NoClassDefFoundError - Rejecting re-init on previously-failed class](https://stackoverflow.com/questions/12696561/noclassdeffounderror-rejecting-re-init-on-previously-failed-class/35751439#35751439)