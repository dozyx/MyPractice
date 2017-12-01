The fundamental idea of ReactiveX is that events are data and data are events.    

Observable 与 Java 8 stream 或Kotlin sequence 的区别：The key difference is that Observable pushes the items while Streams and sequences pull the items. 


相关概念：    
+ Observable    
+ Observer    
+ emit/emission    
+ operator    


## Observable:    
### 运作
在最高层级上，Observable 通过传递三种类型的事件进行工作：
+ onNext
+ onComplete
+ onError

### Observable.create
```java
Observable<String> source = Observable.create(emitter -> {
            emitter.onNext("Alpha");
            emitter.onNext("Beta");
            emitter.onNext("Gamma");
            emitter.onNext("Delta");
            emitter.onNext("Epsilon");
            emitter.onComplete();
        });
        source.subscribe(s -> System.out.println("RECEIVED: " + s));
```
输出：

```shell
RECEIVED: Alpha
RECEIVED: Beta
RECEIVED: Gamma
RECEIVED: Delta
RECEIVED: Epsilon
```



P88















