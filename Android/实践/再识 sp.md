> 20180207：果然，实践才是检验真理的唯一标准。通过实践才能发现不断完善自身的知识。今天遇到了的一个问题，在自己手机上显示正常，在某个手机上最后的文字却显示为了两行。虽然想吐槽竟然还有人使用如此低分辨率的屏幕，但作为一名专业的码农，还是不得不正视自己的问题。毕竟，在代码世界里，有可能发生的终将发生。

sp 与 dp 类似，它会使字体根据屏幕分辨率不同而占用不同的像素点，只是 sp 还会受到用户字体大小偏好的影响。我之前的一个错误的想法在于，潜意识里认为在小屏幕上，字体会缩小。事实上并不是这样，使用 sp 为单位，只是使字体在小屏幕上占用的像素变“少”，但这并不意味着字体看起来是小的。

假如，在一个 1080 x 1920 的 xxhdpi （480dpi）屏幕上，如果想要将该屏幕的内容完全显示在一个“同样大小”的 hdpi （240dpi）屏幕上，那么该屏幕的分辨率至少为 540 x 960，如果低于该分辨率，那么内容将无法完全容纳，这时候就可能出现内容显示不一致。



所以，适配针对的并不是小屏幕，而是小分辨率，而适配的方法与 drawable 的方式类似。