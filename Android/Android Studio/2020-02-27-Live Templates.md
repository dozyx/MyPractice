快速生成模板代码

入口：Settings -> Editor -> Live Templates

### 技巧

对于不清楚的语法，参照已有模板做修改，比如某个变量的取值。



### 个人常用模板

### 单例

Abbreviation：`singleton`

Template text：

```java
private $class$() {
    
}

public static $class$ getInstance() {
    return Holder.INSTANCE;
}

private static class Holder { 
    private static $class$ INSTANCE = new $class$();
}
```

Application in Java `declaration`

varialble：class -> `className()`



### 问题

#### 生成代码没有格式化

配置模板代码时，选中 `Reformat according to style`



