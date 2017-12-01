| 新              | 旧        | 说明                                       |
| -------------- | -------- | ---------------------------------------- |
| implementation | compile  | 告诉 Gradle 该 dependency 在 compile 时不会暴露给其他module，即 dependency 仅在 runtime 时对其他 module 可用。使用该配置可以极大地提高重新编译时的速度，因为在该 dependency 改变时，仅需要重编译该 dependency 和依赖它的 module。 |
| api            | compile  | 该 dependency 在 compile 和 runtime 时均对其他 module 有效。 |
| compileOnly    | provided | 仅用于 compile，不会添加到编译后的输出中                 |
| runtimeOnly    | apk      | 仅用于 runtime                              |

implementation 举例：假如 module A 使用 implementation 依赖于 lib，而 module B 依赖于 module B，这时候 lib 发生了修改，在重新编译时只会编译 lib 和 module A，而不需要编译 module B（compile 阶段，module B 也无法使用 lib）。

在 implementation 文档介绍中：

> When your module configures an `implementation` dependency, it's letting Gradle know that the module does not want to leak the dependency to other modules at compile time. That is, the dependency is available to other modules only at runtime.

对于 `is available to other modules only at runtime` 不是很理解，compile 没通过的话，怎么进入 runtime。。。



参考：

[new configurations](https://developer.android.com/studio/build/gradle-plugin-3-0-0-migration.html#new_configurations)