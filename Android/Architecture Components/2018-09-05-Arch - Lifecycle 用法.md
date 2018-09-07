1. 需要监视生命周期的对象实现 LifecycleObserver
2. 为需要监视生命周期的方法添加 `OnLifecycleEvent` 注解
3. 使用 `Lifecycle#addObserver` 添加



```java
public class MyObserver implements LifecycleObserver {
    @OnLifecycleEvent(Lifecycle.Event.ON_RESUME)
    public void connectListener() {
        ...
    }

    @OnLifecycleEvent(Lifecycle.Event.ON_PAUSE)
    public void disconnectListener() {
        ...
    }
}

myLifecycleOwner.getLifecycle().addObserver(new MyObserver());
```

> LifecycleObserver 接口是一个标记接口



## Best practices for lifecycle-aware components

+ UI 控制器（activity 和 fragment）尽可能精简。它们不应该尝试去获得数据，而是使用 ViewModel 来处理，通过对观察一个 LiveData 对象来将变化反映给 view。
+ 尝试编写数据驱动 UI，UI controller 的职责是当数据变化时更新 view，或者将用户的动作传给 ViewModel。
+ 将数据逻辑放在 ViewModel 类。ViewModel 应作为 UI controller 和 app 中其他部分的连接器，应注意，**获取数据（如网络）并不是 ViewModel 的职责**。相反，ViewModel 应通过调用适当的组件来获取数据，然后将结果提供给 UI controller。
+ 使用 Data Binding 来维护 view 和 UI controller 之间的干净接口。
+ 如果 UI 十分复杂，可以考虑创建一个 [presenter](http://www.gwtproject.org/articles/mvp-architecture.html#presenter) 来处理 UI 的变动，这可能会很麻烦，但可以使 UI 组件更易于测试。
+ 避免在 ViewModel 中引用 View 或者 Activity 的 context。







参考：

[lifecycle](https://developer.android.com/topic/libraries/architecture/lifecycle)