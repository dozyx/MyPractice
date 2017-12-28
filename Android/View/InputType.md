> 疑问：InputType 究竟是如何影响输入的，包括内容和输入法？

InputType 包括了三种配置：class、variation、flag，class 通过与 variation 和 flag 的结合来表明想要的行为。

+ class：确定接受的文本的整体类别。包括：
  + TYPE_CLASS_TEXT
  + TYPE_CLASS_NUMBER
  + TYPE_CLASS_PHONE
  + TYPE_CLASS_DATETIME
+ variation：确定基本内容类别的变体，如 TYPE_TEXT_VARIATION_PASSWORD。
+ flag：额外选项



参考：

[InputType](https://developer.android.com/reference/android/text/InputType.html)

[Specifying the Input Method Type](https://developer.android.com/training/keyboard-input/style.html#Type)