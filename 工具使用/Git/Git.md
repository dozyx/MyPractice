#### 修改 git bash 启动路径

+ 右键属性
+ 删除 “目标” 末尾的 `--cd-to-home`
+ 将起始位置改为启动路径



#### git status 中文乱码

乱码：

`"\346\265\213\350\257\225.txt"`

解决方法：

`git config --global core.quotepath false`



参考：    

[Git实用小技巧：git status 中文文件名编码问题解决](http://blog.csdn.net/mlq8087/article/details/52174834)

### 