## 性能

* FrameLayout 为 wrap_content，如果有超过一个 child 的宽或高为 match_parent 时，会影响性能

  FrameLayout 源码：

  ```java
      @Override
      protected void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {
          int count = getChildCount();
  
          final boolean measureMatchParentChildren =
                  MeasureSpec.getMode(widthMeasureSpec) != MeasureSpec.EXACTLY ||
                  MeasureSpec.getMode(heightMeasureSpec) != MeasureSpec.EXACTLY;
          mMatchParentChildren.clear();
          ...
          for (int i = 0; i < count; i++) {
              ...
                  if (measureMatchParentChildren) {
                      if (lp.width == LayoutParams.MATCH_PARENT ||
                              lp.height == LayoutParams.MATCH_PARENT) {
                          mMatchParentChildren.add(child);
                      }
                  }
          }
          ...
          if (count > 1) {
              // 对子控件进行了第二次测量
              for (int i = 0; i < count; i++) {
                  ...
                  child.measure(childWidthMeasureSpec, childHeightMeasureSpec);
              }
          }
      }
  ```

  

## 可读性

Editor：

* 使用 tools 预览

* 使用 `editor-fold` 注释提供折叠功能

  ```xml
      <!-- <editor-fold desc="标题">-->
      <Button
          ... />
  
      <Button
          ... />
      <!-- </editor-fold>-->
  ```

  

