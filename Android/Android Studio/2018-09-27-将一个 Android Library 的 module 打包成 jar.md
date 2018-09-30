> Android Library 在 build 的时候生成的是 aar 文件，但有时候我们只需要 module 中的源代码，这样提供一个 jar 会更为方便。当然，我们也可以直接创建一个 Java Library，这样 build 出来的就是一个 jar，不过这样不方便调用 android sdk。

在 module 的 build.gradle 中添加以下代码：

```groovy
task deleteJar(type: Delete) {
    delete 'libs/lib.jar'
}

task createJar(type: Copy) {
    from('build/intermediates/bundles/release')
    into('libs/')
    include('classes.jar')
    rename('classes.jar', 'lib.jar')
}

createJar.dependsOn(deleteJar, build)
```

然后在 Gradle 面板相应 module -> others 下就会多了两个 task：createJar 和 deleteJar，只要运行 createJar 就可以在 libs 下找到生成的 jar。











参考：

[How do I build jar file in Android studio using gradle?](https://www.quora.com/How-do-I-build-jar-file-in-Android-studio-using-gradle)