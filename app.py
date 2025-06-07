
import streamlit as st
import pandas as pd
import random
import altair as alt
from collections import Counter

st.set_page_config(page_title="Tool Soi Cầu Baccarat", layout="wide")

# Sidebar - Nhập dữ liệu & tùy chọn
with st.sidebar:
    st.title("🎯 Soi Cầu Baccarat")
    raw_input = st.text_area("🔢 Nhập chuỗi kết quả (P, B, T cách nhau bằng dấu phẩy):", height=150)
    filter_option = st.selectbox("📂 Lọc lịch sử theo:", ["Tất cả", "Player", "Banker", "Tie"])
    predict_button = st.button("🔮 Dự đoán tiếp theo")
    st.markdown("---")
    st.markdown("💡 Ghi chú soi cầu:")
    user_note = st.text_area("✏️ Nhập ghi chú cho chuỗi này", height=100)

# Hàm xử lý dữ liệu
def parse_input(data):
    return [x.strip().upper() for x in data.split(",") if x.strip().upper() in ["P", "B", "T"]]

def filter_history(data, option):
    if option == "Tất cả":
        return data
    mapping = {"Player": "P", "Banker": "B", "Tie": "T"}
    return [x for x in data if x == mapping[option]]

def count_streaks(data):
    if not data: return []
    streaks = []
    current = data[0]
    count = 1
    for x in data[1:]:
        if x == current:
            count += 1
        else:
            streaks.append((current, count))
            current = x
            count = 1
    streaks.append((current, count))
    return streaks

def smart_predict(data):
    if not data: return "Không đủ dữ liệu"
    last = data[-1]
    counts = Counter(data[-10:])  # thống kê 10 ván gần nhất
    if counts["P"] > counts["B"]:
        return "Player"
    elif counts["B"] > counts["P"]:
        return "Banker"
    elif last == "T":
        return random.choice(["Player", "Banker"])  # sau Tie thường không rõ xu hướng
    return random.choice(["Player", "Banker", "Tie"])

# Phân tích
parsed_data = parse_input(raw_input)
filtered_data = filter_history(parsed_data, filter_option)

# Giao diện chính
st.title("🧠 Phân Tích & Dự Đoán Baccarat")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📜 Lịch sử kết quả")
    st.write(f"Tổng số: {len(filtered_data)} kết quả sau lọc")
    st.write(filtered_data)

    if parsed_data:
        st.subheader("📊 Biểu đồ tỷ lệ")
        df_counts = pd.DataFrame(Counter(parsed_data).items(), columns=["Kết quả", "Số lần"])
        chart = alt.Chart(df_counts).mark_bar().encode(
            x=alt.X('Kết quả', sort=["P", "B", "T"]),
            y='Số lần',
            color='Kết quả'
        ).properties(width=300)
        st.altair_chart(chart)

        st.subheader("📈 Chuỗi liên tiếp")
        streaks = count_streaks(parsed_data)
        df_streaks = pd.DataFrame(streaks, columns=["Kết quả", "Số lần"])
        st.dataframe(df_streaks)

with col2:
    st.subheader("🔮 Dự đoán thông minh")
    if predict_button:
        prediction = smart_predict(parsed_data)
        st.success(f"✅ Ván tiếp theo có thể là: **{prediction}**")
    else:
        st.info("⏳ Nhấn nút 'Dự đoán tiếp theo' để xem kết quả")

    st.subheader("📝 Ghi chú của bạn")
    if raw_input and user_note:
        st.write("📌 Ghi chú đã lưu:")
        st.code(user_note)
    elif raw_input:
        st.info("Bạn có thể nhập ghi chú bên sidebar")

st.markdown("---")
st.caption("© 2025 Tool soi cầu Baccarat thông minh - by bạn và ChatGPT")
