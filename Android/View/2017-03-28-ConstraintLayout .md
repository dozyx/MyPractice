---
title: ConstraintLayout 学习
tags:
  - android
date: 2017-03-28 15:37:22
categories: 笔记
---

[ConstraintLayout](https://developer.android.com/reference/android/support/constraint/ConstraintLayout.html)

[现在能用 ConstraintLayout 做些什么？](https://realm.io/cn/news/constraintlayout-it-can-do-what-now/)

java.lang.Object
   ↳	android.view.View
 	   ↳	android.view.ViewGroup
 	 	   ↳	android.support.constraint.ConstraintLayout



ConstraintLayout，约束布局。

目前可使用的约束条件有：

+ Relative positioning
+ Margins
+ Centering positioning
+ Visibility behavior
+ Dimension constraints
+ Chains
+ Virtual Helpers objects



## 约束条件

### Relative positioning

​	相对定位的约束条件可以使一个widget相对于另一个widget进行放置。

​	可用约束：

- `layout_constraintLeft_toLeftOf`
- `layout_constraintLeft_toRightOf`
- `layout_constraintRight_toLeftOf`
- `layout_constraintRight_toRightOf`
- `layout_constraintTop_toTopOf`
- `layout_constraintTop_toBottomOf`
- `layout_constraintBottom_toTopOf`
- `layout_constraintBottom_toBottomOf`
- `layout_constraintBaseline_toBaselineOf`
- `layout_constraintStart_toEndOf`
- `layout_constraintStart_toStartOf`
- `layout_constraintEnd_toStartOf`
- `layout_constraintEnd_toEndOf`

![relative-positioning-constraints](https://ws3.sinaimg.cn/large/006tKfTcgy1fizao2sxo6j30fy04b74i.jpg)

> 这些属性接受的是一个引用id或者*parent*（指向父容器）。以layout_constraintLeft_toLeftOf为例进行说明，第一个Left表示该widget的left位置，第二个left表示另一个widget的left，该属性指定的是一个widget左边位置与另一个widget的左边位置对齐。



### Margins

![relative-positioning-margin](https://ws1.sinaimg.cn/large/006tKfTcgy1fizao1y8o8j30df03zaa3.jpg)

普通的margin属性：

- `android:layout_marginStart`
- `android:layout_marginEnd`
- `android:layout_marginLeft`
- `android:layout_marginTop`
- `android:layout_marginRight`
- `android:layout_marginBottom`

> margin只能为正数或零。



#### Margins when connected to a GONE widget

​	当约束的target的可见性为GONE时，使用另外的margin属性：

- `layout_goneMarginStart`
- `layout_goneMarginEnd`
- `layout_goneMarginLeft`
- `layout_goneMarginTop`
- `layout_goneMarginRight`
- `layout_goneMarginBottom`



### Centering positioning and bias

以下代码将使button居中

```xml
<android.support.constraint.ConstraintLayout ...>
             <Button android:id="@+id/button" ...
                 app:layout_constraintLeft_toLeftOf="parent"
                 app:layout_constraintRight_toRightOf="parent/>
         </
```

![centering-positioning](https://ws4.sinaimg.cn/large/006tKfTcgy1fizao7gkjaj30bp02pjrd.jpg)

#### Bias

​	上面的约束可以使widget居中，但通过bias属性可以使widget偏向一边：

- `layout_constraintHorizontal_bias`

- `layout_constraintVertical_bias`

  示例代码：

```xml
<android.support.constraint.ConstraintLayout ...>
             <Button android:id="@+id/button" ...
                 app:layout_constraintHorizontal_bias="0.3"
                 app:layout_constraintLeft_toLeftOf="parent"
                 app:layout_constraintRight_toRightOf="parent/>
         </>
```

![centering-positioning-bias](https://ws1.sinaimg.cn/large/006tKfTcgy1fizao7enbbj30bp02pjrd.jpg)

> 此控件是水平居中，所以只能进行水平的偏向，此时设置layout_constraintVertical_bias将无效。



### Visibility behavior

​	当widget被标记为`View.GONE`时，ConstraintLayout会有特殊的处理。通常，widget变为GONE后，将不会显示并且不再是布局的一部分。但根据布局计算，GONE的widget仍然是其中的一部分，只是有一个重大的区别：

+ 在布局传递中，它们的尺寸将被当作零（根本上来说，它们将被视为一个点）
+ 如果它们与其它widget间有约束，它们仍会被考虑，但它们的margin会被视作零![visibility-behavior](https://ws3.sinaimg.cn/large/006tKfTcgy1fizao8iyenj30f007at8z.jpg)。

> 可以通过设置gone的margin属性来确保在A变为gone时，B到left间的margin与A保持一致。



### Dimensions constraints

#### 最小尺寸

- `android:minWidth` 
- `android:minHeight` 



#### Widgets dimension constraints

​	widget的尺寸可以通过设置`android:layout_width`和`android:layout_height`属性来指定，使用方式有三种：

+ 使用具体的尺寸大小（如123dp或Dimension引用）
+ 使用WRAP_CONTENT
+ 使用0dp，等同于`MACTH_CONSTRAINT`

![dimension-match-constraints](https://ws2.sinaimg.cn/large/006tKfTcgy1fizao6vvfaj30d6099mxk.jpg)

​	前两种方式与其它布局一致。第三种将调整widget的大小来匹配设置的约束条件。上图中，(a)为wrap_content，(b)为0dp，(c)为设置了margin的情形。

> 重要：ConstraintLayout中的widget不支持MATCH_PARENT。



#### Ratio

​	我们可以按照某一边的比例来设置widget的另一边，实现此效果的前提是至少有一边的尺寸为0dp，然后通过属性`layout_constraintDimentionRatio` 来指定比例，如

```xml
<Button android:layout_width="wrap_content"
                   android:layout_height="0dp"
                   app:layout_constraintDimensionRatio="1:1" />
```

​	上面代码将使button的height与width大小一样。

​	ratio可以使用以下形式：

+ float值
+ “width：height”形式

  ​也可以将所有的尺寸均指定为`MATCH_CONSTRAINT`(0dp)，这种情况下，系统将设置满足所有约束条件的最大尺寸并保持指定的横纵比。可以通过添加W或H来设置指定约束的边，使约束边基于另一边的尺寸来变化。

  ​如：

```xml
<Button android:layout_width="0dp"
                   android:layout_height="0dp"
                   app:layout_constraintDimensionRatio="H,16:9"
                   app:layout_constraintBottom_toBottomOf="parent"
                   app:layout_constraintTop_toTopOf="parent"/>
```

​	上面代码将根据16:9来设置button的height，而button的width将匹配parent的约束条件。

> width和height同时为0dp时不太好理解，上面代码的效果是button的height等于parent的height，而button的width为button的height的9/16。个人理解：当值前面带有H或W时，不能简单地将后面的比例作为width：height，而是更应该当作一个float值，H或W表示将要进行约束的边，如为H时，H=16/9 * W，即W=H * 9/16；而为W时，W = 16/9 * H。



### Chains

​	chains可以在某一轴实现group-like效果，而另一轴仍可以单独地约束。

> 想象每一个约束都有一个箭头从一个widget指向另一个widget，当这些箭头出项双向时便形成了一条链。

#### Creating a chain

​	几个widget之间如果是双向连接，则可视为一个链。![chains](https://ws1.sinaimg.cn/large/006tKfTcgy1fizao82t3hj30hi04uaac.jpg)

#### Chain heads

​	chain由第一个元素的属性进行控制。

![chains-head](https://ws2.sinaimg.cn/large/006tKfTcgy1fizao3lx7cj30ph03rjrq.jpg)

#### Margins in chains

​	连接中指定的margin将会被处理。



#### Chain Style

​	设置chain的第一个元素的`layout_constraintHorizontal_chainStyle` 或者 `layout_constraintVertical_chainStyle`属性，chain的行为将会根据指定的style改变（默认为CHAIN_SPREAD）。

+ CHAIN_SPREAD

  默认，元素会铺开

+ Weighted chain

  CHAIN_SPREAD模式下，如果有widget设置了`MATCH_CONTRAINT`，它们将切割可用空间。

+ CHAIN_SPREAD_INSIDE：最后的端点不会被铺开

+ CHAIN_PACKED：chain中的元素挤在一起。![chains-styles](https://ws4.sinaimg.cn/large/006tKfTcgy1fizao5jib1j31200h4whb.jpg)



##### Weighted chains

​	默认的chain会将元素按可用空间等距地铺开，如果一个或多个元素使用了MATCH_CONSTRAINT，它们将使用空的可用空间（平等分配）。属性`layout_constraintHorizontal_weight` 和 `layout_constraintVertical_weight`可以用来控制使用了MATCH_CONSTRAINT的元素如何分配空间。



### Virtual Helper objects

​	目前，Guideline对象可以可以创建相对于ConstraintLayout容器的水平和垂直guideline。widget可以通过对这些guideline的约束来放置。



## Guideline

​	代表了用于ContraintLayout的Guideline辅助对象（helper object）的工具类。Helper objects不会在设备中显示（被标记为View.GONE），并且只以布局为目的，这些对象只能用于ConstraintLayout。

​	Guideline可以为水平或者垂直：

+ 垂直Guideline的width为零，height为它们的父ConstraintLayout
+ 水平Guideline的height为零，width为它们的父ConstraintLayout

  ​有三种定位到Guideline的可能方式:

+ 指定一个到left或top的固定距离（layout_constraintGuide_begin）
+ 指定一个到right或bottom的固定距离（layout_constraintGuide_end）
+ 指定一个width或height的百分比（layout_constraintGuide_percent）

  ​示例：

```xml
<android.support.constraint.ConstraintLayout
        xmlns:android="http://schemas.android.com/apk/res/android"
        xmlns:app="http://schemas.android.com/apk/res-auto"
        xmlns:tools="http://schemas.android.com/tools"
        android:layout_width="match_parent"
        android:layout_height="match_parent">

    <android.support.constraint.Guideline
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:id="@+id/guideline"
            app:layout_constraintGuide_begin="100dp"
            android:orientation="vertical"/>

    <Button
            android:text="Button"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:id="@+id/button"
            app:layout_constraintLeft_toLeftOf="@+id/guideline"
            android:layout_marginTop="16dp"
            app:layout_constraintTop_toTopOf="parent" />

</android.support.constraint.ConstraintLayout>
```

> Guideline相当于创建一个布局用的基准线，android:orientation用于指定guideline的方向，如当其为vertical时，guideline的width为0，height等于ConstraintLayout的height，示例中设置了app:layout_constraintGuide_begin="100dp"，那么button的left将与100dp处对齐。









