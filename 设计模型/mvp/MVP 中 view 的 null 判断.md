presenter 一般都会实现 attachView(View) 和 detachView()，在 detach 后，如果我们调用 view 的方法时，将出现 NPE ，为此，我们很容易地就会加上一大堆

```java
if(view != null) {
    view.XX();
}
```

狗血的代码，但看似又无可奈何。。。

在 [Don’t put view != null checks in your Presenters](https://android.jlelse.eu/dont-put-view-null-checks-in-your-presenters-4b6026c67423) 里，作者主要推荐了两种处理方式：

+ 对于明确知道 view 不为 null 的情况下，创建 getViewOrThrow() 方法，在该方法中如果 view 为 null，主动抛出 IllegalStateException。
+ 使用  [ThirtyInch](https://github.com/grandcentrix/ThirtyInch) 库的 sendToView(ViewAction) 方法。

对于 getViewOrThrow()，感觉还是挺不错的，虽然会给用户带来一些体验上的不友好，但这些问题一般会在测试阶段暴露。而第二种方式，因为这种原因引入一个开源库感觉不太好，但作者也提到可以单独抽取出该方法的思想来实现自己的代码。其他方法如 Optionals 和 WeakReferences 虽然也能避免 NPE，但仍然避免不了各种检查。

**在评论中，有网友提到使用 RxJava 和动态代理，但暂时不是很了解，自我感觉这两种方式会更好，等以后弄懂了再补充。**

我自己想的一种方法是可以为 view 创建一个空实现类，在 getView() 中如果 view 为null，则返回空实现类，但这样每一个 View 接口都要新增一个空实现类，仍然不太可取。

> 感觉最后也还没指明一条正确的路，但慢慢摸索，总会找到的。



在 [android-architecture](https://github.com/googlesamples/android-architecture) 的 mvp 中，为 View 接口添加了 isActive() 方法，对于实现该接口的 Fragment，它返回的是 isAdded() 的结果。感觉这种实现比 attach 和 detach 高明。

