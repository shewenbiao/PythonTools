# PythonTools
Markdown文件相关操作（标题添加序号；标题添加目录索引），淘宝抢购等


## MarkdownTools

### 介绍

生成目录索引和生成标题编号的脚本主要来自于https://github.com/Higurashi-kagome/pythontools (其中还有其他有意思的脚本）。
在使用原有的生成标题编号的脚本时，发现在同级标题个数>=10的情况下，标题编号错误的问题，于是在原有脚本的基础上修改了该问题。
生成目录索引的脚本在原有脚本的基础上，根据自己的需要，做了稍微改动（比如显示目录分级标志等）。

### 使用

1. 生成标题带编号的文件

```python
python3 markdown_create_title_number.py your_markdown_file
```

执行脚本后，在your_markdown_file的同级目录下会生成一个新文件，新文件是在原有文件名上加了后缀_withNum。比如原有文件是test.md，则标题带编号的文件是test_withNum.md。

2. 生成标题目录索引的文件

```python
python3 markdown_create_title_catalog.py your_markdown_file
```

执行脚本后，在your_markdown_file的同级目录下会生成一个新文件，新文件是在原有文件名上加了后缀_withCatalog。比如原有文件是test.md，则标题带编号的文件是test_withCatalog.md。


另外我们可以配合使用两脚本。先用生成标题编号的脚本生成标题带编号的文件，然后对标题带编号的文件再用生成目录索引的脚本生成标题目录索引的文件。
