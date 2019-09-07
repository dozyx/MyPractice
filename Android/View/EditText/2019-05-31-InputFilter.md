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



### 输入文本发生重复（多余）

为了限制输入空格，写了一个 InputFilter：

```java
public class SpaceInputFilter implements InputFilter {
    @Override
    public CharSequence filter(CharSequence source, int start, int end, Spanned dest, int dstart, int dend) {
        if (source == null) {
            return null;
        }
        return source.toString().replaceAll("\\s", "");
    }
}
```

然而，测试在测试兼容性时，发现某些手机上会出现输入多余的字符。经过一轮分析后，发现问题是这样的：输入法使用 26 键中文输入，在输入过程中，联想的中文显示在输入法区域最上面的候选栏，而 Edittext 会显示输入的字母，而在输入下一个字母时，Editetext 增加的是整个新的候选词的首字母，这就是多余字母的来源。

在输入过程中，输入的字母只是预览在 EditText 中（有些输入法不会，所以没问题），连续的输入会作为 source 传入，而不是一次一个字母，dstart 的值为第一个输入字母插入的位置，即 source 替代的是整个预览的输入范围。当 filter 返回一个 String，即上面的 source.toString() 时，预览的内容会立即当作实际的输入，但是后续的 source 还是包含了上一次的输入，这就导致了输入的重复。不过不同的输入法也不一样，有的输入法就只是将后面输入的作为 source。

所以这里存在的一个问题是，为什么当 filter() 方法返回 String 时，会被当做为实际的输入？

这个问题暂时没有找到答案。。。

最终，代码改成了：

```java
public class SpaceInputFilter implements InputFilter {
    @Override
    public CharSequence filter(CharSequence source, int start, int end, Spanned dest, int dstart, int dend) {
        if (TextUtils.isEmpty(source) || !source.toString().contains(" ")) {
            return null;// null 换成 source 也没发现有问题
        }
        return source.toString().replaceAll("\\s", "");
    }
}
```



参考：

[InputFilter在过滤空格时重复输入的问题](https://www.cnblogs.com/yuanting/p/5613009.html)（里面的实现无法限制复制进来的空格）

[InputFilter on EditText cause repeating text](https://stackoverflow.com/questions/18529034/inputfilter-on-edittext-cause-repeating-text)





