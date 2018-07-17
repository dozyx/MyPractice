Android Studio 内置了两种 TODO：todo 和 fixme。

如果需要添加自定义的 TODO，可以按照以下步骤（以 refactor 为例）：

+ 定义一个 TODO
  + Settings -> Editor -> TODO -> Add
  + 输入正则表达式，仿照 todo 的写法：`\brefactor\b.*`，这里表达式匹配的是 `\b` 和 `\.*`间的内容
  + (可选)还可以自定义是否大小写敏感和显示颜色
+ 编写一个 Live Templates
  + Settings -> Editor -> Live Templates
  + 选中AndroidComments 类别，点击 Add，abbreviation 缩写填入 `rf`，Template text 填入 `// REFACTOR: $date$ $todo$ `，其中 date 和 todo 为占位符，点击 Edit variables，将 date 的 Expression 表达式改为 date()，这样在生成代码时，将自动填入日期
  + 点击 Template Text 下面的 Define，配置，该模板应用场景，对于 rf，选中 Java
  + 勾选 Reformat according to style
  + 保存退出，在 Java 文件中输入 rf 即可自动生成模板代码





参考：

[Creating TODO Items](https://www.jetbrains.com/help/idea/creating-todo-items.html)