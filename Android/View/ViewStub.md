ViewStub 的唯一缺陷是不支持 merge 标签。在使用时还要注意出现因为 id 而导致某个 View 为 null 的情况。



### setVisibility 和 inflate

使 ViewStub 的布局加载进来的方式有两种：setVisibility(int visibility)和 inflate()。

+ 在第一次调用，setVisibility(int visibility) 且 visibility 为 VISIBLE 或 INVISIBLE 时，ViewStub 将调用 inflate() 方法来加载布局，后续的调用将直接传给加载出来的 view。
+ inflate() 方法将布局加载到 ViewStub 所处的位置。

inflate() 只能调用一次，因为在 inflate 后，viewStub 将被移除，再次调用将导致异常。好像在源码中没看出非要调用 inflate() 的好处。。。



源码：

```java
/**
 * When visibility is set to {@link #VISIBLE} or {@link #INVISIBLE},
 * {@link #inflate()} is invoked and this StubbedView is replaced in its parent
 * by the inflated layout resource. After that calls to this function are passed
 * through to the inflated view.
 *
 * @param visibility One of {@link #VISIBLE}, {@link #INVISIBLE}, or {@link #GONE}.
 *
 * @see #inflate() 
 */
@Override
@android.view.RemotableViewMethod
public void setVisibility(int visibility) {
    if (mInflatedViewRef != null) {
        View view = mInflatedViewRef.get();
        if (view != null) {
            view.setVisibility(visibility);
        } else {
            throw new IllegalStateException("setVisibility called on un-referenced view");
        }
    } else {
        super.setVisibility(visibility);
        if (visibility == VISIBLE || visibility == INVISIBLE) {
            inflate();
        }
    }
}

/**
 * Inflates the layout resource identified by {@link #getLayoutResource()}
 * and replaces this StubbedView in its parent by the inflated layout resource.
 *
 * @return The inflated layout resource.
 *
 */
public View inflate() {
    final ViewParent viewParent = getParent();

    if (viewParent != null && viewParent instanceof ViewGroup) {
        if (mLayoutResource != 0) {
            final ViewGroup parent = (ViewGroup) viewParent;
            final LayoutInflater factory;
            if (mInflater != null) {
                factory = mInflater;
            } else {
                factory = LayoutInflater.from(mContext);
            }
            final View view = factory.inflate(mLayoutResource, parent,
                    false);

            if (mInflatedId != NO_ID) {
                view.setId(mInflatedId);
            }

            final int index = parent.indexOfChild(this);
            parent.removeViewInLayout(this);

            final ViewGroup.LayoutParams layoutParams = getLayoutParams();
            if (layoutParams != null) {
                parent.addView(view, index, layoutParams);
            } else {
                parent.addView(view, index);
            }

            mInflatedViewRef = new WeakReference<View>(view);

            if (mInflateListener != null) {
                mInflateListener.onInflate(this, view);
            }

            return view;
        } else {
            throw new IllegalArgumentException("ViewStub must have a valid layoutResource");
        }
    } else {
        throw new IllegalStateException("ViewStub must have a non-null ViewGroup viewParent");
    }
}
```