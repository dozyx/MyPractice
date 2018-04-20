> 有时候，我们需要为同一个 TextView 根据情况设置不同颜色的文本，又或者同一个字符串中有多种颜色。为了实现这样的效果，我们可以使用 SpannableString，但对于一些比较简单的需求，比如只是简单的颜色变化，我们也可以直接利用 html 来实现。

比如实现如下样式：

![TIM截图20180420144327](../../photo/TIM截图20180420144327.png)

我们可以直接在代码中设置：

```java
textView.setText(Html.fromHtml("<font color=\"#ff0000\">你好啊</font>你好啊<font "
                + "color=\"#00ff00\">你好啊</font>"));
```

但硬编码看起来不好看，而且不利于复用，于是我们将字符串定义在 strings.xml 中

```xml
<string name="style_text"><font color="#ff0000">你好啊</font>你好啊<font color="#00ff00">你好啊</font></string>
```

然后设置

```java
textLog.setText(Html.fromHtml(getString(R.string.style_text)))
```

但这样设置后，文本并没有显示出想要的颜色，这是因为 getString 只会获取“字符串”，在 getString 的 javadoc 中对返回值的描述有这样一句 “The string data associated with the resource, stripped of styled text information.”，意思是返回的字符串会去掉文本的样式信息。如果我们将 getString(R.string.style_text) 的结果打印出来，只能看到 “你好啊你好啊你好啊”。

> 注意：如果是直接在布局文件中设置字符串，html 的标签是会生效的。

使用 strings.xml 中的 html 文本以下几种方式：

+ 转义
+ 使用 getText 方法
+ 使用 CDATA



### 转义字符

为了解决上面的问题，我们可以对 strings.xml 文本中定义的字符串的 html 标签进行转义，再通过 Html.fromHtml 获取，需要注意，转义后，如果该文本用于布局文件中，将显示出 html 的信息。

实现：

+ 将标签的开括号使用转义字符 `&lt;`代替

  ```xml
  <string name="style_text">&lt;font color="#ff0000">你好啊&lt;/font>你好啊&lt;font color="#00ff00">你好啊&lt;/font></string>
  ```

+ 在代码中设置文本

  ```
  setText(Html.fromHtml(getString(R.string.style_text)))
  ```



如果我们想要将 html 字符串显示为原始的字符，即显示为

`<font color="#ff0000">你好啊</font>你<b>好</b>啊<font color="#00ff00">你好啊`

我们可以利用 TextUtils.htmlEncode 方法进行编码，该方法会主动将字符串中的一些符号进行转义，如 `<` 转为 `&lt;`。



### getText

[getText(int)](https://developer.android.com/reference/android/content/Context.html#getText(int)) 方法会保留字符串中的富文本信息，不过评论里有人提到不同版本的 api 支持的 tag 不一样，比如 font 在 api23 才支持，但[源码](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-4.2.2_r1/core/java/android/content/res/StringBlock.java#L161)中显示是支持的。对此，还没有验证。



### CDATA

将字符串放在 <![CDATA[字符串]] 中。

```xml
<string name="style_text2"><![CDATA[<font color="#ff0000">你好啊</font>你<b>好</b>啊<font color="#00ff00">你好啊</font>]]></string>
```

当我们使用 getString 获取字符串时，字符串中的 html 信息将保留，比如 getString(R.string.style_text2) 结果为：

`<font color=#ff0000>你好啊</font>你<b>好</b>啊<font color=#00ff00>你好啊</font>`

这种方式应该是最灵活的，因为我们不用在 html 标签，不过需要注意如果该字符串用于字符串，里面的 html 标签也会显示出来。







参考：

[string resources](https://developer.android.com/guide/topics/resources/string-resource.html#FormattingAndStyling)

[HTML in string resource?](https://stackoverflow.com/questions/2667319/html-in-string-resource)