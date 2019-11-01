默认情况下，当 configuration （如系统语言、屏幕方向等）改变时，Activity 会重新启动，如果不希望 Activity 重启，可以在 manifest 文件中给 <activity> 配置 configChanges 属性。这样当 configChanges 设置的配置改变时将回调 Activity 的 onConfigurationChanged 方法，而不会重建，但这就要求 Activity 自行处理这些配置变化。

> 不过这个属性用起来跟想象中有点不一样，比如我希望在横竖屏切换时不重建，然后设置了 android:configChanges="orientation"，接着旋转屏幕，Activity 还是重建了。原因可能是旋转屏幕的时候，不止 orientation 一个配置发生了变化。。。建议的设置是 android:configChanges="orientation|keyboardHidden|screenSize"，实际验证不设置 keyboardHidden 也可以触发 onConfigurationChanged，keyboardHidden 跟 accessibility 有关。

感觉这个属性有点鸡肋，因为配置的改变可能不是单一的。比如如果要使字体大小改变时不重建 activity，只设置 `android:configChanges="fontScale"` 是不行的，要设置 `android:configChanges="fontScale|uiMode"`，这个只是我试验的结果，谁知道会不会还会有其他条件的影响，或者说不同的设置会不会一样。