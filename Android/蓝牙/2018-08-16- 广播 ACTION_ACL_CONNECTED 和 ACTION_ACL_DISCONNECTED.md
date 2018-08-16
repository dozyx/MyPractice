app 中使用 了 ACTION_ACL_CONNECTED 和 ACTION_ACL_DISCONNECTED 来监听蓝牙连接状态，但实际使用过程中出现两个奇怪的问题：

+ 手动关闭蓝牙没有收到 ACTION_ACL_DISCONNECTED 
+ 同一手机多 app 根据 mac 地址连接同一蓝牙设备，第二个 app 连接成功没有触发 ACTION_ACL_CONNECTED



### 上述第二个问题的一点验证加一点猜测

app 通过监听广播 ACTION_ACL_CONNECTED 和 ACTION_ACL_DISCONNECTED 来判断蓝牙设备是否连接并进行某些操作，但在某些情况下，发现这两个广播并没有按预想的触发。如，app1 连接蓝牙设备，系统发出 ACTION_ACL_CONNECTED，用 app2 连接该设备，没有收到 ACTION_ACL_CONNECTED，而且 ACTION_ACL_DISCONNECTED   也没有，断开蓝牙连接（调用接口断开或者设备断开电源），app1 和 app2 均收到 ACTION_ACL_DISCONNECTED，但有明显延迟。

先看下该广播的说明：

```java
    /**
     * Broadcast Action: Indicates a low level (ACL) connection has been
     * established with a remote device.
     * <p>Always contains the extra field {@link #EXTRA_DEVICE}.
     * <p>ACL connections are managed automatically by the Android Bluetooth
     * stack.
     * <p>Requires {@link android.Manifest.permission#BLUETOOTH} to receive.
     */
    @SdkConstant(SdkConstantType.BROADCAST_INTENT_ACTION)
    public static final String ACTION_ACL_CONNECTED =
            "android.bluetooth.device.action.ACL_CONNECTED";
```

因为试验中与蓝牙设备的通讯都是通过第三方提供的 sdk 进行的，不太确定它们具体的实现，只是结合试验结果与文档说明做下猜测：该广播表示的是与远程设备的连接是否建立，在同一手机上使用两个 app 分别进行连接时，手机与远程设备的连接并没有在切换过程中断开，因此 app2 连接时不会发出连接成功广播也不会发出断开连接广播，只有 app 明确断开连接，这时候才会确实地断开与远程设备的连接。不过这里也有个奇怪的地方，当我使用 app2 连接设备时，设备上的蓝牙标记是先断开然后再连接的。



### 总结

+ 蓝牙开关通过 ACTION_STATE_CHANGED 状态判断
+ 蓝牙设备连接状态最好能通过实际发生通讯的接口来跟踪（如果能确定只有一个 app 可以连接该蓝牙设备，使用 ACL 问题也不大）