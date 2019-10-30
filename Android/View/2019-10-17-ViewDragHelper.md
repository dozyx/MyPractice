作用：工具类，提供了许多用来在父 ViewGroup 中拖动和重新放置 view 的有用操作和状态跟踪。

ViewDragHelper 实例通过静态方法 `create(ViewGroup forParent, Callback cb)`获取，第一个参数为要监视的父 view，第二个参数为 drag 提供相关的信息和处理事件。

ViewDragHelper 通过 ViewGroup 的 onInterceptTouchEvent(ev) 和 onTouchEvent(ev) 两个方法来 hook 触摸事件实现 drag。所以，需要在这父 ViewGroup 的这两个方法中分别调用 `ViewDragHelper#shouldInterceptTouchEvent(ev)` 和 `ViewDragHelper#processTouchEvent(ev)`，接着，就可以通过 `Callback` 来实现拖拉子 view。但是，仅仅是这样子 view 还是不能被 drag 的，还需要在 `Callback` 中提供一些其他信息。

### Callback 重要方法

Callback 是一个抽象类，它只有一个方法是抽象的：

`public abstract boolean tryCaptureView(@NonNull View child, int pointerId)`

如果想要对该子 view 进行 drag，则应该返回 ture。

* （重要）`int clampViewPositionVertical(@NonNull View child, int top, int dy)`：限制子 View 在垂直方向移动的量，默认实现会返回 0，即不允许垂直移动。所以如果希望 drag 可以垂直移动则必须实现该方法。返回一个非 0 值之后，子 View 就可以进行了 drag 的动作了。还需要注意的一点是，第二个参数 top 表示的的是**尝试移动**的位置，即已经包含了 dy 的移动量。返回值为子 view 新的 top 位置，如果希望移动的量与触摸一致则直接返回 top。

  > clamp：英文翻译为夹紧，按我的理解是限制在某个范围。

* `int clampViewPositionHorizontal(@NonNull View child, int left, int dx)`

* `void onViewDragStateChanged(int state)`：drag 状态发生变化

  * 三种状态：

    STATE_IDLE：没有被 drag 或者 fling、snap

    STATE_DRAGGING：正在 drag 

    STATE_SETTLING：处于放置的状态，比如 fling 之后或者其他非交互的动作。

* `void onViewPositionChanged(…)`：drag 或 settle 导致的位置变化

* `int getViewVerticalDragRange(View child)` 返回可拖拽子 view 垂直运动范围的大小。如果不能垂直移动则应该返回 0。

  > 不是很理解这个方法。我在代码里返回了 0，还是可以实现 drag。源码中，这个方法主要影响了 touch slop 的计算，以及 settle 时间的计算。
  >
  > 个人理解这个方法并不是拿来限制移动的，而是提供一个移动范围的值，然后 ViewDragHelper 用来进行一些计算。

* `int getViewHorizontalDragRange(View child)` 

* `void onViewReleased(View releasedChild, float xvel, float yvel)` 子 view 脱离 drag 状态时回调。可在该回调通过 `ViewDragHelper#settleCapturedViewAt(int, int)` 和 `ViewDragHelper#flingCapturedView(int, int, int, int)`方法来实现 settle  和 fling，如果调用了这两个方法的话，ViewDragHelper 将进入 STATE_SETTLING 状态，否则子 view 将停住，ViewDragHelper 进入 STATE_IDLE 状态。

  > settleCapturedViewAt() 返回 true 的话，需要为接下来的每一帧刷新调用 continueSettling(boolean) 来保持移动的持续，并且当 continueSettling(boolean) 返回 true 时，也需要继续调用，直到 返回 false。
  >
  > settleCapturedViewAt() 内部的实现是调用了 Scroller 的 startScroll() 方法，所以，跟 Scroller 一样，移动并不是在这个方法里产生的。实际的移动依靠的的是 continueSettling()，continueSettings() 调用了ViewCompat.offsetLeftAndRight() 来移动一定的量，这个移动的量通过 Scroller 计算得到。
  >
  > 从上面的分析可以知道，要使移动可以持续，就要像 Scroller 一样不断触发重绘。一种方式是在 View 的 computeScroll() 方法中调用并不断 invalid，另一种是类似于 BottomSheetBehavior 中使用 ViewCompat.postOnAnimation() 运行一个 SettleRunnable 的 task，在 task 中调用 continueSettling()，并在返回 true 时继续 postOnAnimation()。



### 总结

1. 需要在 ViewGroup 的 onInterceptTouchEvent(ev) 和 onTouchEvent(ev) 方法中分别调用 ViewDragHelper 的 `shouldInterceptTouchEvent(ev)` 和 `processTouchEvent(ev)` 来将 event 传递给 ViewDragHelper
2. 一个被 drag 的 view 可能处于三个状态：STATE_IDLE 空闲，STATE_DRAGGING 正在被 drag，STATE_SETTLING fling 或平滑滚动中。
3. ViewDragHelper#Calllback 提供 drag 所需要的信息
   * `tryCaptureView()` 决定是否对该子 view 进行 drag
   * `clampViewPositionXXX()` 方法返回要移动的距离
   * `onViewReleased()` 子 view 脱离 darg 状态。在这个回调中进行 fling 处理或者将子 view 放置到新的位置。
4. `ViewDragHelper#settleCapturedViewAt()` 将拖拽的 view 平滑滚动到其他位置，需要持续调用 `continueSettling()` 来实现持续移动。



### 附：源码分析

> 分析得有点烂，还是根据问题看实际代码吧。。。

### ViewDragHelper#shouldInterceptTouchEvent

该方法用来检查 parent view 的 onInterceptTouchEvent 是否应该拦截触摸事件，拦截之后，parent view 将调用自己的 onTouchEvent()，并可以选择在 onTouchEvent() 中将 event 移交给 ViewDragHelper 的 processTouchEvent() 方法。只有当 ViewDragHelper 状态为 STATE_DRAGGING 时，该方法会返回 true。

> 不明白这个方法的返回值什么时候会为 true。因为第一次触摸的时候状态肯定不是 STATE_DRAGGING，那么会返回 false，如果子 view 也没有消耗 event，那么将调用到 parent 的 onTouchEvent()，这时候如果需要进行 drag，则 parent 的 onTouchEvent() 返回了 true，状态变为了 STATE_DRAGGING，但是因为 parent 已经接手了 event 流，那么 parent 的 onInterceptTouchEvent() 也不会再次被调用，如果没有在其他地方调用 ViewDragHelper 的 shouldInterceptTouchEvent() 的话，这个方法也就不会再次被调用。即 shouldInterceptTouchEvent() 不会在 STATE_DRAGGING 状态进入，自然无法返回 true。并且只会接收到一次 Down 事件，后续的 move 和 up 都不再触发该方法。
>
> 所以，只能把这个方法理解为根据 event 来改变 ViewDragHelper 的一些信息。

```java
    public boolean shouldInterceptTouchEvent(@NonNull MotionEvent ev) {
        final int action = ev.getActionMasked();
        final int actionIndex = ev.getActionIndex();

        if (action == MotionEvent.ACTION_DOWN) {
            // Reset things for a new event stream, just in case we didn't get
            // the whole previous stream.
            // 重置状态
            cancel();
        }

        // 设置速度跟踪
        if (mVelocityTracker == null) {
            mVelocityTracker = VelocityTracker.obtain();
        }
        mVelocityTracker.addMovement(ev);

        switch (action) {
            case MotionEvent.ACTION_DOWN: {
                final float x = ev.getX();
                final float y = ev.getY();
                final int pointerId = ev.getPointerId(0);
                saveInitialMotion(x, y, pointerId);

                final View toCapture = findTopChildUnder((int) x, (int) y);

                // Catch a settling view if possible.
                // setting 过程中重新 capture 之前的 drag 的 view
                if (toCapture == mCapturedView && mDragState == STATE_SETTLING) {
                    tryCaptureViewForDrag(toCapture, pointerId);
                }

                final int edgesTouched = mInitialEdgesTouched[pointerId];
                if ((edgesTouched & mTrackingEdges) != 0) {
                    mCallback.onEdgeTouched(edgesTouched & mTrackingEdges, pointerId);
                }
                break;
            }
            ...
            // 从前面分析，其他 event 并不会触发，所以不继续做分析。其实这些 event 的处理与 processTouchEvent 类似

        }

        return mDragState == STATE_DRAGGING;
    }
```



### ViewDragHelper#processTouchEvent

在 parent 的 onToucheEvent 方法中调用该方法。

```java
    public void processTouchEvent(@NonNull MotionEvent ev) {
        final int action = ev.getActionMasked();
        final int actionIndex = ev.getActionIndex();

        if (action == MotionEvent.ACTION_DOWN) {
            // Reset things for a new event stream, just in case we didn't get
            // the whole previous stream.
            cancel();
        }

        if (mVelocityTracker == null) {
            mVelocityTracker = VelocityTracker.obtain();
        }
        mVelocityTracker.addMovement(ev);

        switch (action) {
            case MotionEvent.ACTION_DOWN: {
                final float x = ev.getX();
                final float y = ev.getY();
                final int pointerId = ev.getPointerId(0);
                final View toCapture = findTopChildUnder((int) x, (int) y);

                saveInitialMotion(x, y, pointerId);

                // Since the parent is already directly processing this touch event,
                // there is no reason to delay for a slop before dragging.
                // Start immediately if possible.
                tryCaptureViewForDrag(toCapture, pointerId);

                final int edgesTouched = mInitialEdgesTouched[pointerId];
                if ((edgesTouched & mTrackingEdges) != 0) {
                    mCallback.onEdgeTouched(edgesTouched & mTrackingEdges, pointerId);
                }
                break;
            }

            case MotionEvent.ACTION_POINTER_DOWN: {
                // 存在多个触摸点，需要根据新的触摸点来处理 event
                final int pointerId = ev.getPointerId(actionIndex);
                final float x = ev.getX(actionIndex);
                final float y = ev.getY(actionIndex);

                saveInitialMotion(x, y, pointerId);

                // A ViewDragHelper can only manipulate one view at a time.
                if (mDragState == STATE_IDLE) {
                    // If we're idle we can do anything! Treat it like a normal down event.

                    final View toCapture = findTopChildUnder((int) x, (int) y);
                    tryCaptureViewForDrag(toCapture, pointerId);

                    final int edgesTouched = mInitialEdgesTouched[pointerId];
                    if ((edgesTouched & mTrackingEdges) != 0) {
                        mCallback.onEdgeTouched(edgesTouched & mTrackingEdges, pointerId);
                    }
                } else if (isCapturedViewUnder((int) x, (int) y)) {
                    // We're still tracking a captured view. If the same view is under this
                    // point, we'll swap to controlling it with this pointer instead.
                    // (This will still work if we're "catching" a settling view.)

                    tryCaptureViewForDrag(mCapturedView, pointerId);
                }
                break;
            }

            case MotionEvent.ACTION_MOVE: {
                if (mDragState == STATE_DRAGGING) {
                    // If pointer is invalid then skip the ACTION_MOVE.
                    if (!isValidPointerForActionMove(mActivePointerId)) break;

                    final int index = ev.findPointerIndex(mActivePointerId);
                    final float x = ev.getX(index);
                    final float y = ev.getY(index);
                    final int idx = (int) (x - mLastMotionX[mActivePointerId]);
                    final int idy = (int) (y - mLastMotionY[mActivePointerId]);
                    // drag 动作，dragTo 中会调用 Callback 的 clampViewPositionXXX 方法
                    dragTo(mCapturedView.getLeft() + idx, mCapturedView.getTop() + idy, idx, idy);

                    saveLastMotion(ev);
                } else {
                    // Check to see if any pointer is now over a draggable view.
                    final int pointerCount = ev.getPointerCount();
                    for (int i = 0; i < pointerCount; i++) {
                        final int pointerId = ev.getPointerId(i);

                        // If pointer is invalid then skip the ACTION_MOVE.
                        if (!isValidPointerForActionMove(pointerId)) continue;

                        final float x = ev.getX(i);
                        final float y = ev.getY(i);
                        final float dx = x - mInitialMotionX[pointerId];
                        final float dy = y - mInitialMotionY[pointerId];

                        reportNewEdgeDrags(dx, dy, pointerId);
                        if (mDragState == STATE_DRAGGING) {
                            // Callback might have started an edge drag.
                            break;
                        }

                        final View toCapture = findTopChildUnder((int) x, (int) y);
                        if (checkTouchSlop(toCapture, dx, dy)
                                && tryCaptureViewForDrag(toCapture, pointerId)) {
                            break;
                        }
                    }
                    saveLastMotion(ev);
                }
                break;
            }

            case MotionEvent.ACTION_POINTER_UP: {
                // 一个触摸点移除，需要找到另一个触摸点
                final int pointerId = ev.getPointerId(actionIndex);
                if (mDragState == STATE_DRAGGING && pointerId == mActivePointerId) {
                    // Try to find another pointer that's still holding on to the captured view.
                    int newActivePointer = INVALID_POINTER;
                    final int pointerCount = ev.getPointerCount();
                    for (int i = 0; i < pointerCount; i++) {
                        final int id = ev.getPointerId(i);
                        if (id == mActivePointerId) {
                            // This one's going away, skip.
                            continue;
                        }

                        final float x = ev.getX(i);
                        final float y = ev.getY(i);
                        if (findTopChildUnder((int) x, (int) y) == mCapturedView
                                && tryCaptureViewForDrag(mCapturedView, id)) {
                            newActivePointer = mActivePointerId;
                            break;
                        }
                    }

                    if (newActivePointer == INVALID_POINTER) {
                        // We didn't find another pointer still touching the view, release it.
                        releaseViewForPointerUp();
                    }
                }
                clearMotionHistory(pointerId);
                break;
            }

            case MotionEvent.ACTION_UP: {
                if (mDragState == STATE_DRAGGING) {
                    releaseViewForPointerUp();
                }
                cancel();
                break;
            }

            case MotionEvent.ACTION_CANCEL: {
                if (mDragState == STATE_DRAGGING) {
                    dispatchViewReleased(0, 0);
                }
                cancel();
                break;
            }
        }
    }
```









参考：

[ViewDragHelper](https://developer.android.com/reference/android/support/v4/widget/ViewDragHelper)