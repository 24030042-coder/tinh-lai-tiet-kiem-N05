import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tính lãi tiết kiệm", page_icon="🏦", layout="centered")

# ---------- Giao diện ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;700&display=swap');

/* Chỉ áp font cho chữ, không đụng tới font icon của Streamlit */
html, body, .stApp, p, h1, h2, h3, h4, label, li,
div[data-testid="stMetricValue"], div[data-testid="stMetricLabel"],
.stButton button, .stRadio label, .stSelectbox label, .stNumberInput label {
    font-family: 'Be Vietnam Pro', sans-serif;
}

.stApp { background: linear-gradient(135deg, #e0f7fa 0%, #fff8e1 100%); }

.header-card {
    background: linear-gradient(135deg, #0f766e 0%, #134e4a 100%);
    padding: 24px 28px; border-radius: 20px;
    margin-bottom: 20px;
}
.header-card h1, .header-card p { color: white !important; margin: 0; }
.header-card p { opacity: 0.85; margin-top: 6px; }

/* Khung chứa ô nhập (st.container có viền) */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,0.9);
    border-radius: 20px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.06);
}

div.stButton > button {
    background: #00897b; border: none;
    border-radius: 12px; width: 100%; height: 50px;
}
div.stButton > button p { color: white !important; font-size: 18px; font-weight: 700; }
div.stButton > button:hover { background: #00796b; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-card">
    <h1>🏦 Sổ Tiết Kiệm Thông Minh</h1>
    <p>Mini App Tài chính - Ngân hàng | Nhóm N05</p>
</div>
""", unsafe_allow_html=True)


def vnd(x: float) -> str:
    """Định dạng tiền kiểu Việt Nam: 100.000.000 đ"""
    return f"{x:,.0f}".replace(",", ".") + " đ"


# ---------- Nhập liệu ----------
with st.container(border=True):
    col1, col2 = st.columns(2)

    with col1:
        von = st.number_input(
            "💵 Số tiền gửi (VNĐ)", min_value=1_000_000, value=100_000_000, step=1_000_000
        )
        thang = st.selectbox("📅 Kỳ hạn (tháng)", [1, 3, 6, 9, 12, 18, 24, 36], index=4)

    with col2:
        lai = st.number_input(
            "📈 Lãi suất (%/năm)", min_value=0.1, max_value=20.0, value=5.0, step=0.1
        )
        kieu = st.radio("🔁 Loại lãi", ["Lãi đơn", "Lãi kép"], horizontal=True)

    rut_truoc = st.checkbox("⏪ So sánh nếu rút trước hạn")
    if rut_truoc and thang > 1:
        c_a, c_b = st.columns(2)
        thang_rut = c_a.slider("Số tháng thực gửi", 1, thang - 1, max(1, thang // 2))
        lai_kkh = c_b.number_input(
            "Lãi suất không kỳ hạn (%/năm)", min_value=0.0, max_value=2.0, value=0.1, step=0.05
        )
    elif rut_truoc:
        st.caption("Kỳ hạn 1 tháng không có lựa chọn rút trước hạn để so sánh.")
        rut_truoc = False

    tinh = st.button("💰 TÍNH LÃI NGAY")
    # ---------- Kết quả ----------
if tinh:
    r = lai / 100.0
    lai_don = von * r * thang / 12
    lai_kep = von * ((1 + r / 12) ** thang - 1)
    tien_lai = lai_don if kieu == "Lãi đơn" else lai_kep
    tong = von + tien_lai

    st.subheader("📋 Kết quả")
    c1, c2, c3 = st.columns(3)
    c1.metric("Tiền gửi", vnd(von))
    c2.metric("Tiền lãi", vnd(tien_lai))
    c3.metric("Tổng nhận", vnd(tong))

    if rut_truoc:
        lai_rut = von * (lai_kkh / 100.0) * thang_rut / 12
        st.warning(
            f"⏪ Nếu rút sau {thang_rut} tháng (lãi không kỳ hạn {lai_kkh}%/năm): "
            f"nhận lãi **{vnd(lai_rut)}**, tổng **{vnd(von + lai_rut)}**. "
            f"Thiệt hơn giữ đủ kỳ hạn: **{vnd(tien_lai - lai_rut)}**."
        )

    st.subheader("📊 So sánh lãi đơn và lãi kép")
    ds_thang = list(range(0, thang + 1))
    df = pd.DataFrame({
        "Tháng": ds_thang,
        "Lãi đơn": [von + von * r * t / 12 for t in ds_thang],
        "Lãi kép": [von * (1 + r / 12) ** t for t in ds_thang],
    }).set_index("Tháng")
    st.line_chart(df)
    st.caption("Biểu đồ luôn vẽ cả hai cách tính để so sánh. Lãi kép giả định lãi nhập vốn hàng tháng.")

    st.info(
        f"Lãi đơn: {vnd(lai_don)} | Lãi kép: {vnd(lai_kep)} | "
        f"Chênh lệch: {vnd(lai_kep - lai_don)}"
    )

    with st.expander("📑 Xem bảng chi tiết từng tháng"):
        bang = df.copy()
        bang["Lãi đơn"] = bang["Lãi đơn"].map(vnd)
        bang["Lãi kép"] = bang["Lãi kép"].map(vnd)
        st.dataframe(bang, use_container_width=True)

    st.caption("⚠️ Kết quả mang tính tham khảo. Thực tế ngân hàng thường tính lãi theo số ngày/365.")
