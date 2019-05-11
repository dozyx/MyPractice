

## 实践

### 如何将 ViewModel 的生命周期与某个 Fragment 关联

场景：单 Activity 多 Fragment，部分 Fragment 共享某个 viewModel，需要在某个 Fragment 退出时销毁改 viewModel，但此时 Activity 并未退出。

问题：系统实现里，viewModel 的生命周期只能跟某个 fragment 或 activity 关联，多个 fragment 共享的 viewModel 需要使用 activity 来创建，那么它的销毁就只能与 activity 一致，这样就不能满足使用场景。

思路：

方案一：调用 Acitivty 的 `getViewModelStore().clear()`，但回清理 Activity 里所有的 viewModel

方案二：添加一个没有 UI 的 fragment，viewModel 的生命周期与改 fragment 关联。不方便的地方是每个使用该 viewModel 的其他 fragment 都会与该 fragment 产生依赖。

方案三：使用 [scoped-vm](https://github.com/dhabensky/scoped-vm)。没有实际使用该库，但从源码来看，用法还是比较简单，可以使 viewModel 与某个 fragment 生命周期关联，同时其他 fragment 也能通过 scope 访问。看了下源码，它的主要思想是：host 和 client 都是 ViewModelStoreOwner 对象，client 与 scope 关联，host 会实现一个 host viewModel，host viewModel 会为每个 scope 维护一个 ViewModelStore，client 中使用的 viewModel 就通过该 ViewModelStore 产生，一个 host 下可以有多个 client，当多个 client 使用同一个 scope 产生 viewModel 时，这些 viewModel 的生命周期是一致的，它们会在所有的 client 销毁时清除。

方案四：使 Application 实现 ViewModelStoreOwner 接口，通过 Application 的 ViewModelStore 来产生 viewModel。这种做法的一个问题是 viewModel 的生命周期会与整个 app 一致，所以需要手动销毁。除了使用 Application，感觉使用单例实现 ViewModelStoreOwner  做法也是一样。



参考：

[Shared ViewModel lifecycle for Android JetPack](https://stackoverflow.com/questions/53236574/shared-viewmodel-lifecycle-for-android-jetpack)

[Share ViewModel between fragments that are in different Activity](https://stackoverflow.com/questions/44641121/share-viewmodel-between-fragments-that-are-in-different-activity)



### 多个 Activity 共享 viewModel

暂时没有遇到这种场景。

参考：

[How to shere same instance of view model between activities?](https://github.com/googlesamples/android-architecture-components/issues/29)

[Share ViewModel between multiple activity](https://issuetracker.google.com/issues/64988610)