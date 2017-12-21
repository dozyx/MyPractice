### 为同一 TextView 的内容设置不同字号

例子：

```java
SpannableString ss = new SpannableString("test1111");   
ss.setSpan(new AbsoluteSizeSpan(12, true), 0, 1, 0);
textView.setText(ss);
```

> setSpan 方法最后一个参数为 flag，用于设置对后续输入的的字符采用的策略，暂时也太不是十分明确。