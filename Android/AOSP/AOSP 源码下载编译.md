---
title: Android 源码下载编译
tags:
  - android
date: 2017-02-11 15:37:22
categories: 笔记
---

[Android系统源码学习步骤](http://www.cnblogs.com/xiaoran1129/archive/2012/11/02/2751446.html)  
[Android Source](https://source.android.com/source/index.html)  
[MacPorts卡在"正在运行软件包脚本"解决方法](http://blog.csdn.net/ruiqiangzh/article/details/51017342)  
[Mac OS X 下 Android6.0源码的下载与编译](http://blog.csdn.net/loften_93663469/article/details/51503293)  
[Android 镜像使用帮助](https://mirrors.tuna.tsinghua.edu.cn/help/AOSP/)

[解决macOSX10.12.SDK下编译Android Open Source Project出错的问题](http://palanceli.com/2016/09/25/2016/0925AOSPOnMac/)

## 源码下载和编译

### 配置编译环境（Mac）

​	默认安装时，Mac系统运行的是保留大小写但不区分大小写的文件系统，git无法支持此类系统，并且会导致一些git指令出现异常。

1. 创建区分大小写的disk image

   方法一：启动磁盘工具，选择“New Image”，至少要分配25GB空间，此空间允许在后期增加。在格式化时，需要选择“case sensitive,journaled”进行卷格式化。

   方法二：在shell中运行以下指令

   + 创建（创建出来的文件为一个`.dmg`或者`.dmg.sparseimage`）

     `# hdiutil create -type SPARSE -fs 'Case-sensitive Journaled HFS+' -size 40g ~/android.dmg`

   + 扩展卷容量

     `# hdiutil resize -size <new-size-you-want>g ~/android.dmg.sparseimage`

   + 加载分区（直接执行指令或者添加宏后运行宏）  
     （可选）对保存在home目录下名为android.dmg的disk iamge，可以在`~/.bash_profile`中添加辅助函数，如

     + 执行mountAndroid挂载image（如果是`.dmg.sparseimage`需要对应修改）

       ```shell
       # mount the android file image
       function mountAndroid { hdiutil attach ~/android.dmg -mountpoint /Volumes/android; }
       ```

     + 执行unmountAndroid卸载

       ```shell
       # unmount the android file image
       function umountAndroid() { hdiutil detach /Volumes/android; }
       ```

2. 安装JDK

   + 安装必须的包

     + Xcode命令行工具

       `$ xcode-select --install`

     + 从[macports.org](http://www.macports.org/install.php)安装MacPorts

       需要确保path中` /opt/local/bin`在` /usr/bin`前面，如果没有，则使用以下指令添加到`~/.bash_profile`中：

       `export PATH=/opt/local/bin:$PATH`

     + 从MacPorts中获取make、git和GPG包

       `$ POSIXLY_CORRECT=1 sudo port install gmake libsdl git gnupg`
       > 如果安装过程中卡住无法安装成功，则可以根据https://trac.macports.org/wiki/Mirrors获取镜像地址，然后修改/opt/local/etc/macports/sources.conf，把最后的rsync注释掉换成其它镜像源，最后运行sudo port selfupdate。

       如果是Mac OS X v10.4，还需要安装bison

       `$ POSIXLY_CORRECT=1 sudo port install bison`

   + 设置文件描述符限制（file descriptor limit）

     Mac系统中，file descriptors默认可同时打开的文件数目过低，可通过在`~/.bash_profile`中添加如下内容增加

     ```shell
     # set the number of open files to be 1024
     ulimit -S -n 1024
     ```



### 下载源码  
#### 传统方法  

1. 安装Repo

   + 确保home目录下有一个bin目录，并已经包含到path中

     ```shell
     $ mkdir ~/bin
     $ PATH=~/bin:$PATH
     ```

   + 下载repo并确保它可执行

     ```shell
     $ curl https://storage.googleapis.com/git-repo-downloads/repo > ~/bin/repo
     $ chmod a+x ~/bin/repo
     ```

2. 初始化Repo客户端

   + 创建一个空目录来存放工作文件

     ```shell
     $ mkdir WORKING_DIRECTORY
     $ cd WORKING_DIRECTORY
     ```

   + 配置git

     ```shell
     $ git config --global user.name "Your Name"
     $ git config --global user.email "you@example.com"
     ```

   + 运行repo init

     ```shell
     $ repo init -u https://android.googlesource.com/platform/manifest
     ```

     manifest的URL用来指定Android源码中不同的仓库，如果需要check out “master” 以外的分支则通过`-b`指定。[Source Code Tags and Builds](https://source.android.com/source/build-numbers.html#source-code-tags-and-builds)

     ```shell
     $ repo init -u https://android.googlesource.com/platform/manifest -b android-4.0.1_r1
     ```

     初始化完成后，客户端目录会包含一个`.repo`目录。

3. 下载Android源码树

   ```shell
   $ repo sync
   ```

#### 镜像源方法（清华大学TUNA镜像源）
  参照传统方法，将 https://android.googlesource.com/ 全部使用 https://aosp.tuna.tsinghua.edu.cn/ 代替。  
+ 下载repo工具

   ```Shell
   mkdir ~/bin
   PATH=~/bin:$PATH
   curl https://storage.googleapis.com/git-repo-downloads/repo > ~/bin/repo
   #如果上述 URL 不可访问，可以用下面的：
   #curl https://storage-googleapis.proxy.ustclug.org/git-repo-downloads/	repo > ~/bin/repo
   chmod a+x ~/bin/repo
   ```

+ 然后建立一个工作目录（名字任意）

    mkdir WORKING_DIRECTORY
    ​	cd WORKING_DIRECTORY

+ 初始化仓库

     repo init -u git://mirrors.ustc.edu.cn/aosp/platform/manifest
     ​	## 如果提示无法连接到 gerrit.googlesource.com，可以编辑 ~/bin/repo，
     ​	## 把 REPO_URL 一行替换成下面的：
     ​	## REPO_URL = 'https://gerrit-googlesource.proxy.ustclug.org/git-repo'

+ 如果需要某个特定的 Android 版本（[Android 版本列表](https://source.android.com/source/build-numbers.html#source-code-tags-and-builds)）

    repo init -u git://mirrors.ustc.edu.cn/aosp/platform/manifest -b android-6.0.1_r79

+ 同步源码树（以后只需执行这条命令来同步）

    repo sync


 也可以先下载[初始包](https://mirrors.tuna.tsinghua.edu.cn/aosp-monthly/aosp-latest.tar)，然后执行 `repo sync` 来进行更新。	
​	

### 准备编译
​	同步完成后，将AOSP文件夹拷贝到分区，打开分区目录进行编译。  
​	`$ cd /Volumes/android/AOSP/`

1. 配置环境

   ```shell
   $ . build/envsetup.sh
   ```

2. 选择target

   ```shell
   $ lunch aosp_arm-eng
   ```

   编译的target都采用了`BUILD-BUILDTYPE`形式，BUILDTYPE的区别如下：

   | Buildtype | Use                                      |
   | --------- | ---------------------------------------- |
   | user      | limited access; suited for production    |
   | userdebug | like "user" but with root access and debuggability; preferred for debugging |
   | eng       | development configuration with additional debugging tools |

3. 编译代码

   ```shell
   $ make -j4
   ```

   `-jN`参数中的N通常使用的是硬件线程数目的一到两倍。如dual-E5520机器（两个CPU，每个CPU有4个核心，每个核心有两个线程），最快的编译命令在`make -j16`和`make -j32`之间。

4. 运行  
   可通过虚拟器或将通过flash编译到设备中（注意：目标硬件需要有专用的二进制文件，个人理解为驱动）。  
    `$ emulator`



### 下载技巧

#### 避免下载中断

在 sync 过程中可能出现中断，我们可以通过以下脚本来自动在中断后重新开始
```bash
#!/bin/bash 
#FileName  syn.sh

repo sync 
while [ $? = 1 ]; do 
echo "================sync failed, re-sync again =====" 
sleep 3 
repo sync 
done
```

#### 快速下载当前分支

> 使用此方法无法切换分支
> 方法出自 [Mac 下载 编译 debug Android 源码](http://www.jianshu.com/p/759a6677c946)
> 在执行完 `repo init` 后，会生成一个 `.repo` 文件夹，在 `.repo/manifests/default.xml` 中记录了所有要下载的 project 信息，部分 project 信标签会配置 `clone-depth="1"`，它的作用是 clone 最新的内容，而不 clone 历史记录。因此，通过为每个 project 添加这个配置，就可以达到快速下载目的。
> 通过运行以来 python 来自动为每个 project 添加（需要将 default.xml 和该 py 文件放在同一文件夹，然后在终端执行脚本，执行后终端将生成修改后的内容，然后复制到 default.xml 中）
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

file_object = open('default.xml')

change_content = ''
while 1:
    line = file_object.readline()
    if not line.__contains__('clone-depth'):
        try:
            endpos = line.index("/>")
            line = line[0:endpos] + ' clone-depth="1"' + line[endpos: line.__len__()]
            pass
        except Exception, e:
            pass

    change_content += line
    if not line:
        break
    pass  # do something

print change_content
```

#### repo设置代理

```
export http_proxy=http://127.0.0.1:1080
export https_proxy=https://127.0.0.1:1080
```



## 编译问题汇总

### curl版本错误

```shell
FAILED: setup-jack-server 
/bin/bash -c "(prebuilts/sdk/tools/jack-admin install-server prebuilts/sdk/tools/jack-launcher.jar prebuilts/sdk/tools/jack-server-4.11.ALPHA.jar  2>&1 || (exit 0) ) && (JACK_SERVER_VM_ARGUMENTS=\"-Dfile.encoding=UTF-8 -XX:+TieredCompilation\" prebuilts/sdk/tools/jack-admin start-server 2>&1 || exit 0 ) && (prebuilts/sdk/tools/jack-admin update server prebuilts/sdk/tools/jack-server-4.11.ALPHA.jar 4.11.ALPHA 2>&1 || exit 0 ) && (prebuilts/sdk/tools/jack-admin update jack prebuilts/sdk/tools/jacks/jack-4.30.CANDIDATE.jar 4.30.CANDIDATE || exit 47 )"
Writing client settings in /Users/zero/.jack-settings
Unsupported curl, please use a curl not based on SecureTransport
Jack server installation not found
Unsupported curl, please use a curl not based on SecureTransport
Unsupported curl, please use a curl not based on SecureTransport
[ 46% 14844/32210] host Java: apksig (...IBRARIES/apksig_intermediates/classes)
ninja: build stopped: subcommand failed.
09:43:44 ninja failed with: exit status 1
```

原因：curl版本错误，使用 `$ /usr/bin/curl --version` 查看版本，如果为 「SecureTransport」 ，需要切换为 「OpenSSL」

解决：

+ 安装[Homebrew](https://brew.sh/)

+ 执行

  ```shell
  brew install curl --with-openssl
  # 需要指定使用的curl版本路径，如果查看版本错误，可以重新指定下
  export PATH=$(brew --prefix curl)/bin:$PATH
  caffeinate make -j4	
  ```



### 找不到tools.jar

```shell
build/core/config.mk:658: error: Error: could not find jdk tools.jar at /System/Library/Frameworks/JavaVM.framework/Versions/Current/Commands/../lib/tools.jar, please check if your JDK was installed correctly.
14:35:41 ckati failed with: exit status 1
make: *** [run_soong_ui] Error 1
```

原因：环境变量设置错误

解决：执行(jdk版本需要修改为自己系统的版本，本人是通过打开/usr/libexec/java_home，感觉这个方法有点笨。。。)

`export ANDROID_JAVA_HOME=$(/usr/libexec/java_home -v 1.8.0_121)`



### 找不到MacOSX10.8.sdk

```shell
build/core/combo/mac_version.mk:41: * Can not find SDK 10.8 at /Developer/SDKs/MacOSX10.8.sdk
```

原因：OSX系统更新后，版本不对应

解决：修改build/core/combo/mac_version.mk，在`mac_sdk_versions_supported :=`后面添加当前系统版本

### ‘syscall’过时

```shell
system/core/libcutils/threads.c:38:10: error: 'syscall' is deprecated: first deprecated in OS X 10.12 - syscall(2) is unsupported; please switch to a supported interface. For SYS_kdebug_trace use kdebug_signpost(). [-Werror,-Wdeprecated-declarations]
  return syscall(SYS_thread_selfid);
         ^
/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.12.sdk/usr/include/unistd.h:733:6: note: 'syscall' has been explicitly marked deprecated here
int      syscall(int, ...);
         ^
1 error generated.
[  1% 506/33035] host C: libcutils <= system/core/libcutils/fs.c
ninja: build stopped: subcommand failed.
make: *** [ninja_wrapper] Error 1
```

原因：新的MacOSX10.12.sdk不支持

解决：使用旧版本sdk。下载 [MacOSX10.11.sdk](https://github.com/phracker/MacOSX-SDKs/releases/tag/MacOSX10.11.sdk) ，解压拷贝到/Applications/XCode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs目录下，注意在AOSP源码build/core/combo/mac_version.mk文件的`mac_sdk_versions_supported`中要去掉10.12。

> 为避免升级时被删除，可以放到~/Document/MacOSX10.11.sdk，再给它创建一个软链接：$ ln -s ~/Documents/MacOSX10.11.sdk /Applications/XCode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.11.sdk



### .jack-settings:Permissiondenied

```shell
FAILED: /bin/bash -c "(prebuilts/sdk/tools/jack-admin install-server prebuilts/sdk/tools/jack-launcher.jar prebuilts/sdk/tools/jack-server-4.8.ALPHA.jar  2>&1 || (exit 0) ) && (JACK_SERVER_VM_ARGUMENTS=\"-Dfile.encoding=UTF-8 -XX:+TieredCompilation\" prebuilts/sdk/tools/jack-admin start-server 2>&1 || exit 0 ) && (prebuilts/sdk/tools/jack-admin update server prebuilts/sdk/tools/jack-server-4.8.ALPHA.jar 4.8.ALPHA 2>&1 || exit 0 ) && (prebuilts/sdk/tools/jack-admin update jack prebuilts/sdk/tools/jacks/jack-2.28.RELEASE.jar 2.28.RELEASE || exit 47; prebuilts/sdk/tools/jack-admin update jack prebuilts/sdk/tools/jacks/jack-3.36.CANDIDATE.jar 3.36.CANDIDATE || exit 47; prebuilts/sdk/tools/jack-admin update jack prebuilts/sdk/tools/jacks/jack-4.7.BETA.jar 4.7.BETA || exit 47 )"
prebuilts/sdk/tools/jack-admin: line 49: /Users/zero/.jack-settings: Permission denied
prebuilts/sdk/tools/jack-admin: line 55: SETTING_VERSION: unbound variable
prebuilts/sdk/tools/jack-admin: line 49: /Users/zero/.jack-settings: Permission denied
prebuilts/sdk/tools/jack-admin: line 55: SETTING_VERSION: unbound variable
prebuilts/sdk/tools/jack-admin: line 49: /Users/zero/.jack-settings: Permission denied
prebuilts/sdk/tools/jack-admin: line 55: SETTING_VERSION: unbound variable
prebuilts/sdk/tools/jack-admin: line 49: /Users/zero/.jack-settings: Permission denied
prebuilts/sdk/tools/jack-admin: line 55: SETTING_VERSION: unbound variable
[  0% 144/19818] target thumb C++: lib...orks/native/opengl/libs/EGL/eglApi.cpp
ninja: build stopped: subcommand failed.
make: *** [ninja_wrapper] Error 1
```

解决：修改.jack-settings文件权限：显示简介 -> 修改staff权限为读与写（不确定是哪个用户组，最后全修改后通过）



### xt_DSCP.h文件找不到

```shell
external/iptables/extensions/../include/linux/netfilter_ipv4/ipt_ECN.h:13:10: fatal error: 'linux/netfilter/xt_DSCP.h' file not found
#include <linux/netfilter/xt_DSCP.h>
```

解决：自行下载文件添加到指定目录



### no space left on device

原因：一开始以为磁盘空间会自动增长，所以只分配了40g...

解决：扩展卷容量（需要先卸载并退出使用该卷的终端）

`# hdiutil resize -size <new-size-you-want>g ~/android.dmg.sparseimage`



###  找不到 jdk tools.jar

```
build/core/config.mk:695: error: Error: could not find jdk tools.jar at /System/Library/Frameworks/JavaVM.framework/Versions/Current/Commands/../lib/tools.jar, please check if your JDK was installed correctly.
```

解决：

`$ export ANDROID_JAVA_HOME=$(/usr/libexec/java_home -v 1.7)`



### bison 报错

```
[  3% 2279/59686] yacc out/soong/.inte.../system/tools/aidl/aidl_language_y.cpp
FAILED: out/soong/.intermediates/system/tools/aidl/libaidl-common/darwin_x8664static/gen/yacc/system/tools/aidl/aidl_language_y.cpp out/soong/.intermediates/system/tools/aidl/libaidl-common/darwin_x8664static/gen/yacc/system/tools/aidl/aidl_language_y.h 
BISON_PKGDATADIR=external/bison/data prebuilts/misc/darwin-x86/bison/bison -d  --defines=out/soong/.intermediates/system/tools/aidl/libaidl-common/darwin_x8664static/gen/yacc/system/tools/aidl/aidl_language_y.h -o out/soong/.intermediates/system/tools/aidl/libaidl-common/darwin_x8664static/gen/yacc/system/tools/aidl/aidl_language_y.cpp system/tools/aidl/aidl_language_y.yy
[  3% 2282/59686] lex out/soong/.inter.../system/tools/aidl/aidl_language_l.cpp
ninja: build stopped: subcommand failed.
14:03:54 ninja failed with: exit status 1
make: *** [run_soong_ui] Error 1
```

[build aosp on Mac OS 10.13 failed](https://groups.google.com/forum/#!topic/android-building/D1-c5lZ9Oco)

> 这个问题对我来说是个巨坑，在两个月里尝试了各种方法都没弄好，怪自己手贱，就因为差几个小版本就强迫自己重新下一份源码。

最终采用以下方法解决：

- Patch [bison fix](https://android-review.googlesource.com/c/platform/external/bison/+/517740) for High Sierra and build bison:

- - cd /Volumes/AOSP/external/bison
  - git cherry-pick c0c852bd6fe462b148475476d9124fd740eba160
  - mm

- Replace prebuilt bison binary with patched binary

- - cp /Volumes/AOSP/out/host/darwin-x86/bin/bison /Volumes/AOSP/prebuilts/misc/darwin-x86/bison/

- Build





## repo使用

[Repo command reference](https://source.android.com/source/using-repo.html)

### 还原所有改动

`repo forall -c "git checkout ."`

-c "COMMAND TO EXECUTE"：实际执行的指令



### 同步其他分支

更新manifest

`repo init -b <my_selected_android_version>`

同步

`repo sync`

> 个人试验貌似切换后文件没有变化，最后通过直接删除了.repo外的文件，然后重新repo init，再sync，速度也不会很慢，因为.repo外的文件也只是从.repo中check out，而不是重新下载。
>

### 查看当前android版本号

在build/core/version_defaults.mk文件中查看PLATFORM_VERSION



## 下载记录

### 20171210

.repo 文件夹大小：26g

checkout 后的源码大小：30g

out 文件夹大小：42g

