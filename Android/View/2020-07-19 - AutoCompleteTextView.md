AutoCompleteTextView 继承于 EditText，所以它本质上也是一个编辑框。主要实现了：

- 监听输入产生自动补全数据
- 使用 ListPopupWindow 来承载自动补全的数据





## 源码分析

### 文本输入

#### 概括

* `AutoCompleteTextView` 设置 TextWatcher 监听输入变化
* `Filter` 异步处理 filter 操作，执行 `performFiltering(CharSequence constraint)` 方法
* `Filter` 将执行结果通过 UI 线程发布，执行 `publishResults(CharSequence constraint, FilterResults results)` 方法，并触发 `Filter.FilterListener` 的回调
* `AutoCompleteTextView` 在 `onFilterComplete(int count)` 回调中展示自动补全弹窗

#### 具体分析

使用 `addTextChangedListener(..)` 监听输入，输入变化后回调到 MyWatcher

```java
public class AutoCompleteTextView extends EditText implements Filter.FilterListener {
    ...
    private class MyWatcher implements TextWatcher {
        private boolean mOpenBefore;

        public void beforeTextChanged(CharSequence s, int start, int count, int after) {
            if (mBlockCompletion) return;

            // when text is changed, inserted or deleted, we attempt to show
            // the drop down
            mOpenBefore = isPopupShowing();
            if (DEBUG) Log.v(TAG, "before text changed: open=" + mOpenBefore);
        }

        public void afterTextChanged(Editable s) {
            if (mBlockCompletion) return;

            // if the list was open before the keystroke, but closed afterwards,
            // then something in the keystroke processing (an input filter perhaps)
            // called performCompletion() and we shouldn't do any more processing.
            if (DEBUG) {
                Log.v(TAG, "after text changed: openBefore=" + mOpenBefore
                        + " open=" + isPopupShowing());
            }

            if (mOpenBefore && !isPopupShowing()) return;

            refreshAutoCompleteResults();
        }

        public void onTextChanged(CharSequence s, int start, int before, int count) {
        }
    }
    ...
}
```

`afterTextChanged(..)` 调用 `refreshAutoCompleteResults()` 来刷新自动补全

```java
public class AutoCompleteTextView extends EditText implements Filter.FilterListener {
    ...
    public final void refreshAutoCompleteResults() {
        // enoughToFilter() 判断当输入超过设置了字符数，即 threshold 时，需要进行 filter 操作
        if (enoughToFilter()) {
            // mFilter 是 adapter 里设置的 filter，要求使用的 adapter 实现了 Filterable 接口
            if (mFilter != null) {
                mPopupCanBeUpdated = true;
                
                performFiltering(getText(), mLastKeyCode);
            }
        } else {
            if (!mPopup.isDropDownAlwaysVisible()) {
                dismissDropDown();
            }
            if (mFilter != null) {
                mFilter.filter(null);
            }
        }
    }
    protected void performFiltering(CharSequence text, int keyCode) {
        // performFiltering(..)实际上调用的是 Filter#filter(..) 方法
        mFilter.filter(text, this);
    }
    ...
}
```

`Filter` 是一个抽象类，有两个抽象方法：

* protected abstract FilterResults `performFiltering`(CharSequence constraint);
* protected abstract void `publishResults`(CharSequence constraint, FilterResults results);

显然一个是用来执行 filter 操作，一个是用来接收 filter 结果的。其中 `performFiltering(..)` 是异步的。

接着，看下 `Filter` 的源码

```java
public abstract class Filter {
    ...
    public final void filter(CharSequence constraint, FilterListener listener) {
        synchronized (mLock) {
            if (mThreadHandler == null) {
                // 创建一个异步的用于处理 request 的 handler
                HandlerThread thread = new HandlerThread(
                        THREAD_NAME, android.os.Process.THREAD_PRIORITY_BACKGROUND);
                thread.start();
                mThreadHandler = new RequestHandler(thread.getLooper());
            }

            // 可以设置一个延时处理时间
            final long delay = (mDelayer == null) ? 0 : mDelayer.getPostingDelay(constraint);
            
            Message message = mThreadHandler.obtainMessage(FILTER_TOKEN);
    
            // 将要 filter 的信息封装 request 参数
            RequestArguments args = new RequestArguments();
            // make sure we use an immutable copy of the constraint, so that
            // it doesn't change while the filter operation is in progress
            args.constraint = constraint != null ? constraint.toString() : null;
            args.listener = listener;
            message.obj = args;
    
            // 发送 message 进行异步处理，也就是发送给了 RequestHandler
            mThreadHandler.removeMessages(FILTER_TOKEN);
            mThreadHandler.removeMessages(FINISH_TOKEN);
            mThreadHandler.sendMessageDelayed(message, delay);
        }
    }
    ...
}
```

`RequestHandler` 处理 FILTER_TOKEN 信息，注意，这里是异步的

```java
public abstract class Filter {
    ...
    private class RequestHandler extends Handler {
        public RequestHandler(Looper looper) {
            super(looper);
        }
        
        public void handleMessage(Message msg) {
            int what = msg.what;
            Message message;
            switch (what) {
                case FILTER_TOKEN:
                    RequestArguments args = (RequestArguments) msg.obj;
                    try {
                        // 调用抽象方法 performFiltering(..) 执行 filter
                        // args.results 的类型是 FilterResults
                        // filter 结果保存到 request 参数里
                        args.results = performFiltering(args.constraint);
                    } catch (Exception e) {
                        args.results = new FilterResults();
                        Log.w(LOG_TAG, "An exception occured during performFiltering()!", e);
                    } finally {
                        // 将结果封装成 message 发送到 mResultHandler
                        // 这里有个知识点，obtainMessage(..) 会将 message 的 targe 设置为调用此方法的 Handler
                        message = mResultHandler.obtainMessage(what);
                        // request 参数保存到 message 的 obj 里
                        message.obj = args;
                        message.sendToTarget();
                    }

                    synchronized (mLock) {
                        // 发送通知结束异步 handler
                        if (mThreadHandler != null) {
                            Message finishMessage = mThreadHandler.obtainMessage(FINISH_TOKEN);
                            mThreadHandler.sendMessageDelayed(finishMessage, 3000);
                        }
                    }
                    break;
                case FINISH_TOKEN:
                    synchronized (mLock) {
                        if (mThreadHandler != null) {
                            mThreadHandler.getLooper().quit();
                            mThreadHandler = null;
                        }
                    }
                    break;
            }
        }
    }
    ...
}
```

`ResultsHandler` 接收到包含 filter 处理结果的信息，将在 UI 线程处理

```java
public abstract class Filter {
    ...
    private class ResultsHandler extends Handler {
      
        @Override
        public void handleMessage(Message msg) {
            RequestArguments args = (RequestArguments) msg.obj;

            // 调用 Filter 的另一个抽象 publishResults(..) 来通知 filter 结果
            publishResults(args.constraint, args.results);
            // 也会调用请求参数里的设置的 listener
            // AutoCompleteTextView 调用 Filter#filter(..) 时也传入了这个 listener
            if (args.listener != null) {
                int count = args.results != null ? args.results.count : -1;
                args.listener.onFilterComplete(count);
            }
        }
    }
    ...
}
```

AutoCompleteTextView 对 filter 的结果处理

```java
public class AutoCompleteTextView extends EditText implements Filter.FilterListener {
    ...
    public void onFilterComplete(int count) {
        updateDropDownForFilter(count);
    }
  
    private void updateDropDownForFilter(int count) {
        // Not attached to window, don't update drop-down
        if (getWindowVisibility() == View.GONE) return;

        /*
         * This checks enoughToFilter() again because filtering requests
         * are asynchronous, so the result may come back after enough text
         * has since been deleted to make it no longer appropriate
         * to filter.
         */

        final boolean dropDownAlwaysVisible = mPopup.isDropDownAlwaysVisible();
        final boolean enoughToFilter = enoughToFilter();
        if ((count > 0 || dropDownAlwaysVisible) && enoughToFilter) {
            if (hasFocus() && hasWindowFocus() && mPopupCanBeUpdated) {
                // 弹出自动补全提示框
                showDropDown();
            }
        } else if (!dropDownAlwaysVisible && isPopupShowing()) {
            dismissDropDown();
            // When the filter text is changed, the first update from the adapter may show an empty
            // count (when the query is being performed on the network). Future updates when some
            // content has been retrieved should still be able to update the list.
            mPopupCanBeUpdated = true;
        }
    }
    
    public void showDropDown() {
        // 为输入法设置补全选项？手机使用搜狗输入法没看到效果
        buildImeCompletions();

        if (mPopup.getAnchorView() == null) {
            if (mDropDownAnchorId != View.NO_ID) {
                mPopup.setAnchorView(getRootView().findViewById(mDropDownAnchorId));
            } else {
                mPopup.setAnchorView(this);
            }
        }
        if (!isPopupShowing()) {
            // Make sure the list does not obscure the IME when shown for the first time.
            mPopup.setInputMethodMode(ListPopupWindow.INPUT_METHOD_NEEDED);
            mPopup.setListItemExpandMax(EXPAND_MAX);
        }
        mPopup.show();
        mPopup.getListView().setOverScrollMode(View.OVER_SCROLL_ALWAYS);
    }
    ...
}
```

`onFilterComplete(..)` 的处理并没有对 adapter 进行操作，对 adapter 的数据的处理是放到 Filter 里的。比如，`ArrayAdapter`  提供了一个 `ArrayFilter`，它的实现中对 `ArrayAdapter` 内部的 mObjects 进行了处理，得到新的数据源。

