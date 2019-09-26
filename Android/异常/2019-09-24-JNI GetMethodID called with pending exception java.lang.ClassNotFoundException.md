在使用一个第三方 sdk 时，release 出现 native crash。既然 debug 没问题，那第一个会想到的原因肯定是混淆问题，不过一开始也不是很确定，因为是 native 的错误，混淆会导致 native 报错？这个一直没有遇到过。于是加了下面的混淆规则：

```java
-keep class com.hjimi.** 
```

问题还存在（内心ps：我就说嘛，混淆怎么会是 native 报错）。

于是，我又浪费了几个小时。。。最后，实在没办法了，又试了加混淆规则，这样：

```java
-keep class com.hjimi.**  {* ;}
```

异常消失了。。。

由于对混淆和 JNI 的不熟悉，导致浪费了好几个小时。。。

猜测之所以混淆导致 native 报错，是因为 native 方法中调用了  Java 代码。

[常见问题解答：为什么 `FindClass` 找不到我的类？](https://developer.android.com/training/articles/perf-jni#%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E8%A7%A3%E7%AD%94%EF%BC%9A%E4%B8%BA%E4%BB%80%E4%B9%88-findclass-%E6%89%BE%E4%B8%8D%E5%88%B0%E6%88%91%E7%9A%84%E7%B1%BB%EF%BC%9F)

其实，这个问题浪费了更多的时间还有另一个原因，就是我没注意到 `JNI DETECTED ERROR IN APPLICATION: JNI GetMethodID called with pending exception java.lang.ClassNotFoundException` 这句话，一直光顾着看那一堆 so 的报错了，也没看出什么东西。。。



部分奔溃日志：

```java
2019-09-24 09:52:49.007 31183-31191/? E/jimi.colordept: Failed to send DDMS packet REAQ to debugger (-1 of 20): Broken pipe
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542] JNI DETECTED ERROR IN APPLICATION: JNI GetMethodID called with pending exception java.lang.ClassNotFoundException: Didn't find class "com.hjimi.api.iminect.ImiUpgrade" on path: DexPathList[[zip file "/system/framework/org.apache.http.legacy.boot.jar", zip file "/data/app/com.hjimi.colordepth-1G6i-j4AFHNWvWAlxQLNVA==/base.apk"],nativeLibraryDirectories=[/data/app/com.hjimi.colordepth-1G6i-j4AFHNWvWAlxQLNVA==/lib/arm, /system/fake-libs, /data/app/com.hjimi.colordepth-1G6i-j4AFHNWvWAlxQLNVA==/base.apk!/lib/armeabi-v7a, /system/lib, /vendor/lib]]
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   at java.lang.Class dalvik.system.BaseDexClassLoader.findClass(java.lang.String) (BaseDexClassLoader.java:171)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   at java.lang.Class java.lang.ClassLoader.loadClass(java.lang.String, boolean) (ClassLoader.java:379)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   at java.lang.Class java.lang.ClassLoader.loadClass(java.lang.String) (ClassLoader.java:312)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   at java.lang.String java.lang.Runtime.nativeLoad(java.lang.String, java.lang.ClassLoader) (Runtime.java:-2)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   at void java.lang.Runtime.loadLibrary0(java.lang.ClassLoader, java.lang.String) (Runtime.java:1014)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   at void java.lang.System.loadLibrary(java.lang.String) (System.java:1669)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   at void com.hjimi.api.iminect.B.e() (:80)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   at int com.hjimi.api.iminect.B.c() (:20)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   at void com.hjimi.colordepth.MainActivity$d.run() (:148)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   at void java.lang.Thread.run() (Thread.java:764)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542] 
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]     in call to GetMethodID
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]     from java.lang.String java.lang.Runtime.nativeLoad(java.lang.String, java.lang.ClassLoader)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542] "Thread-4" prio=5 tid=18 Runnable
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   | group="main" sCount=0 dsCount=0 flags=0 obj=0x12f45d00 self=0xe3ffb600
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   | sysTid=31218 nice=0 cgrp=default sched=0/0 handle=0xd4f79970
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   | state=R schedstat=( 2974791 3430157 6 ) utm=0 stm=0 core=5 HZ=100
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   | stack=0xd4e76000-0xd4e78000 stackSize=1042KB
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   | held mutexes= "mutator lock"(shared held)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   native: #00 pc 002db517  /system/lib/libart.so (art::DumpNativeStack(std::__1::basic_ostream<char, std::__1::char_traits<char>>&, int, BacktraceMap*, char const*, art::ArtMethod*, void*, bool)+134)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   native: #01 pc 00373567  /system/lib/libart.so (art::Thread::DumpStack(std::__1::basic_ostream<char, std::__1::char_traits<char>>&, bool, BacktraceMap*, bool) const+210)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   native: #02 pc 0036fc35  /system/lib/libart.so (art::Thread::Dump(std::__1::basic_ostream<char, std::__1::char_traits<char>>&, bool, BacktraceMap*, bool) const+36)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   native: #03 pc 0023319b  /system/lib/libart.so (art::JavaVMExt::JniAbort(char const*, char const*)+694)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   native: #04 pc 002334fb  /system/lib/libart.so (art::JavaVMExt::JniAbortV(char const*, char const*, std::__va_list)+58)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   native: #05 pc 000c4e7f  /system/lib/libart.so (art::(anonymous namespace)::ScopedCheck::AbortF(char const*, ...)+42)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   native: #06 pc 000c3b11  /system/lib/libart.so (art::(anonymous namespace)::ScopedCheck::CheckPossibleHeapValue(art::ScopedObjectAccess&, char, art::(anonymous namespace)::JniValueType)+1052)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   native: #07 pc 000c2ffd  /system/lib/libart.so (art::(anonymous namespace)::ScopedCheck::Check(art::ScopedObjectAccess&, bool, char const*, art::(anonymous namespace)::JniValueType*)+624)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   native: #08 pc 000c6575  /system/lib/libart.so (art::(anonymous namespace)::CheckJNI::GetMethodIDInternal(char const*, _JNIEnv*, _jclass*, char const*, char const*, bool)+508)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   native: #09 pc 000b7b3f  /system/lib/libart.so (art::(anonymous namespace)::CheckJNI::GetMethodID(_JNIEnv*, _jclass*, char const*, char const*)+22)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   native: #10 pc 0000a73f  /data/app/com.hjimi.colordepth-1G6i-j4AFHNWvWAlxQLNVA==/lib/arm/libImiSdk.jni.so (JNI_OnLoad+62)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   native: #11 pc 002360dd  /system/lib/libart.so (art::JavaVMExt::LoadNativeLibrary(_JNIEnv*, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const&, _jobject*, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>*)+2324)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   native: #12 pc 00002f5b  /system/lib/libopenjdkjvm.so (JVM_NativeLoad+230)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   native: #13 pc 002dd2eb  /system/framework/arm/boot-core-oj.oat (offset 2c9000) (java.lang.Runtime.nativeLoad [DEDUPED]+130)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   native: #14 pc 00413975  /system/lib/libart.so (art_quick_invoke_stub_internal+68)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   native: #15 pc 003ecbd3  /system/lib/libart.so (art_quick_invoke_static_stub+222)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   native: #16 pc 000a1c77  /system/lib/libart.so (art::ArtMethod::Invoke(art::Thread*, unsigned int*, unsigned int, art::JValue*, char const*)+154)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   native: #17 pc 001e6e65  /system/lib/libart.so (art::interpreter::ArtInterpreterToCompiledCodeBridge(art::Thread*, art::ArtMethod*, art::ShadowFrame*, unsigned short, art::JValue*)+236)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   native: #18 pc 001e195f  /system/lib/libart.so (bool art::interpreter::DoCall<false, false>(art::ArtMethod*, art::Thread*, art::ShadowFrame&, art::Instruction const*, unsigned short, art::JValue*)+814)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   native: #19 pc 003e870b  /system/lib/libart.so (MterpInvokeStatic+130)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   native: #20 pc 00406914  /system/lib/libart.so (ExecuteMterpImpl+14612)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   native: #21 pc 000da3da  /system/framework/boot-core-oj.vdex (java.lang.Runtime.loadLibrary0+38)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   native: #22 pc 001c60db  /system/lib/libart.so (_ZN3art11interpreterL7ExecuteEPNS_6ThreadERKNS_20CodeItemDataAccessorERNS_11ShadowFrameENS_6JValueEb.llvm.448845121+378)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   native: #23 pc 001ca7c1  /system/lib/libart.so (art::interpreter::ArtInterpreterToInterpreterBridge(art::Thread*, art::CodeItemDataAccessor const&, art::ShadowFrame*, art::JValue*)+152)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   native: #24 pc 001e1947  /system/lib/libart.so (bool art::interpreter::DoCall<false, false>(art::ArtMethod*, art::Thread*, art::ShadowFrame&, art::Instruction const*, unsigned short, art::JValue*)+790)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   native: #25 pc 003e772f  /system/lib/libart.so (MterpInvokeVirtual+442)
2019-09-24 09:52:49.337 31183-31218/? A/jimi.colordept: java_vm_ext.cc:542]   native: #26 pc 00406794  /system/lib/libart.so (ExecuteMterpImpl+14228)
...
```

