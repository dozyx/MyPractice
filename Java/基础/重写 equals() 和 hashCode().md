### 复写 equals()

#### 什么时候需要复写

+ 类具有自己特有的“逻辑相等”概念（不同于对象相等）
+ 超类没有覆盖 equals 以实现期望的行为



#### 实现 equals 方法

+ 使用 “==” 检查 “参数是否为这个对象的引用”，如果是，则返回 true
+ 使用 instanceof 检查 “参数是否为正确的类型”，如果不是，返回 false
+ 将参数转换为正确的类型
+ 对于该类中的每个 “关键” 域，检查参数中的域是否与该对象中对应的域相匹配    
  对于既不是 float 也不是 double 类型的基本类型，可以使用 “==” 进行比较；对于对象引用域，可以递归地调用 equals 方法；对于 float 域，可以使用 Float.compare 方法；对于 double 域，则使用 Double.compare。float 和 double 的处理是因为考虑到 Float.NaN、-0.0f 以及类似的 double 常量。如 0.0 与 -0.0 在使用 “==” 比较时，前者与后者相等，但使用 Float.compare 时，前者大于后者，具体说明 Float.equals 文档（这样设计的目的应该是为了更符合自然排序）。对于数组域，则要把以上的指导原则应用到每个元素上，如果数组域中的每个元素都很重要，可以使用 Arrays.equals 方法。



### 复写 hashCode

> 每个覆盖了 equals 方法的类中，也必须覆盖 hashCode 方法。如果不这样做的话,就会违反 Object.hashCode 的通用约定，从而导致该类无法与所有基于 hash 的集合一起工作，如 HashMap、HashSet、Hashtable。

下面是约定的内容（JavaSE6）：

+ 只要对象 equals 方法的比较操作所用到的信息没有被修改，那么对该对象调用多次 hashCode 方法都必须返回同一个整数。
+ 相等的对象必须具有相等的 hash code。
+ 如果两个对象的 equals 方法比较是不相等的，那么两个对象的 hashCode 方法不一定要产生不同的整数结果。但给不相等对象产生截然不同的整数结果，有可能提高 hash table 的性能。



### 如何生成 hash code

一个好的散列函数通常倾向于“为不相等的对象产生不相等的散列码”，理想情况下，散列函数应该把集合中不相等的实例均匀地分布到所有可能的散列值上。下面是相对接近于这种理想情形的简单方法：

1. 指定一个非零常数值，比如 17，保存到一个 int 类型的变量 result 中
2. 对于对象中的每个关键域 f（指 equals 方法中涉及的每个域），完成以下步骤：
   + 为该域计算 int 类型的散列码 c：
     + boolean 类型，计算 (f ? 1 : 0)
     + byte、char、short或int类型，计算 (int)f
     + long 类型，计算 (int)(f^(f >>> 32))
     + float 类型，计算 Float.floatToIntBits(f)
     + double 类型，计算 Double.doubleToLongBits(f)，然后再按 long 类型计算
     + 对象引用，并且类的 equals 通过递归调用 equals 的方法来比较该域，那么可以为该域递归地调用 hashCode
     + 数组，把每一个元素当做单独的域来处理，如果数组域中每个元素都很重要，可以使用 Arrays.hashCode 方法
   + 按下面公式将上面计算的散列码 c 合并到 result 中：result = 31 * result + c
3. 返回 result



如一个 PhoneNumber 类的 hashCode 方法：

```java
@Override public int hashCode() {
	int result = 17;
	result = 31 * result + areaCode;
	result = 31 * result + prefix;
	result = 31 * result + lineNumber;
	return result;
}
```

如果计算散列码的开销很大，那么可以考虑把散列码缓存在对象内部：

```java
// Lazily initialized, cached hashCode
private volatile int hashCode; // (See Item 71)
@Override public int hashCode() {
	int result = hashCode;
	if (result == 0) {
		result = 17;
		result = 31 * result + areaCode;
		result = 31 * result + prefix;
		result = 31 * result + lineNumber;
		hashCode = result;
	}
	return result;
}
```



参考：    

《Effective Java 第2版》    
​	第 8 条 覆盖 equals 时请遵守通用约定    
​	第 9 条 覆盖 equals 时总要覆盖 hashCode
