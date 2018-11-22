Lambda 表达式，本质上就是可以传递给其他函数的一小段代码。

## Lambda 表达式和成员引用
### 简介：作为函数参数的代码块
例子：
匿名内部类实现监听器
```java
/* Java */
button.setOnClickListener(new OnClickListener) {
    @Override
    public void onClick(View view) {
        ...
    }
};
```
lambda 实现
```
button.setOnClickListener {...}
```

### Lambda 和集合
例子：
找出列表中年龄最大的人，手动在集合中搜索

```scala
data class Person(val name: String, val age: Int)

fun findTheOldest(people: List<Person>) {
    var maxAge = 0
    var theOldest: Person? = null
    for (person in people) {
        if (person.age > maxAge) {
            maxAge = person.age
            theOldest = person
        }
    }
    println(theOldest)
}
```
用 lambda 在集合中搜索
```scala
people.maxBy { it.age }
```
maxBy 可以在任何集合上调用，且只需要一个实参：一个函数，指向比较哪个值来找到最大元素。如果 lambda 刚好是函数或者属性的委托，可以用成员引用替换。
```scala
people.maxBy (Person::age)
```

### Lambda 表达式的语法
`{x: Int, y: Int -> x + y}`
* `->` 左侧为参数，右侧为 函数体
* 始终在花括号内

可以把 lambda 表达式存储在一个变量中，把这个变量当做普通函数对待（即通过相应实参调用它）。（ps：这时不应该把变量当做一个值看待）
```
>>> val sum = {x: Int, y:Int -> x + y}
>>> println(sum(1, 2))
3
```
如果你乐意，还可以直接调用 lambda 表达式
```
>>> {println(42)}()
42
```
但这样的语法毫无可读性，也没有什么意义。如果确实需要把一小段代码封闭到一个代码块中，可以使用库函数 run 来执行传给它的 lambda：
```
>>> run { println(42)}
42
```


代码：
```scala
people.maxBy { it.age }
```
如果不用简明语法，将是：
```scala
people.maxBy ({p: Person -> p.age})
```
Kotlin 有一种语法约定：如果 lambda 表达式是函数调用的最后一个实参，它可以放到括号的外边。
```
people.maxBy() {p: Person -> p.age}
```
当 lambda 是函数唯一的实参时，还可以去掉调用代码中的空括号对：
```
people.maxBy {p: Person -> p.age}
```
省略 lambda 参数类型：
```
people.maxBy {p -> p.age}
```
 使用默认参数名称 it 代替命名参数。如果当前上下文期望的是只有一个参数的 lambda 且这个参数的类型可以推断出来，就会生成这个名称。
```
people.maxBy { it.age} // it 是自动生成的
```
> it 约定能大大缩短代码，但不应该滥用。显式声明参数在某些情况下可读性更高。  

### 在作用域中访问变量
forEach 函数：在集合中的每一个元素都调用给定的 lambda。它比普通的 for 循环更简洁一些，但它并没有更多其他优势。
```scala
fun printMessagesWithPrefix(messages: Collection<String>, prefix: String) {
    messages.*forEach***{***println*("$prefix $**it**") **}**
}
```
和 Java 不一样，Kotlin 允许在 lambda 内部访问非 final 变量甚至修改它们。从 lambda 内访问外部变量，我们称这些变量被 lambda 捕捉。
> 捕捉可变变量：实现细节 
> class Ref<T>(var value: T)  //模拟捕捉可变变量的类  
>
> `>>>` val counter = Ref(0) 
> `>>>` val inc = (counter.value++) 
> 上面代码创建了一个包装类，它存储要改变的值的引用。
> 在 Kotlin 实际代码中，不需要创建这样的包装器，可以直接修改这个变量：
> val counter = 0 
> val inc = {counter.value ++ } 
> 第一部分代码就是第二部分代码背后的原理。   

### 成员引用
Kotlin 和 Java8 一样，如果把函数转换成一个值，你就可以传递它。使用 `::` 来装换：
```
val getAge = Person::age
```
这种表达式称为成员引用。
Person::age
`::` 左侧为类，右侧为成员。
下面是一个 lambda 表达式，它做同样的事情：
```
val getAge = { person: Person -> person.age}
```
成员引用和调用该函数的 lambda 具有一样的类型，所以可以互换使用：
```
person.maxBy(Person::age)
```
还可以引用顶层函数（不是类的成员）：
```
fun salute() = println("Salute!")
>>> run(::salute)
Salute!
```

> ps：Lambda 表达式和成员引用时两个概念，它们可以在某些情况可以相互转换。可以将它们理解为将函数（代码块）存储到变量中，然后在使用时进行展开？  

## 集合的函数式 API
### 基础：filter 和 map
```scala
fun main(args: Array<String>) {
    val list = listOf(1, 2, 3, 4)
    println(list.filter { it % 2 == 0 })
}
```
 filter 从集合中移除不想要的元素，但并不会改变这些元素。

```scala
fun main(args: Array<String>) {
    val list = listOf(1, 2, 3, 4)
    println(list.map { it * it })
}
```
map 对集合中的每一个元素应用给定的函数并把结果收集到一个新集合。
还可以对 map 应用过滤和变换函数：
```scala
fun main(args: Array<String>) {
    val numbers = mapOf(0 to "zero", 1 to "one")
    println(numbers.mapValues { it.value.toUpperCase() })
}
```
输出

### all、any、count、find：对集合应用判断式
```scala
data class Person(val name: String, val age: Int)

val canBeInClub27 = { p: Person -> p.age <= 27 }

fun main(args: Array<String>) {
    val people = listOf(Person("Alice", 27), Person("Bob", 31))
    println(people.all(canBeInClub27))
}
```
all 是否所有元素都满足
```scala
fun main(args: Array<String>) {
    val list = listOf(1, 2, 3)
    println(!list.all { it == 3 })
    println(list.any { it != 3 })
}
```
any 集合中至少存在一个匹配的元素
count 检查集合中有多少元素满足了判断式
```scala
data class Person(val name: String, val age: Int)

val canBeInClub27 = { p: Person -> p.age <= 27 }

fun main(args: Array<String>) {
    val people = listOf(Person("Alice", 27), Person("Bob", 31))
    println(people.find(canBeInClub27))
}
```
find 返回第一个符合条件的元素，它有一个同义方法 firstOrNull

### groupBy：把列表转换成分组的 map
```scala
data class Person(val name: String, val age: Int)

fun main(args: Array<String>) {
    val people = listOf(Person("Alice", 31),
            Person("Bob", 29), Person("Carol", 31))
    println(people.groupBy { it.age })
}
```
 操作结果是一个 map，是元素分组依据的键（age）和元素分组（persons）之间的映射。

### flatMap 和 flatter：处理嵌套集合中的元素
```scala
fun main(args: Array<String>) {
    val strings = listOf("abc", "def")
    println(strings.flatMap { it.toList() })
}
```
```scala
class Book(val title: String, val authors: List<String>)

fun main(args: Array<String>) {
    val books = listOf(Book("Thursday Next", listOf("Jasper Fforde")),
                       Book("Mort", listOf("Terry Pratchett")),
                       Book("Good Omens", listOf("Terry Pratchett",
                                                 "Neil Gaiman")))
    println(books.flatMap { it.authors }.toSet())
}
```
flapMap 做了两件事：首先根据作为实参给定的函数对集合中的每一个元素做变换（map），然后把多个列表合并（flat）成一个列表。
如果不需要做任何变换，只是需要平铺一个集合，可以使用 flatten 函数。

## 惰性集合操作：序列
如：
```
people.map(Person::name).filter { it.startWith("A") }
```
上面的例子中，map 和 filter 都会创建一个列表。如果元素很多，（链式）调用就会变得十分低效。
为了提高效率，可以把操作变成使用序列，而不是直接使用集合：
people.asSequence()
​    .map(Person::name)
​    .filter { it.startsWith(“A”) }
​    .toList()

Kotlin 惰性集合操作的入口就是 Sequence 接口。通常，需要对一个大型集合执行链式操作时要使用序列。

### 执行序列操作：中间和末端操作
序列操作分为两类：中间的和末端的。一次中间操作返回的是另一个序列，这个新序列知道如何变换原始序列中的元素。而一次末端操作返回的是一个结果，这个结果可能是集合、元素、数字，或者其他从初始集合的变换序列中获取的任意对象。
如：
sequence.map{…}.filter{…}.toList()
其中，map 和 filter 是中间操作，toList 是末端操作。
中间操作始终是惰性的，末端操作触发执行了所有的延期计算。
> ps：中间操作被延时执行。  
> 对序列来说，所有操作是按顺序应用在每一个元素上。

### 创建序列
除了在集合上调用 asSequence()，另一种创建序列的方法是使用 generateSequence 函数。
```
fun main(args: Array<String>) {
    val naturalNumbers = generateSequence(0) { it + 1 }
    val numbersTo100 = naturalNumbers.takeWhile { it <= 100 }
    println(numbersTo100.sum())
}
```
上面的 naturalNumbers 和 numbersTo100 都是有延期操作。

## 使用 Java 函数式接口
将一个 lambda 传给 Java 方法的例子：
```
button.setOnClickListener { /* 点击之后的动作 */ }
```
这种方式可以工作的原因是 OnClickListener 接口只有一个抽象方法。这种接口被称为函数式接口，或者 SAM 接口，SAM 代表单抽象方法。

### 把 lambda 当做参数传递给 Java 方法
可以把 lambda 传给任何期望函数式接口的方法。
如：
```
postponeComputation(int delay, Runnable computation);
```
Kotlin 调用：
```
postponeComputation(1000) { println(42)}
```
也可以通过显式创建匿名对象：
```
postponeComputation(1000, object: Runnable {
    override fun run() {
        println(42)
    }
})
```
当显式地声明对象时，每次调用都会创建一个新的实例。使用 lambda 的情况则不同：如果 lambda 没有访问任何来自自定义它的函数的变量，相应的匿名类实例可以在多次调用之间重用。
因此，完全等价的实现如下：
```
val runnable = Runnable { println(42) }
fun handleComputation() {
    postponeComputation(1000, runnable)
}
```
如果 lambda 从包围它的作用域中捕捉了变量，每次调用就不再可能重用同一个实例了。如：
```
fun handleComputation(id: String) {
    postponeComputation(1000) { println(id) }
}
```

### SAM 构造方法：显式地把 lambda 转换成函数式接口
SAM 构造方法是编译器生成的函数，让你执行从 lambda 到函数式接口实例的显式转换。
```
fun createAllDoneRunnable(): Runnable {
    return Runnable { println("All done!") }
}
```
SAM 构造方法还可以用在需要把从 lambda 生成的函数式接口实例存储在一个变量的情况。如：
```
val listener = OnClickListener { view -> 
    val text = when (view.id) {
        R.id.button1 -> "First button"
        R.id.button2 -> "Second button"
        else -> "Unknown button"
    }
}
```

> 注意，lambda 内部没有匿名对象那样的 this：没有办法引用到 lambda 转换成的匿名类实例。从编译器的角度来看，lambda 是一个代码块，不是一个对象，而且也不能把它当成对象引用。Lambda 中的 this 引用指向的是包围它的类。  
> 如果你的事件监听器在处理事件时还需要取消它自己，不能使用 lambda 这样做。  

## 带接收者的 lambda ： “with” 与 “apply”
### “with” 函数
``` kotlin
fun alphabet(): String {
    val result = StringBuilder()
    for (letter in 'A'..'Z') {
         result.append(letter)
    }
    result.append("\nNow I know the alphabet!")
    return result.toString()
}
```
使用 with 重写
```kotlin
fun alphabet(): String {
    val stringBuilder = StringBuilder()
    return with(stringBuilder) {
        for (letter in 'A'..'Z') {
            this.append(letter)
        }
        append("\nNow I know the alphabet!")
        this.toString() 
        // this 可以省略
    }
}
```
With 实际上是一个接收两个参数的函数：这个例子中两个参数分别是 StringBuilder 和一个 lambda。with 函数把它的第一个参数转换成作为第二个参数传给它的 lambda 的接收者。
进一步重构去掉额外的 StringBuilder 变量：
```kotlin
fun alphabet() = with(StringBuilder()) {
    for (letter in 'A'..'Z') {
        append(letter)
    }
    append("\nNow I know the alphabet!")
    toString()
}
```

### “apply” 函数
apply 几乎和 with 函数一模一样，唯一的区别是 apply 始终会返回作为实参传递给他的对象（即接收者对象）。
使用 apply 重构：
```
fun alphabet() = StringBuilder().apply {
    for (letter in 'A'..'Z') {
        append(letter)
    }
    append("\nNow I know the alphabet!")
}.toString()
```
apply 被声明成一个扩展函数。它的接收者变成了作为实参的 lambda 的接收者。
进一步使用标准库函数简化：
```
fun alphabet() = buildString {
    for (letter in 'A'..'Z') {
        append(letter)
    }
    append("\nNow I know the alphabet!")
}
```