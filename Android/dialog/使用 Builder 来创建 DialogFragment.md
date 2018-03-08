> 20180308 几乎所有的程序员都知道 DRY，包括我，于是我在遇到什么问题，总本能地进行 google，但很多东西，其实本就已经知道了答案，只是自己变得越来越不自信，才会想在网上找到一样的答案。而且，有时候，答案已经表现在了另一问题上，但却没有针对这一问题的答案，于是自己又陷入了自我的怀疑。
>
> 其实，路一直都在，路也不止一条，能走得通，就说明这条路是对的，即使不是最正确的。我们很难在一开始就找到最正确的答案，而且未必存在最正确的，所以，坚定地去尝试，这样，我们将看到更多不一样的东西。

其实，如何使用 Builder 来创建 DialogFragment，这没有什么难的，只是普通的 Builder，然后使用它来取代 newInstance 创建 DialogFragment 实例，一开始想要用 DialogFragment 来模仿 AlertDialog 的实现时是我想多了。现在，我大致的想法如下：

```java
public class MyDialogFragment {
    private MyDialogFragment(Builder builder){
        Bundle bundle = new Bundle();
        bundle.put("key", builder.a());
        ...
    }
    
    public static class Builder(){
        
    }
}
```

对于点击事件的监听，则可以通过 getTargetFragment.onActivityResult 来实现，或者创建一个监听器 interface，启动 fragment 实现该接口，然后在 Builder 中将启动 fragment 的 tag 作为参数传入，这样 dialogFragment 将可以找到该 fragment（来自 [AlertDialogFragment.java](https://gist.github.com/noxi515/5504493) 的启发）。