描述：运行无法执行编译，提示 apk 不存在

解决：Edit Configuration -> Android App，确认 Gradle-aware Make 是否存在，如果没有则添加，添加时输入 task 可留空。

![IM截图2018032917252](../../../photo/TIM截图20180329172529.png)