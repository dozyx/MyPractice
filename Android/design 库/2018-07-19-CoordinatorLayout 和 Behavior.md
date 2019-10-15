CoordinatorLayout 继承于 ViewGroup，可以将它理解为一个功能更强大的 FrameLayout。

它主要用于以下两种场景：

1. 作为顶层的应用框架布局
2. 作为一个可以让一个或多个子 View 进行特定交互的容器



通过为 CoordinatorLayout 的子 View 指定 Behaviors，可以在单个 parent 中使用多种不同的交互，并且这些 view 之间也可以相互交互。View 类可以通过 `CoordinatorLayout.DefaultBehavior` 注解来指定一个作为 CoordinatorLayout 子 view 时的默认 behavior。



## Behavior

Behavior 提供了一个时机，使子 View 可以在 CoordinatorLayout 处理一些事件之前，直接由子 View 的 Behavior 接手。这些事件包括：

* 触摸事件
  * 即使触摸的 view 不是该子 View，也能交给该子 View 的 Behavior 处理。
* measure
* layout
* scroll

我们还可以在 Behavior 中指定一个 dependent view，使该 View 可以跟随 dependent view 发生变化。










参考：

[CoordinatorLayout](https://developer.android.com/reference/android/support/design/widget/CoordinatorLayout)

[彻底搞懂CoordinatorLayout](https://www.jianshu.com/p/b81f5e0d3241)