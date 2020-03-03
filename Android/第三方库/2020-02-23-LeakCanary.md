### 原理

> 当一个对象不再使用时，调用 RefWatcher.watch(Object) 方法，将 object 放入 WeakReference 中，构造 WeakReference 时调用的构造函数会传入一个 ReferenceQueue 引用队列，当 gc 标记该对象为可回收时，object 会被放入这个队列里。接着主动触发 gc，如果这时候检查引用队列里不存在这个 object，那么判定这个对象泄漏。

