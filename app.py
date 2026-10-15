import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tinh lai tiet kiem", page_icon="🏦", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;700&display=swap');
* { font-family: 'Be Vietnam Pro', sans-serif; }
.stApp { background: linear-gradient(135deg, #e0f7fa 0%, #fff8e1 100%); }
.header-card {
    background: linear-gradient(135deg, #0f766e 0%, #134e4a 100%);
    padding: 24px 28px; border-radius: 20px; color: white;
    margin-bottom: 20px;
}
.input-card {
    background: rgba(255,255,255,0.9);
    border-radius: 20px; padding: 20px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.06);
}
div.stButton > button {
    background: #00897b; color: white;
    font-size: 18px; font-weight: 700;
    border-radius: 12px; width: 100%; height: 50px; border: none;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-card">
    <h1>🏦 So Tiet Kiem Thong Minh</h1>
    <p>Mini App Tai chinh - Ngan hang | Nhom N05</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="input-card">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    von = st.number_input("💵 So tien gui (VND)", min_value=1000000, value=100000000, step=1000000)
    thang = st.selectbox("📅 Ky han (thang)", [1, 3, 6, 9, 12, 18, 24, 36], index=4)

with col2:
    lai = st.number_input("📈 Lai suat (%/nam)", min_value=0.1, max_value=20.0, value=5.0, step=0.1)
    kieu = st.radio("🔁 Loai lai", ["Lai don", "Lai kep"])

tinh = st.button("💰 TINH LAI NGAY")

st.markdown('</div>', unsafe_allow_html=True)

if tinh:
    r = lai / 100.0
    lai_don = von * r * thang / 12
    lai_kep = von * ((1 + r / 12) ** thang - 1)
    tien_lai = lai_don if kieu == "Lai don" else lai_kep
    tong = von + tien_lai

    c1, c2, c3 = st.columns(3)
    c1.metric("Tien gui", f"{von:,.0f}")
    c2.metric("Tien lai", f"{tien_lai:,.0f}")
    c3.metric("Tong nhan", f"{tong:,.0f}")

    st.balloons()

    st.subheader("📊 So sanh lai don va lai kep")
    ds_thang = list(range(0, thang + 1))
    df = pd.DataFrame({
        "Thang": ds_thang,
        "Lai don": [von + von * r * t / 12 for t in ds_thang],
        "Lai kep": [von * (1 + r / 12) ** t for t in ds_thang],
    }).set_index("Thang")
    st.line_chart(df)

    st.info(f"Lai don: {lai_don:,.0f} VND | Lai kep: {lai_kep:,.0f} VND | Chenh lech: {lai_kep - lai_don:,.0f} VND")m **{lai_kep - lai_don:,.0f} VNĐ** so với phương thức còn lại.")
else:
    st.markdown("<br><center style='color:#9ca3af'>👆 Nhập thông tin và bấm Tính lãi để xem kết quả</center>", unsafe_allow_html=True) 
