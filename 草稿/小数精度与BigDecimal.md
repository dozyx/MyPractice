## 浮点数丢失精度问题

> 运行 `System.out.print(0.4 + 0.2);`，结果为 0.6000000000000001，计算机算错了吗？



## BigDecimail

注意事项：

+ BigDecimail 大多数操作方法都是返回一个新的 BigDecimail 实例，所以需要注意对新实例进行操作，而不是旧的实例

  ​

### rounding mode

在 BigDecimal 中定义了以下几种 rounding mode：

+ `BigDecimal.ROUND_UP`
+ `BigDecimal.ROUND_DOWN`
+ `BigDecimal.ROUND_CEILING`
+ `BigDecimal.ROUND_FLOOR`
+ `BigDecimal.ROUND_HALF_UP`
+ `BigDecimal.ROUND_HALF_DOWN`
+ `BigDecimal.ROUND_HALF_EVEN`
+ `BigDecimal.ROUND_UNNECESSARY`

关于它们的区别将在下面的例子中进行注释

```java
public class Test {
    public static void main(String[] args) {
        String value = "1.955";
        BigDecimal num;
        num = new BigDecimal(value);// 因为 setScale 将返回一个新的实例，所以每次都需要 new 一个新的
        num = num.setScale(2, BigDecimal.ROUND_UP);// 正数往正无穷取舍，负数往负无穷取舍
        System.out.println("BigDecimal.ROUND_UP -> " + num);
        num = new BigDecimal(value);
        num = num.setScale(2, BigDecimal.ROUND_DOWN);// 向零取舍
        System.out.println("BigDecimal.ROUND_DOWN -> " + num);
        num = new BigDecimal(value);
        num = num.setScale(2, BigDecimal.ROUND_CEILING);// ceiling 天花板，向正无穷大取舍
        System.out.println("BigDecimal.ROUND_CEILING -> " + num);
        num = new BigDecimal(value);
        num = num.setScale(2, BigDecimal.ROUND_FLOOR);// 向负无穷大取舍
        System.out.println("BigDecimal.ROUND_FLOOR -> " + num);
        num = new BigDecimal(value);
        num = num.setScale(2, BigDecimal.ROUND_HALF_UP);// 向最接近的进行取舍，四舍五入
        System.out.println("BigDecimal.ROUND_HALF_UP -> " + num);
        num = new BigDecimal(value);
        num = num.setScale(2, BigDecimal.ROUND_HALF_DOWN);// 向最接近的进行取舍，五将舍弃
        System.out.println("BigDecimal.ROUND_HALF_DOWN -> " + num);
        num = new BigDecimal(value);
        num = num.setScale(2, BigDecimal.ROUND_HALF_EVEN);// 向相邻的偶数取舍
        System.out.println("BigDecimal.ROUND_HALF_EVEN -> " + num);
        num = new BigDecimal(value);
        num = num.setScale(2, BigDecimal.ROUND_UNNECESSARY);
        // 断言请求的操作具有精确的结果,因此不需要舍入。如果使用该舍入模式将产生不精确的结果，
        // 那么将抛出ArithmeticException。如这里 scale 为 2 时将抛出异常，改为3后正常
        System.out.println("BigDecimal.ROUND_UNNECESSARY -> " + num);
    }
}
```



参考：

[代码之谜（五）- 浮点数（谁偷了你的精度？）](http://justjavac.com/codepuzzle/2012/11/11/codepuzzle-float-who-stole-your-accuracy.html)