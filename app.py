import streamlit as st

# ตั้งค่าหน้าเว็บให้ดูคลีนๆ
st.set_page_config(page_title="Simple Calculator", layout="centered")

# CSS ปรับแต่งให้ตัวหนังสือใหญ่ อ่านง่าย เหมือนในรูป
st.markdown("""
<style>
    .big-font { font-size: 24px !important; font-weight: bold; color: #4CAF50; }
    .label-font { font-size: 18px !important; font-weight: bold; }
    div[data-testid="stMetricValue"] { font-size: 30px !important; }
</style>
""", unsafe_allow_html=True)

st.title("เครื่องคิดเลขหุ้น 📉")

tab1, tab2 = st.tabs(["💵 คำนวณต้นทุน (DCA)", "➗ คำนวณเปอร์เซ็นต์"])

# ==========================================
# ส่วนที่ 1 : คำนวณต้นทุนเฉลี่ย (ตามรูปแรก)
# ==========================================
with tab1:
    st.markdown("### 1. ของเดิมที่มี")
    c1, c2 = st.columns(2)
    with c1:
        old_shares = st.number_input("หุ้นที่มีอยู่ (Share)", min_value=0.0, step=1.0, format="%.4f")
    with c2:
        old_price = st.number_input("ต้นทุนต่อหุ้นเดิม (Price)", min_value=0.0, step=0.1, format="%.2f")

    st.divider()
    
    st.markdown("### 2. ถ้าซื้อเพิ่ม")
    
    # เลือกโหมดก่อน ว่าจะซื้อด้วย "จำนวนเงิน" หรือ "จำนวนหุ้น"
    buy_mode = st.radio("ระบุการซื้อโดย:", ["ระบุจำนวนเงิน (USD)", "ระบุจำนวนหุ้น (Share)"], horizontal=True)
    
    b1, b2 = st.columns(2)
    with b1:
        new_price = st.number_input("ราคาที่จะซื้อใหม่ (New Price)", min_value=0.0, value=old_price, step=0.1)
    
    with b2:
        if "จำนวนเงิน" in buy_mode:
            amount_input = st.number_input("ใส่จำนวนเงิน (USD)", min_value=0.0, step=100.0)
            # คำนวณกลับเป็นหุ้น
            new_shares = amount_input / new_price if new_price > 0 else 0
        else:
            new_shares = st.number_input("ใส่จำนวนหุ้น (Share)", min_value=0.0, step=1.0)
            amount_input = new_shares * new_price

    # --- ส่วนแสดงผลลัพธ์ (Show Result) ---
    st.divider()
    st.markdown("<p class='label-font'>✨ ต้นทุนจะกลายเป็น</p>", unsafe_allow_html=True)
    
    total_shares = old_shares + new_shares
    total_cost = (old_shares * old_price) + amount_input
    avg_price = total_cost / total_shares if total_shares > 0 else 0

    r1, r2 = st.columns(2)
    with r1:
        st.metric(label="มีหุ้นรวมทั้งหมด (หุ้น)", value=f"{total_shares:,.4f}")
    with r2:
        st.metric(label="ต้นทุนเฉลี่ยต่อหุ้น (Avg)", value=f"{avg_price:,.2f}")


# ==========================================
# ส่วนที่ 2 : คำนวณเปอร์เซ็นต์ (Automation)
# ==========================================
with tab2:
    st.markdown("### คำนวณราคา ↔ เปอร์เซ็นต์")

    # เก็บค่าลงตัวแปรกลาง (Session State) เพื่อให้แก้ช่องไหน อีกช่องก็เปลี่ยนตาม
    if 'target_price' not in st.session_state: st.session_state.target_price = 0.0
    if 'pct' not in st.session_state: st.session_state.pct = 0.0

    # 1. ราคาตั้งต้น
    base_price = st.number_input("ราคาปัจจุบัน (Base Price)", value=100.0, step=0.1)

    # ฟังก์ชันคำนวณ (Callback Functions)
    def on_pct_change():
        # เมื่อแก้ %, ให้ไปแก้ราคา
        st.session_state.target_price = base_price + (base_price * st.session_state.pct / 100)

    def on_price_change():
        # เมื่อแก้ราคา, ให้ไปแก้ %
        if base_price > 0:
            st.session_state.pct = ((st.session_state.target_price - base_price) / base_price) * 100

    st.write("---")
    
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        # ช่องกรอก %
        st.number_input(
            "ระบุ เปอร์เซ็นต์ (+/-)", 
            key="pct", 
            step=1.0, 
            on_change=on_pct_change  # เมื่อพิมพ์เสร็จ ให้เรียกฟังก์ชันคำนวณราคา
        )

    with col_p2:
        # ช่องกรอก ราคา
        st.number_input(
            "ระบุ ราคาเป้าหมาย (+/-)", 
            key="target_price", 
            step=0.5, 
            on_change=on_price_change # เมื่อพิมพ์เสร็จ ให้เรียกฟังก์ชันคำนวณ %
        )

    # แสดงผลสรุปด้านล่างอีกทีให้ชัดเจน
    st.info(f"จากราคา {base_price:,.2f} ถ้าเปลี่ยนแปลง {st.session_state.pct:.2f}% ราคาจะเป็น {st.session_state.target_price:,.2f}")
