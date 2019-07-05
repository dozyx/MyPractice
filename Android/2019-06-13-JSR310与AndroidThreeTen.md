JSR-310 使用 `Date` 和 `Calendar` 的替代品，Java8 已经完全实现了 JSR-310，package 为 `java.time.*`，在 Android 中如果需要使用需要 min sdk 为 26 以上。[ThreeTenABP](https://github.com/JakeWharton/ThreeTenABP) 是实现了 JSR-310 的一个库，可以兼容到 Java6。

> 之前我一直都是用的 Date 和 Calendar，需要有一些不爽，但也没想过换掉，但多次在一些开源项目中注意到 ThreeTenABP，于是学习一番。如果想要了解下 Date 和 Calendar 有什么不爽，可以查看[这篇文章](https://blog.csdn.net/jerome_s/article/details/45285645)。

ThreeTenABP 的 API 与 Java8 里 JSR-310 的实现的 API 基本一致，主要的类：

* LocalDate：没有时区的日期，如 `2007-12-03`
* LocalDateTime：没有时区的日期时间，如 `2007-12-03T10:15:30`
* LocalTime：没有时区的时间，如 `22:10:26.846`
* MonthDay：月日，如：`--06-13`
* Instant：时间线上的瞬时点
* Duration：基于时间的时间量
* Clock：使用时区提供当前时刻、日期和时间的时钟
* ...



### 使用

> 等到实际应用到项目中再补充







参考：

[ThreeTenABP](https://github.com/JakeWharton/ThreeTenABP)