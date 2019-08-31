MotionLayout 可以让用户交互的 UI 元素具有动画效果。MotionLayout 是 ConstraintLayout 的子类，MotionLayout 可以在 layoutDescription 属性中指定一个 MotionScene 文件，该文件包含了动画的所有信息。



示例：

https://github.com/Moosphan/ConstraintSample



MotionLayout 根据 view 的开始和结束位置（也可以在中间插入位置），确定一条路径，然后根据 progress 来确定位置。当 progress 根据时间变化改变时就成了动画，我们也可以根据其他条件来设置 progress。





资料：

[Introduction to MotionLayout](https://medium.com/google-developers/introduction-to-motionlayout-part-i-29208674b10d)