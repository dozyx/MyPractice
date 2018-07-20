> ps：协调布局使 view 之间产生关联，一个 view 可以根据其他 view 的状态变化而做出行为变化。

CoordinatorLayout （父类为 ViewGroup）是一个超级强大的 FrameLayout。

CoordinatorLayout 主要用于两种场景：

1. 作为 top-level 应用框架布局（As a top-level application decor or chrome layout）
2. 作为与一个或多个子 View 进行特殊交互的容器（As a container for a specific interaction with one or more child views）

+ Behaviros

  通过为 CoordinatorLayout 中的子View 指定 `Behaviors`，可以在单个 parent 中使用多种不同的交互，并且这些 view 之间也可以相互交互。View 类可以通过 `CoordinatorLayout.DefaultBehavior` 注解来指定一个作为 CoordinatorLayout 子 view 时的默认 behavior。

+ anchor

+ insetEdge












参考：

[CoordinatorLayout](https://developer.android.com/reference/android/support/design/widget/CoordinatorLayout)