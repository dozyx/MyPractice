## 包
```kotlin
package my.demo
import java.util.*
```
目录与包名可以不匹配，即源文件可以任意放置。

## 方法
```kotlin
fun sum(a: Int, b: Int): Int {
    return a + b
}
```
两个 Int 参数，并且返回类型为 Int

```kotlin
fun sum(a: Int, b: Int) = a + b
```
方法体为一个表达式，其返回类型通过推断确定

```kotlin
fun printSum(a: Int, b: Int): Unit {
    println("sum of $a and $b is ${a + b}")
}
```
可以忽略 Unit 返回类型

## 变量
```kotlin
val a: Int = 1  // immediate assignment
val b = 2   // `Int` type is inferred
val c: Int  // Type required when no initializer is provided
c = 3       // deferred assignment
```
只读本地变量

```
var x = 5 // `Int` type is inferred
x += 1
```
易变变量

```kotlin
val PI = 3.14
var x = 0

fun incrementX() { 
    x += 1 
}
```
 顶层变量

## 注释
```kotlin
// This is an end-of-line comment

/* This is a block comment
   on multiple lines. */
```
Kotlin 中的块注释可以嵌套。??

## 使用字符串模板
```kotlin
var a = 1
// simple name in template:
val s1 = "a is $a" 

a = 2
// arbitrary expression in template:
val s2 = "${s1.replace("is", "was")}, but now is $a"
```

## 使用条件表达式
```kotlin
fun maxOf(a: Int, b: Int): Int {
    if (a > b) {
        return a
    } else {
        return b
    }
}
```
 用表达式表示：
```kotlin
fun maxOf(a: Int, b: Int) = if (a > b) a else b
```

## 使用可为 null 的值以及 null 检查
当引用可能为 null 时，必须进行显式标记。
```kotlin
fun parseInt(str: String): Int? {
    // ...
}
```
当 str  不是整型时，返回 null。

## 使用类型检查以及自动转换
`is` 操作符检查表达式是否为某个类型的实例，如果一个不可变的本地变量或属性已经经过指定类型的检测，那么将不需要再进行显式的转换
```kotlin
fun getStringLength(obj: Any): Int? {
    if (obj is String) {
        // `obj` is automatically cast to `String` in this branch
        return obj.length
    }

    // `obj` is still of type `Any` outside of the type-checked branch
    return null
}
```
或者
```kotlin
fun getStringLength(obj: Any): Int? {
    if (obj !is String) return null

    // `obj` is automatically cast to `String` in this branch
    return obj.length
}
```
甚至
```kotlin
fun getStringLength(obj: Any): Int? {
    // `obj` is automatically cast to `String` on the right-hand side of `&&`
    if (obj is String && obj.length > 0) {
        return obj.length
    }

    return null
}
```

## for 循环
```kotlin
val items = listOf("apple", "banana", "kiwi")
for (item in items) {
    println(item)
}
```
或者
```kotlin
val items = listOf("apple", "banana", "kiwi")
for (index in items.indices) {
    println("item at $index is ${items[index]}")
}
```

## while 循环
```kotlin
val items = listOf("apple", "banana", "kiwi")
var index = 0
while (index < items.size) {
    println("item at $index is ${items[index]}")
    index++
}
```

## when 表达式
```kotlin
fun describe(obj: Any): String =
when (obj) {
    1          -> "One"
    "Hello"    -> "Greeting"
    is Long    -> "Long"
    !is String -> "Not a string"
    else       -> "Unknown"
}
```

## 使用范围
```kotlin
val x = 10
val y = 9
if (x in 1..y+1) {
    println("fits in range")
}
```
使用 `in` 操作符判断一个数字是否在范围内

```kotlin
val list = listOf("a", "b", "c")

if (-1 !in 0..list.lastIndex) {
    println("-1 is out of range")
}
if (list.size !in list.indices) {
    println("list size is out of valid list indices range too")
}
```
 检查数字是否超出范围

```kotlin
for (x in 1..5) {
    print(x)
}
```
在范围内进行迭代

```kotlin
for (x in 1..10 step 2) {
    print(x)
}
println()
for (x in 9 downTo 0 step 3) {
    print(x)
}
```
 或者跨越一个进度

## 使用集合
```kotlin
fun main(args: Array<String>) {
    val items = listOf("apple", "banana", "kiwi")
    for (item in items) {
        println(item)
    }
}
```
集合的迭代

```kotlin
when {
    "orange" in items -> println("juicy")
    "apple" in items -> println("apple is fine too")
}
```
使用 `in` 操作符判断集合是否包含某个对象

```kotlin
fruits
.filter { it.startsWith("a") }
.sortedBy { it }
.map { it.toUpperCase() }
.forEach { println(it) }
```
 使用 lambda 表达式来 filter 和 map 集合

## 创建基本的类和它们的表达式
```kotlin
fun main(args: Array<String>) {
    val rectangle = Rectangle(5.0, 2.0) //no 'new' keyword required
    val triangle = Triangle(3.0, 4.0, 5.0)
    println("Area of rectangle is ${rectangle.calculateArea()}, its perimeter is ${rectangle.perimeter}")
    println("Area of triangle is ${triangle.calculateArea()}, its perimeter is ${triangle.perimeter}")
}

abstract class Shape(val sides: List<Double>) {
    val perimeter: Double get() = sides.sum()
    abstract fun calculateArea(): Double
}

interface RectangleProperties {
    val isSquare: Boolean
}

class Rectangle(
    var height: Double,
    var length: Double
) : Shape(listOf(height, length, height, length)), RectangleProperties {
    override val isSquare: Boolean get() = length == height
    override fun calculateArea(): Double = height * length
}

class Triangle(
    var sideA: Double,
    var sideB: Double,
    var sideC: Double
) : Shape(listOf(sideA, sideB, sideC)) {
    override fun calculateArea(): Double {
        val s = perimeter / 2
        return Math.sqrt(s * (s - sideA) * (s - sideB) * (s - sideC))
    }
}
```

参考：
[Basic Syntax](https://kotlinlang.org/docs/reference/basic-syntax.html)