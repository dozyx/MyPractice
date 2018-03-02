fragment 在 启动 dialogFragment 之前，使用 Fragment#setTargetFragment 设置一个 target fragment

`void setTargetFragment(@Nullable Fragment fragment, int requestCode)`

dialogFragment 在向 fragment 回传数据时，先使用 getTargetFragment 得到 target fragment，然后调用 target fragment 的 onActivityResult 方法来传递数据

`void onActivityResult(int requestCode, int resultCode, Intent data)`