



在调用 observe 时，会接收到上一次的数据，即上一次 setValue 的值，即使是 null，如果 observer 前没有值，则不会触发。如，旋转屏幕时，将可能一直触发上一次的数据。如果不希望有这种问题，可以参考 googlesample 的 [SingleLiveEvent](https://github.com/googlesamples/android-architecture/blob/dev-todo-mvvm-live/todoapp/app/src/main/java/com/example/android/architecture/blueprints/todoapp/SingleLiveEvent.java) 类。

SingleLiveEvent 设置了一个标记位，每一次 setValue 时置为 true，然后事件被消耗时置为 false。需要注意的一点是，仅有一个 observer 可以接受到值，因为值被第一个 observer 消耗后，标记位就变成了 false。



### MutableLiveData 与 LiveData 

唯一区别： posValue 和 setValue 两个方法在 MutableLiveData 中是 public 的，而 LiveData 中是 protect 的。



### MediatorLiveData

observe 其他的 LiveData。

示例代码：

```java
LiveData liveData1 = ...;
LiveData liveData2 = ...;

MediatorLiveData liveDataMerger = new MediatorLiveData<>();
liveDataMerger.addSource(liveData1, value -> liveDataMerger.setValue(value));
liveDataMerger.addSource(liveData2, value -> liveDataMerger.setValue(value));
```

MediatorLiveData 会响应任何一个 source 的变化。























参考：

[LiveData](https://developer.android.com/topic/libraries/architecture/livedata.html)