[README](https://android.googlesource.com/platform/development/+/master/tools/idegen/README)

- 打开终端，在AOSP目录下执行

  `make idegen && development/tools/idegen/idegen.sh`

  执行完，将在 AOSP 目录生成一个 android.ipr 文件

- 在 Project Structure -> SDKs 中，配置一个没有库的 Java SDK，即删除 classpath 下的所有的 jar 包

- 在android studio 中 open project ，选择打开 android.ipr

- 等待完成

- Project Structure -> Modules，删除所有 .jar 依赖，最后只剩下一个没有库的 Java 依赖

- Project Structure -> Modules -> Sources，找到 `out/target/common/R`，右键点击 Sources




[Setting up Intellij with CyanogenMod/AOSP development](https://shuhaowu.com/blog/setting_up_intellij_with_aosp_development.html)