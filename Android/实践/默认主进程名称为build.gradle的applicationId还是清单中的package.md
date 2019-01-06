答：为 applicationId。

分析：    

> android:package 属性的作用只有两方面：
>
> + 为生成的 R.java 类提供命名空间
> + 声明在 manifest 中的类的相对名称
>
> 在编译结束后，编译工具会将 applicationId 复制到最终的清单文件中（可以通过反编译查看）。
>
> Android API 中的 “package name” 实际为 application ID，如 Context.getPackageName()。

> BuildConfig 文件的 package 与 manifest 中的 package 一致。

参考：    

[Set the Application ID](https://developer.android.com/studio/build/application-id.html)



