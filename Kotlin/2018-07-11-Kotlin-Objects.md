> 个人总结：
>
> 本篇主要讲解了 object 的三种使用方式：
>
> 1. object 表达式，类似于 Java 中的匿名类
> 2. object 声明，用来创建单例
> 3. companion object，类似于 static，不过会创建实例。内部类？没有完全理解，有点像静态方法，有点像静态内部类，有点像工厂方法。。
>
> 不要将 Kotlin 的 object 与 Java 的 Object 混淆，而是应该作为一种全新的类型看待。

有些时候，我们需要创建一个只对某个类进行了小改动的对象，通常，我们不会显式地为此声明一个子类。Java 中，处理这种情况的方式是匿名内部类。而 Kotlin 使用 object 表达式和 object 声明来对这个概念进行了稍微的概括。



## Object 表达式

创建一个匿名类的 object：

```kotlin
window.addMouseListener(object : MouseAdapter() {
    override fun mouseClicked(e: MouseEvent) {
        // ...
    }

    override fun mouseEntered(e: MouseEvent) {
        // ...
    }
})
```

如果一个 supertype 有一个构造函数，相应参数也需要传入。如果有多个 supertype（只能有一个 class），则使用逗号分隔

```kotlin
open class A(x: Int) {
    public open val y: Int = x
}

interface B {...}

val ab: A = object : A(1), B {
    override val y = 15
}
```

如果，我们“只是需要”一个没有 supertype 的 object，还可以写成：

```kotlin
fun foo() {
    val adHoc = object {
        var x: Int = 0
        var y: Int = 0
    }
    print(adHoc.x + adHoc.y)
}
```

注意，**匿名 object 只能作为 local 和 private 的声明的类型使用**。

```kotlin
class C {
    // Private function, so the return type is the anonymous object type
    private fun foo() = object {
        val x: String = "x"
    }

    // Public function, so the return type is Any
    // 用于 public 的声明时，返回类型为该匿名的 supertype 或者 Any（object 没有 supertype时），object 中新增的成员无法被访问
    fun publicFoo() = object {
        val x: String = "x"
    }

    fun bar() {
        val x1 = foo().x        // Works
        val x2 = publicFoo().x  // ERROR: Unresolved reference 'x'
    }
}
```

> 对于匿名 object 用于 public 声明的一点猜测：尽管匿名 object 类不需要编写新的类，但实际编译时还是会自动生成一个类，但该类并不是 public 的。。。这个想法是不对的。。private 类型无法作为 public 方法的返回类型。。。另一个猜测，出于便利性目的，因为 public 方法可从外部，如果允许访问匿名 object 的成员，会不方便。。。呃。。。希望能找到正确答案。。

与 Java 匿名类型类相似，object 表达式中的代码可以访问 enclosing scope （作用域？）中的变量。不同的点在于，Kotlin 不限制变量必须为 final。

```kotlin
fun countClicks(window: JComponent) {
    var clickCount = 0
    var enterCount = 0

    window.addMouseListener(object : MouseAdapter() {
        override fun mouseClicked(e: MouseEvent) {
            clickCount++
        }

        override fun mouseEntered(e: MouseEvent) {
            enterCount++
        }
    })
    // ...
}
```



## Object 声明

使用 object 可以快速声明一个单例：

```kotlin
object DataProviderManager {
    fun registerDataProvider(provider: DataProvider) {
        // ...
    }

    val allDataProviders: Collection<DataProvider>
        get() = // ...
}
```

这种用法称为 object declaration，object 声明的初始化时**线程安全**的。

引用该 object 时，可以直接使用它的名称：

```kotlin
DataProviderManager.registerDataProvider(...)
```



### Companion Objects

> 伴随对象？兄弟对象？

```kotlin
class MyClass {
    companion object Factory {
        fun create(): MyClass = MyClass()
    }
}
```

companion object 中的成员可以直接通过类名进行调用：

```kotlin
val instance = MyClass.create()
```

可以直接忽略 companion object 的名称，这是将使用 `Companion` 作为名称：

```kotlin
class MyClass {
    companion object {
    }
}

val x = MyClass.Companion
```

注意，尽管 companion object 跟其他语言的 static 成员很像，但在运行时，这些都是实际对象的实例成员，并且，还可以实现接口：

```kotlin
interface Factory<T> {
    fun create(): T
}


class MyClass {
    companion object : Factory<MyClass> {
        override fun create(): MyClass = MyClass()
    }
}
```



### objcect 表达式和 object 声明的区别

+ object 表达式会立即执行
+ object 声明是懒初始化
+ companion 在相应类进行加载时初始化，这与 Java 的 static 初始化类似。



参考：

[Object Expressions and Declarations](https://kotlinlang.org/docs/reference/object-declarations.html)