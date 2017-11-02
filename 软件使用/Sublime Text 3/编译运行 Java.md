
> 目的：编写 Java 文件，Ctrl + B 运行，在 Sublime Text 控制台输出结果。

为了实现编译 + 运行功能，我们需要修改 Sublime Text 的编译系统文件 `.sublime-build`

### OS X 系统

+ 打开 Packages    
`$ cd /Applications/Sublime\ Text.app/Contents/MacOS/Packages/`

+ 创建一个临时目录    
`$ mkdir java`

+ 将 「Java.sublime-package」复制到临时目录中    

`$ cp Java.sublime-package java/`
`$ cd java`

+ 解压 「Java.sublime-package」    
`$ unzip Java.sublime-package`

+ 编辑  JavaC.sublime-build 配置文件,将里面的内容改为    
```json
{
    "cmd": ["javac \"$file_name\" && java \"$file_base_name\""],
    "shell": true,
    "file_regex": "^(...*?):([0-9]*):?([0-9]*)",
    "selector": "source.java"
}
```
 
+ 压缩文件并替换原来的文件    
`$ zip Java.sublime-package *`
`$ mv Java.sublime-package ../`

+ 删除临时目录    
`$ cd ..`
`$ rm -fr java/`

+ 重启 Sublime Text，Ctrl +B 运行    

### Windows 

+ 编写一个 runJava.bat 脚本文件，内容如下：
```shell
@ECHO OFF  
cd %~dp1  
ECHO Compiling %~nx1.......  
IF EXIST %~n1.class (  
DEL %~n1.class  
)  
javac %~nx1  
IF EXIST %~n1.class (  
ECHO -----------OUTPUT-----------  
java %~n1  
)  
```

+ 将 runJava.bat 放到 JDK 安装目录的 bin 文件夹内（bin 目录需要已经添加到环境变量的 PATH 中）

+ 找到 Sublime Text 3 的安装目录，使用压缩文件打开 Java.sublime-package 文件（不需要解压），修改 JavaC.sublime-build 文件
```yaml
{  
    "cmd": ["runJava.bat", "$file"],  
    "file_regex": "^(...*?):([0-9]*):?([0-9]*)",  
    "selector": "source.java",  
    "encoding": "gbk"  
}  
```

+ 保存退出后，Ctrl + B 即可编译并输出结果。

参考：    
[How to run Java using Sublime Text 3 on Mac OS](https://stackoverflow.com/questions/24319143/how-to-run-java-using-sublime-text-3-on-mac-os)    
[Sublime Text 3 编译/运行Java程序](https://zhuanlan.zhihu.com/p/25820430)    
[在Sublime Text 3上编译和运行java程序（亲测通过）](http://blog.csdn.net/ksearch/article/details/20701495)    
