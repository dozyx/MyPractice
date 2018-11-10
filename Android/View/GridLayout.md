GridLayout 继承于 ViewGroup

### 属性

#### GridLayout 直接属性

```xml
<declare-styleable name="GridLayout">
        <!-- 添加子视图的方向。比如水平情况下，columnCount 属性让该行添加满后创建新的行来添加视图，注意，如果创建的行数超过了 rowCount，仍会继续增加行数。-->
        <attr name="orientation" />
        <!-- 最大行数 -->
        <attr name="rowCount" format="integer" />
        <!-- 最大列数-->
        <attr name="columnCount" format="integer" />
        <!-- 当子视图没有指定时，是否使用默认的 margin，默认为false。比如，子 View 指定了 layout_marginTop 为 0dp，即使此属性为 true，仍不会使用默认 margin，但在测试中发现，如果是将子 View 的 layout_margin 设置为 0dp，并且该属性为 true，此时将使用默认 margin。
		When set to true, tells GridLayout to use default margins when none are specified
        in a view's layout parameters.
        The default value is false.
        See {@link android.widget.GridLayout#setUseDefaultMargins(boolean)}.-->
        <attr name="useDefaultMargins" format="boolean" />
        <!-- 子 View 之间进行对齐时，是与相同索引的 view 的边界还是 margin 的边界（即 margin 的起点）对齐。默认为alignMargins。-->
        <attr name="alignmentMode" />
        <!-- 是否强制使行的边界与行的索引顺序一致。
		When set to true, forces row boundaries to appear in the same order
        as row indices.
        The default is true.
        See {@link android.widget.GridLayout#setRowOrderPreserved(boolean)}.-->
        <attr name="rowOrderPreserved" format="boolean" />
        <!-- When set to true, forces column boundaries to appear in the same order
        as column indices.
        The default is true.
        See {@link android.widget.GridLayout#setColumnOrderPreserved(boolean)}.-->
        <attr name="columnOrderPreserved" format="boolean" />
    </declare-styleable>
```

columnOrderPreserved 属性进一步说明：该属性为 true 是，GridLayout 将强制增加列的边界，这样相关的网格的索引将以升序呈现。如果为 false，GridLayout 可以以**约束条件下**最合适的顺序自由的放置水平列的边界。

```java
	/**
     * When this property is {@code true}, GridLayout is forced to place the column boundaries
     * so that their associated grid indices are in ascending order in the view.
     * <p>
     * When this property is {@code false} GridLayout is at liberty to place the horizontal column
     * boundaries in whatever order best fits the given constraints.
     * <p>
     * The default value of this property is {@code true}.
     *
     * @param columnOrderPreserved use {@code true} to force GridLayout to respect the order
     *        of column boundaries.
     *
     * @see #isColumnOrderPreserved()
     *
     * @attr name android:columnOrderPreserved
     */
    public void setColumnOrderPreserved(boolean columnOrderPreserved) {
        mHorizontalAxis.setOrderPreserved(columnOrderPreserved);
        invalidateStructure();
        requestLayout();
    }
```



#### GridLayout 子视图属性

```xml
<declare-styleable name="GridLayout_Layout">
        <!-- 该 View 位于哪一行，不能超过最大行数。会影响其后的 View 的摆放。
		The row boundary delimiting the top of the group of cells
        occupied by this view. -->
        <attr name="layout_row" format="integer" />
        <!-- 该 View 跨越多少行，默认为 1。 -->
        <attr name="layout_rowSpan" format="integer" min="1" />
        <!-- 与 LinearLayout 的 weight 类似，确定所占空余空间的比例
		The relative proportion of vertical space that should be allocated to this view
        during excess space distribution. -->
        <attr name="layout_rowWeight" format="float" />
        <!-- 该 View 位于哪一行 -->
        <attr name="layout_column" />
        <!-- 该 View 跨越多少列。 -->
        <attr name="layout_columnSpan" format="integer" min="1" />
        <!-- The relative proportion of horizontal space that should be allocated to this view
        during excess space distribution. -->
        <attr name="layout_columnWeight" format="float" />
        <!-- 在格子内如何放置该 View。默认为 LEFT | BASELINE。
		Gravity specifies how a component should be placed in its group of cells.
        The default is LEFT | BASELINE.
        See {@link android.widget.GridLayout.LayoutParams#setGravity(int)}. -->
        <attr name="layout_gravity" />
    </declare-styleable>
```





### 实践

#### 使每列高度一致

原理：将子 View 的宽设为 0，然后设置 layout_columnWeight 为 1。

除了在 xml 中设置属性，也可以在代码中添加：

```java
GridLayout.LayoutParams layoutParams = new GridLayout.LayoutParams(GridLayout.spec(GridLayout.UNDEFINED, 1f),
                GridLayout.spec(GridLayout.UNDEFINED, 1f));
        layoutParams.width = 0;
```

