BottomSheetDialogFragment 是 support 包中的一个类，用来在底部显示对话框。它的使用也很简单，就是继承  BottomSheetDialogFragment，然后重写 onCreateView 即可。

在这里只是对其实现进行一些简单的分析：

首先，说明一下 DialogFragment 的一点实现细节，在使用 DialogFragment 时，我们可以选择重写 onCreateView 或者 onCreateDialog，无论哪一个，最终显示的都是一个 dialog，并且当重写了 onCreateView 时，会通过 Dialog#setContentView 来将布局设置给 dialog（onCreateDialog 默认实现也会返回一个 dialog 实例）。而 BottomSheetDialogFragment  的实现也很简单，只是重写了 onCreateDialog，其方法实现是直接返回一个 BottomSheetDialog。而在 BottomSheetDialog 中，对 setContentView 进行了重写，将参数里的 view 通过 addView 加到内部的布局中，这样就实现了将 onCreateView 返回的 view 添加到页面底部。还需要注意的一点是，BottomSheetDialog 的 window 的宽高被设置为了 match_parent。