# JobRequirementCrawler

![](https://picbed-toootu.oss-cn-wuhan-lr.aliyuncs.com/pics/202411152021688.png)


## 简介

JobRequirementCrawler 是一个基于 Python 的简单 web 应用项目，可以根据用户输入的职位名词，爬取并分析该职位的任职要求信息，并以可个性化的词云形式展示。

## 功能

- 用户输入职位，爬取该职位相关链接，并保存至本地
- 根据链接文件爬取每一个对应网页中的“任职要求”，并保存至本地
- 数据清洗，提取关键词，并生成词云图

![](https://picbed-toootu.oss-cn-wuhan-lr.aliyuncs.com/pics/202411152028729.png)


## 代码结构

该项目包含以下主要文件：

- `spider_urls.py`：负责爬取职位相关链接
- `spider_req.py`：负责爬取职位信息
- `wash_data`：负责清洗数据
- `get_keywords.py`：负责提取关键词并生成词云
- `main.py`：负责创建 Streamlit 应用
- `data/`：存放爬取到的职位信息及生成的词云图

## 引入的包

- `os`
- `sys`
- `selenium`
- `beautifulsoup4`
- `jieba`
- `sklearn.feature_extraction.text`
- `imageio`
- `wordcloud`
- `matplotlib.pyplot`
- `streamlit`

## 使用方法

1. 确保已安装所有上述依赖包。

2.  `main.py` 文件，运行 `streamlit run main.py` 启动应用

3. 在 Streamlit 应用中输入职位，点击 "生成词云" 按钮，等待1h左右时间（或者更长）爬虫，爬虫完毕即可看到生成的词云图。

## 其他说明

- 请确保在使用该应用时，已遵守相关法律法规，不爬取和使用非法信息。
- 该项目仅用于学习和研究目的，不应用于任何商业用途。
