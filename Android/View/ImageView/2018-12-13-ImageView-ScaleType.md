* fitXY - 宽高同时缩放，最终 src 与 dst 一致，可能会改变 src 的原比例
* fitCenter - 对一边进行缩放，最终 src 会完全在 dst 中，且至少有一条边与 dst 一致。
* center - **没有缩放**，居中显示
* centerCrop - 原比例缩放宽高，最终图片的宽高**等于或大于** view 的宽高
* centerInside - 原比例缩放宽高，最终图片的宽高**等于或小于** view 的宽高，居中显示
* fitEnd - 原比例缩放宽高，使图片完全在 view 中，并且至少有一条边相同。将图片放置在 view 的 right 和 bottom
* fitStart - 原比例缩放宽高，使图片完全在 view 中，并且至少有一条边相同。将图片放置在 view 的 left 和 top
* matrix - 使用 matrix 的缩放



### centerCrop  和 centerInside 比较

centerCrop 是图片不小于 view，然后显示中间部分，可能发生裁剪；centerInside 使图片不大于 view