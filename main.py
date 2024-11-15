import os
import streamlit as st
from spider_urls import scrape_job_links
from spider_req import scrape_job_requirements
from wash_data import clean_requirements_file
from get_keywords import process_keywords
import time

def main():
    st.set_page_config(page_title="求职需求爬爬爬")

    st.title("🧑‍💻求职需求爬爬爬 - 词云版")
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <p style="margin-bottom:0; font-style: italic;">
        爬虫来源：<a href="https://www.zhaopin.com/">智联招聘</a><br>
        项目作者：@Tutu</p>
    """, unsafe_allow_html=True)

    # 间隔线
    st.markdown("---")

    # 搜索框和按钮
    left, right = st.columns([5,1])

    job_keyword = left.text_input("请输入要爬取的职位关键词", "", placeholder="职位关键字")
    right.markdown('<div style="height: 34px;"></div>', unsafe_allow_html=True)
    button = right.button("生成词云")
    # 错误消息占位符
    error_placeholder = st.empty()

    # 检查是否点击按钮且没有输入关键词
    if button and not job_keyword:
        error_placeholder.error("请输入职位关键词!")
        time.sleep(2)
        error_placeholder.empty()
    else:
        error_placeholder.empty()
    
    st.markdown("<br>", unsafe_allow_html=True)

    # 字体选择（所列字体均为我本地PC中字体）
    font_option = st.selectbox("选择词云字体", ("PingFangSC-Medium.otf", "PingFangSC-Light.otf", "PingFangSC-Semibold.otf", "HYZhengYuan-55W.ttf", "MiSans VF.ttf", 
                                            "OPPOSans-B.ttf", "OPPOSans-L.ttf", "OPPOSans-R.ttf", "HarmonyOS_Sans_SC_Thin.ttf", "HarmonyOS_Sans_SC_Medium.ttf", "HarmonyOS_Sans_SC_Black.ttf"), index=0)
    st.markdown("<br>", unsafe_allow_html=True)

    if 'save_path' not in st.session_state:
        st.session_state.save_path = None

    # 上传背景图片
    uploaded_file = st.file_uploader("自定义词云背景图片（白底为佳）", type=["jpg", "png", "jpeg", "webp"])
    if uploaded_file:
        col1, col2, col3 = st.columns(3)
        with col2:
            # 图片居中显示
            st.image(uploaded_file, caption="预览", width=200)
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        save_dir = os.path.join(current_dir, "data/image")
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, uploaded_file.name)
        st.write(f"{save_path}")

        if button:
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.session_state.save_path = save_path

    # 按钮触发爬虫过程
    if button and job_keyword:
        st.markdown("<br>", unsafe_allow_html=True)

        # 检查所需文件是否存在
        if all([
            os.path.exists(f'./data/output_reqs/{job_keyword}_job_reqs.txt'),
            os.path.exists(f'./data/output_urls/{job_keyword}_job_links.txt'),
            os.path.exists(f'./data/output_washed/{job_keyword}_cleaned_data.txt')
        ]):
            with st.spinner('正在生成词云... 请稍等'):
                # 直接生成词云
                process_keywords(job_keyword, st.session_state.save_path, font_option)
            st.success(f"词云已生成，已保存至 ./data/output_wordcloud/{job_keyword}.png")
        else:
            with st.spinner('正在爬取职位信息... 请稍等'):
                # 爬取职位链接
                scrape_job_links(job_keyword)

                # 爬取职位要求
                scrape_job_requirements(job_keyword)

                # 清洗数据
                clean_requirements_file(job_keyword)

                # 生成关键词并生成词云
                process_keywords(job_keyword, st.session_state.save_path, font_option)

            st.success(f"爬取完成，词云已生成，已保存至 ./data/output_wordcloud/{job_keyword}.png")
        
        wordcloud_path = f"./data/output_wordcloud/{job_keyword}.png"
        if os.path.exists(wordcloud_path):
            col1, col2, col3 = st.columns(3)
            with col2:
                # 图片居中显示
                st.image(wordcloud_path, caption="词云图展示", use_container_width=True)


    st.markdown("---")
    st.write("📌推荐以下词云背景图")
    # 预置词云背景图片流
    image_urls = [
        "./data/image/chiikawa.webp",
        "./data/image/pink_flower_emoji.jpg",
        "./data/image/moon.jpg",
        "./data/image/pink_cake.jpg",
        "./data/image/pink_telephone.png",
        "./data/image/shaun_the_sheep.jpg",
        "./data/image/strawberry.jpg",
        "./data/image/pixel_star.jpg",
        "./data/image/white_green_flower.jpg",
        "./data/image/tutu.jpg",
        "./data/image/record.jpg"
    ]

    if 'clicked_image' not in st.session_state:
        st.session_state.clicked_image = None

    # 创建两列布局
    col1, col2 = st.columns(2)

    # 遍历图片URL列表
    for i, url in enumerate(image_urls):
        # 根据索引决定将图片放在哪一列
        column = col1 if i % 2 == 0 else col2
        
        with column:
        # 创建一个容器来包装图片和隐藏的按钮
            container = st.container()
            caption = os.path.splitext(os.path.basename(url))[0]
            
            # 显示图片
            container.image(url, caption=caption, use_container_width=True)
            
            # 创建按钮
            if st.session_state.clicked_image == i:
                if st.button("已选择", key=f"btn_{i}", type="primary"):
                    st.session_state.clicked_image = None
            else:
                if st.button("使用图片", key=f"btn_{i}"):
                    st.session_state.clicked_image = i
                    st.write(f"已选择图片地址: {url}")
                    st.session_state.save_path = url
                
    # 添加CSS来调整按钮样式
    st.markdown("""
    <style>
        .stButton > button {
            width: 100%;
            margin-top: -15px;
        }
    </style>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
