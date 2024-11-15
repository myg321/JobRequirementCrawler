from sklearn.feature_extraction.text import TfidfVectorizer
import jieba
from imageio import imread
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import os
import sys


# 提取关键词
def extract_keywords(data):
    
    sentences = [line.strip() for line in data if line.strip()]
    sent_words = [" ".join(jieba.cut(sent0)) for sent0 in sentences]

    # 创建TF-IDF向量化器，并拟合数据
    tv = TfidfVectorizer(use_idf=True, smooth_idf=True, norm='l1')
    tv_fit = tv.fit_transform(sent_words)

    # 特征名称 (词)
    feature_names = tv.get_feature_names_out()
    # 获取TF-IDF权重矩阵 (二维数组)
    weights = tv_fit.toarray()

    # 字典 存储每个特征的最大TF-IDF值
    feature_TFIDF = {}
    for i in range(len(weights)):
        for j in range(len(feature_names)):
            if feature_names[j] not in feature_TFIDF:
                feature_TFIDF[feature_names[j]] = weights[i][j]
            else:
                feature_TFIDF[feature_names[j]] += weights[i][j]

    # 归一化TF-IDF值
    for word in feature_TFIDF:
        feature_TFIDF[word] /= len(weights)

    # 将TF-IDF值从大到小排序
    featureList = sorted(feature_TFIDF.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    return featureList

# 生成词云
def generate_wordcloud(keywords, job_keyword, mask_path, font_name):
    words = " ".join([kw[0] for kw in keywords])
    mask = imread(mask_path) 
    os.environ['FONT_PATH'] = r'C:\Users\Joseph\AppData\Local\Microsoft\Windows\Fonts'  # 系统字体文件夹
    font_path = os.path.join(os.environ['FONT_PATH'], font_name)

    wc = WordCloud(
        scale=4,
        background_color="white",
        max_words=2000,
        font_path=font_path, 
        mask=mask
    )
    wc.generate(words)
 
    # 提取模板图片各部分的颜色
    image_colors = ImageColorGenerator(mask)

    # 显示原生词云图、按模板图片颜色的词云图和模板图片，按左、中、右显示
    fig, axes = plt.subplots(1, 3)
    # 最左边的图片显示原生词云图
    axes[0].imshow(wc)
    # 中间的图片显示按模板图片颜色生成的词云图，采用双线性插值的方法显示颜色
    axes[1].imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
    # 右边的图片显示模板图片
    axes[2].imshow(mask, cmap=plt.cm.gray)
    for ax in axes:
        ax.set_axis_off()
    plt.show()

    # 给词云对象按模板图片的颜色重新上色
    wc_color = wc.recolor(color_func=image_colors)
    wc_color.to_file(f"./data/output_wordcloud/{job_keyword}.png")

# 总函数，提取关键词并生成词云
def process_keywords(job_keyword, mask_path, font_name):
    # 读取清洗后的数据文件
    try:
        with open(f'./data/output_washed/{job_keyword}_cleaned_data.txt', 'r', encoding='utf-8') as file:
            data = file.readlines()
    except FileNotFoundError:
        print(f"文件 {job_keyword}_cleaned_data.txt 未找到...")
        sys.exit(1)

    # 提取关键词
    keywords = extract_keywords(data)
    
    print('TF-IDF排名前100的：')
    for i in range(100):
        print(keywords[i][0], keywords[i][1])
    
    # 生成词云
    generate_wordcloud(keywords[:100], job_keyword, mask_path, font_name)
    print(f"词云已生成，已保存至 ./data/output_wordcloud/{job_keyword}.png")


# 调用：
# process_keywords("数据挖掘")