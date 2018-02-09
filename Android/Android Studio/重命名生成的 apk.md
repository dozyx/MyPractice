默认生成的 apk 名称为 app-release。我们通过通过在 build.gradle 中做以下修改来修改编译出来的 apk 名称：

```groovy
// If you use each() to iterate through the variant objects,
// you need to start using all(). That's because each() iterates
// through only the objects that already exist during configuration time—
// but those object don't exist at configuration time with the new model.
// However, all() adapts to the new model by picking up object as they are
// added during execution.
android.applicationVariants.all { variant ->
    variant.outputs.all {
        outputFileName = "${variant.name}-${variant.versionName}.apk"
    }
}
```

编译后名称如：**baiduDebug-1.0.apk**，即“变体名称+版本号”的形式。

通过进一步的修改，我们可以在名称中添加更多的信息：

```groovy
android.applicationVariants.all { variant ->
    variant.outputs.all {
        def date = new Date().format("MMddHH")
        def productFlavorName = variant.productFlavors[0].name
        outputFileName = "应用名称" + "_${variant.versionName}_" + productFlavorName + "_" + date + "_${variant.buildType.name}" + ".apk"
    }
}
```

编译出来的 apk 名称如：**应用名称-1.0-baidu-020917-debug.apk**。



参考：

[variant_api](https://developer.android.com/studio/build/gradle-plugin-3-0-0-migration.html#variant_api)