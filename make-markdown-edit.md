今天太闲得慌了！开发一个简易的Markdown编辑器吧！

# 准备工作
你需要：
1. 一台电脑💻
2. 一个浏览器🛜
3. 一个可以打`html` + `javascript` + `css`的代码编辑器，也可以是IDE
4. 一颗学习钻研的心

如果以上都准备好了，那么就让我们开始吧！读完本文你将可以获得这样的效果：
![效果图](https://img.doing1024.us.kg/file/65d3500a4138520662153.png)
# 编辑栏
首先我们要实现左边写Markdown源码的部件。

这让我们联想到一个很常见的通用功能：编辑代码。这种需求肯定有轮子🛞可以用的，这里我使用CodeMirror。

## 引入轮子
首先我们引入它的css，在`<head>`和`</head>`之间添加如下代码：
```html
<!--codemirror主文件-->
<link rel="stylesheet" href="https://unpkg.com/codemirror@5.40.0/lib/codemirror.css">
<!--xq-light主题-->
<link rel="stylesheet" href="https://unpkg.com/codemirror@5.40.0/theme/xq-light.css">
```
如果`unpkg.com`访问过慢可以自行更换其他cdn（强烈🧱不推荐🙅jsdelivr，太慢了）

接下来引入它的js，将以下代码添加到`</body>`以后：
```html
<!--codemirror主文件-->
<script src="https://unpkg.com/codemirror@5.40.0/lib/codemirror.js"></script>
<!--markdown代码高亮支持-->
<script src="https://unpkg.com/codemirror@5.40.0/mode/markdown/markdown.js"></script>
```

## 具体实现 

首先我们在`<body>`和`</body>`中新建一个空的`textarea`，里面可以写初始文字，但是为了以后的可拓展性，我们在这里暂时不设置文字：
```html
<textarea id="edit"></textarea>
```
接下来我们编写页面的js，我们将所有的javascript统一写入`script.js`：
```javascript
var editor = CodeMirror.fromTextArea(document.getElementById("edit"),{ // 新建一个CodeMirror实例
    lineNumbers: true, // 启用行号
    mode: "markdown", // Markdown语法高亮
    theme: "xq-light" // xq-light主题

});
var text = 
`任何你想在初始显示的文字，
可以多行`;
editor.setValue(text); // 设置初始文本为text
```
然后在`index.html`中引入`script.js`文件，在`</html>`之前写入以下内容（注意一定要写在其他script标签以后）：
```html
<!--导入javascript-->
<script src="script.js"></script>
```

紧接着我们要把编辑栏设为在左侧占一半的空间，以便给后边的预览窗口留空间，将以下代码写入`style.css`:
```css
.CodeMirror{
    top: 0vh;
    left: 0px;
    position: fixed;
    width: 50vw;
    height: 100vh;
}
```

最后我们要在`index.html`中引入`style.css`，将其写入`<head>`与`</head>`之间:
```html
<!--引入css-->
<link rel="stylesheet" href="style.css"> 
```
现在你可以尝试用浏览器打开`index.html`看看效果了，大概应该长酱紫：
![效果图1](https://img.doing1024.us.kg/file/d9073eb28363d8ab4a541.png)

# 预览栏

接下来我们要实现右侧的预览窗口。

## 导入轮子🛞

首先我们导入css，在`<head>`和`</head>`之间写入如下内容：
```html
<!--导入github-markdown样式-->
<link rel="stylesheet" href="https://unpkg.com/github-markdown-css@5.6.1/github-markdown-light.css">
```
还有js，写到`</body>`以后：
```html
<!--showdown是一个将markdown转为html的库-->
<script src="https://unpkg.com/showdown@2.1.0/dist/showdown.min.js"></script>
```

## 实现

首先新建一个`div`来“盛”预览的内容：
```html
<!-- class="markdown-body"是为了让github-markdown识别到它 -->
<div id="show" class='markdown-body'></div>
```

然后我们写js:
```javascript
var converter = new showdown.Converter({ // 新建showdown转换器
    tables: true, // 支持表格
    extensions: [
        showdownKatex({ // 支持Latex公式
            throwOnError: true, // 公式有错时，是否抛出错误
            displayMode: false, // 如果为false，公式以inline方式渲染
            delimiters: [
                { left: '$$', right: '$$', display: true },
                { left: '$', right: '$', display: false },
                { left: '~', right: '~', display: false, asciimath: true },
            ],
        }),
    ],
});
var showbar = document.getElementById('show');
editor.on('change', (codemirrorIns, codemirrorObj) => { // 改变时的事件
    showbar.innerHTML = converter.makeHtml(editor.getValue()); // 重新生成html填入showbar
});
// 以上内容要写在editor.setValue(text)以前
```
最后写css：
```css
#show{
    width: 50vw;
    height: 100vh;
    position: fixed;
    top: 0vh;
    right: 0px;
    overflow:auto;
}
.katex-html{
    display: none;
}
```
现在你就可以达到文章开头时的效果图啦！自己运行试试吧！

更多效果和功能尽请期待下一篇：[从零开始带你做Markdown编辑器（二）：深色主题](./make-markdown-edit2.md)
