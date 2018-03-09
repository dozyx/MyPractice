> 相对于通过自定义 View 来创建一个单独的 UI 组件，复用布局文件可能会更简单。

创建一个复用的布局：

`titlebar.xml`

```xml
<FrameLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:background="@color/titlebar_bg"
    tools:showIn="@layout/activity_main" >

    <ImageView android:layout_width="wrap_content"
               android:layout_height="wrap_content"
               android:src="@drawable/gafricalogo" />
</FrameLayout>
```



## 使用 include 标签

```xml
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:orientation="vertical"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="@color/app_bg"
    android:gravity="center_horizontal">

    <include layout="@layout/titlebar"/>

    <TextView android:layout_width="match_parent"
              android:layout_height="wrap_content"
              android:text="@string/hello"
              android:padding="10dp" />

    ...

</LinearLayout>
```

我们可以在 include 中重写根 view 的所有的布局属性（layout_*），如

```Xml
<include android:id="@+id/news_title"
         android:layout_width="match_parent"
         android:layout_height="match_parent"
         layout="@layout/title"/>
```

**为了使其它布局属性生效，必须重写 android:layout_width 和 android:layout_height。**



## 使用 merge 标签

merge 可以减少视图的层级。

```xml
<merge xmlns:android="http://schemas.android.com/apk/res/android">

    <Button
        android:layout_width="fill_parent"
        android:layout_height="wrap_content"
        android:text="@string/add"/>

    <Button
        android:layout_width="fill_parent"
        android:layout_height="wrap_content"
        android:text="@string/delete"/>

</merge>
```

当 include 该布局时，系统将忽略 merge 元素并用两个 button 直接替代 include 标签。

**merge 只是一个占位符，而不是一个 ViewGroup，当 inflate 时，merge 标签下的属性不会被使用。**这里有一个不方便的地方就是，我们将带 merge 的布局 inflate 到一个自定义 View 时，不能直接使用 xml 来设置自定义 View 的属性。这时，可以采取一个折中的方法，就是将需要设置的属性作为一个 style，然后在自定义 View 中使用该 style。



参考：

[Re-using Layouts with <include/>](https://developer.android.com/training/improving-layouts/reusing-layouts.html)