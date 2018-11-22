与 Java 区别：
* Kotlin 接口可以包含属性声明
* Kotlin 的声明默认是 final 和 public
* 嵌套的类默认并不是内部类：它们并不能包含对其外部类的隐式引用
* data 类会自动生成若干标方法
* …

## 定义类的继承结构

### Kotlin 中的接口
与 Java8 相似，Kotlin 的接口可以包含抽象方法的定义以及非抽象方法的实现，但它们不能包含任何的状态。
Kotlin 使用冒号来代替 Java 中的 extends 和 implements，和 Java 一样，一个类可以实现任意多个接口，但是只能继承一个类。
接口的方法可以有一个默认实现，与 Java8 不同的是，Java8 中需要在这样的实现上标注 default 关键字，而 Kotlin 没有。
```
interfact Clickable {
    fun click()
    fun showOff() = println("I'm clickable")
}
```
> 假如在另一个接口中也定义了 showOff，并提供默认实现，那么如果一个类同时实现了这两个接口，该类不同调用两个接口中的任何一个，而是要求显式实现 showOff。  
> 如下方式可以表明调用哪个父类的实现：
```dart
class Button : Clickable, Focusable {
    override fun click() = println("I was clicked")

    override fun showOff() {
        super<Clickable>.showOff()
        super<Focusable>.showOff()
    }
}

interface Clickable {
    fun click()
    fun showOff() = println("I'm clickable!")
}

interface Focusable {
    fun setFocus(b: Boolean) =
        println("I ${if (b) "got" else "lost"} focus.")

    fun showOff() = println("I'm focusable!")
}
```
> Kotlin 1.0 是以 Java 6 为目标设计的，其并不支持接口中的默认方法。因此它会把每个带默认方法的接口编译成一个普通接口和一个将方法体作为静态函数的类的结合体。  

### open、final 和 abstract 修饰符：默认为 final
> Java 允许创建任意类的子类并重写任意方法，除非显式地使用了 final 关键字进行标注。这样导致了一个问题：对基类进行修改会导致子类不正确的行为，这就是所谓的脆弱的基类问题，因为基类代码的修改不再符合在其子类中的假设。  
> ps：有时候看见 base 就蛋疼。  
> 《Effective Java》：要么为继承做好设计并记录文档，要么禁止这么做。  
> Kotlin 中，如果想允许创建一个类的子类，需要使用 open 修饰符来标示这个类，此外，需要给每一个可以被重写的属性或方法添加 open 修饰符。
```
interface Clickable {
    fun click()
    fun showOff() = println("I'm clickable!")
}

open class RichButton : Clickable {

    fun disable() {} // final 子类不能重写

    open fun animate() {} // open，子类可以重写

    override fun click() {} // 重写了 open 函数，其本身同样是 open， 子类可以重新声明为 final
}
```
> 类默认为 final 带来了一个重要的好处就是这使得在大量场景中的智能转换（当检查过一个变量的类型后就不再需要进行转换，而是可以直接当做检查过的类型来使用）成为可能。因为智能转换只能在进行类型检查后没有改变过的变量上起作用。  
> 与 Java 一样，Kotlin 也可以将一个类声明为 abstract，这样的类不能被实例化，抽象类成员始终是 open 的（非抽象函数并不是默认 open），所以不需要显式地使用 open 修饰符。 

### 可见性修饰符：默认 public
* public：默认
* protected：在 Java 中，可以从同一个包中访问一个 protected 成员，但是 Kotlin 不允许，protected 成员只在类和它的子类中可见。（ps：之前也没注意 Java 可以从包中访问）
* private
* internal：新增，表示「只在模块内部可见」。一个模块是一组一起编译的 Kotlin 文件，可能是一个 IDEA 模块、一个 Eclipse 项目、一个 Maven 或 Gradle 项目或者一组使用调用 Ant 任务进行编译的文件（感觉解释地还是很模糊）。

Internal 可见性的优势在于它提供了对模块实现细节的真正封装。使用 Java  时，这种封装很容易被破坏，因为外部代码可以将类定义到与你代码相同的包中，从而得到访问你的包私有声明的权限。
> 一直都没注意到 Java 还有这中套路。。  
> 另一个区别是，Kotlin 允许在顶层声明中使用 private 可见性，包括类、函数、属性。这些声明就会只在声明它们的文件中可见。（这是书中的说法，不过有问题，不知道是不是翻译问题，实际上，一个类中的 private 方法仅对该类可见）
```
internal open class TalkativeButton {
    private fun yell() = *println*("Hey!")
    protected fun whisper() = *println*("Let's talk!")
}

fun TalkativeButton.giveSpeech() {//错误：public 成员暴露了其 internal 接收者类型 TalkativeButton
    yell() // 错误：不能访问 private 成员
    whisper() // 错误：不能访问 protected 成员
}
```
> Java 中没有与 internal 类似的概念，因此 internal 修饰符在字节码中会变成 public。  
> 另一个 Kotlin 与 Java 之间可见性规则的区别就是，在 Kotlin 中一个外部类不能看到其内部（或者嵌套）类的 private 成员。

> 总结：Kotlin 与 Java 在可见性方面的差异还是蛮大的，感觉相互间转换会有点麻烦  
> 1. Kotlin 没有 package，多了一个 internal  
> 2. Kotlin 允许在顶层声明 private（Java 中顶层类不能为 private）  
> 3. Kotlin 中的 protected 只在类和其子类中可见，Java 同一个包也能访问  
> 4. Kotlin 中外部类不能访问内部类或嵌套类的 private 成员。  

### 内部类和嵌套类：默认是嵌套类
与 Java 的区别在于，Kotlin 的嵌套类不能访问外部类的实例，除非特别地做出了要求。
Kotlin 中没有显式修饰符的嵌套类与 Java 中的 static 嵌套类是一样的。要把它变成一个内部类来持有一个外部类的引用的话需要使用 inner 修饰符。

嵌套类：Java 中 `static class A`，Kotlin 中 `class A`
内部类：Java 中 `class A`，Kotlin 中 `inner class A`
> 嵌套类不持有外部类的引用，而内部类持有  
> 在 Kotlin 中需要使用 `this@Outer` 从 Inner 类去访问 Outer 类。

### 密封类：定义受限的类继承结构
```scala
interface Expr
class Num(val value: Int) : Expr
class Sum(val left: Expr, val right: Expr) : Expr

fun eval(e: Expr): Int =
    when (e) {
        is Num -> e.value
        is Sum -> eval(e.right) + eval(e.left)
        else ->
            throw IllegalArgumentException("Unknown expression")
    }
```
上面代码存在的一些问题：
* when 表达式中强制提供 else 分支，即必须提供一个默认分支，即使什么都没处理
* 假如添加了一个新的 Expr 子类，编译器并不能发现有地方改变了，如果忘记了添加一个新分支，就会选择默认的选项，这有可能导致潜在的 bug。

Kotlin 为这个问题提供了一个解决方案：sealed 类。
「为父类添加一个 sealed 修饰符，对可能创阿金的子类做出严格的限制，所有的直接子类必须嵌套在父类中」。密封类不能在类外部拥有子类。
Kotlin 1.1 允许在同一个文件的任何位置定义 sealed 类的子类。
```scala
sealed class Expr {
    class Num(val value: Int) : Expr()
    class Sum(val left: Expr, val right: Expr) : Expr()
}

fun eval(e: Expr): Int =
    when (e) { 
    // when 中涵盖所有可能的情况，所以不需要 else 分支。
        is Expr.Num -> e.value
        is Expr.Sum -> eval(e.right) + eval(e.left)
    }
```
> 注意，sealed 修饰符隐含的这个类是一个 open 类。  
> ps：当涵盖所有可能情况的时候，不要求 when 使用 else 分支，但并不是指 when 一定需要涵盖 sealed 类的所有可能，在不需要涵盖所有可能的情况下，仍可以使用 else。  

## 声明一个带非默认构造方法或属性的类
Kotlin 区分了主构造方法（通常是主要而简洁的初始化类的方法，并且在类体外部声明）和从构造方法（在类体内部声明）。与 Java 一样允许在初始化体语句块中添加额外的初始化逻辑。
```
class User(val nickname: String) // val 意味着相应的属性会用构造方法的参数来初始化
```
```
class User constructor(_nickname: String) {// 带一个参数的主构造方法，
    val nickname: String
    init {// 初始化语句块
        nickname = _nickname
    }
}
```
```
class User(_nickname: String) {
    val nickname = _nickname
}
```
以上三种写法是等价的，但第一种最为简洁。我们也可以像函数参数一样，为构造方法参数声明一个默认值。

如果一个类具有父类，主构造方法同样需要初始化父类。
```
open class User(val nickname: String) {...}
class TwitterUser(nickname: String) : User(nickname) {...}
```
如果没有给一个类声明任何的构造方法，将会生成一个不做任何事情的默认构造方法：
```
open class Button
```
如果继承 Button 类并且没有提供任何的构造方法，必须显式地调用父类的构造方法，即使它没有任何的参数：
```
class RadioButton: Button()
```
如果想要确保类不被其他代码实例化，必须把构造方法标记为 private：
```
class Secretive private constructor() {}
```

### 构造方法：用不同的方式来初始化父类
通常来讲，使用多个构造方法的类中 Kotlin 代码中不如在 Java 中常见。大多数在 Java 中需要重载构造方法的场景都被 Kotlin 支持参数默认值和参数命名的语法涵盖了。不过 Kotlin 也能支持多构造函数的常见：
```scala
open class View {// 没有主构造方法
    constructor(ctx: Context) {

    }

    constructor(ctx: Context, attr: AttributeSet) {

    }
}

class MyButton : View {
    constructor(ctx: Context) : this(ctx, MY_STYLE) {// 委托给这个类的另一个构造方法

    }

    constructor(ctx: Context, attr: AttributeSet) : super(ctx, attr) {

    }
}

```
为了方便观察构造函数执行顺序，我将 Context 改成了 String
```
open class View {
    constructor(ctx: String) {

    }

    constructor(ctx: String, attr: AttributeSet?) {
        println(3)
    }
}

class MyButton : View {
    constructor(ctx: String) : this(ctx, null) {
        println(1)
    }

    constructor(ctx: String, attr: AttributeSet?) : super(ctx, attr) {
        println(2)
    }
}
```
打印结果为：3 2 1。可以看出，这种行为是与 Java 在构造方法中调用 super 是类似的。

### 实现在接口中声明的属性
在 Kotlin 中，接口可以包含抽象属性声明。
```scala
interface User {
    val nickname: String
    // 实现 User 接口的类需要提供一个取得 nickname 值的方式
}
class PrivateUser(override val nickname: String) : User //主构造方法属性 

class SubscribingUser(val email: String) : User {
    override val nickname: String
        get() = email.substringBefore('@')// 自定义 getter
}

class FacebookUser(val accountId: Int) : User {
    override val nickname = getFacebookName(accountId)// 属性初始化
}
```

除了抽象属性声明外，接口还可以包含具有 getter 和 setter 的属性，只要它们没有引用一个支持字段（支持字段需要在接口中存储状态，而这时不允许的）。
```scala
interface User {
    val email: String
    val nickname: String
        get() = email.substringBefore('@')
}
```

### 通过 getter 或 setter 访问支持字段
```scala
class User(val name: String) {
    var address: String = "unspecified"
        set(value: String) {
            println("""
                Address was changed for $name:
                "$field" -> "$value".""".trimIndent())
            field = value // 在 sette 的函数体中，使用了特殊的标识符 field 来访问 
        }
}

fun main(args: Array<String>) {
    val user = User("Alice")
    user.address = "Elsenheimerstrasse 47, 80687 Muenchen"
}
```
输出：
Address was changed for Alice:
"unspecified" -> "Elsenheimerstrasse 47, 80687 Muenchen".
> backing fields：支持字段（这翻译感觉有点怪），是由 Kotlin 自动生成的。一个类在 Kotlin 中是不能有 field 的，val 和 var 声明的是属性，它们具有 getter 或 setter 访问器。但是，在使用自定义的访问器时有可能需要 backing field。  
> 在上面的代码中，如果将 field 直接改为 address，IDE 会提示错误，因为属性的赋值是通过 setter 来进行的，这样就导致了死循环。这也是为什么需要 backing field。  

### 修改访问器的可见性
```scala
class LengthCounter {
    var counter: Int = 0
        private set

    fun addWord(word: String) {
        counter += word.length
    }
}
```

## 编译器生成的方法：数据类和类委托
### 通用对象方法
> 在 Kotlin 中，== 运算符是比较两个对象的默认方式：本质上说它就是通过调用 equals 来比较两个值的。想要进行引用比较，可以使用 === 运算符，这与 Java 中的 == 比较对象引用的效果一模一样。  
```scala
class Client(val name: String, val postalCode: Int) {
    override fun equals(other: Any?): Boolean {
        if (other == null || other !is Client)
            return false
        return name == other.name &&
               postalCode == other.postalCode
    }
    override fun hashCode(): Int = name.hashCode() * 31 + postalCode
    override fun toString() = "Client(name=$name, postalCode=$postalCode)"
}
```
> 完成这一切太过于繁琐。。  

### 数据类：自动生成通用方法的实现
```scala
data class Client(val name: String, val postalCode: Int)
```
equals 和 hashCode 方法会将所有在主构造方法中声明的属性纳入考虑。
> equals、hashCode、toString 并不是 data 类生成有用方法的完整列表。  
> 注意，数据类的属性并没有要求是 val，但还是强烈推荐只使用只读属性，让数据类的实例不可变。
> 为了让使用不可变对象的数据类变得更容易，Kotlin 编译器为它们多生成了一个方法：一个允许 copy 类的实例的方法，并在 copy 的同时修改某些属性的值。

### 类委托：使用“by”关键字
设计大型面向对象系统的一个常见问题是由继承的实现导致的脆弱性。当你扩展一个类并重写某些方法时，你的代码被变得依赖你自己继承的那个类的实现细节了。当系统不断演进并且基类的实现被修改或者新方法被添加进去时，你做出的关于类行为的假设会失败，所以你的代码也许最后就以不正确的行为而告终。
Kotlin 默认将类视作 final，这确保了只有那些设计成可扩展的类可以被继承。但是有时候仍需要向其他类中添加一些行为，即使它没有被设计为可扩展。一个常用的实现方式以装饰器模式闻名。这种模式的本质就是创建一个新类，实现与原始类一样的接口并将原来的类的实例作为一个字段保存。与原始类拥有同样行为的方法不用被修改，只需要直接转发到原始类的实例。这种方式的一个缺点是需要相当多的样板代码。
在 Kotlin 中，可以使用 by 关键字将接口的实现委托给另一个对象，编译器会自动生成类中所有的方法实现。
```scala
class CountingSet<T>(
        val innerSet: MutableCollection<T> = HashSet<T>()
) : MutableCollection<T> by innerSet {

    var objectsAdded = 0

    override fun add(element: T): Boolean {
        objectsAdded++
        return innerSet.add(element)
    }

    override fun addAll(c: Collection<T>): Boolean {
        objectsAdded += c.size
        return innerSet.addAll(c)
    }
}
```


## “object” 关键字：将声明一个类与创建一个实例结合起来
object 核心理念：这个关键字定义一个类并同时创建一个实例。
使用场景：
* object 声明是定义单例的一种方式
* companion object 伴生对象可以持有工厂方法和其他这个类相关，但在调用时并不依赖类实例的方法。它们的成员可以通过类名为访问。
* object 表达式用来替代 Java 的匿名内部类。

### object 声明：创建单例
与类一样，一个 object  声明也可以包含属性、方法、初始化语句块等的声明。唯一不允许的就是构造方法（包含主构造方法和从构造方法）。
```scala
object CaseInsensitiveFileComparator : Comparator<File> {
    override fun compare(file1: File, file2: File): Int {
        return file1.path.compareTo(file2.path,
                ignoreCase = true)
    }
}
```
> 在 Java 中调用：CaseInsensitiveFIleComparator.INSTANCE.compare(file, file2;  

### companion 对象：工厂方法和静态成员
Kotlin 中的类不能拥有静态成员。使用 companion 关键字可以实现类似于 static 的功能。
```scala
class A {
    companion object {
        fun bar() {
            println("Companion object called")
        }
    }
}

fun main(args: Array<String>) {
    A.bar()
}
```
companion object 可以访问类中的所有 private 成员，包括 private 构造方法，它是实现工厂模式的理想选择。
```scala
class User private constructor(val nickname: String) {
    companion object {
        fun newSubscribingUser(email: String) =
            User(email.substringBefore('@'))

        fun newFacebookUser(accountId: Int) =
            User(getFacebookName(accountId))
    }
}

fun main(args: Array<String>) {
    val subscribingUser = User.newSubscribingUser("bob@gmail.com")
    val facebookUser = User.newFacebookUser(4)
    println(subscribingUser.nickname)
}
```

### 作为普通对象使用的 companion object
Companion object 是一个声明在类中的普通对象。它可以有名字，实现一个接口或者有扩展函数或属性。默认名字为 Companion。

### object 表达式：改变写法的匿名内部类
```scala
window.addMouseListener (
    object:MouseAdapter(){
        override fun mouseCLicked(e: MouseEvent) {
            
        }
        
        override fun mouseEntered(e: MouseEvent) {
            
        }
    })
```

与 Java 匿名内部类只能扩展一个类或实现一个接口不同，Kotlin 的匿名对象可以实现多个接口或者不实现接口。与 Java 的匿名类一样，在 object 表达式中的代码可以访问创建它的函数中的变量。但是与 Java 不同，访问并没有被限制为 final 变量，还可以在 object 表达式中修改变量的值。