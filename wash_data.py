import re
import jieba
import sys

# from nltk.corpus import stopwords
# # 加载英文停用词
# stop_words_en = set(stopwords.words('english'))

# 定义中文停用词列表，包含无意义的词以及与职业要求不相关的词
stop_words_cn = []

# 加载中文停用词
with open('./data/stop_words_cn.txt', 'r', encoding='utf-8') as file:
    for line in file:
        stop_words_cn.append(line.strip())

# 清洗文本函数
def clean_text(text):
    # 分词（使用jieba分词）
    words = jieba.cut(text)
    # 转换为小写并处理特殊字符
    words = [re.sub(r'[^\w\s]', '', word.lower()) for word in words]
    # 去除停用词（中英文）和保留词
    words = [word for word in words if word not in stop_words_cn]
    # 去除条目数字（中文数字、顿号、英文点、右括号等）
    words = [re.sub(r'^[0-9一二三四五六七八九十]+[\.、）)]?', '', word) for word in words]
    # 去除若干空格
    words = [word for word in words if word.strip() != '']
    # 返回单词列表
    return words

# 总函数，清洗职位要求
def clean_requirements_file(job_keyword):
    try:
        with open(f'./data/output_reqs/{job_keyword}_job_reqs.txt', 'r', encoding='utf-8') as file, \
            open(f'./data/output_washed/{job_keyword}_cleaned_data.txt', 'w', encoding='utf-8') as outfile:
            lines = file.readlines()
            current_text = ""
            count = 0
            ignore_lines = False  # 添加一个标志来忽略行

            for line in lines:
                line = line.strip()
                if line.startswith(("职位要求", "任职要求", "岗位要求", "任职资格", "Requirements", "我们需要你")):
                    if current_text:
                        cleaned_words = clean_text(current_text)
                        count += 1
                        print(f"=== 清洗中：{count%50} /50 (第 {count//50 + 1} 轮) ===")
                        print(' '.join(cleaned_words))  # 将单词列表连接成字符串以便打印
                        outfile.write(' '.join(cleaned_words) + '\n')  # 将单词列表连接成字符串后写入文件
                        current_text = ""
                        if count % 50 == 0:
                            outfile.flush()  # 刷新输出缓冲区
                    ignore_lines = False  # 重置忽略标志
                elif line.startswith(("职位福利", "职位亮点", "福利", "薪酬", "薪资")):
                    ignore_lines = True  # 设置忽略标志
                elif line and not ignore_lines:  # 如果不是空行且未被忽略
                    current_text += " " + line
                else:
                    print(f"=== 忽略：{line} ===")
                    continue

            # 处理最后一段文本
            if current_text:
                cleaned_words = clean_text(current_text)
                outfile.write(' '.join(cleaned_words) + '\n')

    except FileNotFoundError:
        print(f"文件 {job_keyword}_job_reqs.txt 未找到...")
        sys.exit(1)
        
    print(f"=== 清洗完成，共计 {count} 条数据！===")

# 调用：
# clean_requirements_file("数据挖掘")