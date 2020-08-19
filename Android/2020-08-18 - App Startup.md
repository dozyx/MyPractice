使多个组件初始化共同使用一个 content provider，以加速 app 的启动。

依赖使用 content provider 初始化的缺点：

* provider 的初始化是昂贵的
* 初始化顺序不确定



其实，startup 的目的就是将原本单独在每个 content provider 中初始化的过程，统一放到同一个 content provider 中，并且可以指定相互之间的依赖关系。对于第三方库，可以在 manifest 中指定 `tools:node="remove"` 将该 provider 移除，然后再主动调用它的初始化。



### 基本使用

* 每个需要进行初始化的组件都要实现 Initializer。`create(..)` 执行组件的初始化，`dependencies(..)` 配置依赖的组件初始化过程，组件会先于该组件进行初始化。

  ```java
  public interface Initializer<T> {
  
      T create(@NonNull Context context);
      List<Class<? extends Initializer<?>>> dependencies();
  }
  ```

* 自动初始化：在 manifest 的 `InitializationProvider` 下使用 `meta-data` 指定要初始化的 Initializer。使用 `/gradlew :app:lintDebug` 可以检查组件初始化是否配置正确。

* 手动初始化：

  * 先禁止自动初始化

    ```xml
    <provider
        android:name="androidx.startup.InitializationProvider"
        android:authorities="${applicationId}.androidx-startup"
        android:exported="false"
        tools:node="merge">
        <meta-data android:name="com.example.ExampleLoggerInitializer"
                  tools:node="remove" />
    </provider>
    ```

    或者禁用全部组件的自动初始化

    ```java
    <provider
        android:name="androidx.startup.InitializationProvider"
        android:authorities="${applicationId}.androidx-startup"
        tools:node="remove" />
    ```

  * 调用初始化

    ```java
    AppInitializer.getInstance(context)
        .initializeComponent(ExampleLoggerInitializer::class.java)
    ```



### 源码

自动初始化的 InitializationProvider 实际上调用了 `AppInitializer.getInstance(context).discoverAndInitialize();`

```java
public final class AppInitializer {
   ...
    /**
     * Initializes a {@link Initializer} class type.
     *
     * @param component The {@link Class} of {@link Initializer} to initialize.
     * @param <T>       The instance type being initialized
     * @return The initialized instance
     */
    @NonNull
    @SuppressWarnings("unused")
    public <T> T initializeComponent(@NonNull Class<? extends Initializer<T>> component) {
        return doInitialize(component, new HashSet<Class<?>>());
    }

    @NonNull
    @SuppressWarnings({"unchecked", "TypeParameterUnusedInFormals"})
    <T> T doInitialize(
            @NonNull Class<? extends Initializer<?>> component,
            @NonNull Set<Class<?>> initializing) {
        synchronized (sLock) {
            ...
            try {
                ...
                if (initializing.contains(component)) {
                    // 避免在一个组件初始化链中循环依赖，比如 A 依赖 B，B 依赖 A 这种情况
                    String message = String.format(
                            "Cannot initialize %s. Cycle detected.", component.getName()
                    );
                    throw new IllegalStateException(message);
                }
                Object result;
                if (!mInitialized.containsKey(component)) {
                    // mInitialized 记录已初始化的组件，避免重复初始化
                    initializing.add(component);
                    try {
                        // 创建出 Initializer 实例
                        Object instance = component.getDeclaredConstructor().newInstance();
                        Initializer<?> initializer = (Initializer<?>) instance;
                        // 得到 Initializer 的依赖
                        List<Class<? extends Initializer<?>>> dependencies =
                                initializer.dependencies();

                        if (!dependencies.isEmpty()) {
                            // 先对依赖初始化
                            for (Class<? extends Initializer<?>> clazz : dependencies) {
                                if (!mInitialized.containsKey(clazz)) {
                                    doInitialize(clazz, initializing);
                                }
                            }
                        }
                        ...
                        // 执行初始化
                        result = initializer.create(mContext);
                        ...
                        initializing.remove(component);
                        mInitialized.put(component, result);
                    } catch (Throwable throwable) {
                        throw new StartupException(throwable);
                    }
                } else {
                    result = mInitialized.get(component);
                }
                return (T) result;
            } finally {
                Trace.endSection();
            }
        }
    }

    @SuppressWarnings("unchecked")
    void discoverAndInitialize() {
        try {
            Trace.beginSection(SECTION_NAME);
            ComponentName provider = new ComponentName(mContext.getPackageName(),
                    InitializationProvider.class.getName());
            ProviderInfo providerInfo = mContext.getPackageManager()
                    .getProviderInfo(provider, GET_META_DATA);
            Bundle metadata = providerInfo.metaData;
            // 找到注册的 InitializationProvider，并提取出 meta data 信息
            String startup = mContext.getString(R.string.androidx_startup);
            if (metadata != null) {
                Set<Class<?>> initializing = new HashSet<>();
                Set<String> keys = metadata.keySet();
                for (String key : keys) {
                    String value = metadata.getString(key, null);
                    if (startup.equals(value)) {
                        // value 为 androidx.startup 的 metadata 是要初始化的 Initializer
                        Class<?> clazz = Class.forName(key);
                        if (Initializer.class.isAssignableFrom(clazz)) {
                            Class<? extends Initializer<?>> component =
                                    (Class<? extends Initializer<?>>) clazz;
                            if (StartupLogger.DEBUG) {
                                StartupLogger.i(String.format("Discovered %s", key));
                            }
                            // 对 Initializer 执行初始化
                            doInitialize(component, initializing);
                        }
                    }
                }
            }
        } catch (PackageManager.NameNotFoundException | ClassNotFoundException exception) {
            throw new StartupException(exception);
        } finally {
            Trace.endSection();
        }
    }
}
```

从源码上看整个过程其实也很简单：

* 将每个要初始化的组件封装成 `Initializer` 对象，并且可以指定它的依赖组件
* 统一初始化的 `InitializationProvider` 在 onCreate() 里通过 metadata 信息找到所有要初始化的 `Initializer`，然后通过反射创建出来并执行每个 `Initializer` 的初始化过程
* 当然如果不想自动初始化也可以直接使用 `AppInitializer`，但好像也没什么必要吧



### 思考

* 对于库模块可以实现 startup 的初始化，这样不同的库就可以通过同一个 provider 进行初始化
* 对于现在已经使用独立的 provider 进行初始化的第三方库，可以在我们的 manifest 中通过 `tools:node="remove"` 将这个 provider 移除，然后为它创建 `Initializer` 来初始化，但如果后续库升级可能改变它的初始化方法，那么我们这边也得注意同步修改。这个感觉还是比较麻烦的，这要求记住库的每个 provider。
* 而且这些初始化都是通过反射创建的，现在反射的影响这么低了吗？不过 provider 本身也是反射创建的吧。







参考：

[startup](https://developer.android.com/topic/libraries/app-startup)