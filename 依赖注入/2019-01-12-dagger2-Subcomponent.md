### 定义

subcomponent 是继承并扩展 parent component 的 component。它可以依赖于 parent component 中绑定的对象，反之则不行，也就是说，subcomponent 的 parent 的对象图是它自身的一张子图。

> ps：感觉像是跟子类意思差不多。



### 使用

* 声明

  ```java
  @Subcomponent(modules = RequestModule.class)
  interface RequestComponent {
    RequestHandler requestHandler();
  
    @Subcomponent.Builder
    interface Builder {
      Builder requestModule(RequestModule module);
      RequestComponent build();
    }
  }
  ```

* 添加到 parent

  ```java
  @Module(subcomponents = RequestComponent.class)
  class ServerModule {}
  
  @Singleton
  @Component(modules = ServerModule.class)
  interface ServerComponent {
    RequestRouter requestRouter();
  }
  
  @Singleton
  class RequestRouter {
    @Inject RequestRouter(
        Provider<RequestComponent.Builder> requestComponentProvider) {}
  
    void dataReceived(Data data) {
      RequestComponent requestComponent =
          requestComponentProvider.get()
              .data(data)
              .build();
      requestComponent.requestHandler()
          .writeResponse(200, "hello, world");
    }
  }
  ```



### Subcomponent 与 scope

+ subcomponent 不能使用与 parent 相同的 scope
+ 兄弟 subcomponent 可以使用相同的 scope

```java
@RootScope @Component
interface RootComponent {
  BadChildComponent.Builder badChildComponent(); // ERROR!
  SiblingComponentOne.Builder siblingComponentOne();
  SiblingComponentTwo.Builder siblingComponentTwo();
}

@RootScope @Subcomponent
interface BadChildComponent {...}

@ChildScope @Subcomponent
interface SiblingComponentOne {...}

@ChildScope @Subcomponent
interface SiblingComponentTwo {...}
```







资料：

[subcomponents](https://google.github.io/dagger/subcomponents.html)