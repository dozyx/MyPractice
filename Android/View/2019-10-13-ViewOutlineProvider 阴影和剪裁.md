`ViewOutlineProvider`：抽象类，View 构建 `Outline` 的接口，用于阴影投射和裁剪。API21 以上可用。

`Outline`（轮廓）：定义一个简单的形状以界定图形区域。

相关方法：

[Drawable.getOutline(Outline)](https://developer.android.com/reference/android/graphics/drawable/Drawable.html#getOutline(android.graphics.Outline))

[View.setOutlineProvider(android.view.ViewOutlineProvider)](https://developer.android.com/reference/android/view/View.html#setOutlineProvider(android.view.ViewOutlineProvider))



> 所有 View 的绘制区域都是矩形的，但在绘制阴影时，投射的阴影不一定是通过矩形投射得到，而是应该根据显示内容的轮廓来计算。

ViewOutlineProvider 类提供了三个具体实现：

* BACKGROUND：View 默认的 ViewOutlineProvider。获取 background 的 outline，如果没有 background 则根据 view 的尺寸生成一个矩形透明的 outline。比如，background 是一个 shape 的 drawable，那么这个 shape 就是 outline
* 
* BOUNDS：以 View 的矩形边界作为 outline
* PADDED_BOUNDS：以去掉内边距的矩形边界作为 outline



为了添加阴影效果，需要给 View 设置 elevation 或者 translationZ 属性。

> elevation 和 translationZ 共同决定了 View 的 Z 属性。Z 属性会导致 View 的显示区域变大，因为要增加额外的区域显示阴影。



### 剪裁

Outline 可以确定阴影的显示形状，但是如果 View 的大小比阴影大小大，则 View 会将阴影遮挡住。

在给一个 View 设置了 Outline 之后，通过通过 `setClipToOutline(true)` 来将 View 的显示内容限定在 Outline 内，即对 View 的显示内容进行了剪裁。

参考：

[ViewOutlineProvider](https://developer.android.com/reference/android/view/ViewOutlineProvider.html)

[Outline](https://developer.android.com/reference/android/graphics/Outline.html)

[Create Shadows and Clip Views](https://developer.android.com/training/material/shadows-clipping)

[Android5.0新特性——阴影和剪裁（shadow）](https://www.cnblogs.com/McCa/p/4465597.html)

