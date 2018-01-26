>  20180126：Parcelable 是 Android 提供的一种更高效的序列化方式，之前对它的理解都比较表面，知道在实际使用时遇到的一个问题，才发现自己潜意识里的一个错误认识：对 Parcelable 进行反序列化时，得到的是一个新的对象。
>
>  问题：同一个 Activity，里面用到两个 Fragment A 和 B，A 将一个 Parcelable 对象传给 B，然后反序列化得到该 Parcelable 的一个实例，B 修改了该实例的值，然后 A 中相应实例的值也发生了改变。
>
>  问题模拟：在同一 Activity 中序列化一个 Parcelable 对象，再进行反序列化得到另一个对象，打印看到两个对象引用相同，并且修改第二个对象的值会导致第一个对象的值发生改变；在一个 Activity 中序列化一个 Parcelable 对象，在另一 Activity 中反序列化，两个对象引用不同。
>
>  当我意识到这个问题时，仿佛发现了一个谎言。。。









参考：

[Parcel](https://developer.android.com/reference/android/os/Parcel.html)

[Does retrieving a parcelable object through bundle always create new copy?](https://stackoverflow.com/questions/39916021/does-retrieving-a-parcelable-object-through-bundle-always-create-new-copy)