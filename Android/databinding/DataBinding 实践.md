+ ViewDataBinding 类在 build 结束后才会自动生成


+ DataBinding 可以找到 include 标签的控件，但要求 include 标签具有 id 属性，这样才可以通过 include 标签生成的 field 来找到 include 布局的 view。（注：好像 include 中的布局的根标签也要是 layout，不过暂时没找过明确提到这点的地方）
+ viewstub 标签也能使用 data binding
+ DataBinding 获取布局的 view 时更加方便，如果是使用 findViewById 则需要注意 id 名称，这在存在大量类似 id 名称时很容易出错。
+ 如果修改布局后生成类中没有变化，可以尝试 rebuild project 或者重命名布局。




#### 问题记录

+ 20180315：发生 “Type parameter T has incompatible upper bounds: ViewDataBinding” 错误，对 Android Studio 进行 invalidate and restart 操作后，有一个使用 \<layout> 的布局被还原，而 SVN 尚未保存，天坑。。。（注：该文件是几天前已写好，今天发生了断电导致电脑关机，不过应该布局文件还原是发生在重启 android studio 后，因为重启后的错误提示成为了找不到类） 
+ 修改 id 名称后，没有自动变更生成类中的变量名，rebuild 也无效，令人捉狂
+ 出现 Binding 类没有找到的问题，可以尝试通过修改布局文件名来重新生成


参考：

[Android Data Binding: That <include> Thing](https://medium.com/google-developers/android-data-binding-that-include-thing-1c8791dd6038)

[data binding viewstub](https://developer.android.com/topic/libraries/data-binding/index.html#viewstubs)

[Android Data Binding - how to use ViewStub with data binding](https://stackoverflow.com/questions/34712952/android-data-binding-how-to-use-viewstub-with-data-binding)