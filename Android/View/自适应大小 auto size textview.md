属性：

* autoSizeTextType
  * uniform：在 TextView 尺寸内缩放文本大小
  * none：不自动改变大小
* autoSizeMinTextSize：最小值，不设置的话使用默认的 `12sp`。
* autoSizeMaxTextSize：最大值，不设置的话使用默认的 `112sp`。
* autoSizeStepGranularity：两个尺寸间的间隔。不设置的话使用默认的 `1px`。注意是 `px`。

> 关于上面提及的默认值，可以在 AppCompatTextViewAutoSizeHelper 这个类中查看。

### 注意

* auto size 会导致 setTextSize() 失效，text size 的 作用只是用来计算 TextView 的高度。



### 问题

#### textSize 使用 dp 作为单位，并应用 uniform 自适应大小之后，文本底部被截断

原因：auto size 的大小是有范围的，当 TextView 的 height 小于文字的高度时，就出现了显示不全的问题。

分析：这个问题的出现还有另一个条件：在系统设置里改变了字体大小。首先，要明确一点，无论使用 dp 还是 sp，代码中最终应用的都是 px。当设置 textSize 为 dp 值时，TextView 将该 dp 值转换成 px 来计算 TextView 的高度。auto size 有一个默认的最小值 12sp，如果 TextView 的 height 小于 12 sp，那么就会显示不全。如果系统字体大小使用的是默认，通常 dp 和 sp 转为 px 之后，大小是相同的，但如果系统字体改大了，那么 12dp < 12sp。这样文本就会显示有问题。解决方法有好几种（指的是解决文字显示不全的问题）：

* 不使用 autosize
* 修改 autoSizeMinTextSize，使 autoSizeMinTextSize 小于或等于 textSize，并且最好使用跟 textSize 相同的单位。



从这个问题的分析中，有一个值得注意的结论：

* **autoSizeMinTextSize 大于 textSize 的时候，会使用 autoSizeMinTextSize**
* **使用 dp 作为 textSize 单位，并使用 auto size 时，需要注意 autoSizeMinTextSize 的影响**



### 设置 android:singleLine="true" 文字无法缩小

singleLine 为 true 时，会设置 ellipsize 为 ELLIPSIZE_END，文本被省略之后， TextView 的尺寸总是能容纳全部文字，那么自然没必要缩小。









参考：

[Autosizing TextViews](https://developer.android.com/guide/topics/ui/look-and-feel/autosizing-textview.html#setting-textview-autosize)