### 基本使用

在构建好一个依赖表之后，会自动为 `@Component` 注解的 interface 生成一个 Dagger 前缀的实现类，这个实现类表示的就是整个依赖表，通过它就可以为其他类提供注入的依赖。比如

```java
@Singleton
@Component
public interface AppComponent {

}
```

DaggerAppComponent：

```java
public final class DaggerAppComponent implements AppComponent {
  private DaggerAppComponent(Builder builder) {}

  public static Builder builder() {
    return new Builder();
  }

  public static AppComponent create() {
    return new Builder().build();
  }

  public static final class Builder {
    private Builder() {}

    public AppComponent build() {
      return new DaggerAppComponent(this);
    }
  }
}
```

生成实现类之后就可以通过 AppComponent.create() 来获取实现类的实例。如果 AppComponent 有一个依赖无法通过注入方式添加，比如该依赖为 Application：

```java
@Singleton
@Component
public interface AppComponent {
    Application app();
}
```

这时候编译将失败，因为 Application 没有注入。我们可以为 @Component 中添加一个 module 类，然后在 module类中使用 `@Provides` 注入 Application，除此之后，也可以在实例化 AppComponent 时设置进去。观察上面的 DaggerAppComponent 可以知道，DaggerAppComponent 实际是以 Builder 的方式来创建的，通过为 Builder 添加设置方法就可以来为我们设置依赖。为了生成这样的 Builder，需要在 AppComponent 中添加一个 `@Component.Builder` 注解的 interface，interface 中提供依赖的方法需要使用 `@BindsInstance` 注解。这样 AppComponent 将变成：

```java
@Singleton
@Component
public interface AppComponent {
    Application application();

    @Component.Builder
    interface Builder {
        @BindsInstance
        Builder application(Application application);

        AppComponent build();
    }
}
```

DaggerAppComponent：

```java
public final class DaggerAppComponent implements AppComponent {
  private Application application;

  private DaggerAppComponent(Builder builder) {
    initialize(builder);
  }

  public static AppComponent.Builder builder() {
    return new Builder();
  }

  @SuppressWarnings("unchecked")
  private void initialize(final Builder builder) {
    this.application = builder.application;
  }

  @Override
  public Application application() {
    return application;
  }

  private static final class Builder implements AppComponent.Builder {
    private Application application;

    @Override
    public AppComponent build() {
      if (application == null) {
        throw new IllegalStateException(Application.class.getCanonicalName() + " must be set");
      }
      return new DaggerAppComponent(this);
    }

    @Override
    public Builder application(Application application) {
      this.application = Preconditions.checkNotNull(application);
      return this;
    }
  }
}
```



AppComponent 可以为我们提供一些全局的依赖，接下来，我们尝试为 Activity 成员变量采用注入的方式实例化。比如：Activity 中需要用到 Applicaiton

```java
public class MainActivity extends AppCompatActivity {
    @Inject
    Application application;
    ...
}
```

application 的实例化需要通过依赖表，也就是 `@Component` 实现类来提供，因为依赖表“知道”如何实例化。Application 在 AppComponent 中，我们可以直接通过 AppComponent 为整个 MyActivity 注入依赖，但通常每个 Activity 会有自己的 Component。为此，创建一个 MainComponent：

```java
@ActivityScope
@Component(dependencies = AppComponent.class)
public interface MainComponent {
    void inject(MainActivity activity);
}
```

生成类 DaggerMainComponent：

```java
public final class DaggerMainComponent implements MainComponent {
  private AppComponent appComponent;

  private DaggerMainComponent(Builder builder) {
    initialize(builder);
  }

  public static Builder builder() {
    return new Builder();
  }

  @SuppressWarnings("unchecked")
  private void initialize(final Builder builder) {
    this.appComponent = builder.appComponent;
  }

  @Override
  public void inject(MainActivity activity) {
    injectMainActivity(activity);
  }

  private MainActivity injectMainActivity(MainActivity instance) {
    MainActivity_MembersInjector.injectApplication(
        instance,
        Preconditions.checkNotNull(
            appComponent.application(),
            "Cannot return null from a non-@Nullable component method"));
    return instance;
  }

  public static final class Builder {
    private AppComponent appComponent;

    private Builder() {}

    public MainComponent build() {
      if (appComponent == null) {
        throw new IllegalStateException(AppComponent.class.getCanonicalName() + " must be set");
      }
      return new DaggerMainComponent(this);
    }

    public Builder appComponent(AppComponent appComponent) {
      this.appComponent = Preconditions.checkNotNull(appComponent);
      return this;
    }
  }
}
```

我们只要调用 MainComponent 的 inject 方法，就会自动为 MainActivity 中的 application 提供实例，为此需要先得到 DaggerMainComponent 的实例，它需要通过 Builder 来构建，而 Builder 需要依赖 AppComponent，所以还需要先获取 DaggerAppComponent。这样最终的调用就类似于这样子：

```java
DaggerMainComponent.builder().appComponent(
                SampleApplication.getAppComponent()).build().inject(this);
```

接着，就可以直接调用 applicaiton 的方法。



### 简化 Activity 注入





资料：

[Dagger & Android](https://google.github.io/dagger/android.html)









