



### 定制

#### 无法设置可见 item 数量

[参考](https://github.com/Bigkoo/Android-PickerView/issues/713)

WheelView 中有一个变量 itemsVisible 配置可见的 item 数量，不过该变量是 private 的。如果想要修改显示数量，可以采用以下两种方式：

* 使 WheelView 高度固定（也可设置父 view 的高度固定），设置 gravity 为 居中
* 使用反射



#### label 居中

WheelView 的一个属性 isCenterLabel 可以用来控制只显示居中 item 的 label。需要注意，isCenterLabel 为 true 时，label 只会显示在右边。



#### WheelView 点击下一个 item，第二次没有触发

> WheelView 计算触摸点击事件时计算好像有点问题



