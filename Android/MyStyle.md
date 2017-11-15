+ 将通用的基类放于 common 包中，如 adapter、activity
+ 图片资源前缀 `ic_`
+ 考虑以 Helper 而不是 Util 作为后缀

共享常量位置（阿里）：
1. 跨应用共享常量：放置在二方库中，通常是 client.jar 中的 constant 目录下。
2. 应用内共享常量：放置在一方库中，通常是 modules 中的 constant 目录下。    
反例：易懂变量也要统一定义成应用内共享常量，两位攻城师在两个类中分别定义了表示“是”的变量：    
类 A 中：public static final String YES = "yes";    
类 B 中：public static final String YES = "y";    
A.YES.equals(B.YES)，预期是 true，但实际返回为 false，导致线上问题。
3. 子工程内部共享常量：即在当前子工程的 constant 目录下。
4. 包内共享常量：即在当前包下单独的 constant 目录下。
5. 类内共享常量：直接在类内部 private static final 定义。


Android Studio 代码风格文件：    
[官方AndroidStyle](https://github.com/aosp-mirror/platform_development/blob/master/ide/intellij/codestyles/AndroidStyle.xml)

[阿里巴巴Java开发手册](https://github.com/alibaba/p3c/blob/master/%E9%98%BF%E9%87%8C%E5%B7%B4%E5%B7%B4Java%E5%BC%80%E5%8F%91%E6%89%8B%E5%86%8C%EF%BC%88%E7%BB%88%E6%9E%81%E7%89%88%EF%BC%89.pdf)

代码风格：    
[android-guidelines](https://github.com/ribot/android-guidelines/blob/master/project_and_code_guidelines.md) 这里面给出的很多命名的前缀都比较符合我的想法    
