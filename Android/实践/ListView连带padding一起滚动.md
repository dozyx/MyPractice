问题：列表距离顶部有一定间隔，如果为此添加一个额外的 View 或者直接设置 padding，滑动列表时，间隔部分都不会有所变化，这样就显得很不顺眼。

解决：padding + 设置 clipToPadding 为 false

分析：clipToPadding 的作用为 ViewGroup 是否对它的 children 进行裁剪并将其大小调整到 padding 处，该属性默认为 true。（好像不是很好理解。。。网上的一些博客将其解释为是否允许在 padding 区域绘制。）

> Defines whether the ViewGroup will clip its children and resize (but not clip) any EdgeEffect to its padding, if padding is not zero. This property is set to true by default.











参考：

[ListView padding on scrolling](https://stackoverflow.com/questions/22778938/listview-padding-on-scrolling)

[android:clipToPadding](https://developer.android.com/reference/android/view/ViewGroup.html#attr_android:clipToPadding)