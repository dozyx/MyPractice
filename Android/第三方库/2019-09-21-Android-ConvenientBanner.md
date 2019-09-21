[Android-ConvenientBanner](https://github.com/saiwu-bigkoo/Android-ConvenientBanner)

注意：

* 自动滚动需要手动设置时间

### 将 indicator 显示在 banner 下方

ConvenientBanner 的布局包含两部分：banber 展示部分（实际是一个 RecyclerView ）和 indicator 部分。这两部分放在一个 ReleativeLayout 中，banber 部分的宽高均为 match_parent，与 ReleativeLayout 一致；indicator 位于底部。

ConvenientBanner 没有提供直接修改布局的方法，所以 indicator 是与 banner 重叠的。

如果要实现将 indicator 展示在 banner 下方，可以这样实现：

* 法一：banner 展示位布局的 id 为 cbLoopViewPager，我们可以通过 findViewById 来找到这个 banner 的 view，然后设置它 bottom 的 padding 或 margin，这样就可以调整与 indicator 的距离。
* 法二：在设置的 banner 布局（即每个 item 的布局）中，添加 padding，使下面保持空白。



### 问题

#### 不显示

ScrollView 的子 View 为 LinearLayout，ConvenientBanner 放在 LinearLayout 中，item 显示不出来。CBPageAdapterHelper 的 onCreateViewHolder 中，parent.width 在运行时为 0，parent 即 banner 的控件，是一个 RecyclerView。

去掉 ScrollView 或改成其他 ViewGroup 后，能显示出来，但是 indicator 显示到了 LinearLayout 底部。

整个页面为一个 Fragment，放在 ViewPager 中。进一步测试发现，我将 banner 数据的加载放在 onStart 中，第一次进来没显示，然后返回桌面重新进入，能正常显示。。。不过，为什么不使用 ScrollView 第一次就能显示？

将数据加载改为异步之后（不是子线程，类似于 handler），第一次进来也能正常显示。

是因为 fragment 的加载时机导致 view 的宽度还没有被正确计算？不过为什么去掉 ScrollView 就正常。。。

数据加载改到 onResume 也一样。