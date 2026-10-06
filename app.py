import streamlit as st

st.title("Tính lãi tiền gửi tiết kiệm")

von = st.number_input("Số tiền gửi (VNĐ)", min_value=0, value=100_000_000, step=1_000_000)
thang = st.selectbox("Kỳ hạn (tháng)", [1, 3, 6, 9, 12, 18, 24, 36])
lai = st.number_input("Lãi suất (%/năm)", min_value=0.0, value=5.0, step=0.1)
kieu = st.radio("Loại lãi", ["Lãi đơn", "Lãi kép"])

if st.button("Tính"):
    r = lai / 100
    if kieu == "Lãi đơn":
        tien_lai = von * r * thang / 12
    else:
        tien_lai = von * ((1 + r / 12) ** thang - 1)
    st.success(f"Tiền lãi: {tien_lai:,.0f} VNĐ")
    st.info(f"Tổng nhận cuối kỳ: {von + tien_lai:,.0f} VNĐ")
