doc：定义了一个 drawable 的 xml 文件，该 drawable 被嵌入了特定的距离。当一个 View 需要使用一个比它实际大小要小的 background 时，该处理将显得十分有效。

> 个人理解就是为一个 drawable 增加额外的边距。

语法：

```java
<?xml version="1.0" encoding="utf-8"?>
<inset
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:drawable="@drawable/drawable_resource"
    android:insetTop="dimension"
    android:insetRight="dimension"
    android:insetBottom="dimension"
    android:insetLeft="dimension" />
```

除了使用 android:drawable 来设置被 inset 的 drawable 外，我们也可以使用如 shape 等元素。如：

```xml
<inset xmlns:android="http://schemas.android.com/apk/res/android"
    android:inset="50dp">
    <shape android:shape="rectangle" >
        <size android:width="50dp" android:height="50dp"/>
        <solid android:color="@color/colorAccent"/>
    </shape>
</inset>
```



参考：

[drawable resource Inset](https://developer.android.com/guide/topics/resources/drawable-resource.html#Inset)

[InsetDrawable](https://developer.android.com/reference/android/graphics/drawable/InsetDrawable.html)