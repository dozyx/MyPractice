TextAppearance 属性可以为 TextView 引入一个属性集来描述该文本的外形。

TextAppearance 包含的属性有：

```xml
<declare-styleable name="TextAppearance">
        <attr name="textColor" />
        <attr name="textSize" />
        <!-- bold, italic, bolditalic -->
        <attr name="textStyle" />
        <!-- normal, sans, serif, monospace -->
        <attr name="typeface" />
        <!-- Font family (named by string) for the text. -->
        <attr name="fontFamily" />
        <attr name="textColorHighlight" />
        <attr name="textColorHint" />
        <!-- Color of the links. -->
        <attr name="textColorLink" />
        <!-- Present the text in ALL CAPS. This may use a small-caps form when available. -->
        <attr name="textAllCaps" format="boolean" />
        <!-- Place a blurred shadow of text underneath the text, drawn with the
             specified color. The text shadow produced does not interact with
             properties on View that are responsible for real time shadows,
             {@link android.R.styleable#View_elevation elevation} and
             {@link android.R.styleable#View_translationZ translationZ}. -->
        <attr name="shadowColor" format="color" />
        <!-- Horizontal offset of the text shadow. -->
        <attr name="shadowDx" format="float" />
        <!-- Vertical offset of the text shadow. -->
        <attr name="shadowDy" format="float" />
        <!-- Blur radius of the text shadow. -->
        <attr name="shadowRadius" format="float" />
        <!-- Elegant text height, especially for less compacted complex script text. -->
        <attr name="elegantTextHeight" format="boolean" />
        <!-- Text letter-spacing. -->
        <attr name="letterSpacing" format="float" />
        <!-- Font feature settings. -->
        <attr name="fontFeatureSettings" format="string" />
    </declare-styleable>
```

