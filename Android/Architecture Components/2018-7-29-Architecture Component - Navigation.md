

> 思考：  
> navigation 可以用来实现单 Activity 多 Fragment（并不是指一个 app 只有一个 Activity，而是主要为 Fragment，Activity 仅作为容器使用）？  
> Fragment 之间如何传递数据？  
> 如果一次性回退栈中多个 Fragment，类似于 Activity 的 singleTask？  
> 子 Fragment？  
> 普通写法的 Fragment 与 navigation 中的 Fragment 是否有区别？如果有区别，如何相互转化?  
> app 变得复杂后，Fragment 之间的指向是否会变得很乱？  
> 不同 module 的 Fragment ？组件化？  


## 导航原则
应用内导航的目标应当是为用户提供连贯并且可预知的体验。
+ 应用应该有一个固定的起点：该地点是用户从 launcher 启动应用的页面，同时也是用户点击返回键回到 launcher 前的一个最后页面。
+ 使用 stack （先进先出）来表示应用的“导航状态”
+ up 按钮永远不会退出应用
+ up 和返回键是等价的
+ 使用 deep link 到达一个目的地或者导航到一个目的地，应当有相同的栈
	+ 不确定理解是否有问题，原文：Deep linking to a destination or navigating to the same destination should yield the same stack
A user can enter an app at the start destination and navigate to a destination. A user can also use a deep link, if available, to navigate to the same destination. In both of these cases, the navigation stack should have the same stack of destinations. Specifically, the user should be able to use the Back or Up button, regardless of how they got to a destination, to navigate through destinations back to the start destination. Any existing navigation stack is removed and replaced with the deep link’s navigation stack.

## 实现 Navigation
Navigation 架构组件简化了应用中 destination 之间的导航。
+ destination - app 中的一个页面。默认支持 fragment 和 activity 作为 destination，但也可以添加新的 destination 类型。
+ navagation graph -  一组 destination 
+ action - 在 navigation graph 中，destination 间的连接
  如下图，它展示了一个包含 6 个 destination 和 5 个 action 的 navigation graph![navigation-graph.png](https://ws1.sinaimg.cn/large/801b780agy1fttuho5u9sj212f0zf75t.jpg) 

### 搭建一个 navigation
1. 添加依赖
```scala
implementation "android.arch.navigation:navigation-fragment:$nav_version" // use -ktx for Kotlin
implementation "android.arch.navigation:navigation-ui:$nav_version" // use -ktx for Kotlin
```
2. res 目录，New -> Android resource file -> New Resource
3. 输入文件名，如 nav_graph
4. Resource type 选择 Navigation，确认
5. Android Studio 将生成一个 navigation 资源目录和一个 nav_graph.xml 文件

### 确定 destination
创建 navigation  graph 的第一步是确定 app 中的 destination。
步骤：
1. 打开 Graph Editor，New Destination，将显示 destination 对话框
2. 选择已有的 fragment/activity 或者新建一个空白的 destination（将进入创建 Fragment 引导）
3. 这样我们就创建好了一个 destination，点击该 destination，在 attribute editor 中我们可以配置该 destination 的属性。
4. 我们还可以点击 Text 栏直接切换到 XML 文件中来对属性进行修改。如下为添加一个空白 Fragment 后的 nav_graph.xml 文件。
```xml
<?xml version="1.0" encoding="utf-8"?>
<navigation xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    xmlns:android="http://schemas.android.com/apk/res/android"
    app:startDestination="@id/blankFragment">
    <fragment
        android:id="@+id/blankFragment"
        android:name="com.example.cashdog.cashdog.BlankFragment"
        android:label="Blank"
        tools:layout="@layout/fragment_blank" />
</navigation>
```

### 连接 destination
步骤：
1. 在 Graph Editor 中，将一个 Fragment 连接到另一个 Fragment，它们间将产生一个连接线
2. 点击连接线，我们在 attribute editor 中设置该 action 的属性
3. 点击 Text 栏可以切换到对应的 XML 文件
如：
```xml
<?xml version="1.0" encoding="utf-8"?>
<navigation xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    xmlns:android="http://schemas.android.com/apk/res/android"
    app:startDestination="@id/blankFragment">
    <fragment
        android:id="@+id/blankFragment"
        android:name="com.example.cashdog.cashdog.BlankFragment"
        android:label="fragment_blank"
        tools:layout="@layout/fragment_blank" >
        <action
            android:id="@+id/action_blankFragment_to_blankFragment2"
            app:destination="@id/blankFragment2" />
    </fragment>
    <fragment
        android:id="@+id/blankFragment2"
        android:name="com.example.cashdog.cashdog.BlankFragment2"
        android:label="fragment_blank_fragment2"
        tools:layout="@layout/fragment_blank_fragment2" />
</navigation>
```

#### 指定一个页面作为起始 destination
Graph Editor 会给 app 的第一个 destination 放置一个 house 图标。该图标表示 Navigation Graph 的起始 destination。
可以通过以下步骤来重新指定：
+ 在 Graph Editor 中点击该 destination
+ 点击 Attribute 面板中的 Set Start Destination

### 修改 activity 对 navigation 进行管理
activity 通过已经添加到 activity 布局中的 NavHost 接口的实现来管理 navigation。
在 Navigation 架构组件中，默认的 NavHost 实现是 NavHostFragment。有了 NavHost 之后，还需要通过 navGraph 属性将 navigation graph 与 NavHostFragment 关联起来。
一个包含 NavHostFragment 的 activity 的布局如下：
```xml
<?xml version="1.0" encoding="utf-8"?>
<android.support.constraint.ConstraintLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <fragment
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:id="@+id/my_nav_host_fragment"
        android:name="androidx.navigation.fragment.NavHostFragment"
        app:navGraph="@navigation/nav_graph"
        app:defaultNavHost="true"
        />

</android.support.constraint.ConstraintLayout>
```
`app:defaultNavHost` 属性用于确保 NavHostFragment 拦截系统返回键。

### 将 destination 与 UI 控件进行绑定
导航到一个 destination 是通过 NavController 类来实现的。
可以通过以下静态方法来获得 NavController：
+ NavHostFragment.findNavController(Fragment)
+ Navigation.findNavController(Activity, @IdRes int viewId)
+ Navigation.findNavController(View)
在得到 NavController 后，通过调用 navigate() 方法来导航到 destination，该方法接收一个资源 ID 参数，这个 ID 可以是特定 destination 或者是一个 action 的 ID。使用 action ID 的一个好处是，可以使用过渡动画。
示例代码：
```scala
viewTransactionsButton.setOnClickListener { view ->
   view.findNavController().navigate(R.id.viewTransactionsAction)
}
```
> 上面是 Kotlin 的代码 View#findNavController 是一个扩展函数。  
NavController 中还提供下以下方面来进行返回操作：
+ `NavController.navigateUp()`
+ `NavController.popBackStack()`

对于 button，还可以使用下面的便利方法来进行导航：
```scala
button.setOnClickListener(Navigation.createNavigateOnClickListener(R.id.next_fragment, null))
```

#### 将 destination 与 menu-driven(菜单驱动) UI 控件绑定
menu-driven UI 如 navigation  drawer 和 overflow menu，我们可以通过使用与 destination 相同的 id 来将 UI 与 destination 进行绑定。
示例代码：
详情页面
```xml
<fragment android:id="@+id/details_page_fragment"
     android:label="@string/details"
     android:name="com.example.android.myapp.DetailsFragment" />
```
menu_nav_drawer.xml
```xml
<item
    android:id="@id/details_page_fragment"
    android:icon="@drawable/ic_details"
    android:title="@string/details" />
```
menu_overflow.xml
```xml
<item
    android:id="@id/details_page_fragment"
    android:icon="@drawable/ic_details"
    android:title="@string/details"
    android:menuCategory:"secondary" />
```

Navigation 架构组件包含了一个 NavigationUI 类，通过类中的静态方法可以将菜单项与 destination 连接起来。
如：
```scala
val navigationView = findViewById<NavigationView>(R.id.nav_view)
navigationView.setupWithNavController(navController)
```
> NavigationView 通常用于 DrawerLayout 中。  

### destination 间的数据传递
传递数据的方式有两种：
+ Bundle 对象
	1. Graph Editor，点击 destination
	2. 在 Attributes 面板添加参数
	3. 输入 name 和默认值
	4. 点击 Text 栏，可以看到 destination 下新增了一个 argument
```xml
<fragment
   android:id="@+id/confirmationFragment"
   android:name="com.example.cashdog.cashdog.ConfirmationFragment"
   android:label="fragment_confirmation"
   tools:layout="@layout/fragment_confirmation">
   <argument android:name="amount" android:defaultValue=”0” />	
```
	4. 在调用 navigate() 导航到该 destination 时，附带一个 bundle
```scala
var bundle = bundleOf("amount" to amount)
view.findNavController().navigate(R.id.confirmationAction, bundle)	
```
	5. 在 destination 中使用传入的参数
```scala
val tv = view.findViewById(R.id.textViewAmount)
tv.text = arguments.getString("amount")	
```
+ 使用 safeargs gradle 插件
safeargs 是  Navigation 架构组件中的一个 gradle 插件，用来生成用于访问 destination 或者 action 参数的简单对象和 builder。
> The Navigation Architecture Component has a Gradle plugin, called safeargs, that generates simple object and builder classes for type-safe access to arguments specified for destinations and actions.   
添加：
```scala
apply plugin: 'com.android.application'
apply plugin: 'androidx.navigation.safeargs'

android {
   //...
}
```
使用 type-safe 参数步骤：
	1. Graph Editor，点击接收参数的 destination
	2.  点击 Attribute 面板的 argument 区域的添加按钮
	3. 输入 name，选择 type，输入默认值
	4. 切换到 Text 栏，可以看到：
```xml
<fragment
    android:id="@+id/confirmationFragment"
    android:name="com.example.buybuddy.buybuddy.ConfirmationFragment"
    android:label="fragment_confirmation"
    tools:layout="@layout/fragment_confirmation">
    <argument android:name="amount" android:defaultValue="1" app:type="integer"/>
</fragment>
```

Safeargs 插件会为 action 和 destination 生成简单的 object 和 builder 类，这些类包括：
+ 一个用于发起 action 的 destination 的类，该类以 `Directions` 结尾。比如，一个原始的 fragment 为 `SpecifyAmountFragment`，生成类名称为 `SpecifyAmountFragmentDirections`。这个类有一个用来打包参数的方法，名称为传递参数的 action，如 `confirmationAction()`
+ 一个内部类，名称基于传递参数的 action。如果 action 名为 `confirmationAction`，那么该类名为 `ConfirmationAction`
+  一个用于参数所传递给的 destination 的类，该类以`Args` 结尾。比如，destination 名为 `ConfirmationFragment`，则生成的类名为 `ConfirmationFragmentArgs`。使用生成类的 `fromBundle()` 方法来获取参数。
> ps：简单地说，就是 safeargs 会生成三个类，Directions 类用来发起 action，Directions 类会有一个内部类为 Action 类，Action 用来携带 action 的参数（有点像 Intent），第三个类为 Args 类，该类用来读取参数。分别对应 action、传参、取参三个过程。safeargs 中 safe 的含义大概是所有的参数都会称为生成类中的属性，这样就不存到类型判断出错问题。  
示例代码：设置参数并传给 `navigate()`方法
```scala
override fun onClick(v: View?) {
   val amountTv: EditText = view!!.findViewById(R.id.editTextAmount)
   val amount = amountTv.text.toString().toInt()
   val action = SpecifyAmountFragmentDirections.confirmationAction(amount)
   action.amount = amount
   v.findNavController().navigate(action)
}
```
示例代码：读取参数
``` scala
override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
    val tv: TextView = view.findViewById(R.id.textViewAmount)
    val amount = ConfirmationFragmentArgs.fromBundle(arguments).amount
    tv.text = amount.toString()
}
```

### 将多个 destination 组成一个嵌套的 navigation graph
一系列的 destination 可以组成一个 navigation graph 中的 sub-graph，该 sub-graph 被称为 「nested graph」，而包含它的 graph 被称为 「root graph」。
nested graph 必须有一个起始的 destination，外部的 destination 只能通过起始 destination 来访问 nested graph。

将多个 destination 组成 nested graph 的步骤：
1. Graph Editor，按住 「shift」，点击需要包含到 nested graph 中的 destination
2. 右键，「Move to Nested Graph > New Graph」，这样就得到了一个 nested graph
3. 点击 nested graph，我们可以 type 和 ID
4. 切换到 Text 栏，我们可以发现其实就是 navigation 标签包含了另一个 navigation 标签。

在代码中可以通过 action 的 ID 来连接 root graph 和 nested graph
```scala
view.findNavController(view).navigate(R.id.action_mainFragment_to_sendMoneyGraph)
```

### 为 destination 创建一个 deep link
在 Android 中，deep link 是一个指向特定 destination 的 URI。
步骤：
1. Graph Editor，选中 destination
2. 在 Attribute 面板的 Deep Links 区域点击添加
3. 输入 URI，如 "www.cashdog.com/sendmoney" 表示一个转账的 nested graph 的起始 destination。需要注意：
	+ 不带 scheme 的 URI 被假设为 http 和 https
	+ `{placeholder_name}` 格式的占位符匹配一个或多个字符
	+ `.*` 用于匹配 0 或多个字符
4. （可选）「Auto Verify」需要 Google 来验证 URI 是否属于你。
5. 点击 Add 后，destination 上将出现一个代表 link 的图标。

```xml
<deepLink app:uri="https://cashdog.com/sendmoney"/>
```

#### 为 deep link 添加 intent filter
必须在 manifest.xml 中做额外处理来启用 deep link
+ Android Studio 3.0 和 3.1，需要手动添加 intent-filter。[Create Deep Links to App Content](https://developer.android.com/training/app-links/deep-linking.html)
+ Android Studio 3.2，可以直接将 `nav-graph` 添加到 activity 元素中。
```xml
<activity name=".MainActivity">
    <nav-graph android:value="@navigation/main_nav" />
</activity>
```
> 实际上 deep link 在 intent filter 中被转为 android:scheme、android:host   

### destination 间的过渡动画
```xml
<fragment
    android:id="@+id/specifyAmountFragment"
    android:name="com.example.buybuddy.buybuddy.SpecifyAmountFragment"
    android:label="fragment_specify_amount"
    tools:layout="@layout/fragment_specify_amount">
    <action
        android:id="@+id/confirmationAction"
        app:destination="@id/confirmationFragment"
        app:enterAnim="@anim/slide_in_right"
        app:exitAnim="@anim/slide_out_left"
        app:popEnterAnim="@anim/slide_in_left"
        app:popExitAnim="@anim/slide_out_right" />
 </fragment>
```





参考：
[google codelabs](https://codelabs.developers.google.com/codelabs/android-navigation/)
[googlesamples NavigationBasicSample](https://github.com/googlesamples/android-architecture-components/tree/master/NavigationBasicSample)
[Navigation](https://developer.android.com/topic/libraries/architecture/navigation/)
[how-to-get-a-result-from-fragment-using-navigation-architecture-component](https://stackoverflow.com/questions/50754523/how-to-get-a-result-from-fragment-using-navigation-architecture-component)


