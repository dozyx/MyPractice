## 在 Kotlin 中创建集合
```
val set = hashSetOf(1, 7, 53)
val list = arrayListOf(1, 7, 53)
val map = hashMapOf(1 to "one", 7 to "seven", 53 to "fifty-three")
```
上面的三个变量的类型分别为 HashSet、ArrayList、HashMap。
> Kotlin 没有采用自己的集合类，而是采用的标准的 Java 集合类，不过 Kotlin 还对 Java 集合类进行了扩展。  

## 让函数更好调用
首先，实现一个函数来格式化集合的输出
```
fun <T> joinToString(
        collection: Collection<T>,
        separator: String,
        prefix: String,
        postfix: String
): String {

    val result = StringBuilder(prefix)

    for ((index, element) in collection.withIndex()) {
        if (index > 0) result.append(separator)
        result.append(element)
    }

    result.append(postfix)
    return result.toString()
}
```

接下来，我们将从以下几个方面进行修改
* 可读性：比如一个调用 `joinToString(collection, " ", " ", ".")`，我们将很难看出 String 对应的是哪些参数，为了使调用更优雅，Kotlin 可以在调用时显式标明一些参数的名称，如`joinToString(collection, separator = " ", prefix = " ", postfix = ".")`。
> 注意，当你调用 Java 的函数时，不能采用命名参数。因为把参数名称存到 .class 文件是 Java8 及其更高版本的一个可选功能，而 Kotlin 需要保持和 Java6 的兼容性。  
* 默认参数值：Java 的一个普遍问题是重载函数过多，这就导致一个结果：重复。在 Kotlin 中，可以在声明函数时，指定参数的默认值，这样就可以避免创建重载函数。
```
fun <T> joinToString(
        collection: Collection<T>,
        separator: String = “， ”,
        prefix: String = “”,
        postfix: String = “”
): String
```
如果是常规调用，必须按照函数声明中定义的参数顺序来给定参数，可以省略的只有末尾的参数；如果使用命名参数，可以省略中间的一些参数，也可以以你想要的任意顺序只给定你需要的参数。
> 考虑到 Java 没有参数默认值的概念，当你从 Java 中调用 Kotlin 函数时，必须显式地指定所有参数值。不过也可以通过 @JvmOverloads 注解来生成重载函数。  
* 消除静态工具类：顶层函数和属性
  出于各种目的，我们通常会编写大量的 Util 为后缀的类，这些类不包含任何转态或者实例函数，而是仅仅作为一堆静态函数的容器，如 Collections。在 Kotlin 中，根本就不需要去创建这些无意义的类。相反，可以把这些函数直接放到代码文件的顶层，不用从属于任何的类。
  将 joinToString 直接放到 strings 的包中
```
package strings
fun joinToString(...):String{...}
```
在编译该文件时，会生成一些类，比如 join.kt 生成的类名为 JoinKt，当从 Java 调用这个函数时，和调用任何其他静态函数一样。
> 要修改包含 Kotlin 顶层函数的生成的类的名称，需要为这个文件添加 @JvmName 的注解，将其放到这个文件的开头。  
> 和函数一样，属性也可以放到文件的顶层。默认情况下，顶层属性和其他任意的属性一样，是通过访问器暴露给 Java 使用的。为了方便使用，如果你想要把一个常量以 public static final 的属性暴露给 Java，可以用 const 来修饰它。

## 扩展函数和属性
如为 String 添加一个方法来计算一个字符串的最后一个字符：
```
fun String.lastChar(): Char = this.get(this.length - 1)
```
上面代码中，String 为接收者类型（类的名称），this 为接收者对象（用来调用这个扩展函数的对象）。上面的 this 也可以省略。
调用：
```
println("Kotlin".lastChar())
```
> 注意，扩展函数不能访问私有的或者是受保护的成员。  
### 导入扩展函数
如果需要使用扩展函数，需要进行导入。在导入的时候可以使用 as 关键字来修改导入的类或函数名称。如：
```java
import strings.lastChar as last
```

### Java 中调用扩展函数
实质上，扩展函数是静态函数，它把调用对象作为了它的第一个参数。比如，扩展函数声明在一个叫 StringUtil.kt 的文件中：
```java
/* Java */
char c = StringUtilKt.lastChar("Java");
```

### 作为扩展函数的工具函数
```kotlin
fun <T> Collection<T>.joinToString(
        separator: String = ", ",
        prefix: String = "",
        postfix: String = ""
): String {
    val result = StringBuilder(prefix)

    for ((index, element) in this.withIndex()) {
        if (index > 0) result.append(separator)
        result.append(element)
    }

    result.append(postfix)
    return result.toString()
}
```

### 不可重写的扩展函数
扩展函数的静态性质也决定了扩展函数不能被子类重写。
扩展函数并不是类的一部分，它是声明在类之外的。尽管可以给基类和子类都分别定义一个同名的扩展函数，当这个函数被调用时，它是由该变量的静态类型所决定的，而不是这个变量的运行时类型——这个子类重写父类的函数不同。
```
open class View {
    open fun click() = println("View clicked")
}

class Button: View() {
    override fun click() = println("Button clicked")
}

fun View.showOff() = println("I'm a view!")
fun Button.showOff() = println("I'm a button!")

fun main(args: Array<String>) {
    val view: View = Button()
    view.showOff()
}
```
输出结果为：I'm a view!
> 注意，如果一个类的成员函数和扩展函数有相同的签名，成员函数往往会被优先使用。  

### 扩展属性
尽管被称为属性，但扩展属性可以没有任何状态，因为没有合适的地方来存储它，不可能给现有的 Java 对象的实例添加额外的字段。
```
val String.lastChar: Char 
    get() = get(length - 1)
```
扩展属性必须定义 getter，因为没有支持字段，因此没有默认 getter 的实现。同理，也不可以初始化。

## 处理集合：可变参数、中缀调用和库的支持
### 可变参数
Kotlin 可变参数需要使用关键字 vararg 进行修饰，与 Java 的另一个区别在于当传递的参数为数组时，需要使用展开运算符`*`显式地解包数组。
```
fun listOf<T>(vararg values: T): List<T> {...}
```
```
fun main(args: Array<String>) {
    val list = listOf("args: ", *args)
    println(list)
}
```
> Kotlin 中可变参数可以不放在参数最后，这是看到的一个例子，以后有准确解释再补充  
### 键值对的处理
创建：
```
val map = mapOf(1 to "one", 7 to "seven", 53 to "fifty-three")
```
上面代码中的 to 并不是内置的结构，而是一种特殊的函数调用，被称为中缀调用。
下面两种调用方式是等价的：
1. 一般 to 函数的调用：`1.to(“one”)`
2. 使用中缀符号调用 to 函数：`1 to “one”`

中缀调用可以与只有一个参数的函数一起使用，要允许使用中缀符号调用安徽省农户，需要使用 infix 修饰符来标记它。
下面是一个简单的 to 函数声明：
```
infix fun Any.to(other: Any) = Pair(this, other)
// to 函数返回一个 Pair 类型的对象
```
也可以直接用 Pair 的内容来初始化两个变量：
```
val (number, name) = 1 to "one"
// Pair 的元素分别初始化 number 和 name
```
这个功能称为解构声明。这种特征还能用于循环，如：
```
fun ((index, element) in collection.withIndex()) {
    println("$index: $element")
}
```
> to 函数是一个扩展函数，可以创建一对任何元素。  
> 疑问：中缀调用指的是 to 函数的一种变形写法？  

## 字符串和正则表达式的处理
### 分割字符串
Java 中，String 的 spilt 方法在以点号分割“12.345-6.A” 时得到的是一个空数组，因为 spilt 接受的是一个正则表达式，而 `.` 在正则中表示任何字符。
Kotlin 把该函数进行了隐藏，作为替换，提供了一些名为 split 的，具有不同参数的重载的扩展函数。

### 正则表达式和三重引号的字符串
例子：将路径分割为目录，文件名，扩展名
使用 String 的扩展函数
```
fun parsePath(path: String) {
    val directory = path.substringBeforeLast("/")
    val fullName = path.substringAfterLast("/")

    val fileName = fullName.substringBeforeLast(".")
    val extension = fullName.substringAfterLast(".")

    println("Dir: $directory, name: $fileName, ext: $extension")
}

fun main(args: Array<String>) {
    parsePath("/Users/yole/kotlin-book/chapter.adoc")
}
```
使用正则表达式
```
fun parsePath(path: String) {
    val regex = """(.+)/(.+)\.(.+)""".toRegex()
    val matchResult = regex.matchEntire(path)
    if (matchResult != null) {
        val (directory, filename, extension) = matchResult.destructured
        println("Dir: $directory, name: $filename, ext: $extension")
    }
}

fun main(args: Array<String>) {
    parsePath("/Users/yole/kotlin-book/chapter.adoc")
}
```
上面的正则表达式表示中使用了三重引号，在这样的字符串汇总，不需要对任何字符进行转义。

### 多行三重引号的字符串
使用三重引号的另一种方便之处在于，可以简单地把半酣换行符的文本嵌入到程序汇中：
```
val kotlinLogo = """| //
                   .|//
                   .|/ \"""
fun main(args: Array<String>) {
    println(kotlinLogo.trimMargin("."))
}
```
输出：
| 
|
|/ \


## 让你的代码更整洁：局部函数和扩展
带重复代码的函数：
```
class User(val id: Int, val name: String, val address: String)

fun saveUser(user: User) {
    if (user.name.isEmpty()) {
        throw IllegalArgumentException(
            "Can't save user ${user.id}: empty Name")
    }

    if (user.address.isEmpty()) {
        throw IllegalArgumentException(
            "Can't save user ${user.id}: empty Address")
    }

    // Save user to the database
}
// 进行了两次 isEmpty 判断
```
提取局部函数来避免重复
```
class User(val id: Int, val name: String, val address: String)

fun saveUser(user: User) {

    fun validate(user: User,
                 value: String,
                 fieldName: String) {
        if (value.isEmpty()) {
            throw IllegalArgumentException(
                "Can't save user ${user.id}: empty $fieldName")
        }
    }

    validate(user, user.name, "Name")
    validate(user, user.address, "Address")

    // Save user to the database
}
// 第一次看到函数还能嵌套，有点惊讶。。
```
在局部函数中访问外层函数的参数
```
class User(val id: Int, val name: String, val address: String)

fun saveUser(user: User) {
    fun validate(value: String, fieldName: String) {
        if (value.isEmpty()) {
            throw IllegalArgumentException(
                "Can't save user ${user.id}: " +
                    "empty $fieldName")
        }
    }

    validate(user.name, "Name")
    validate(user.address, "Address")

    // Save user to the database
}
// 没啥，只是去掉了 User 参数
```
提取逻辑到扩展函数
```
class User(val id: Int, val name: String, val address: String)

fun User.validateBeforeSave() {
    fun validate(value: String, fieldName: String) {
        if (value.isEmpty()) {
            throw IllegalArgumentException(
               "Can't save user $id: empty $fieldName")
        }
    }

    validate(name, "Name")
    validate(address, "Address")
}

fun saveUser(user: User) {
    user.validateBeforeSave()

    // Save user to the database
}
// 好吧，其实我已开始想得修改就是扩展函数。。不过我没想到有局部函数这种东西。。
```
> 扩展函数也可以被声明为局部函数，但是深层嵌套的局部函数往往令人费解、  