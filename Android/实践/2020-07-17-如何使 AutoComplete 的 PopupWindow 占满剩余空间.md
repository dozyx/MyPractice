

难点：

* AutoCompleteTextView 无法直接获取到 popup window
* setDropDownHeight 设置为 match parent 会导致 popup window 占满全屏



处理：

* 类似于 PopupWindow#getMaxAvailableHeight 计算出最大高度
* setDropDownHeight 设置高度为最大高度
  * 出现另一个问题：输入法收起来之后，高度没有变化
  * setDropDownHeight 不会触发 window 改变



解决方案：

> 暂时没找到合适的方法

* 使用一个背景 view，在自动补全弹窗 show、dismiss 的时候显示、隐藏。

