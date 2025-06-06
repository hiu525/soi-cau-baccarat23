
import streamlit as st
import pandas as pd
from collections import Counter

st.set_page_config(page_title="Tool Soi Cầu Baccarat - Dự đoán thông minh", layout="centered")

st.title("🎲 Tool Soi Cầu Baccarat")
st.markdown("Nhập kết quả các ván Baccarat (P = Player, B = Banker) để phân tích soi cầu và **dự đoán thông minh** ván tiếp theo.")

# Nhập kết quả
input_str = st.text_area("🔢 Nhập kết quả (cách nhau bằng dấu phẩy hoặc xuống dòng):", 
                         placeholder="Ví dụ: P, B, P, P, B, B, P...")

if input_str:
    results = [x.strip().upper() for x in input_str.replace("\n", ",").split(",") if x.strip().upper() in ["P", "B"]]

    if results:
        df = pd.DataFrame({
            'Ván': range(1, len(results) + 1),
            'Kết quả': results
        })

        # Phân tích chuỗi cầu
        df['Chuỗi'] = (df['Kết quả'] != df['Kết quả'].shift()).cumsum()
        df['Lặp lại'] = df.groupby('Chuỗi').cumcount() + 1

        st.subheader("📊 Bảng soi cầu")
        st.dataframe(df, use_container_width=True)

        # Thống kê
        count_p = results.count("P")
        count_b = results.count("B")
        total = len(results)
        st.markdown(f"- ✅ Tổng số ván: {total}")
        st.markdown(f"- 🟦 Player thắng: {count_p} ({count_p/total*100:.1f}%)")
        st.markdown(f"- 🟥 Banker thắng: {count_b} ({count_b/total*100:.1f}%)")

        # Dự đoán bằng thống kê chuỗi Markov đơn giản
        transitions = [(results[i], results[i+1]) for i in range(len(results) - 1)]
        transition_counter = Counter(transitions)

        last = results[-1]
        prob_p = transition_counter.get((last, "P"), 0)
        prob_b = transition_counter.get((last, "B"), 0)
        total_trans = prob_p + prob_b

        st.subheader("🧠 Dự đoán thông minh")

        if total_trans > 0:
            percent_p = prob_p / total_trans * 100
            percent_b = prob_b / total_trans * 100
            prediction = "P" if prob_p > prob_b else "B"
            st.success(f"Dự đoán: **{prediction}** với độ tin cậy: 🟦 P = {percent_p:.1f}%, 🟥 B = {percent_b:.1f}%")
        else:
            st.info("Không đủ dữ liệu để dự đoán.")

        # Gợi ý dựa trên chuỗi hiện tại
        last_row = df.iloc[-1]
        if last_row['Lặp lại'] >= 3:
            st.info(f"📈 Cầu bệt {last_row['Kết quả']} đang chạy ({last_row['Lặp lại']} ván) → Có thể theo tiếp.")
        elif last_row['Lặp lại'] == 1 and df.iloc[-2]['Lặp lại'] == 1:
            st.info("🔁 Cầu 1-1 đang xuất hiện → Có thể cược xen kẽ.")
        else:
            st.info("🤔 Không có cầu rõ ràng → Cân nhắc quan sát thêm.")
    else:
        st.warning("⚠️ Không tìm thấy kết quả hợp lệ để phân tích.")
