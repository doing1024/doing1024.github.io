大家好，欢迎来到`MojoStarter`，从0开始学习`Mojo`。今天是`#001`：Mojo介绍与Hello,World。

# Mojo介绍

Mojo是一种新的编程语言，由Chris Lattner（LLVM和Swift语言的创始人）创建的Modular AI公司开发。它结合了Python的易用性和C的性能，旨在为人工智能开发者提供一种能够高效编程AI硬件和模型的工具.

# Hello,World

入门一门语言，首先要掌握的肯定是~~如何用电脑~~如何实现“Hello,World”。首先我们需要新建一个mojo源文件，mojo的源文件后缀名是`.mojo`或者`.🔥`，是的你没有看错，非常“炸裂”的后缀。但是从实用性角度来说，还是推荐大家使用`.mojo`。

mojo需要在`main`函数中写入主程序，这点与`C++`等语言有点类似，在mojo中定义函数可以用`fn`或者`def`。两者有区别，但是我们现在不需要考虑这些问题，等用到再说。在mojo中输出使`print`，用法与`Python`类似，参考代码：
```
# 因为prism.js不支持mojo，所以没有代码高亮

# fn版本
fn main()：
    print("Hello, World!")

# ---------------------------
# def版本
def main():
    print("Hello, World!")
```
