import streamlit as st

# 1. ตั้งค่าหน้าเพจให้กว้างและ Title เล็กๆ
st.set_page_config(page_title="Quick Calc", layout="centered")

# 2. CSS: ซ่อนปุ่ม +/- และลดช่องว่าง (Padding) ให้ทุกอย่างชิดกัน หน้าเดียวจบ
st.markdown("""
<style>
    /* ซ่อนปุ่ม +/- ของ Number Input */
    button[kind="secondary"] { display: none; }
    div[data-testid="stNumberInputStepUp"] { display: none; }
    div[data-testid="stNumberInputStepDown"] { display: none; }
    
    /* ปรับขนาด Font ให้ใหญ่ เห็นชัด */
    input[type="number"] { font-size: 20px !important; font-weight: bold; color: #333; }
    
    /* ลดช่องว่างระหว่างบรรทัดให้ Compact สุดๆ */
    .block-container { padding-top: 2rem; padding-bottom: 1rem; }
    div[data-testid="column"] { padding: 0px; }
    h3 { margin-bottom: 0px; padding-bottom: 5px; font-size: 18px; }
    p { font-size: 14px; margin-bottom: 2px; }
    
    /* แต่งผลลัพธ์ให้เด่น */
    .result-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-top: 10px;
    }
    .result-val { font-size: 24px; font-weight: bold; color: #0068c9; }
    .result-lbl { font-size: 14px; color: #555; }
</style>
""", unsafe_allow_html=True)

# สร้าง Tabs
tab1, tab2 = st.tabs(["📉 ถัวเฉลี่ยหุ้น", "🔄 คำนวณ % Auto"])

# ==========================================
# TAB 1 : ถัวเฉลี่ย (Layout ตามรูปวาด 1)
# ==========================================
with tab1:
    # --- Row 1: ของเดิม ---
    c1, c2 = st.columns(2)
    with c1:
        st.caption("หุ้นที่มีอยู่ (Share)")
        old_shares = st.number_input("old_s", min_value=0.0, step=0.0, label_visibility="collapsed", key="t1_os")
    with c2:
        st.caption("ทุนเดิม (Price)")
        old_price = st.number_input("old_p", min_value=0.0, step=0.0, label_visibility="collapsed", key="t1_op")

    st.markdown("---") # เส้นขีดคั่นบางๆ

    # --- Row 2: ซื้อเพิ่ม (3 ช่องตามรูป: หุ้น | เงิน | ราคา) ---
    st.caption("🛒 **ถ้าซื้อเพิ่ม** (กรอกช่องไหนก็ได้ ระบบคำนวณให้)")
    
    # ใช้ Session State เพื่อ Link 3 ช่องนี้เข้าด้วยกัน
    if 'buy_shares' not in st.session_state: st.session_state.buy_shares = 0.0
    if 'buy_amount' not in st.session_state: st.session_state.buy_amount = 0.0
    if 'buy_price' not in st.session_state: st.session_state.buy_price = 0.0 if old_price == 0 else old_price

    # Callback functions
    def update_from_shares():
        st.session_state.buy_amount = st.session_state.buy_shares * st.session_state.buy_price
    def update_from_amount():
        if st.session_state.buy_price > 0:
            st.session_state.buy_shares = st.session_state.buy_amount / st.session_state.buy_price
    def update_from_price():
        st.session_state.buy_amount = st.session_state.buy_shares * st.session_state.buy_price

    b1, b2, b3 = st.columns(3)
    with b1:
        st.caption("จำนวนหุ้น")
        st.number_input("add_s", key="buy_shares", step=0.0, label_visibility="collapsed", on_change=update_from_shares)
    with b2:
        st.caption("จำนวนเงิน (USD)")
        st.number_input("add_a", key="buy_amount", step=0.0, label_visibility="collapsed", on_change=update_from_amount)
    with b3:
        st.caption("ราคาที่ซื้อ")
        st.number_input("add_p", key="buy_price", step=0.0, label_visibility="collapsed", on_change=update_from_price)

    # --- Row 3: ผลลัพธ์ (Clean & Big) ---
    st.markdown("### ✨ ต้นทุนจะกลายเป็น")
    
    total_shares = old_shares + st.session_state.buy_shares
    total_cost = (old_shares * old_price) + st.session_state.buy_amount
    avg_price = total_cost / total_shares if total_shares > 0 else 0

    r1, r2 = st.columns(2)
    with r1:
        st.markdown(f"<div class='result-box'><div class='result-val'>{total_shares:,.2f}</div><div class='result-lbl'>หุ้นรวม</div></div>", unsafe_allow_html=True)
    with r2:
        st.markdown(f"<div class='result-box'><div class='result-val'>{avg_price:,.2f}</div><div class='result-lbl'>ต้นทุนเฉลี่ย</div></div>", unsafe_allow_html=True)


# ==========================================
# TAB 2 : คำนวณ % Auto 4 ทิศทาง (ตามรูปวาด 2)
# ==========================================
with tab2:
    # Initialize State
    if 'base' not in st.session_state: st.session_state.base = 100.0
    if 'pct' not in st.session_state: st.session_state.pct = 0.0
    if 'diff' not in st.session_state: st.session_state.diff = 0.0
    if 'final' not in st.session_state: st.session_state.final = 100.0

    # Logic การเชื่อมโยง 4 ช่อง
    def calc_from_base():
        # เปลี่ยนฐาน -> คำนวณส่วนต่างและปลายทางใหม่ (ยึด % เดิม)
        st.session_state.diff = st.session_state.base * (st.session_state.pct / 100)
        st.session_state.final = st.session_state.base + st.session_state.diff

    def calc_from_pct():
        # เปลี่ยน % -> คำนวณส่วนต่างและปลายทาง
        st.session_state.diff = st.session_state.base * (st.session_state.pct / 100)
        st.session_state.final = st.session_state.base + st.session_state.diff

    def calc_from_diff():
        # เปลี่ยน USD -> คำนวณ % และปลายทาง
        if st.session_state.base != 0:
            st.session_state.pct = (st.session_state.diff / st.session_state.base) * 100
        st.session_state.final = st.session_state.base + st.session_state.diff

    def calc_from_final():
        # เปลี่ยนปลายทาง -> คำนวณส่วนต่างและ %
        st.session_state.diff = st.session_state.final - st.session_state.base
        if st.session_state.base != 0:
            st.session_state.pct = (st.session_state.diff / st.session_state.base) * 100

    # --- UI Layout ---
    # Row 1: ราคาปัจจุบัน (Base)
    st.caption("ราคาปัจจุบัน (Base Price)")
    st.number_input("base_inp", key="base", step=0.0, label_visibility="collapsed", on_change=calc_from_base)

    st.write("") # space นิดนึง

    # Row 2: 3 ช่องเรียงกัน ( % | USD | สรุป )
    col_pct, col_diff, col_final = st.columns(3)

    with col_pct:
        st.caption("เปอร์เซ็นต์ %")
        st.number_input("pct_inp", key="pct", step=0.0, label_visibility="collapsed", on_change=calc_from_pct)
    
    with col_diff:
        st.caption("ส่วนต่าง USD")
        st.number_input("diff_inp", key="diff", step=0.0, label_visibility="collapsed", on_change=calc_from_diff)
        
    with col_final:
        st.caption("สรุป/ราคาจบ")
        st.number_input("final_inp", key="final", step=0.0, label_visibility="collapsed", on_change=calc_from_final)

