import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Tính lãi tiết kiệm", page_icon="🏦", layout="centered")

# --- CSS SIÊU ĐẸP ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;700&display=swap');
* { font-family: 'Be Vietnam Pro', sans-serif; }

.stApp {
    background: radial-gradient(circle at 20% 30%, #a7f3d0 0%, transparent 40%),
                radial-gradient(circle at 80% 70%, #fef3c7 0%, transparent 40%),
                linear-gradient(180deg, #f0fdfa 0%, #ffffff 100%);
}

.block-container { padding-top: 2rem; }

.header-card {
    background: linear-gradient(135deg, #0f766e 0%, #134e4a 100%);
    padding: 28px 32px; border-radius: 24px; color: white;
    box-shadow: 0 20px 40px rgba(15, 118, 110, 0.25);
    margin-bottom: 24px;
}
.header-card h1 { color: white !important; margin: 0; font-size: 28px; text-align: left; }
.header-card p { opacity: 0.85; margin: 6px 0 0 0; }

.input-card {
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(0,0,0,0.05);
    border-radius: 20px; padding: 24px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.06);
}

div.stButton > button {
    background: linear-gradient(135deg, #0d9488 0%, #0f766e 100%);
    color: white; font-size: 18px; font-weight: 700;
    border-radius: 14px; width: 100%; height: 52px; border: none;
    box-shadow: 0 8px 20px rgba(13, 148, 136, 0.35);
    transition: all 0.2s ease;
}
div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 28px rgba(13, 148, 136, 0.45);
    background: linear-gradient(135deg, #0f766e 0%, #115e59 100%);
}

.result-card {
    background: white; border-radius: 16px; padding: 18px;
    text-align: center; border: 1px solid #f0fdfa;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
.result-card .label { font-size: 13px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px; }
.result-card .value { font-size: 20px; font-weight: 700; color: #134e4a; margin-top: 4px;}
.result-card.highlight {
    background: linear-gradient(135deg, #ccfbf1 0%, #fef9c3 100%);
    border: 1px solid #99f6e0;
}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div class="header-card">
    <h1>🏦 Sổ Tiết Kiệm Thông Minh</h1>
    <p>Mini App Tài chính - Ngân hàng | Nhóm N05 • Tính lãi chính xác đến từng đồng</p>
</div>
""", unsafe_allow_html=True)

# --- INPUT ---
st.markdown('<div class="input-card">', unsafe_allow_html=True)
col1, col2 = st.columns(2, gap="large")
with col1:
    von = st.number_input("💵 Số tiền gửi (VNĐ)", min_value=0, value=100_000_000, step=1_000_000, format="%d")
    thang = st.select_slider("📅 Kỳ hạn", options=[1, 3, 6, 9, 12, 18, 24, 36], value=12)
with col2:
    lai = st.number_input("📈 Lãi suất (%/năm)", min_value=0.0, value=5.0, step=0.1)
   kieu = st.radio("🔁 Phương thức tính", ["Lãi đơn", "Lãi kép"], horizontal=True)

st.write("")
tinh = st.button("💰 TÍNH LÃI NGAY")
st.markdown('</div>', unsafe_allow_html=True)

if tinh:
    r = lai / 100
    lai_don = von * r * thang / 12
    lai_kep = von * ((1 + r / 12) ** thang - 1)
    tien_lai = lai_don if kieu == "Lãi đơn" else lai_kep
    tong = von + tien_lai

    st.markdown("<br>", unsafe_allow_html=True)
    # --- KẾT QUẢ DẠNG CARD ---
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="result-card"><div class="label">Tiền gửi</div><div class="value">{von:,.0f} đ</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="result-card"><div class="label">Tiền lãi</div><div class="value">+ {tien_lai:,.0f} đ</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="result-card highlight"><div class="label">Tổng nhận</div><div class="value">{tong:,.0f} đ</div></div>', unsafe_allow_html=True)
    
    st.balloons()

    # --- BIỂU ĐỒ ĐẸP HƠN ---
    st.markdown("#### 📊 Tăng trưởng theo thời gian")
    ds_thang = list(range(0, thang + 1))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ds_thang, y=[von + von * r * t / 12 for t in ds_thang],
                             mode='lines+markers', name='Lãi đơn', line=dict(color='#94a3b8', width=2, dash='dash')))
    fig.add_trace(go.Scatter(x=ds_thang, y=[von * (1 + r / 12) ** t for t in ds_thang],
                             mode='lines+markers', name='Lãi kép', 
                             line=dict(color='#0d9488', width=3), fill='tozeroy', fillcolor='rgba(13,148,136,0.1)'))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10,r=10,t=10,b=10), height=320,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        font=dict(family="Be Vietnam Pro")
    )
    st.plotly_chart(fig, use_container_width=True)

    st.success(f"**Phân tích:** Với {kieu.lower()}, bạn lãi thêm **{lai_kep - lai_don:,.0f} VNĐ** so với phương thức còn lại.")
else:
    st.markdown("<br><center style='color:#9ca3af'>👆 Nhập thông tin và bấm Tính lãi để xem kết quả</center>", unsafe_allow_html=True) 
