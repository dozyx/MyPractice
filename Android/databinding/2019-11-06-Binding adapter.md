[DataBinding使用指南(四)：BindingAdapter](https://blog.csdn.net/guiying712/article/details/80411597)

当值发生改变时，生成的 binding 类会调用该 View 的 setter 方法。

* 自动选择方法

  比如，`android:text="@{user.name}"`，binding 会查找签名相同的 `setText(arg)` 方法。

  **即使是不存在的属性，DataBinding 还是可以正确调用。**比如：

  ```xml
  <android.support.v4.widget.DrawerLayout
      android:layout_width="wrap_content"
      android:layout_height="wrap_content"
      app:scrimColor="@{@color/scrim}"
      app:drawerListener="@{fragment.drawerListener}">
  ```

  scrimColor 和 drawerListener 是两个没有声明的属性，但还是可以正确调用 DrawerLayout 的 setScrimColor(int) 和 setDrawerListener(DrawerListener) 方法。通过这种方式，可以为任何的 setter 创建属性。

* 指定调用的方法

  有些属性没有匹配的 setter，那么可以通过使用 `BindingMethods` 注解将一个属性与 setter 关联。

  ```java
  @BindingMethods({
         @BindingMethod(type = "android.widget.ImageView",
                        attribute = "android:tint",
                        method = "setImageTintList"),
  })
  ```

* 提供自定义逻辑

  有些属性没有单独设置的方法，那么需要提供自定义的逻辑来调用其他方法来实现功能。这种情况可以使用 `BindingAdapter` 来实现。

  比如：

  ```java
  @BindingAdapter("android:paddingLeft")
  public static void setPaddingLeft(View view, int padding) {
    view.setPadding(padding,
                    view.getPaddingTop(),
                    view.getPaddingRight(),
                    view.getPaddingBottom());
  }
  ```

  第一个参数为关联的 View，第二个属性为绑定表达式接受的参数类型。

  另一个例子：

  ```java
  @BindingAdapter({"imageUrl", "error"})
  public static void loadImage(ImageView view, String url, Drawable error) {
    Picasso.with(view.getContext()).load(url).error(error).into(view);
  }
  ```

  ```java
  <ImageView 
          app:imageUrl="@{venue.imageUrl}" 
          app:error="@{@drawable/venueError}" />
  ```

  如果不需要在所有属性都设置的时候才调用，可以设置 `requireAll` 标记

  ```java
  @BindingAdapter(value={"imageUrl", "placeholder"}, requireAll=false)
  public static void setImageUrl(ImageView imageView, String url, Drawable placeHolder) {
    if (url == null) {
      imageView.setImageDrawable(placeholder);
    } else {
      MyImageLoader.loadInto(imageView, url, placeholder);
    }
  }
  ```

  在方法种使用旧值：

  ```java
  @BindingAdapter("android:paddingLeft")
  public static void setPaddingLeft(View view, int oldPadding, int newPadding) {
    if (oldPadding != newPadding) {
        view.setPadding(newPadding,
                        view.getPaddingTop(),
                        view.getPaddingRight(),
                        view.getPaddingBottom());
     }
  }
  ```

  

  