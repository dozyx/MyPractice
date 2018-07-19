## Input Type 输入类型

默认输入类型为 "text|textMultiLine"。



## 输入内容限制

### 只能输入数字（包括小数）

法一：

`android:inputType="numberDecimal|numberSigned"`

设置后只接受小数点和数字，不过存在的一个问题是首位可以为小数点。

法二：

为自定义 EditText 或者为所用的 EditText 设置 TextWatcher。

> 通常金额最多保留两位小数，所以最好要找一个开源的自定义 EditText 或者自己实现一个。
>
> 规则：
>
> + 小数点后位数
> + 小数点舍入模式
> + 小数点为首位或末尾无效（自动补零或者禁用下一步）



### 只能输入汉字或字母

正则表达式 + InputFilter

```java
InputFilter typeFilter = new InputFilter() {
        @Override
        public CharSequence filter(CharSequence source, int start, int end, Spanned dest, int dstart, int dend) {
            Pattern p = Pattern.compile("[a-zA-Z|\u4e00-\u9fa5]+");
            Matcher m = p.matcher(source.toString());
            if (!m.matches()) return "";
            return null;
        }
    };

editText.setFilters(new InputFilter[]{typeFilter});
```

设置了 filter 后，将导致 `android:maxLength` 属性无效，如果需要限制长度，需要设置一个 LengthFilter。



## error 提示

有时候，需要在用户输入信息不满足规则时显示错误信息，学习 android 两年了都没注意到 TextView 里还有一个 setError 方法直到学习 TextInputLayout 时才发现。。。通过该方法可以在 EditText 右侧显示一个指示错误的图标，然后在 EditText 获得焦点时显示一个弹出式的错误信息。

通过源码发现错误信息使用的布局如下：

```xml
<TextView xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:textAppearance="?android:attr/textAppearanceSmall"
    android:textColor="?android:attr/textColorPrimaryInverse"
/>
```

因此，我们可以通过在 theme 中设置 textAppearanceSmall 和 textColorPrimaryInverse 属性来修改外观。（只是理论分析，暂未尝试）





参考：

[Android 限制 EditText 只能输入英文加汉字](http://www.jianshu.com/p/690c46d58aeb)