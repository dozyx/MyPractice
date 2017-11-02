[How to run Java using Sublime Text 3 on Mac OS](https://stackoverflow.com/questions/24319143/how-to-run-java-using-sublime-text-3-on-mac-os)

[Sublime Text 3 编译/运行Java程序](https://zhuanlan.zhihu.com/p/25820430)



> 在 Sublime Text 中编写一个代码文件，然后按下 Ctrl + B，将会对文件进行编译，但并不会显示出运行结果，如一个 Hello.java 文件，Ctrl + B，将自动编译为一个 Hello.class 文件，Sublime Text 只会输出 “[Finished in XXs]”。 为了实现代码的运行，需要对修改对应的配置文件。下面以 Java 文件为例。



### OS X 系统

Sublime Text 构建系统的配置数据保存在 .sublime-build 后缀文件中，

先打开 Packages

> $ cd /Applications/Sublime\ Text.app/Contents/MacOS/Packages/

创建一个临时目录

> $ mkdir java

将 「Java.sublime-package」复制到临时目录中

> $ cp Java.sublime-package java/
>
> $ cd java

解压 「Java.sublime-package」

> $ unzip Java.sublime-package

接下来编辑  JavaC.sublime-build 配置文件

将里面的内容改为

```json
{
    "cmd": ["javac \"$file_name\" && java \"$file_base_name\""],
    "shell": true,
    "file_regex": "^(...*?):([0-9]*):?([0-9]*)",
    "selector": "source.java"
}
```

（主要就是在 javac 后面加了 java 部分）

最后压缩文件并替换原来的文件

> $ zip Java.sublime-package *
>
> $ mv Java.sublime-package ../

删除临时目录

> $ cd ..
>
> $ rm -fr java/

现在，重启 Sublime Text，重新运行代码，就可以直接在 Sublime Text 中看到输出。



### Windows 

编写一个 runJava.bat 脚本文件，内容如下：

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

将 runJava.bat 放到 JDK 安装目录的 bin 文件夹内（bin 需要已经添加到环境变量的 PATH 中）

找到 Sublime Text 3 的安装目录，使用压缩文件打开 Java.sublime-package 文件（不需要解压），打开 JavaC.sublime-build 文件，修改内容为

```yaml
{  
    "cmd": ["runJava.bat", "$file"],  
    "file_regex": "^(...*?):([0-9]*):?([0-9]*)",  
    "selector": "source.java",  
    "encoding": "gbk"  
}  
```

保存退出后，Ctrl + B 即可编译并输出结果。