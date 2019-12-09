> 先了解下 ListView 的缓存，有利于理解 RecyclerView 缓存的理解。详看参考资料。

概念：

* scrap view：已进入暂时 detached 状态的子 view。scrap view 可能被复用
* dirty view：在显示之前必须被 adapter 重新绑定的子 view
* 一个 Item 的显示包括 createView 和 bindView 两步



### 高级用法

### 局部 bind

`RecyclerView.Adapter` 中有一个带 payloads 参数的 onBindViewHolder() 方法

```
        public void onBindViewHolder(@NonNull VH holder, int position,
                @NonNull List<Object> payloads) {
            onBindViewHolder(holder, position);
        }
```

它的默认实现就是直接回调带两个参数的重载方法。

当我们只想刷新 item 里的某个 view 时，通过重载该方法来实现部分的 bind，可以提高 RecyclerView 的性能。

在 `Adatper#notifyXXX()` 方法中，有的方法可以传入一个 payload 的 Object，表示该 item 只有部分发生了改变，payload 用来携带修改的信息。因为多次调用 notifyXXX() 传入的 payload 可能被合并，所以这里传入的是一个 List<Object>。

需要注意，在某些情况下，payload 可能被丢弃。

比如：

```kotlin
adapter.notifyItemChanged(2)
adapter.notifyItemChanged(2,"1111")
// "1111" 会被丢弃，因为需要进行 full bind
```

> payload 有效负载，在计算机中指的是传输数据中实际的预期数据，即有用数据。



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