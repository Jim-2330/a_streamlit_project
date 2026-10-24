import streamlit as st
from paddleocr import PaddleOCR
import numpy as np
from PIL import Image



# 页面基础配置
st.set_page_config(
    page_title="智能图片转文字工具",
    page_icon="📷",
    layout="centered"
)

st.title("📷 智能图片转文字系统")
st.markdown("---")

# 初始化 PaddleOCR 引擎（使用缓存避免重复加载）
@st.cache_resource
def load_ocr():
    return PaddleOCR(use_angle_cls=True, lang='ch', show_log=False)

with st.spinner("正在加载本地 OCR 引擎..."):
    ocr = load_ocr()

# 文件上传组件
uploaded_file = st.file_uploader("选择或拖拽图片到这里（支持 PNG、JPG、JPEG）", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    # 读取并展示图片
    image = Image.open(uploaded_file)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("原始图片")
        st.image(image, width="stretch")

    with col2:
        st.subheader("操作面板")
        run_ocr = st.button("🚀 开始提取文字", type="primary", width="stretch")

    if run_ocr:
        with st.spinner("AI 正在疯狂识别中..."):
            # 将 PIL 转换为 OpenCV 格式 (numpy array)
            img_np = np.array(image)

            # 执行 OCR 识别（移除了不支持的 cls=True 参数）
            result = ocr.ocr(img_np)

            extracted_text = []
            if result and result[0]:
                for line in result[0]:
                    extracted_text.append(line[1][0])

                final_result = "\n".join(extracted_text)
            else:
                final_result = "未在图中检测到有效文字。"

        st.success("识别成功！")

        # 结果展示与文本框
        st.subheader("📝 提取结果")
        st.text_area("您可以直接复制以下文本：", value=final_result, height=200)

        # 提供下载按钮
        st.download_button(
            label="💾 保存为文本文件",
            data=final_result,
            file_name="extracted_text.txt",
            mime="text/plain"
        )
