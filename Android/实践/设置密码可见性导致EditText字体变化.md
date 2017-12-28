当设置 EditText 的 input type 为 textPassword 时，它的字体将设置为固定宽度（monospace 字体）。

我们可以采用以下方法来解决这一问题：

```
    @OnCheckedChanged(R.id.check_password_visible)
    void onPasswordVisibleChanged(boolean isChecked) {
        int pos = editLoginPassword.getSelectionEnd();
        Typeface prevTypeFace = editLoginPassword.getTypeface();
        editLoginPassword.setInputType(InputType.TYPE_CLASS_TEXT
                | (isChecked ? InputType.TYPE_TEXT_VARIATION_VISIBLE_PASSWORD
                : InputType.TYPE_TEXT_VARIATION_PASSWORD));
        editLoginPassword.setTypeface(prevTypeFace);
        if (pos > 0) {
            editLoginPassword.setSelection(pos);
        }
    }
```

除此之外，也可以通过设置 TransformationMethod 而不是 input type 来修改密码可见性，这样同样可以防止 typeface 变化

```java
    @OnCheckedChanged(R.id.check_password_visible)
    void onPasswordVisibleChanged(boolean isChecked) {
        int pos = editLoginPassword.getSelectionEnd();
        editLoginPassword.setTransformationMethod(
                isChecked ? PasswordTransformationMethod.getInstance()
                        : HideReturnsTransformationMethod.getInstance());
        if (pos > 0) {
            editLoginPassword.setSelection(pos);
        }
    }
```

上面两种方法都需要增加代码，不过我采用参考中设置 `android:fontFamily="sans-serif" `的方法无效，不知道是不是跟 Android 版本有关（mi5，Android7.0）。





参考：

[Android : Typeface is changed when i apply password Type on EditText](https://stackoverflow.com/questions/24117178/android-typeface-is-changed-when-i-apply-password-type-on-edittext)