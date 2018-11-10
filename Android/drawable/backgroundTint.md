+ android:backgroundTint 从 API21 开始支持，为保持向下兼容，建议使用 app:backgroundTint，相应的，view 也要是 compat 包里的 view
+ app:backgroundTint 会覆盖 android:backgroundTint
+ app:backgroundTint 对 ViewGroup 无效，所以只能使用 android:backgroundTint，因此 API21 以下设备无效。