### 结构

TabLayout 继承于 HorizontalScrollView。它有且仅有一个子视图 SlidingTabIndicator。SlidingTabIndicator 继承于 LinearLayout，tab 将被添加在这个子视图中。每个 tab 对应一个 TabView，TabView 继承于 LinearLayout。

### 用法

布局使用：

```xml
    <com.google.android.material.tabs.TabLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        app:tabMode="fixed"
        app:tabGravity="center"
        android:paddingRight="15dp">

        <com.google.android.material.tabs.TabItem
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_marginLeft="20dp"
            android:text="" />

        <com.google.android.material.tabs.TabItem
            ... />

        <com.google.android.material.tabs.TabItem
            ... />
    </com.google.android.material.tabs.TabLayout>
```

### TabItem

TabItem 继承于 View，但它并没有被当做一个实际的 View 来使用，只是用于在布局中添加 tab 并记录信息。TabItem 保存的信息有三个，分别对应着三个属性：

* `android:text`
* `android:icon`
* `android:layout`

在 addView 的时候，这三个信息会保存在 Tab 这个内部类中。



### Tab

tab 的相关信息都保存在这个类中。Tab 中有一个 `TabView` 的 field 来作为实际显示的 view，TabView 继承于 LinearLayout，它的 orientation 与 `tabInlineLabel` 属性有关系，tabInlineLabel 为 true 时，方向是 HORIZONTAL。

Tab 本身支持有一个 icon 和一个 text。设置 tabInlineLabel 可以控制 icon 是在 text 的上边还是左边。

它们对应的布局文件分别为：

- `design_layout_tab_icon`
- `design_layout_tab_text`

查看这两个文件和源码，可以发现 icon 的大小是固定的，而 text 的 appearance 可以通过 `tabTextAppearance`设置。

在 TabItem 里可以看到还有一个 layout 信息，通过使用这个信息，可以实现 tab 布局的完全自定义。我们可以在 `android:layout` 指定的布局中设置 id 为 `android.R.id.text1` 和 `android.R.id.icon` 的两个 view 来作为 text 和 icon 的显示。我们还可以在布局中添加更多的 view。

> 注意：自定义布局的 text 不会应用 tabTextAppearance。



### 自定义使用

#### 修改 tab 的 padding

TabLayout 提供了对应的属性修改



#### 改变 Tab 的布局

为 TabItem 设置 `android:layout` 属性。只要在自定义布局中提供  `android.R.id.text1` 和 `android.R.id.icon`  两个 id 的 view，那么仍可使用原有的 text 和 icon 信息。



#### 结合 ViewPager 使用，TabItem 会无效

如果使用 ViewPager 时，要修改 tab 的布局，需要在 setupWithViewPager 之后，遍历 tab，然后调用 Tab#setCustomView 方法设置自定义布局。