import os
import time
import sys
from selenium import webdriver
from bs4 import BeautifulSoup

# 配置选项
options = webdriver.ChromeOptions()
# 忽略证书错误
options.add_argument('--ignore-certificate-errors')
# 忽略 Bluetooth: bluetooth_adapter_winrt.cc:1075 Getting Default Adapter failed. 错误
options.add_experimental_option('excludeSwitches', ['enable-automation'])
# 忽略 DevTools listening on ws://127.0.0.1... 提示
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# 总函数
def scrape_job_requirements(job_keyword):

    # 检查文件是否存在
    file_path = f"./data/output_urls/{job_keyword}_job_links.txt"
    if os.path.exists(file_path):
        print(f"正在爬取 {job_keyword} 的职位要求...")
        spider_content(job_keyword)
    else:
        print(f"请先运行 spider-urls.py 获取 {job_keyword}_job_links.txt 文件 :)")

# 爬取职位描述
def spider_content(job_keyword):

    browser = webdriver.Chrome(options=options)    # 创建Chrome浏览器实例

    try:
        with open(f'./data/output_urls/{job_keyword}_job_links.txt', 'r', encoding='utf-8') as link_file:
            links = link_file.readlines()
    except FileNotFoundError:
        print(f"文件 {job_keyword}_job_links.txt 未找到...")
        sys.exit(1)

    job_requirements = []    # 存储任职要求的列表
    save_interval = 50       # 设置每爬取50条数据就保存一次
    count = 0                # 爬取计数器

    for link in links:
        link = link.strip()
        browser.get(link)
        time.sleep(3)  # 等待页面加载，可根据实际情况调整
        soup = BeautifulSoup(browser.page_source, "html.parser")

        # 查找包含职位描述的div
        description_div = soup.find('div', class_='describtion__detail-content') or soup.find('div', class_='job-info__desc job-info__desc-mt12')
        if description_div:
            description_text = description_div.get_text(separator='\n')
            # 查找职位要求相关关键字的位置
            start_index = -1
            for keyword in ["职位要求", "任职要求", "岗位要求", "任职资格", "Requirements", "我们需要你"]:
                index = description_text.find(keyword)
                if index != -1 and (start_index == -1 or index < start_index):
                    start_index = index
            if start_index != -1:
                # 提取任职要求部分内容
                job_requirement_text = description_text[start_index:].strip()
                job_requirements.append(job_requirement_text)
                count += 1  # 更新计数器

                print(f"=== 爬取中：({count%50}) /50 (第 {count//50} 轮)===")
                # print(job_requirement_text + "\n")

                # 每爬取50条数据，就写入文件
                if count % save_interval == 0:
                    with open(f'./data/output_reqs/{job_keyword}_job_reqs.txt', 'a', encoding='utf-8') as f:
                        for requirement in job_requirements:
                            f.write(f"{requirement}\n")
                    job_requirements.clear()  # 清空列表，准备存储下一批数据

    # 保存剩余的职位要求（如果有的话）
    if job_requirements:
        with open(f'./data/output_reqs/{job_keyword}_job_reqs.txt', 'a', encoding='utf-8') as f:
            for requirement in job_requirements:
                f.write(f"{requirement}\n")

    print(f"=== 爬取完成，共爬取 {count} 条数据 ===")

    browser.quit()   # 关闭浏览器


# 调用：
# scrape_job_requirements("数据挖掘")
