TextView 宽度对齐包括两种情形：

+ 文字靠边

  对于这种情况，可以如果在同一父布局下，可以利用父布局的对齐属性来实现，如 RelativeLayout 的 align 属性是左右两边分别对齐即可；而对于不同父布局中的 TextView，可以利用 LinearLayout 的 weight 属性使 TextView 宽度一致，或者使用空格进行占位。各种空格的编码如下：

  ```
  &#32; == 普通的英文半角空格

  &#160; == &nbsp; == &#xA0; == no-break space （普通的英文半角空格但不换行）

  &#12288; == 中文全角空格 （一个中文宽度）

  &#8194; == &ensp; == en空格 （半个中文宽度）

  &#8195; == &emsp; == em空格 （一个中文宽度）

  &#8197; == 四分之一em空格 （四分之一中文宽度）
  ```

+ 文字分散对齐

  暂未用到

