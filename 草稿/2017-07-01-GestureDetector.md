[GestureDetector](https://developer.android.com/reference/android/view/GestureDetector.html)

[Detecting Common Gestures](https://developer.android.com/training/gestures/detector.html)

​	`GestureDetector` 可根据提供的 `MotionEvent` 来检测不同的手势和事件。当特定的动作事件发生时，将通过`OnGestureListener` 回调来通知用户。如果不需要监听所有的 OnGestureListener，可以使用 OnGestureListener 的空实现类 `SimpleOnGestureListener`。

​	使用：

+ 为 View 创建一个 GestureDetector 示例
+ 在 View 的 `onTouchEvent(MotionEvent)`方法中调用 GestureDetector 的 `onTouchEvent(MotionEvent)`方法
+ 如果需要监听 `onContextClick(MotionEvent)`，必须在 View 的`onGenericMotionEvent(MotionEvent)`方法中调用  GestureDetector 的`onGenericMotionEvent(MotionEvent)`方法。（一般动作事件：操纵杆移动、鼠标移动、轨迹球触摸、滚轮移动等）



构造方法：

```java
public GestureDetector(Context context, OnGestureListener listener){
  ...
}

public GestureDetector(Context context, OnGestureListener listener, Handler handler){
  ...
}
//handler 用于延迟的事件：SHOW_PRESS(用户按下但没有移动或移开)、LONG_PRESS、TAP。
```



### 实践

​	对于一个已存在的 View，可以通过调用 view.setOnTouchListener(…) 来处理它的触摸事件，这样可以避免对其子类化，而对于自定义的 View，则可以重写  `onTouchEvent()` 方法。同样的，我们也可以在重写 Activity 的 onTouchEvent()来为 Activity 添加手势监测。

​	在实现 `GestureDetector.OnGestureListener` 时，一般都要使 `onDown()`方法返回 true，否则的话，其他手势都将被忽略，除非真的想要忽略所有的手势才返回 false。