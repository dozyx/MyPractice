> 在发现这个类后，不断跟各种 app 的需求匹配起来，真的是非常使用，如果使用这个类，很多东西都感觉如此简单。

TextInputLayout 以一个 EditText 作为子视图来为 EditText 提供一些额外的功能。

## TextInputLayout

特性：

+ 在获得焦点时，将 hint 显示在 EditText 上面（需要额外空间显示）
+ 在 EditText 下显示 error 文本（需要额外空间显示）
+ 在 EditText 下面右侧显示一个 counter（计数器）来指示当前输入字符数目（需要额外空间显示）
+ 在 EditText 右侧显示密码可见性切换视图，要求 EditText 的输入类型为密码（TextView 本身有一个 setError 方法，TextInputLayout 设置的密码可见性切换视图会与该方法设置的 error 图标位置重叠）

### 属性

```xml
<declare-styleable name="TextInputLayout">
        <attr name="hintTextAppearance" format="reference"/>
        <!-- 悬浮的 hint 文本，EditText 内也将使用该 hint，会与 EditText 的 hint 属性重叠 -->
        <attr name="android:hint"/>
        <!-- 是否使用悬浮 hint 功能 -->
        <attr name="hintEnabled" format="boolean"/>
        <!-- 为 true 时将增加额外布局空间来显示 error -->
        <attr name="errorEnabled" format="boolean"/>
        <attr name="errorTextAppearance" format="reference"/>
        <attr name="counterEnabled" format="boolean"/>
        <!-- counter 最大数目，比如设置为 100，counter 将显示为 x/100，x 为当前数目，x 可以大于最大数目，但这时 counter 视图外观会有所变化 -->
        <attr name="counterMaxLength" format="integer" />
        <attr name="counterTextAppearance" format="reference"/>
        <attr name="counterOverflowTextAppearance" format="reference"/>
        <attr name="android:textColorHint"/>
        <attr name="hintAnimationEnabled" format="boolean"/>
        <attr name="passwordToggleEnabled" format="boolean"/>
        <attr name="passwordToggleDrawable" format="reference"/>
        <attr name="passwordToggleContentDescription" format="string"/>
        <!-- Icon to use for the password input visibility toggle -->
        <attr name="passwordToggleTint" format="color"/>
        <!-- Blending mode used to apply the background tint. -->
        <attr name="passwordToggleTintMode">
            <!-- The tint is drawn on top of the drawable.
                 [Sa + (1 - Sa)*Da, Rc = Sc + (1 - Sa)*Dc] -->
            <enum name="src_over" value="3" />
            <!-- The tint is masked by the alpha channel of the drawable. The drawable’s
                 color channels are thrown out. [Sa * Da, Sc * Da] -->
            <enum name="src_in" value="5" />
            <!-- The tint is drawn above the drawable, but with the drawable’s alpha
                 channel masking the result. [Da, Sc * Da + (1 - Sa) * Dc] -->
            <enum name="src_atop" value="9" />
            <!-- Multiplies the color and alpha channels of the drawable with those of
                 the tint. [Sa * Da, Sc * Dc] -->
            <enum name="multiply" value="14" />
            <!-- [Sa + Da - Sa * Da, Sc + Dc - Sc * Dc] -->
            <enum name="screen" value="15" />
        </attr>
    </declare-styleable>
```





## TextInputEditText

TextInputEditText 是 EditText 的子类，它被设计来用于 TextInputLayout 的子视图，TextInputEditText 增加的特性只有一个（源码也没几行），它被用于在 EditText 没有 hint 的时候，采用父视图的 hint。一种情况就是在某些情况下，点击 EditText 进行输入（横屏），输入法会启动一个新的页面进行输入操作，该新页面将采用父视图的 hint 作为 EditText 的 hint。

> 尽管从谷歌的结果及源码来看，上面的理解应该是正确的，不过在小米 8（android8.1）上试验时，无论使用 TextInputEditText 还是普通的 EditText，进入全屏输入界面均能正确获取 TextInputLayout 中的 hint。可能是最新的版本做过修改，将 TextInputLayout 的 hint 设置给了 EditText（在自身没有 hint 的情况下），又或者 InputConnection 有过修改。
>
> 一般开发直接使用 EditText 应该问题不大。

参考：

[EditText added is not a TextInputEditText. Please switch to using that class instead](https://stackoverflow.com/questions/35775919/edittext-added-is-not-a-textinputedittext-please-switch-to-using-that-class-ins/36269036#36269036)