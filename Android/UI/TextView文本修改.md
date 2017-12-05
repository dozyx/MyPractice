>  感觉有时候对 TextView 的几个属性的用法不是完全了解。。。

```xml
<declare-styleable name="TextView">
  	...
  	<!-- 根据行数指定 TextView 的高度 -->
    <attr name="lines" format="integer" min="0" />
  
  	<!-- 设置 TextView 的最大高度为该行数的高度，当用于 editable text ，inputType 属性的值必须与
	textMultiLine 一起使用才能使 maxLines 属性生效（注意：指的是输入内容为文本，inputType为 number 时仍为一行）。 -->
    <attr name="maxLines" format="integer" min="0" />
  
  	<!-- 参考 maxLines -->
    <attr name="minLines" format="integer" min="0" />
  
  	<!-- 表示该 TextView 使用数字键盘，并且只接受指定的字符（可以为字母等其他字符，甚至是中文。。）。注意：如果值里有逗号，那么表示逗号也能输入 -->
    <attr name="digits" format="string" />
  
  	<!-- 已经被标记为deprecated。推荐使用 maxLines 替代来修改静态文本的布局，并使用 inputType 属性的
 		 textMultiLine 标记来作为可编辑文本 view 的替代。如果同时设置了 singleLine 和 inputType，
		那么inputType将覆盖singleValue的值。-->
    <attr name="singleLine" format="boolean" />
  	...
</declare-styleable>
```

`android:lines`、`andorid:minLines`、`android:maxLines`用于限制控件自身的高度，我一开始迷惑的原因就在于没有分清控件高度和内容高度（行数）。下面举个例子，假如有一个宽度 EditText，只设置了 maxLines = 2，那么 EditText 最大高度可以达到两个高度，但是，如果加上了 inputType 属性，那么必须添加 textMultiLine  标记才能使 maxLines 生效，不过如果 `android:inputType="number|textMultiLine"`，EditText 的 高度仍然为一行的高度（如果想要实现多行的number，可以添加 `android:digits="0123456789\n"`）。

> 需要查看源码才能彻底搞清楚为什么这样。。。

### 文本末尾添加省略号

```xml
    <TextView
		...
        android:maxLines="1"
        android:ellipsize="end"
        ... />
```



### 跑马灯

普通：



列表：





参考：

[inputType=“number” with more than one line](https://stackoverflow.com/questions/32163224/inputtype-number-with-more-than-one-line)