[github 地址](https://github.com/YoKeyword/Fragmentation)

> 一个用于实现单 Activity 开发框架的库。个人并不喜欢这种开发方式，因为本人认为 Acitvity 应该作为容器，其中可以承载单个流程的多个 Fragment，而且单 Activity 开发限制过多。

### 注意

- 复杂 Fragment 页面在 onEnterAnimationEnd 方法中初始化数据，这样可以使 Fragment 动画更流畅。如果没有动画，该方法将在 onActivityCreated 时回调。

  ```java
  public View onCreateView(...) {
      ...
      // 这里仅给toolbar设置标题，返回箭头等轻量UI的操作
      initView();
      return view;
  }
  
  @Override
  protected void onEnterAnimationEnd(Bundle saveInstanceState) {
       // 这里设置Listener、各种Adapter、请求数据等等
      initLazyView();
  }
  ```






### 问题

- 使用 popTo( ,true) 再重新 loadRootFragment，仍然采用了前一个 Fragment 实例
- 嵌套fragment 调用 start 失败
- dialogFragment 不能直接启动
- dialogFragment 里直接启动另一个 fragment，该 fragment 会显示在 dialog 下面
- 使用 fragmentation 后，如果想要移除，工作量会很大

