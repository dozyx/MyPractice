## 函数和变量
一个打印 “Hello, world!” 的程序
```
fun main(args: Array<String>){
    println("Hello, world!")
}
```
从这段代码中，我们可以看到 Kotlin 的一些特性和语法：
* fun 声明一个函数
* 参数的类型写在名称后面
* 函数可以定义在文件的最外层，不需要把它放在类中
* 数组就是类
* 使用 println 代替 System.out.println。println 在 Kotlin 标准库中。
* 可以省略每行代码结尾的分号

### 函数
```
fun max(a: Int, b: Int): Int {
    return if (a > b) a else b
}
```
上面的代码展示了一个函数的基本结构：函数名称、参数列表、返回类型、函数体。需要注意，在 Kotlin 中 if 是有结果值的表达式。
> 语句和表达式：表达式有值，并且能作为另一个表达式的一部分使用；而语句总是包围着它的代码块中的顶层元素，并且没有自己的值。在 Java 中，所有的控制结构都是语句；而在 Kotlin 中，除了循环（for、do 和 do/while）以外大多数控制结构都是表达式。另一方面，Java 中的赋值操作是表达式，在 Kotlin 中反而变成了语句。这样有助于避免比较和赋值之间的混淆。  

#### 表达式函数体
```
fun max(a: Int, b: Int): Int = if (a > b) a else b
```
代码块体：函数体写在花括号中
表达式体：函数直接返回一个表达式。

对于表达式体函数，编译器可以利用类型推导来分析返回类型，所以我们可以忽略函数的返回类型：
```
fun max(a: Int, b: Int) = if (a > b) a else b
```

### 变量
Kotlin 的变量声明以关键字开始，然后是变量名称，最后加上类型（也可以不加）。
> 如果变量没有初始化器，需要显式地指定它的类型。  
> 声明变量的关键字有两个：
* val：value，不可变引用，相当于 Java 中的 final
* var：variable，可变引用

### 字符串模板
和许多脚本语言一样，Kotlin 让你可以在字符串字面值中引用局部变量，只需要在变量名称前面加上字符 $。如果需要引用更复杂的表达式，只需要把表达式用 {} 括起来。
```
fun main(args: Array<String>) {
    println("Hello, ${if (args.size > 0) args[0] else "Kotlin"}!")
}
```

## 类和属性

### 属性
在 Java 中，字段和其访问器（getter、setter）的组合常常被叫做属性；在 Kotlin 中，属性是头等的语言特性，完全代替了字段和访问器方法。
在类中声明一个属性和声明一个变量一样：使用 val 和 var 关键字。val 只读属性会生成一个字段和一个简单的 getter，var 可写属性会生成一个字段、一个 getter 和一个 setter。
> Kotlin 在访问 Java 类时，该类中的 getter 可以被当做 val 属性在 Kotlin 中访问，而一对 getter/setter 可以被当做 var 属性访问。  
> ps：刚开始看 kotlin 代码时，可能会发现有一些变量没有在类中声明，但却直接引用了，这时候可能就是访问的父类中的 getter/setter 方法。  

#### 自定义访问器
比如，声明一个矩形，它能判断自己是否是正方形。我们并不需要一个单独字段来存储这个信息，因为可以随时通过检查矩形的长度来判断。
```
class Rectangle(val height: Int, val width: Int) {
    val isSquare: Boolean
        get() = height == width
}
```
上面的 isSquare 属性只有一个自定义实现的 getter，它的值是每次访问属性的时候计算出来的。

#### 目录和包
Kotlin 和 Java 一样，也有 package 和 import 关键字。
* Kotlin  不区分导入的是类还是函数，它允许使用 import 直接导入顶层函数的名称。
* Kotlin 中，可以把多个类放在同一个文件中，文件的名字可以随意选择。Kotlin 也没有对磁盘上源文件的布局强加任何限制。

## 枚举和 when
> when 可以被认为是 switch 的替代品  

### 声明枚举类
```
enum class Color(val r: Int, val g: Int, val b: Int) {
    RED(255, 0, 0), ORANGE(255, 165, 0), YELLOW(255, 255, 0);
    fun rgb() = (r * 256 + g) * 256 + b
}
```
Kotlin 中，enum 是一个软关键字——只有当它出现在 class 前面时才有特殊的意义，在其他地方可以把它当做普通的名称使用。
注意，上面的代码中使用了分号，这也是 Kotlin 语法中唯一必须使用分号的地方。

### when
```
fun getMnemonic(color: Color) = when (color) {
    Color.RED -> "Richard"
    Color.ORANGE -> "Of"
    Color.YELLOW -> "York"
}
```
* 和 Java 不一样，我们不需要在每一个分支写上 break
* 如果需要将多个值合并到一个分支，只需要用逗号将值隔开。
* when 另一个强大的地方在于，我们可以使用任意的对象作为分支条件。
* 不带参数的 when，即 when 后面直接跟 {}，无参的 when 的分支条件是任意的布尔表达式。


### 智能转换
当已经检查过一个变量是某种类型（is 关键字），后面就不再需要转换它，可以直接把它当做检查过的类型使用，这种行为称为智能转换。
> 如果需要显式转换到特定类型，可以使用 as 关键字。  


## 迭代：“while” 循环和 “for” 循环
Kotlin 中的 for 循环仅以唯一一种形式存在，和 Java 的 for-each 循环一致。
### while 循环
while 和 do-while 与 Java 中的循环一致。

### 迭代数字：区间和数列
区间：如，`1..10`，Kotlin 的区间是闭合的。
如果能迭代区间中所有的值，这样的区间被称作数列。
其他例子：`for(i in 100 downTo 1 step 2)`、`for(x in 0 until size)`

### 迭代 map
```
    val binaryReps = TreeMap<Char, String>()
    for (c in 'A'..'F') {
        val binary = Integer.toBinaryString(c.toInt())
        binaryReps[c] = binary
    }
    for ((letter, binary) in binaryReps) {
        println("$letter = $binary")
    }
```
上面的代码将字符对应的二进制打印了出来。在 map 中我们以字符作为键，以二进制作为值。在第二个 for 循环中，展开的结果存储到了两个独立的变量中：letter 是键，binary 是值。
> 上面的代码中还有一个实用的技巧：map[key] 读取值，map[key] = value 设置值。  

### 实用 in 检查集合和区间的成员
```
fun isLetter(c: Char) = c in 'a'..'z' || c in 'A'..'Z'
fun isNotDigit(c: Char) = c !in '0'..'9'
```

## 异常
Kotlin 异常的抛出与 Java 类似
```
val percentage = if (number in 0..100) number else throw IllegalArgumentException("A percentage value must be between 0 and 100: $number")
```
与 Java 不同的是，Kotlin 中 throw 结构是一个表达式，能作为另一个表达式的一部分使用。

### try catch 和 finally
和 Java 一样，使用带有 catch 和 finally 子句的 try 结构来处理异常。
和 Java 最大的区别就是 Kotlin 中没有 throws，因为 Kotlin 并不区分受检异常和为受检异常。

### try 表达式
```
fun readNumber(reader: BufferedReader) {
    val number = try {
        Integer.parseInt(reader.readLine())
    } catch (e: NumberFormatException) {
        null
    }
    println(number)
}
```
如果一个 try 代码块执行一切正常，代码块中最后一个表达式就是结果，如果捕获到了一个异常，相应的 catch 代码块中最后一个表达式就是结果。
上面的代码如果发生异常，结果值为 null。