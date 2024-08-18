闲来无事，play python，今天准备搞个百度热搜榜爬虫玩玩，记录下开发过程。
![爬虫](https://img.doing1024.us.kg/file/5817633a2489dbdfe2415.jpg)

# 准备工作

首先需要安装轮子🛞，在终端运行如下代码（假如你已经将python添加到path）

```bash
python -m pip install requests beautifulsoup4 lxml
```

PS: 如果是`MacOS`/`Linux`则将`python`替换为`python3`.

# 获得网页内容

首先我们导入刚才安装好的`requests`来获得网页内容。

```python
import requests
```

然后就可以开始获取内容了。

百度热搜榜的网址：[https://top.baidu.com/board?tab=realtime](https://top.baidu.com/board?tab=realtime)

代码：

```python
url = "https://top.baidu.com/board?tab=realtime"  # 指定百度热搜榜网址

response = requests.get(url) # 向url发送GET请求

content = response.text # 获得html内容
```

怎么样？第一部分是不是很简单？接下来我们来处理这些获得到的内容。

# 处理内容

首先还是导入轮子🛞：

```python
from bs4 import BeautifulSoup as bs
```

然后我们要定义一个解析器`soup`：

```python
soup = bs(content, "lxml") # 定义解析器，内容为刚才获得的html，引擎使用lxml
```

接下来我们需要 ”观察“ 热搜榜网页，寻找规律。

首先用浏览器打开百度热搜榜网址，然后右键 -> 检查，你就会看到侧面（下面）有一堆代码，这就是刚才`content`里面内容的来源了。然后我们按`Ctrl + Shift + C`，这时你会发现鼠标在网页的任何地方浮动，都会有地方变色，这时，我们控制鼠标，让第一条热搜变色，像这样：
![这样](https://img.doing1024.us.kg/file/1d64741823b585660a9c4.png)

这时我们注意右侧的一堆代码，发现有一个`<div class="category-wrap_iQLoo horizontal_1eKyQ"> ... </div>`被的背景变成了浅蓝色，这就是我们刚才选中的那条热搜对应的代码，这里简单科普一下`html`，让你能看懂刚才那段东西。

> 在html中，所有“组件”被称为“元素”，`<div>`表示div元素的开始，`</div>`表示这个元素的结束，就像括号一样，两两匹配。`<div somethings> ... </div>`中somethings的位置填写这个元素的设置，像姓啥、名啥、小名是啥、多少岁啦、男的女的都在这里面配置。`...`的位置是元素里面的内容，两个眼睛一个鼻子一个嘴巴两个耳朵什么的...😄

现在回到刚才的`<div class="category-wrap_iQLoo horizontal_1eKyQ"> ... </div>`，我们发现背景高亮的这一行下面还有很多一模一样的。再来看他的属性`class`，你可以把它理解为这些元素“所属的班级”，他们可以身处不同位置，通过班级名字把他们召唤到一起😅。一个元素可以身处很多班级，一个班级也可以有很多人，一个人所属的班级在`class`属性中以空格隔开。既然所有热搜的班级都一样，只要找这个班级里的所有元素，就是所有的热搜条目了。

在`python`中我们可以这样实现：

```python
top_list = soup.find_all("div",attrs={"class": "category-wrap_iQLoo"})
# 详细解释：soup.find_all 返回一个类似于列表的object,div指必须为div元素，attrs为筛选条件，网页中的class被空格分开了，我们选其中一个就可以了。
```

回到百度热搜网页，还是看刚才选中的背景高亮的代码，点击代码左侧小三角展开代码，继续不停展开，像这样（由于屏幕大小原因，我折叠了一部分无关内容，你可以全部展开）：
![](https://img.doing1024.us.kg/file/6db2cbfd97f0242f80d85.png)

我们主要需要两条信息：标题和热搜指数（排名可以通过循环变量递增获得）。通过观察可得，热搜指数在`class`为`hot-index_1Bl1a`的元素中，标题的`class`则为`c-single-text-ellipsis`，根据这些信息，我们就可以获取到所需数据了，参考代码：

```python
for i in range(len(top_list)):
    top = top_list[i]
    title = top.find_all("div",attrs = {"class": "c-single-text-ellipsis"}).get_text().strip()  # get_text用于获取元素中的文本，strip用于去掉头尾空格
    hotindex = top.find_all("div", attrs = {"class": "hot-index_1Bl1a"})[0].get_text().strip() # 同上
    print(f"第{i + 1}名，标题：{title}，热搜指数：{hotindex}")
```

现在运行代码就可以获得所有热搜啦！

# 附：生成表格的简单方法

有的同学可能想生成表格，这里简单提供一个方法：

```python
with open("baidutop.csv",mode="w") as f: # csv文件也是一种表格文件，可以用excel直接打开
    print("列1,列2,列3",file=f) # csv文件每行的列用英文逗号分开，按照这样的原则替换刚才的代码即可。
```
