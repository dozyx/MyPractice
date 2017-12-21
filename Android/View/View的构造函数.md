View的构造方法一般有四个，但最终实际调用是都是参数最多的一个：

```java
public View(Context context, @Nullable AttributeSet attrs, int defStyleAttr, int defStyleRes)
```

attrs：对应我们在布局文件中指定的属性；

defStyleAttr：对应的是我们定义在 theme 中的属性，defStyleAttr 是一个属性，它引用了一个 style 属性集；

defStyleRes：对应的是我们在布局文件使用使用 style 属性指定的 style 属性集。

这三个参数都可以用来确定某个属性对应的值，但他们确定的属性有重复时，优先级为：

attrs > defStyleRes > defStyleAttr，即"属性 > style > theme"。



### 在 theme 中配置某个 View 的属性

当 View 从 xml 布局文件中 inflate 出来时，系统调用的是有两个参数的构造方法：

```java
public View(Context context, @Nullable AttributeSet attrs)
```

如果我们希望在 inflate 时，自动提取 theme 中指定的 Style，则可以声明一个 style 属性，然后在 theme 中使用该属性来引用我们预先定义的 Style。如 Button 中：

```java
public Button(Context context, AttributeSet attrs) {
        this(context, attrs, com.android.internal.R.attr.buttonStyle);
    }
```

而 buttonStyle 属性的声明可以直接添加到 attrs.xml 文件中：

```xml
        <!-- Normal Button style. -->
        <attr name="buttonStyle" format="reference" />

        <!-- Small Button style. -->
        <attr name="buttonStyleSmall" format="reference" />

        <!-- Button style to inset into an EditText. -->
        <attr name="buttonStyleInset" format="reference" />
```



### 最后

在重新对构造函数的思考的时候，我得到了一些新的启发：在开发一个应用前期，我们可以先声明一系列的属性，如上面的 buttonStyle、buttonStyleSmal等，我们不仅可以在自定义的 View 中通过属性指定一个默认的 Style，还能在 xml 布局文件中使用 `?attr` 的方式来间接指定 Style，这样比 style 属性直接指向 Style 更为方便维护。比如，buttonStyleSmall 属性指向 StyleOne，在需要将 StyleTwo 换为 StyleTwo时，只需要更改 buttonStyleSmall，否则的话，将需要将所有已使用 StyleOne 的地方改为 StyleTwo。