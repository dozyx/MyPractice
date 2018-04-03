## EventBus

<http://greenrobot.org/eventbus/documentation/how-to-get-started/>

### 基本使用

- 定义 Event Event 是一个 POJO 类

```
public class MessageEvent {
 
    public final String message;
 
    public MessageEvent(String message) {
        this.message = message;
    }
}
```

- 准备 subscriber
  - @Subscribe 注解 event 的处理方法

```
// This method will be called when a MessageEvent is posted (in the UI thread for Toast)
@Subscribe(threadMode = ThreadMode.MAIN)
public void onMessageEvent(MessageEvent event) {
    Toast.makeText(getActivity(), event.message, Toast.LENGTH_SHORT).show();
}
 
// This method will be called when a SomeOtherEvent is posted
@Subscribe
public void handleSomethingElse(SomeOtherEvent event) {
    doSomethingWith(event);
}
```

- 使用 EventBus 注册、解绑

```
@Override
public void onStart() {
    super.onStart();
    EventBus.getDefault().register(this);
}
 
@Override
public void onStop() {
    EventBus.getDefault().unregister(this);
    super.onStop();
}
```

- 发送 event 使用 EventBus 进行 post

```
EventBus.getDefault().post(new MessageEvent("Hello everyone!"));
```

### 扩展使用

#### ThreadMode

在使用 @Subscribe 时可以指定一个 ThreadMode 来表明处理方法的执行线程。

```
@Subscribe(threadMode = ThreadMode.POSTING)
public void onMessage(MessageEvent event) {
    log(event.message);
}
```

ThreadMode有四种：

- POSTING：默认，与发送 event 线程相同
- MAIN：主线程
- BACKGROUND：后台线程，如果发送 event 线程不是主线程，将直接使用该线程。
- ASYNC：单独线程，这样发送 event 的线程就不需要等待处理方法执行完成。

#### 配置

EventBusBuilder，通过 EventBus.builder() 创建，默认的 EventBus 通过 EventBus.getDefault() 获得。使用 EventBusBuilder 的 installDefaultEventBus() 方法可以配置默认一个新的默认 EventBus 实例。

#### Sticky Event

使用 stivky event 可以使 subscriber 在注册时获得上一次的 event。

- 使用 postSticky 发送
- @Subscribe(sticky = true, threadMode = ThreadMode.MAIN)

如果需要移除 sticky event，可以使用 removeStickyEvent 方法。除了设置 sticky = true 外，也可以使用 getStickyEvent 来检查。

#### 优先级和取消 event

```
@Subscribe(priority = 1);
public void onEvent(MessageEvent event) {
    ...
}
```

不会影响其他 ThreadMode 的分发顺序

```
// Called in the same thread (default)
@Subscribe
public void onEvent(MessageEvent event){
    // Process the event
    ...
    // Prevent delivery to other subscribers
    EventBus.getDefault().cancelEventDelivery(event) ;
}
```

#### Subscriber Index

subscriber 索引是一种用于提高初始订阅注册速度的可选优化，它是 EventBus 3 的一个新特性。

> 看了下大概用法，因为没有实际需求，暂时未深究。

#### ProGuard

> 未实际使用

#### AsyncExecutor

类似于线程池，但有 failure 抛出异常时，AsyncExecutor 将这些异常封装到一个 event 中，然后自动 post。
执行：

```
AsyncExecutor.create().execute(
    new AsyncExecutor.RunnableEx() {
        @Override
        public void run() throws LoginException {
            // No need to catch any Exception (here: LoginException)
            remote.login();
            EventBus.getDefault().postSticky(new LoggedInEvent());
        }
    }
);
```

接收：

```
@Subscribe(threadMode = ThreadMode.MAIN)
public void handleLoginEvent(LoggedInEvent event) {
    // do something
}
 
@Subscribe(threadMode = ThreadMode.MAIN)
public void handleFailureEvent(ThrowableFailureEvent event) {
    // do something
}
```