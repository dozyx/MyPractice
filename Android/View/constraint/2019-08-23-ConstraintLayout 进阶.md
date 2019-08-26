在 2.0.0 版本中，ConstraintLayout 除了本身的库之外，还多了一个 solver 库。其中，solver 使用 Cassowary  算法将约束转换为实际的位置和大小。这部分只是做了下了解，没怎么看，具体参考

[Difference between “ConstraintLayout for android” and “Solver for ConstraintLayout” in android studio SDK tools](https://stackoverflow.com/questions/43366746/difference-between-constraintlayout-for-android-and-solver-for-constraintlayo)

[从 Auto Layout 的布局算法谈性能](https://draveness.me/layout-performance)



###  ConstraintHelper 

ConstraintHelper 继承于 View，它可以引用多个 view 的 id，并为它们指定行为，它的实现包括 Group 和 Barrier。它的一个神奇的属性就是 `constraint_referenced_ids`。我们也可以根据自己的需求实现自己的 ConstraintHelper，

参考

https://github.com/samlu/ConstraintRadioGroup/blob/master/blRadioGroup.java

[ConstraintHelpers 介绍和自定义实现](https://www.polidea.com/blog/android-constraintlayout-the-guide-to-constrainthelpers/)