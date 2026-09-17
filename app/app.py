"""
Streamlit Demo App - Đề tài 16: Phân nhóm quốc gia theo các yếu tố hạnh phúc (World Happiness Report)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="World Happiness Report - Cluster Explorer",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Khám Phá Phân Nhóm Quốc Gia Theo Báo Cáo Hạnh Phúc")
st.markdown("""
*Ứng dụng demo tương tác phục vụ đồ án môn học **Khai thác dữ liệu** - Nhóm 12.*  
Phân tích và phân nhóm các quốc gia dựa trên 6 trụ cột hạnh phúc (GDP, Hỗ trợ xã hội, Tuổi thọ, Tự do, Hào phóng, Nhận thức tham nhũng).
""")

# Sidebar cấu hình
st.sidebar.header("⚙️ Cấu hình phân tích")
selected_year = st.sidebar.selectbox("Chọn năm dữ liệu:", [2019, 2018, 2017, 2016, 2015], index=0)
selected_algo = st.sidebar.selectbox("Thuật toán gom cụm:", ["K-Means", "Hierarchical Clustering", "DBSCAN"], index=0)
k_clusters = st.sidebar.slider("Số lượng cụm (k):", min_value=2, max_value=8, value=3)

st.info(f"Đang hiển thị chế độ phân tích cho năm **{selected_year}** với thuật toán **{selected_algo}** (k = {k_clusters}).")

# Tab nội dung
tab1, tab2, tab3 = st.tabs(["📊 Tổng quan cụm & Radar Chart", "🗺️ Bản đồ thế giới", "🔍 Tra cứu quốc gia"])

with tab1:
    st.subheader("Profile Đặc Trưng Từng Cụm (Radar Chart)")
    st.write("Tại đây hiển thị biểu đồ Radar so sánh các giá trị trung bình giữa các cụm sau khi mô hình đã được huấn luyện.")
    # Placeholder chart
    categories = ['GDP per Capita', 'Social Support', 'Life Expectancy', 'Freedom', 'Generosity', 'Corruption Perception']
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=[0.8, 0.7, 0.9, 0.6, 0.4, 0.3], theta=categories, fill='toself', name='Cụm 1: Phát triển cao'))
    fig.add_trace(go.Scatterpolar(r=[0.4, 0.5, 0.4, 0.4, 0.2, 0.1], theta=categories, fill='toself', name='Cụm 2: Đang phát triển'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Phân bố cụm trên bản đồ thế giới")
    st.write("Trực quan hóa vị trí địa lý của các quốc gia theo màu sắc của từng cụm hạnh phúc.")

with tab3:
    st.subheader("Tra cứu và gán cụm cho quốc gia")
    country_input = st.text_input("Nhập tên quốc gia (ví dụ: Vietnam, Norway, Japan):", value="Vietnam")
    st.write(f"Kết quả phân tích chi tiết cho quốc gia: **{country_input}** sẽ được hiển thị khi kết nối dữ liệu hoàn chỉnh.")
