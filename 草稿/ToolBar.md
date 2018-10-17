> 很久之前就了解过 Toolbar，不过一直没怎么实际使用，而且在公司项目中用的都是自定义的标题栏，突然好奇 Toolbar 的优势在哪，Toolbar 是否能完全地像自定义栏一样使用。

Toolbar 继承于 ViewGroup，所以理论上它是完全可以当做普通的 ViewGroup 进行使用的，但这样就失去了它的意义。Toolbar 除了可以取代传统的ActionBar，也可以放置在视图的任何位置，它包括了以下几个元素：

+ 一个导航按钮
+ 一个品牌logo图标
+ 一个标题和副标题
+ 一个或多个自定义view
+ 一个 ActionMenuView 操作菜单



## 自定义

### 修改导航图标

navigation button，即最右侧的图标，可以通过 `navigationIcon`  属性修改，需要注意，如果使用了 ActionBarDrawerToggle 的话将导致 xml 中定义的 navigationIcon 被覆盖修改，因为在构造 ActionBarDrawerToggle 时，会使用一个 DrawerArrowDrawable 作为 navigationIcon。

修改方法有以下几种：

1. 构建完 ActionBarDrawerToggle 后，在调用一次 Toolbar 的 setNavigationIcon()

2. 继承 DrawerArrowDrawable，实现自己的绘制，然后调用 ActionBarDrawerToggle 的 setDrawerArrowDrawable() 方法来修改。[参考](https://stackoverflow.com/questions/43881131/add-badge-counter-to-hamburger-navigation-menu-icon-in-android)
3. 使用 actionbar 的方法，具体见 [链接](https://stackoverflow.com/questions/39473404/how-to-change-hamburger-icon-in-android-navigationdrawer)。



### 居中标题

为 Toolbar 添加一个子 TextView 作为标题，重写 ToolBar 的 setTitle() 方法来设置标题，设置 TextView 的 layout_gravity 为居中。



### 修改右侧菜单按钮图标

调用 Toolbar 的 setOverflowIcon() 方法



### 在右侧添加文字

为 Toolbar 添加一个子 TextView，设置 layout_gravity 为 right。

> 一开始是考虑能否为右侧菜单按钮直接添加文字，但最后发现并不可行。
>
> Toolbar 右侧显示的是一个 ActionMenuView，其父类为 LinearLayoutCompat（即 LinearLayout，androidx 中名称为 LinearLayoutCompat），它包含了一个 OverflowMenuButton（父类为 AppCompatImageView！！），而且无法获取该 ActionMenuView 对象，所以没办法直接添加文字。



