# 《Kotlin 实战》- 6 Kotlin 的类型系统
## 可空性
现代编程语言包括 Kotlin 解决 NullPointerException 类问题的方法是把运行时的错误转变成编译期的错误。
### 可空类型
问号可以加在任何类型的后面来表示这个类型的变量可以存储 null 引用：String?、Int?、MyCustomType?
没有问号的类型表示这种类型的变量不能存储 null 引用。
### 安全调用运算符：“?.”
`?.`将 null 检查和调用合并成一个动作。比如：s?.toUpperCase() 等同于 if (s != null) s.toSupperCase() else null

### Elvis 运算符：“?:”
也称为 nulll 合并运算符，用来代替 null 的默认值。
```
fun foo(s: String?) {
    val t: String = s ?: ""
}
```
Elvis 运算符通常和安全调用运算符一起使用，用一个值代替对 null 对象调用方法时返回的 null。
```
fun strLenSafe(s: String?)： Int = s?.length ?: 0
```

### 安全转换：“as?”
`as?` 运算符尝试把值转换成指定的类型，如果值不是合适的类型就返回 null。

### 非空断言：“!!”
`!!` 可以把任何值转换成非空类型，如果对 null 值做非空断言，则会抛出异常。

### “let” 函数
let 函数让处理可空表达式变得更为容易。和安全调用运算符一起，它允许你对表达式求值，检查求值结果是否为 null，并把结果保存为一个变量。
比如：
```
fun sendEmailTo(email: String) {...}
```
不能把可空类型传给这个函数：
```kotlin
>>> val email: String? = …
>>> sendEmailTo(email)
```

这里的调用将报错。
处理使用 if 检查 null 外，另一种方式就是使用 let 函数，并通过安全调用来调用它。let 函数做的所有事情就是把一个调用它的对象变成 lambda 表达式的参数。

```
emali?.let { email -> sendEmailTo(email)}
```
或者
```
email?.let{ sendEmailTo(it)}
```

### 延迟初始化的属性
 lateinit 修饰符将属性声明为可以延迟初始化。
```kotlin
class MyService {
    fun performAction(): String = "foo"
}

class MyTest {
    private lateinit var myService: MyService

    @Before fun setUp() {
        myService = MyService()
    }

    @Test fun testAction() {
        Assert.assertEquals("foo",
            myService.performAction())
    }
}
```
> lateinit 属性常见的一种用法是依赖注入。  

### 可空类型的扩展
```scala
fun verifyUserInput(input: String?) {
    if (input.isNullOrBlank()) {
        println("Please fill in the required fields")
    }
}

fun main(args: Array<String>) {
    verifyUserInput(" ")
    verifyUserInput(null)
}
```
上面的代码并不会导致异常，这是因为 isNullOrBlank 显式地检查了 null，这种情况返回 true。
```scala
fun String?isNullOrBlank(): Boolean = this == null || this.isBlank()
```
当你为一个可空类型（以 ？ 结尾）定义扩展函数时，这意味着你可以对可空里的值调用这个函数；并且函数体的 this 可能为 null，所以你必须显式地检查。

### 类型参数的可空性
> ps: 类型参数 = 泛型？  
> Kotlin 中所有泛型类和泛型函数的类型参数默认都是可空的。
```scala
fun <T> printHashCode(t: T) {
    println(t?.hashCode())
}
```
`printHashCode(null)` 输出为 null，T 被推导成`Any?`。
要使类型参数非空，必须要为它指定一个非空的上界。
```scala
fun <T: Any> printHashCode(t: T) {
    println(t?.hashCode())
}
```

### 可空性和 Java
Java 中使用注解来包含可空性信息，当代码中出现这样的信息时，Kotlin 就会使用它。
`@Nullable + Type = Type?`
`@NotNull + Type = Type`

如果不存在注解，Java 类型就会变成 Kotlin 中的平台类型。
> 平台类型本质上是就是 Kotlin 不知道可空性信息的类型。既可以当做可控类型处理，也可以当做非空类型处理。这意味着，使用者要像在 Java 中一样，对在这个类型上做的操作负有全部责任。  
> 在 Kotlin 中不能声明一个平台类型的变量，这些类型只能来自 Java 代码，但你可能在 IDE 的错误信息中看到它们：
```
>>> val i: Int = person.name
ERROR: Type mismatch: inferred type is String! butInt was expected
```
`String!` 表示法被 Kotlin 编译器用来表示来自来自 Java 代码的平台类型，`!`用来强调类型的可空性是未知的。

## 基本数据类型和其他基本类型
### 基本数据类型：Int、Boolean 及其他
Kotlin 不区分基本数据类型和包装类型。
在运行时，数字类型会尽可能地使用最高效的方式来表示。大多数情况下——对于变量、属性、参数和返回类型——Kotlin 的 Int 类型会被编译成 Java 基本数据类型 int。唯一不可行的例外是泛型类，比如集合。

### 可空的基本数据类型：Int?、Boolean? 及其他
Kotlin 中的可空类型不能用 Java 的基本数据类型表示，因为 null 只能被存储在 Java 的引用类型的变量中。

### 数字转换
Kotlin 不会自动地把数字从一种类型转换成另一种，即便是转换成范围更大的类型。
必须显式地进行转换：
```
val i = 1
val 1: Long = i.toLong()
```

基本数据类型字面量：
* 后缀 L 表示 Long 类型：123L
* 使用标准浮点数表示 Double 字面量：0.12、2.0、1.2e10、1.2e-10
* 后缀 F 表示 Float 类型：123.4F、.456F、1e3f
* 前缀 0x 或 0X 表示十六进制
* 前缀 0b 或者 0B 表示二进制字面量

### 根类型：Any 和 Any?
Any 类型是 Kotlin 所有非空类型的超类型。

### Kotlin 的 “void”：Unit
当函数没什么有意思的结果要返回时，它可以用作函数的返回类型：
```
fun f(): Unit {...}
```
Kotlin 的 Unit 与 Java 的 void 区别：
Unit 是一个完备的类型，可以作为类型参数，而 void 却不行。
使用示例：
```kotlin
interface Processor<T> {
    fun process(): T
}

class NoResultProcessor : Processor<Unit> {
    override fun process() {
        //...
    }
}
```

Java 中为了解决使用“没有值”作为类型参数的方式：
1. 使用分开的接口定义：如 Callable 和 Runnable
2. 用特殊的 java.lang.Void 类型作为参数类型。（仍需要加入 return null）

> 采用 Unit 命名原因：在函数式编程语言中，Unit 这个名字习惯上被用来表示“只有一个实例”，这正是 Kotlin 的 Unit 和 Java 的 void 的区别。  

### Nothing：“这个函数永不返回”
对某些 Kotlin 函数来说，“返回类型”的概念没有任何意义，因为它们从来不会成功的结束。
如：
```kotlin
fun fail(message: String): Nothing {
    throw IllegalStateException(message)
}

fun main(args: Array<String>) {
    fail("Error occurred")
}
```
Nothing 类型没有任何值，只有被当作函数返回值使用，或者被当作泛型函数返回值的类型参数使用才会有意义。

## 集合与数组
### 可空性和集合
List<Int?> 是能持有 Int？类型值的列表。
区分变量类型的可空性和用作类型参数的类型的可空性：
* List<Int?>
* List<Int?>?

### 只读集合与可变集合
Kotlin 的集合设计将访问集合数据的接口和修改集合数据的接口分开了。
* Kotlin.collections.Collection
* Kotlin.collections.MutableCollection：继承了 Collection 接口
> ps：之前刚接触 Kotlin 时就听过 Kotlin 集合和 Java 集合是一样的，所以这里有点疑问，不过后面有讲解。  

注意：只读集合不一定是不可变的。一个只读接口类型的变量可能只是同一个集合的多个引用之一，其他的引用有可能拥有一个可变接口类型。如果代码并行运行，这可能导致集合被其他代码修改，这将导致 concurrentModificationException 错误和其他一些问题。因此，必须了解只读集合并不总是线程安全的。

### Kotlin 集合和 Java
一种 Java 集合接口在 Kotlin 中都有两种表示：一种是只读的，另一种是可变的。可变接口直接对应 java.util 包中的接口，而它们的只读版本缺少了所有发生改变的方法。
创建函数：
* 只读：listOf
* 可变 ：mutableListOf、arrayListOf

因为 Java 并不区分只读集合与可变集合，即使 Kotlin 中把集合声明成只读的，Java 代码也能够修改这个集合。

### 作为平台类型的集合
当重写或者实现签名中有集合类型的 Java 方法时，需要决定使用哪一种 Kotlin 类型来表示这个 Java 类型。
* 集合是否可空？
* 集合中的元素是否可空？
* 你的方法会不会修改集合？

### 对象和基本数据类型的数组
默认情况下，应该优先使用集合而不是数组。
使用数组：
```kotlin
fun main(args: Array<String>) {
    for (i in args.indices) {
         println("Argument $i is: ${args[i]}")
    }
}
```
 创建：
* arrayOf
* arrayOfNulls
* Array 构造方法
```kotlin
fun main(args: Array<String>) {
    val letters = Array<String>(26) { i -> ('a' + i).toString() }
    println(letters.joinToString(""))
}
```

向 vararg 方法传递集合：
```kotlin
fun main(args: Array<String>) {
    val strings = listOf("a", "b", "c")
    println("%s/%s/%s".format(*strings.toTypedArray()))
}
```
`*` 是展开运算符。

数组类型的类型参数（泛型？）始终会变成对象类型，如 Array<Int> 对应的 Java 类型为 java.lang.Integer[]。为了表示基本数据类型的数组，Kotlin 提供了若干独立的类，如 IntArray、ByteArray、CharArray 等。
创建：
* 接收 size 的构造方法
* 工厂函数，如 IntArray 的 intArrayOf
* 另一种构造方法接收 size 和一个初始化元素的 lambda
```kotlin
fun main(args: Array<String>) {
    val squares = IntArray(5) { i -> (i+1) * (i+1) }
    println(squares.joinToString())
}
```