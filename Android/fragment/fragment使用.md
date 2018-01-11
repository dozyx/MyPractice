注意事项：

+ 在 Fragment 中使用 ButterKnife 时，需要在 onDestroyView 时，调用 unbind，这时候，所有通过 bind 得到的 view 都被清空，如果再使用这些 view 的方法将导致空指针异常。所以，在进行网络请求后，需要明确是否已进行了 unbind 操作，如果已进行则要避免操作这些 view。