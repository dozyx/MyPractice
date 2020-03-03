> 在使用 [Android-ConvenientBanner](https://github.com/saiwu-bigkoo/Android-ConvenientBanner) 的过程中，遇到了一个很奇怪的问题——设置的 banner 图片显示不出来。具体的现象描述可以查看《2019-09-24-Android-ConvenientBanner》里关于不显示的问题。简单来说就是，banner 放到一个 ScrollView 中，在 Activity 中配置 banner 数据，结果图片没有显示出来，banner 控件的高度为 wrap_content，当我将高度改成固定高度或者延迟设置 banner 数据时，图片能正常显示。
>
> 为了查找原因，接下来就是一波漫长的分析。。。

首先这个 banner 库是这样子的，ConvenientBanner 是 banner 控件，它继承于 RelativeLayout，它有两个子 view：CBLoopViewPager 和 LinearLayout。LinearLayout 用于添加指示器，这个不管。CBLoopViewPager 是展示 banner 的实际控件，它继承 RecyclerView。既然显示不出来，那就应该是跟 item view 的创建有关，既然是 RecyclerView，那么 item 的创建就跟 adapter 有关了，这个 adapter 是 CBPageAdapter，查看它的 onCreateViewHolder 方法：

```java
    @Override
    public Holder onCreateViewHolder(ViewGroup parent, int viewType) {
        int layoutId = creator.getLayoutId();
        View itemView = LayoutInflater.from(parent.getContext()).inflate(layoutId, parent, false);
        helper.onCreateViewHolder(parent,itemView);
        return creator.createHolder(itemView);
    }
```

在这个方法中，item view 被创建，helper 是 CBPageAdapterHelper，查看它的 onCreateViewHolder 方法：

```java
    public void onCreateViewHolder(ViewGroup parent, View itemView) {
        RecyclerView.LayoutParams lp = (RecyclerView.LayoutParams) itemView.getLayoutParams();
        lp.width = parent.getWidth() - ScreenUtil.dip2px(itemView.getContext(), 2 * (sPagePadding + sShowLeftCardWidth));
        itemView.setLayoutParams(lp);
    }
```

可以看到，在这个方法中会对 itemView 的宽度重新计算，通常情况就是使每个 item 的宽度与 RecyclerView 一致。通过添加断点，我发现当图片不显示的时候 parent.getWidth() 值为 0。这样宽度为 0，设置的图片自然无法显示。

那么，为什么会是 0 呢？为什么将 ConvenientBanner 改成固定高度就正常了呢？

于是（其实并没有这么简单就到了于是，中间还折腾了比较久，毕竟为了看这个问题，我看到了凌晨一点半，中间的一些其他尝试忘了，所以下面的分析与实际分析过程会有不同），我给 `CBPageAdapterHelper#onCreateViewHolder` 加上断点进行调试。

> 这次调试主要用的是非中断的断点，可以添加 log，输入 stack trace。一开始是为了断点输出 log，后面熟悉后发现还能输入 stack trace，嗯，真香，有点相见恨晚。

不显示时，stack trace 是这样的：

```java
Breakpoint reached at com.bigkoo.convenientbanner.adapter.CBPageAdapterHelper.onCreateViewHolder(CBPageAdapterHelper.java:22)
Breakpoint reached
	  at com.bigkoo.convenientbanner.adapter.CBPageAdapterHelper.onCreateViewHolder(CBPageAdapterHelper.java:22)
	  at com.bigkoo.convenientbanner.adapter.CBPageAdapter.onCreateViewHolder(CBPageAdapter.java:37)
	  at com.bigkoo.convenientbanner.adapter.CBPageAdapter.onCreateViewHolder(CBPageAdapter.java:18)
	  at androidx.recyclerview.widget.RecyclerView$Adapter.createViewHolder(RecyclerView.java:6794)
	  at androidx.recyclerview.widget.RecyclerView$Recycler.tryGetViewHolderForPositionByDeadline(RecyclerView.java:5975)
	  at androidx.recyclerview.widget.RecyclerView$Recycler.getViewForPosition(RecyclerView.java:5858)
	  at androidx.recyclerview.widget.RecyclerView$Recycler.getViewForPosition(RecyclerView.java:5854)
	  at androidx.recyclerview.widget.LinearLayoutManager$LayoutState.next(LinearLayoutManager.java:2230)
	  at androidx.recyclerview.widget.LinearLayoutManager.layoutChunk(LinearLayoutManager.java:1557)
	  at androidx.recyclerview.widget.LinearLayoutManager.fill(LinearLayoutManager.java:1517)
	  at androidx.recyclerview.widget.LinearLayoutManager.onLayoutChildren(LinearLayoutManager.java:612)
	  at androidx.recyclerview.widget.RecyclerView.dispatchLayoutStep2(RecyclerView.java:3924)
	  at androidx.recyclerview.widget.RecyclerView.onMeasure(RecyclerView.java:3336)
	  at android.view.View.measure(View.java:23223)
	  at android.widget.RelativeLayout.measureChildHorizontal(RelativeLayout.java:715)
	  at android.widget.RelativeLayout.onMeasure(RelativeLayout.java:461)
	  at android.view.View.measure(View.java:23223)
	  at android.view.ViewGroup.measureChildWithMargins(ViewGroup.java:6753)
	  at android.widget.LinearLayout.measureChildBeforeLayout(LinearLayout.java:1535)
	  at android.widget.LinearLayout.measureHorizontal(LinearLayout.java:1187)
	  at android.widget.LinearLayout.onMeasure(LinearLayout.java:706)
	  at android.view.View.measure(View.java:23223)
	  at androidx.core.widget.NestedScrollView.measureChildWithMargins(NestedScrollView.java:1534)
	  at android.widget.FrameLayout.onMeasure(FrameLayout.java:185)
	  at androidx.core.widget.NestedScrollView.onMeasure(NestedScrollView.java:581)
	  at android.view.View.measure(View.java:23223)
	  at android.view.ViewGroup.measureChildWithMargins(ViewGroup.java:6753)
	  at android.widget.LinearLayout.measureChildBeforeLayout(LinearLayout.java:1535)
	  at android.widget.LinearLayout.measureVertical(LinearLayout.java:825)
	  at android.widget.LinearLayout.onMeasure(LinearLayout.java:704)
	  at android.view.View.measure(View.java:23223)
	  at android.view.ViewGroup.measureChildWithMargins(ViewGroup.java:6753)
	  at android.widget.FrameLayout.onMeasure(FrameLayout.java:185)
	  at androidx.appcompat.widget.ContentFrameLayout.onMeasure(ContentFrameLayout.java:143)
	  at android.view.View.measure(View.java:23223)
	  at android.view.ViewGroup.measureChildWithMargins(ViewGroup.java:6753)
	  at androidx.appcompat.widget.ActionBarOverlayLayout.onMeasure(ActionBarOverlayLayout.java:403)
	  at android.view.View.measure(View.java:23223)
	  at android.view.ViewGroup.measureChildWithMargins(ViewGroup.java:6753)
	  at android.widget.FrameLayout.onMeasure(FrameLayout.java:185)
	  at android.view.View.measure(View.java:23223)
	  at android.view.ViewGroup.measureChildWithMargins(ViewGroup.java:6753)
	  at android.widget.LinearLayout.measureChildBeforeLayout(LinearLayout.java:1535)
	  at android.widget.LinearLayout.measureVertical(LinearLayout.java:825)
	  at android.widget.LinearLayout.onMeasure(LinearLayout.java:704)
	  at android.view.View.measure(View.java:23223)
	  at android.view.ViewGroup.measureChildWithMargins(ViewGroup.java:6753)
	  at android.widget.FrameLayout.onMeasure(FrameLayout.java:185)
	  at com.android.internal.policy.DecorView.onMeasure(DecorView.java:737)
	  at android.view.View.measure(View.java:23223)
	  at android.view.ViewRootImpl.performMeasure(ViewRootImpl.java:2807)
	  at android.view.ViewRootImpl.measureHierarchy(ViewRootImpl.java:1657)
	  at android.view.ViewRootImpl.performTraversals(ViewRootImpl.java:1941)
	  at android.view.ViewRootImpl.doTraversal(ViewRootImpl.java:1545)
	  at android.view.ViewRootImpl$TraversalRunnable.run(ViewRootImpl.java:7439)
	  at android.view.Choreographer$CallbackRecord.run(Choreographer.java:1006)
	  at android.view.Choreographer.doCallbacks(Choreographer.java:818)
	  at android.view.Choreographer.doFrame(Choreographer.java:753)
	  at android.view.Choreographer$FrameDisplayEventReceiver.run(Choreographer.java:992)
	  at android.os.Handler.handleCallback(Handler.java:873)
	  at android.os.Handler.dispatchMessage(Handler.java:99)
	  at android.os.Looper.loop(Looper.java:207)
	  at android.app.ActivityThread.main(ActivityThread.java:6820)
	  at java.lang.reflect.Method.invoke(Method.java:-1)
	  at com.android.internal.os.RuntimeInit$MethodAndArgsCaller.run(RuntimeInit.java:547)
	  at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:876)
```

改成固定高度，正常显示：

```java
Breakpoint reached at com.bigkoo.convenientbanner.adapter.CBPageAdapterHelper.onCreateViewHolder(CBPageAdapterHelper.java:22)
Breakpoint reached
	  at com.bigkoo.convenientbanner.adapter.CBPageAdapterHelper.onCreateViewHolder(CBPageAdapterHelper.java:22)
	  at com.bigkoo.convenientbanner.adapter.CBPageAdapter.onCreateViewHolder(CBPageAdapter.java:37)
	  at com.bigkoo.convenientbanner.adapter.CBPageAdapter.onCreateViewHolder(CBPageAdapter.java:18)
	  at androidx.recyclerview.widget.RecyclerView$Adapter.createViewHolder(RecyclerView.java:6794)
	  at androidx.recyclerview.widget.RecyclerView$Recycler.tryGetViewHolderForPositionByDeadline(RecyclerView.java:5975)
	  at androidx.recyclerview.widget.RecyclerView$Recycler.getViewForPosition(RecyclerView.java:5858)
	  at androidx.recyclerview.widget.RecyclerView$Recycler.getViewForPosition(RecyclerView.java:5854)
	  at androidx.recyclerview.widget.LinearLayoutManager$LayoutState.next(LinearLayoutManager.java:2230)
	  at androidx.recyclerview.widget.LinearLayoutManager.layoutChunk(LinearLayoutManager.java:1557)
	  at androidx.recyclerview.widget.LinearLayoutManager.fill(LinearLayoutManager.java:1517)
	  at androidx.recyclerview.widget.LinearLayoutManager.onLayoutChildren(LinearLayoutManager.java:612)
	  at androidx.recyclerview.widget.RecyclerView.dispatchLayoutStep2(RecyclerView.java:3924)
	  at androidx.recyclerview.widget.RecyclerView.dispatchLayout(RecyclerView.java:3641)
	  at androidx.recyclerview.widget.RecyclerView.onLayout(RecyclerView.java:4194)
	  at android.view.View.layout(View.java:20726)
	  at android.view.ViewGroup.layout(ViewGroup.java:6198)
	  at android.widget.RelativeLayout.onLayout(RelativeLayout.java:1083)
	  at android.view.View.layout(View.java:20726)
	  at android.view.ViewGroup.layout(ViewGroup.java:6198)
	  at android.widget.LinearLayout.setChildFrame(LinearLayout.java:1812)
	  at android.widget.LinearLayout.layoutHorizontal(LinearLayout.java:1801)
	  at android.widget.LinearLayout.onLayout(LinearLayout.java:1567)
	  at android.view.View.layout(View.java:20726)
	  at android.view.ViewGroup.layout(ViewGroup.java:6198)
	  at android.widget.FrameLayout.layoutChildren(FrameLayout.java:323)
	  at android.widget.FrameLayout.onLayout(FrameLayout.java:261)
	  at androidx.core.widget.NestedScrollView.onLayout(NestedScrollView.java:1787)
	  at android.view.View.layout(View.java:20726)
	  at android.view.ViewGroup.layout(ViewGroup.java:6198)
	  at android.widget.LinearLayout.setChildFrame(LinearLayout.java:1812)
	  at android.widget.LinearLayout.layoutVertical(LinearLayout.java:1656)
	  at android.widget.LinearLayout.onLayout(LinearLayout.java:1565)
	  at android.view.View.layout(View.java:20726)
	  at android.view.ViewGroup.layout(ViewGroup.java:6198)
	  at android.widget.FrameLayout.layoutChildren(FrameLayout.java:323)
	  at android.widget.FrameLayout.onLayout(FrameLayout.java:261)
	  at android.view.View.layout(View.java:20726)
	  at android.view.ViewGroup.layout(ViewGroup.java:6198)
	  at androidx.appcompat.widget.ActionBarOverlayLayout.onLayout(ActionBarOverlayLayout.java:446)
	  at android.view.View.layout(View.java:20726)
	  at android.view.ViewGroup.layout(ViewGroup.java:6198)
	  at android.widget.FrameLayout.layoutChildren(Fra meLayout.java:323)
	  at android.widget.FrameLayout.onLayout(FrameLayout.java:261)
	  at android.view.View.layout(View.java:20726)
	  at android.view.ViewGroup.layout(ViewGroup.java:6198)
	  at android.widget.LinearLayout.setChildFrame(LinearLayout.java:1812)
	  at android.widget.LinearLayout.layoutVertical(LinearLayout.java:1656)
	  at android.widget.LinearLayout.onLayout(LinearLayout.java:1565)
	  at android.view.View.layout(View.java:20726)
	  at android.view.ViewGroup.layout(ViewGroup.java:6198)
	  at android.widget.FrameLayout.layoutChildren(FrameLayout.java:323)
	  at android.widget.FrameLayout.onLayout(FrameLayout.java:261)
	  at com.android.internal.policy.DecorView.onLayout(DecorView.java:774)
	  at android.view.View.layout(View.java:20726)
	  at android.view.ViewGroup.layout(ViewGroup.java:6198)
	  at android.view.ViewRootImpl.performLayout(ViewRootImpl.java:2881)
	  at android.view.ViewRootImpl.performTraversals(ViewRootImpl.java:2408)
	  at android.view.ViewRootImpl.doTraversal(ViewRootImpl.java:1545)
	  at android.view.ViewRootImpl$TraversalRunnable.run(ViewRootImpl.java:7439)
	  at android.view.Choreographer$CallbackRecord.run(Choreographer.java:1006)
	  at android.view.Choreographer.doCallbacks(Choreographer.java:818)
	  at android.view.Choreographer.doFrame(Choreographer.java:753)
	  at android.view.Choreographer$FrameDisplayEventReceiver.run(Choreographer.java:992)
	  at android.os.Handler.handleCallback(Handler.java:873)
	  at android.os.Handler.dispatchMessage(Handler.java:99)
	  at android.os.Looper.loop(Looper.java:207)
	  at android.app.ActivityThread.main(ActivityThread.java:6820)
	  at java.lang.reflect.Method.invoke(Method.java:-1)
	  at com.android.internal.os.RuntimeInit$MethodAndArgsCaller.run(RuntimeInit.java:547)
	  at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:876)
```

比较两次的 stack trace 可以发现，第一个的 onCreateViewHolder 是发生在 `RecyclerView#onMeasure` 中，而第二个是发生在 `RecyclerView#onLayout` 中，再看一遍 `CBPageAdapterHelper#onCreateViewHolder` 里计算的 parent.getWidth()，对应实现为 `View#getWidth()`：

```java
    public final int getWidth() {
        return mRight - mLeft;
    }
```

查看 View 的源码，可以发现 mRight 和 mLeft 都是在 onLayout 中赋值的，那么在 onMeasure 中 getWidth() 只能得到 0。

继续看 RecyclerView 的 onMeasure 方法：

```java
@Override
    protected void onMeasure(int widthSpec, int heightSpec) {
        if (mLayout == null) {
            defaultOnMeasure(widthSpec, heightSpec);
            return;
        }
        if (mLayout.isAutoMeasureEnabled()) {
            final int widthMode = MeasureSpec.getMode(widthSpec);
            final int heightMode = MeasureSpec.getMode(heightSpec);

            /**
             * This specific call should be considered deprecated and replaced with
             * {@link #defaultOnMeasure(int, int)}. It can't actually be replaced as it could
             * break existing third party code but all documentation directs developers to not
             * override {@link LayoutManager#onMeasure(int, int)} when
             * {@link LayoutManager#isAutoMeasureEnabled()} returns true.
             */
            mLayout.onMeasure(mRecycler, mState, widthSpec, heightSpec);

            final boolean measureSpecModeIsExactly =
                    widthMode == MeasureSpec.EXACTLY && heightMode == MeasureSpec.EXACTLY;
            if (measureSpecModeIsExactly || mAdapter == null) {
                return;
            }

            if (mState.mLayoutStep == State.STEP_START) {
                dispatchLayoutStep1();
            }
            // set dimensions in 2nd step. Pre-layout should happen with old dimensions for
            // consistency
            mLayout.setMeasureSpecs(widthSpec, heightSpec);
            mState.mIsMeasuring = true;
            dispatchLayoutStep2();

            ...
        } else {
            ...
        }
    }
```

可以看到，当 RecyclerView 的高度或者宽度有一个不是精确的值时，会调用 dispatchLayoutStep2() 进行预布局。而使用 ScrollView 时，RecyclerView 用 wrap_content 时就会走到预布局阶段，提前触发了 adapter 创建 ViewHolder。

> 注意：ScrollView 的唯一子 View 的高度会被指定为 MeasureSpec.UNSPECIFIED。





#### 总结

经过分析，之所以不显示是因为 ScrollView 导致 RecyclerView 在 onMeasure 中的预布局导致 `CBPageAdapterHelper#onCreateViewHolder` 里使用的宽度不正确。而为什么延迟之后正常，是因为加上延迟之后，onLayout 已经走过一遍，这时候 getWidth() 已经不是 0。