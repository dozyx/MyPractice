> 先了解下 ListView 的缓存，有利于理解 RecyclerView 缓存的理解。详看参考资料。

概念：

* scrap view：已进入暂时 detached 状态的子 view。scrap view 可能被复用
* dirty view：在显示之前必须被 adapter 重新绑定的子 view
* 一个 Item 的显示包括 createView 和 bindView 两步



### ListView 缓存

ListView 通过内部类 RecycleBin 来实现缓存。

* `View[] mActiveViews` 缓存当前屏幕中的 view
* `ArrayList<View> mCurrentScrap` 缓存移出屏幕的 view，只有一个 viewType 的时候使用
* `ArrayList<View>[] mScrapViews` 缓存移出屏幕的 view，存在多个 viewType 的时候使用

两级缓存：mActiveViews 和 mScrapViews。



### RecyclerView 缓存

`Recycler` 负责缓存的实现。

四级缓存：

* `ArrayList<ViewHolder> mAttachedScrap` ：缓存屏幕内 Item
* `ArrayList<ViewHolder> mCachedViews`：缓存屏幕外的 Item，默认两个。可以直接复用而不需要重新 bindView。
* ` ViewCacheExtension mViewCacheExtension`：有开发者实现的缓存，默认不实现。
* `RecycledViewPool mRecyclerPool`：默认上限为 5，复用需要 bindView。



优势：

* mCacheViews 不需要进行 bindView 就能复用
* 多个 RecyclerView 可以共用一个 mRecyclerPool
* RecyclerView 实现了 ViewHolder 缓存









资料：

[Android ListView工作原理完全解析，带你从源码的角度彻底理解](https://blog.csdn.net/guolin_blog/article/details/44996879)

[Android ListView 与 RecyclerView 对比浅析：缓存机制](https://cloud.tencent.com/developer/article/1005658)