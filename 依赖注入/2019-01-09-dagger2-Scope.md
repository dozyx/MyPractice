> 刚开始看 dagger 的文档时，对 scope 就不是很能理解，只是简单地就认为 @Singleton 就是单例。后来看到一些项目里自定义的 @ActivityScope 之后更加疑惑了，dagger2 是怎样识别出自定义的 scope，然后把 component 的生命周期限制到 Activity 上？接着看 component 的生成代码，@Singleton 注解的 provides 方法似乎没能保证该依赖为单例啊，它只是在该 component 实例中是唯一而已。而且创建两个 @Singleton 注解的 component，这两个 component 也是两个不同的对象。。。
>
> 其实，到这一步，答案已经出现在我面前，只是我先入为主的认为 @Singleton 就是我们常用的单例，@ActivityScope 就是会自动绑定到 Activity 的生命周期，导致我理解不了。
>
> 事实上，这里并没有什么魔法，@Singleton 与 @ActivityScope 本质是一样的，只是名字不同而已，它们都能让使用 @Singleton 或 @ActivityScope 注解的 provides 方法产生唯一实例，只是这个唯一是在 component 内。至于 component 的生命周期，需要由开发者自行控制。

















资料：

[Dagger 2 Custom Scope for each Fragment (or Activity etc…)](https://stackoverflow.com/questions/30972574/dagger-2-custom-scope-for-each-fragment-or-activity-etc)

[Dagger 2 - what is the purpose of a @Singleton annotation class](https://stackoverflow.com/questions/31100041/dagger-2-what-is-the-purpose-of-a-singleton-annotation-class)

[Dependency injection with Dagger 2 – Custom scopes](https://mirekstanek.online/dependency-injection-with-dagger-2-custom-scopes/)