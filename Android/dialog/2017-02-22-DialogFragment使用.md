---
title: API Guides - DialogFragment
tags:
  - android
  - dialog
date: 2017-02-22 15:37:22
categories: 笔记
---

[DialogFragment](https://developer.android.com/reference/android/app/DialogFragment.html)

> DialogFragment 源码并不多，有问题可以直接看源码



#### 用法

​	DialogFragment的一般用法有两种（以下代码摘自官网）：

1. 重载onCreateView方法，然后在Activity如下进行显示

   ```java
   void showDialog() {
       mStackLevel++;

       // DialogFragment.show() will take care of adding the fragment
       // in a transaction.  We also want to remove any currently showing
       // dialog, so make our own transaction and take care of that here.
       FragmentTransaction ft = getFragmentManager().beginTransaction();
       Fragment prev = getFragmentManager().findFragmentByTag("dialog");
       if (prev != null) {
           ft.remove(prev);
       }
       ft.addToBackStack(null);

       // Create and show the dialog.
       DialogFragment newFragment = MyDialogFragment.newInstance(mStackLevel);
       newFragment.show(ft, "dialog");
   }
   ```

2. 实现onCreateDialog(Bundle)来创建自定义的Dialog对象。这通常用来创建一个AlertDialog，然后通过以fragment的方式展示。

   ```java
       @Override
       public Dialog onCreateDialog(Bundle savedInstanceState) {
           int title = getArguments().getInt("title");

           return new AlertDialog.Builder(getActivity())
                   .setIcon(R.drawable.alert_dialog_icon)
                   .setTitle(title)
                   .setPositiveButton(R.string.alert_dialog_ok,
                       new DialogInterface.OnClickListener() {
                           public void onClick(DialogInterface dialog, int whichButton) {
                               ((FragmentAlertDialog)getActivity()).doPositiveClick();
                           }
                       }
                   )
                   .setNegativeButton(R.string.alert_dialog_cancel,
                       new DialogInterface.OnClickListener() {
                           public void onClick(DialogInterface dialog, int whichButton) {
                               ((FragmentAlertDialog)getActivity()).doNegativeClick();
                           }
                       }
                   )
                   .create();
       }
   ```

   activity显示

   ```java
   void showDialog() {
       DialogFragment newFragment = MyAlertDialogFragment.newInstance(
               R.string.alert_dialog_two_buttons_title);
       newFragment.show(getFragmentManager(), "dialog");
   }
   ```

   > 此处未将fragment放入back stack，但dialog通常是模态的，所以仍会进行back stack的操作。



#### Selecting Between Dialog or Embedding

​	DialogFragment也可以选择作为普通的fragment来使用。通常可以根据使用fragment的方式自动选择作为对话框还是普通fragment，但也可以使用[setShowsDialog(boolean)](https://developer.android.com/reference/android/app/DialogFragment.html#setShowsDialog(boolean))来自定义。

> This is normally set for you based on whether the fragment is associated with a container view ID passed to FragmentTransaction.add(int, Fragment). If the fragment was added with a container, setShowsDialog will be initialized to false; otherwise, it will be true.

如：	

```java
public static class MyDialogFragment extends DialogFragment {
    static MyDialogFragment newInstance() {
        return new MyDialogFragment();
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
            Bundle savedInstanceState) {
        View v = inflater.inflate(R.layout.hello_world, container, false);
        View tv = v.findViewById(R.id.text);
        ((TextView)tv).setText("This is an instance of MyDialogFragment");
        return v;
    }
}
```

​	显示为对话框

```java
void showDialog() {
    // Create the fragment and show it as a dialog.
    DialogFragment newFragment = MyDialogFragment.newInstance();
    newFragment.show(getFragmentManager(), "dialog");
}
```

​	作为内容显示

```java
FragmentTransaction ft = getFragmentManager().beginTransaction();
DialogFragment newFragment = MyDialogFragment.newInstance();
ft.add(R.id.embedded, newFragment);
ft.commit();
```


#### 背景

在使用某些主题时，可能出现对话框有一个灰色背景的情况。该背景属于 window 的背景，可以通过在 onStart 中：

```kotlin
dialog.window.setBackgroundDrawableResource(android.R.color.transparent)
```

或者增加一个 style，将属性 android:windowBackground 设为 透明，然后调用 setType 应用。



#### 宽高

在布局中将根视图的宽高设为固定值或者 wrap_content，在显示时，会发现 dialog 发生了变形。

源码分析：

+ 无论重写的是 onCreateView() 还是 onCreateDialog()，实际上显示的都是 Dialog，我们在调用 show 方法时，并没有将 dialogFragment 放入某个 view 中，所以 dialogFragment 并不会直接显示出来。如果我们只重写了 onCreateView()，默认的 onCreateDialog() 实现会返回一个 Dialog 实例，然后在后续中将 getView() 返回的 view （即 onCreateView）通过 setContentView() 来设置给 dialog。所以，两种创建对话框的方式是没什么区别的。

所以，这个问题的根本在于 Dialog 在显示时没有按照设定的宽高进行显示。

貌似这个问题的根本答案没有找到。。先列出几种解决方式：

+ 根布局采用 RelativeLayout（有问题，看下面）
+ 在原根布局外增加一个 FrameLayout，宽高设为 match_parent（ConstraintLayout 试验有效。。再次验证发现其实应该是 FrameLayout 作为根布局就不会变形。如果换成 LinearLayout 会变形）

> 在改用 RelativeLayout 后，发现将一个 view 放置在右侧，然后设置 marginRight 无效，感觉就像是根布局的 layout_width 和 layout_height 被强制改为 wrap_content。所以最终还是换回了增加 FrameLayout 嵌套 方式。