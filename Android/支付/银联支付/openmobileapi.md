在编译代码时，出现多个关于 openmobileapi 的警告，如

```
Warning: com.unionpay.mobile.android.pboctransaction.simapdu.b: can't find referenced class org.simalliance.openmobileapi.Channel
Warning: com.unionpay.mobile.android.pboctransaction.simapdu.b: can't find referenced class org.simalliance.openmobileapi.Reader
...
```

这些 warning 是银联支付 sdk 使用的 api 引起的，openmobileapi 是 android 系统自带的包，但编译时没有引入。可以在混淆文件中添加以下规则来隐藏该类警告：

`-dontwarn org.simalliance.openmobileapi.**`

> 疑问：如果厂商去掉了 openmobileapi，应用在使用银联支付时是不是可能发生奔溃？这个以后可能需要进一步对 openmobileapi 进行了解。



参考：

[SmartcardAPI](https://github.com/seek-for-android/pool/wiki/SmartcardAPI)

[How do I check the version of Open Mobile API on Android?](https://stackoverflow.com/questions/37032422/how-do-i-check-the-version-of-open-mobile-api-on-android)