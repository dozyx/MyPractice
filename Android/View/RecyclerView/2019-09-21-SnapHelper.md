[让你明明白白的使用RecyclerView——SnapHelper详解](https://www.jianshu.com/p/e54db232df62)

> 上面的文章写得很好，很详细，也很长。。。



作用：使 RecyclerView 在滑动后，停留到某个位置。

SnapHelper 是一个抽象类，官方库提供了两个实现：

* LinearSnapHelper：使某个 item 停留在中间位置
* PagerSnapHelper：实现类似于 ViewPager 的效果。

SnapHelper 有三个抽象方法：

```java
View findSnapView(RecyclerView.LayoutManager layoutManager)
```

确定进行 snap 的 view

```java
int[] calculateDistanceToFinalSnap(@NonNull RecyclerView.LayoutManager layoutManager, @NonNull View targetView)
```

计算 targetView 与 snap 的最终位置的距离。返回值为包含水平和垂直距离的数组。

```java
int findTargetSnapPosition(RecyclerView.LayoutManager layoutManager, int velocityX, int velocityY)
```

发生 fling 时，用来确定滚动到哪个位置。