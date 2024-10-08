# 归并排序简介

## 什么是排序算法

排序算法是算法的基石，许多算法都基于排序算法，比如二分搜索、离散化等。这篇文章将要详细介绍将要介绍排序算法之一——归并排序。

## 归并排序的性能

归并排序的时间复杂度稳定在 $\mathcal{O}(n \log(n))$ ，是一种具有稳定性（即相同元素相对位置不变）的排序方法。所以一般来说归并排序优于快速排序。归并排序基于一种叫做“分治”的思想，即分而治之。

# 归并排序原理

下面我们用`1 9 2 7 6 5 8 4`这8个数来演示归并排序。

归并排序主要分为两部分，一部分是分，一部分是合。

## 步骤一：分解

![](https://s21.ax1x.com/2024/07/29/pkLkTEj.png)

对于每个序列，取`mid=(l+r)/2`（向下取整）， 然后分别对左（`[l~mid]`）右（`[mid+1~r]`）两段进行排序。
等等！如果 $l = r$，即只有一个数了，那么这段就不用排了， 直接`return`。

## 步骤二：合并

这个步骤，我们需要将两个子序列进行合并。注意，被合并的两个子序列一定是有序的。这样才可以进行线性的合并。

我们定义两个“箭头”`i`和`j`分别指向两个子序列的开头，并且定义一个“储物间”数组`t`，用来存储排好的数字，就像这样：

[![pkLNwB4.png](https://s21.ax1x.com/2024/07/29/pkLNwB4.png)](https://imgse.com/i/pkLNwB4)

然后我们比较两个箭头指向的数字，看哪个小，就让哪个进入“储物间”，并且把那个箭头向前推进。
比如上面这幅图， $1 < 4$ ，所以就变成这样：

[![pkLN69x.png](https://s21.ax1x.com/2024/07/29/pkLN69x.png)](https://imgse.com/i/pkLN69x)

接下来， $2 < 4$ ，所以让i指向的数进入储物间并向前推进。

[![pkLNggK.png](https://s21.ax1x.com/2024/07/29/pkLNggK.png)](https://imgse.com/i/pkLNggK)

接下来继续，注意！ $7 > 4$ ，所以要让4进入储物间，推进的则是`j`。

[![pkLNfDe.png](https://s21.ax1x.com/2024/07/29/pkLNfDe.png)](https://imgse.com/i/pkLNfDe)

以此类推，请你手动模拟一下后面的部分，如果没有错，模拟完应该是这样的：

[![pkLNIUA.png](https://s21.ax1x.com/2024/07/29/pkLNIUA.png)](https://imgse.com/i/pkLNIUA)

怎么样？自己模拟的对不对？注意如果一个箭头走到了末尾，另一个箭头还要继续走完哦！如果还是不理解可以看一下代码

## 代码实现

```cpp
// a是原序列，t是储物间。
int a[100],t[100];
void mergesort(int l,int r){
    if (l == r) return; // 如果只有一个数就不用排了
    int mid = (l + r) / 2; // 取中间点
    mergesort(l,mid); // 排序左半部分
    mergesort(mid + 1,r); // 排序右半部分
    int tot = 0,i = l,j = mid + 1; // 开始合并，tot表示储物间最后一个被占用的位置
    while (i <= mid && j <= r){
        if (a[i] <= a[j]) t[++tot] = a[i++]; // 如果i指向的数小，那么就把它放入储物间
        else t[++tot] = a[j++]; // 否则就让j指向的数进入储物间
    }
    while (i <= mid) t[++tot] = a[i++]; // 把剩下的部分装进储物间
    while (j <= r) t[++tot] = a[j++]; // 同上
    for (int k = 1;k <= tot;++k) a[l + k - 1] = t[k]; // 把储物间放回到原序列
}
```

# 拓展应用：求逆序对个数

## 原理

逆序对，指数列中的两个数 $a_i  >  a_j$ 并且 $i < j$ 。利用归并排序我们可以以 $\mathcal{O}(n \log(n))$ 的时间复杂度求序列中的逆序对个数。
归并排序在合并过程中，`i`永远小于`j`，这时，如果 $a_i > a_j$ ，说明出现了一组逆序对，而且因为被合并的两个序列是有序的，所以$a_i$ 后面的数也一定大于 $a_j$ ，因此`ans += mid - i + 1`，具体代码如下：

## 代码实现

```cpp
// a是原序列，t是储物间。
int a[100],t[100],ans = 0;
void mergesort(int l,int r){
    if (l == r) return; // 如果只有一个数就不用排了
    int mid = (l + r) / 2; // 取中间点
    mergesort(l,mid); // 排序左半部分
    mergesort(mid + 1,r); // 排序右半部分
    int tot = 0,i = l,j = mid + 1; // 开始合并，tot表示储物间最后一个被占用的位置
    while (i <= mid && j <= r){
        if (a[i] <= a[j]) t[++tot] = a[i++];
        else t[++tot] = a[j++],ans += mid - i + 1; // 如果a[j]更小，那么就是发现了逆序对
    }
    while (i <= mid) t[++tot] = a[i++]; // 把剩下的部分装进储物间
    while (j <= r) t[++tot] = a[j++]; // 同上
    for (int k = 1;k <= tot;++k) a[l + k - 1] = t[k]; // 把储物间放回到原序列
}
```
