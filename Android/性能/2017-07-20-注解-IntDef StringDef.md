---
title: IntDef 和 StringDef
tags:
  - android
  - 注解
date: 2017-07-20 15:37:22
categories: 笔记
---

[Android 性能：避免在Android上使用ENUM](http://blog.csdn.net/ysmintor_/article/details/69788931)

[Android Performance: Avoid using ENUM on Android](https://android.jlelse.eu/android-performance-avoid-using-enum-on-android-326be0794dc3)

[IntDef](https://developer.android.com/reference/android/support/annotation/IntDef.html)

[StringDef](https://developer.android.com/reference/android/support/annotation/StringDef.html)

[深入浅出Android Support Annotations](https://asce1885.gitbooks.io/android-rd-senior-advanced/content/shen_ru_qian_chu_android_support_annotations.html)



public abstract @interface IntDef 
implements Annotation

------

### IntDef 和 StringDef

​	IntDef 和 StringDef 位于 annotation 支持库中，通常处于性能考虑而用来替代 enum。IntDef 用来表示代表逻辑类型的整型注解元素，并且它的值必须为显式命名的常量。如果 IntDef#flag() 属性设为 true，常量将可以作为 flag 使用，即可以使用’｜’或者’&’进行与或等操作，而不仅是作为一个 enum (默认)。

​	示例：

```java
  @Retention(SOURCE)
  @IntDef({NAVIGATION_MODE_STANDARD, NAVIGATION_MODE_LIST, NAVIGATION_MODE_TABS})
  public @interface NavigationMode {}
  public static final int NAVIGATION_MODE_STANDARD = 0;
  public static final int NAVIGATION_MODE_LIST = 1;
  public static final int NAVIGATION_MODE_TABS = 2;
  ...
  public abstract void setNavigationMode(@NavigationMode int mode);
  @NavigationMode
  public abstract int getNavigationMode();
```

​	其中， @Retention(SOURCE) 表示该注解只存在于源代码中，编译时将忽略。

​	设置 flag 属性：

```java
 @IntDef(
      flag = true,
      value = {NAVIGATION_MODE_STANDARD, NAVIGATION_MODE_LIST, NAVIGATION_MODE_TABS})
```

​	StringDef 与 IntDef 类似，示例：

```java
  @Retention(SOURCE)
  @StringDef({
     POWER_SERVICE,
     WINDOW_SERVICE,
     LAYOUT_INFLATER_SERVICE
  })
  public @interface ServiceName {}
  public static final String POWER_SERVICE = "power";
  public static final String WINDOW_SERVICE = "window";
  public static final String LAYOUT_INFLATER_SERVICE = "layout_inflater";
  ...
  public abstract Object getSystemService(@ServiceName String name);
```



### enum 的性能问题

​	enum 中的每一个常量都是一个对象，它的每个声明都会占用运行时的部分内存以便能够引用到这个对象。因此 enum 会比采用 Integer 或 String 的方式占用更多的内存。

​	添加一个ENUM将会增大最终的DEX文件（Integer常量的13倍大）。并且会引起运行时的过度开销，你的应用也会占用更多的空间。因此**过度在android开发中使用ENUM将会增大DEX大小，并会增大运行时的内存分配大小**。(纯复制，罪过。。。)

​	为了解决 enum 的性能问题，同时避免单纯的 int 或 String 易引入非法值的问题，可以采用 TypeDef 注解。使用 IntDef 和 StringDef 将可以确保返回值或参数只使用一组常量中的值。

#### 使用注解替代 enum 示例

（示例代码也是复制的，罪过。。。）

假如存在一个 ConstantSeason 类如下：

```java
 public class ConstantSeason {
    public static final int WINTER = 0;
    public static final int SPRING = 1;
    public static final int SUMMER = 2;
    public static final int FALL = 3;

    public ConstantSeason(int season) {
        System.out.println("Season :" + season);
    }

    public static void main(String[] args) {
        // Here chance to paas invalid value 
        ConstantSeason constantSeason = new ConstantSeason(5);
    }
}
```

该类无法确保用户使用正确的值，为此，将其改为 enum 的实现：

```java
public class EnumSeason {

    public EnumSeason(Season season) {
        System.out.println("Season :" + season);
    }

    public enum Season {
        WINTER, SPRING, SUMMER, FALL
    }

    public static void main(String[] args) {
        EnumSeason enumSeason = new EnumSeason(Season.SPRING);
    }
}
```

该类已经可以很好的工作，但为了解决性能问题，下面将使用注解来实现

首先，进行声明：

```java
// Constants
public static final int WINTER = 0;
public static final int SPRING = 1;
public static final int SUMMER = 2;
public static final int FALL = 3;

// Declare the @IntDef for these constants
@IntDef({WINTER, SPRING, SUMMER, FALL})
@Retention(RetentionPolicy.SOURCE)
public @interface Season {}
```

(@Retention(RetentionPolicy.SOURCE) 表示该注解在编译时将被忽略)

完整的实现类：

```java
public class AnnotationSeason {

    public static final int WINTER = 0;
    public static final int SPRING = 1;
    public static final int SUMMER = 2;
    public static final int FALL = 3;

    public AnnotationSeason(@Season int season) {
        System.out.println("Season :" + season);
    }

    @IntDef({WINTER, SPRING, SUMMER, FALL})
    @Retention(RetentionPolicy.SOURCE)
    public @interface Season {
    }

    public static void main(String[] args) {
        AnnotationSeason annotationSeason = new AnnotationSeason(SPRING);
    }
}
```

