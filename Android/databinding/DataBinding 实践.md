+ ViewDataBinding 类在 build 结束后才会自动生成


+ DataBinding 可以找到 include 标签的控件，但要求 include 标签具有 id 属性，这样才可以通过 include 标签生成的 field 来找到 include 布局的 view。
+ viewstub 标签也能使用 data binding





参考：

[Android Data Binding: That <include> Thing](https://medium.com/google-developers/android-data-binding-that-include-thing-1c8791dd6038)

[data binding viewstub](https://developer.android.com/topic/libraries/data-binding/index.html#viewstubs)

[Android Data Binding - how to use ViewStub with data binding](https://stackoverflow.com/questions/34712952/android-data-binding-how-to-use-viewstub-with-data-binding)