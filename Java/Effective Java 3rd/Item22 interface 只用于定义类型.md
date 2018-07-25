当一个 class 实现了一个 interface，该 interface 将被视为一个可以指向该 class 实例的 type。因此，实现一个 interface 应该表示的是客户端使用该实例能做的事情，出于其他目的来定义一个 interface 都是不可取的。

constant interface 就是一种违反这种用法的方式。如：

```java
// Constant interface antipattern - do not use!
public interface PhysicalConstants {
// Avogadro's number (1/mol)
static final double AVOGADROS_NUMBER = 6.022_140_857e23;
// Boltzmann constant (J/K)
static final double BOLTZMANN_CONSTANT = 1.380_648_52e-23;
// Mass of the electron (kg)
static final double ELECTRON_MASS = 9.109_383_56e-31;
}
```

constant interface 模式是一种糟糕的 interface 使用方式。

+ 一个 class 内部使用某些常量属于实现细节，而实现一个常量 interface 导致该实现细节被 class 的公开 API 泄露。
+ claas 实现了某个 constant interface，这对于类的使用者来说是无关紧要的，还可能造成困扰。
+ 更糟糕的是，它是一种保证，如果以后 class 在某个 release 中被修改，不再需要使用这些常量，但是，它仍然需要实现该 interface来确保 binary compatibility。
+ 如果一个 nonfinal 类实现了一个 constant interface，它所有的子类的命名空间都会被 interface 中的常量所污染（polluted）。（ps：可以直接通过该类名来访问常量）

在 Java 平台库中也有几个 constant interface，如 `java.io.ObjectStreamConstants`。这些 interface 应被视作反常，并且不应模仿。

如果需要公开常量，这里有几种可选方式：

+ 如果常量与 class 或者 interface 是强关联的，就应该将他们放到 class 或 interface 中。

+ 如果常量作为枚举类型的成员会更为直观，就应该将常量通过 enum 类型来公开。（ps：之前看的一些资料会推荐尽量不要在 Android 中使用 enum，所以用或不用还是需要慎重考虑，不能滥用）

+ 还可以将常量通过一个不可实例化的工具类来公开。如：

  ```java
  // Constant utility class
  package com.effectivejava.science;
  public class PhysicalConstants {
  private PhysicalConstants() { } // Prevents instantiation
  public static final double AVOGADROS_NUMBER = 6.022_140_857e23;
  public static final double BOLTZMANN_CONST = 1.380_648_52e-23;
  public static final double ELECTRON_MASS = 9.109_383_56e-31;
  }
  ```

  顺带提下，上面的数字字面量中使用了下划线，这是在 Java7 中加入的，它对数字字面量的值不会有任何影响，不过可以提高数字的可读性。

  总之，interface 只能用于定义 type。它们不应被用来公开 constant。







参考：

[What is binary compatibility in Java?](https://stackoverflow.com/questions/14973380/what-is-binary-compatibility-in-java)