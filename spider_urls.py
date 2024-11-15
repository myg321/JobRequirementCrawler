import time
import json
from selenium import webdriver
from bs4 import BeautifulSoup

# 爬取URL，总函数
def scrape_job_links(job_keyword):
    with open('./data/cities.json', 'r', encoding='utf-8') as f:
        city_dict = json.load(f)

    browser = webdriver.Chrome()  # 创建Chrome浏览器实例
    all_links = []  # 存放一个职位所有链接
    link_50_count = 0  # 初始化计数器

    for city_name, city_code in city_dict.items():
        print(f"正在爬取{city_name}的{job_keyword} URL...")

        # 爬取前5页的数据
        for page_num in range(1, 6):
            url = f"https://www.zhaopin.com/sou/jl{city_code}/kw{job_keyword}/p{page_num}"
            browser.get(url)
            time.sleep(3)   # 等待页面加载完成
            browser.encoding = "utf-8"  # 设置编码

            soup = BeautifulSoup(browser.page_source, "html.parser")
            div_tags = soup.find_all("div", class_='jobinfo__top')
            if div_tags:
                for div_tag in div_tags:
                    job_link = div_tag.find('a')['href']
                    all_links.append(job_link)

                    print(f"=== 爬取中：{city_name} - 第{page_num}页 ===")

                    # 每读取50条数据就写入文件，并重置计数器
                    if len(all_links) % 50 == 0:
                        link_50_count += 1
                        with open(f'./data/output_urls/{job_keyword}_job_links.txt', 'a', encoding='utf-8') as f:
                            for link in all_links:
                                f.write(link + "\n")
                        all_links = []  # 重置存放链接的列表

    # 将剩余的链接写入文件
    with open(f'./data/output_urls/{job_keyword}_job_links.txt', 'a', encoding='utf-8') as f:
        for link in all_links:
            f.write(link + "\n")

    # 打印总共保存了多少条数据
    print(f"=== 共爬取到 {len(all_links) + 50 * link_50_count} 条URL！ ===")

    browser.quit()  # 关闭浏览器


# 调用：
# scrape_job_links("数据挖掘")
