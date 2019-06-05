InputFilter 是一个 interface，它只有一个抽象方法。

```java
public CharSequence filter(CharSequence source, int start, int end, Spanned dest, int dstart, int dend);
```

* source：要插入的字符串
* start、end：source 中要插入的字符串的起点和终点
* dest：source 要插入到那个字符串中
* dstart、dend：插入的位置
* 返回值：最终插入的字符串，null 表示接受最初的输入作为插入的字符串。



如：

EditText 现在显示的是 “ABCDEFG”，选中 “CD”，输入“H”，这时，

source 为 H，start 为 0，end 为 1，dest 为 ABCDEFG，dstart 为 2，dend 为 4。



PS：有一个疑问，start、end 的值有可能不是 0 和 source.length 吗？（我尝试添加两个同样的 InputFilter，结果显示第二个 InputFilter 的 source 为第一个的返回值，所以 start 和 end 还是 0 和 source.length）



