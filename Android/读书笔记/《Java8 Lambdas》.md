[java-8-lambdas-exercises](https://github.com/RichardWarburton/java-8-lambdas-exercises)

## lambda 表达式
```java
Runnable noArguments = () -> System.out.println("Hello World");
```

`()` 表示无参数，该 lambda 表达式实现了一个 Runnable，它只有唯一的不接受参数且无返回类型的方法 run。

```java
ActionListener oneArgument = event -> System.out.println("button clicked");
```

lambda 表达式带一个参数。

```java
Runnable multiStatement = () -> {
	System.out.print("Hello");
	System.out.println(" World");
};
```

具有代码块 的 lamda 表达式，该代码块与普通写法一致，比如返回、抛出异常。

```java
BinaryOperator<Long> add = (x, y) -> x + y;
```

用于多于一个参数的方法。需要注意，表达式并没有将两个数相加，它只是创建了一个用于相加的方法，`add` 变量是一个 `BinaryOperator<Long>` 而不是两个数相加的结果。

```java
BinaryOperator<Long> addExplicit = (Long x, Long y) -> x + y;
```

有时候，最好显式写出类型。



### functional interfaces

函数接口，用作 lambda 表达式类型的只有单个抽象方法的 interface。



### type inference

类型推断：javac 查找与 lambda 表达式相关的信息，然后使用这些信息来断定正确的类型。如：

```java
Predicate<Integer> atLeast5 = x -> x > 5;
```



## Streams

Java 8中最重要的核心库变化是围绕 Collections API 的 streams。

一个普通的迭代：

```java
int count = 0;
for (Artist artist : allArtists) {
if (artist.isFrom("London")) {
	count++;
	}
}
```

将上面的代码展开后，实际为：

```java
int count = 0;
Iterator<Artist> iterator = allArtists.iterator();
while(iterator.hasNext()) {
	Artist artist = iterator.next();
	if (artist.isFrom("London")) {
		count++;
	}
}
```





## Java 8 的一些新特性

+  effectively final ：匿名内部类中是无法使用外部非 final 变量的，如果使用了外部没有 final 修饰的变量，那么这个变量将被认为是 effectively final 的，它只能被赋值一次。



