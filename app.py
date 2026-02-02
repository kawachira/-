import streamlit as st

# ตั้งค่าหน้าเพจ
st.set_page_config(page_title="Pro Stock Calc", layout="centered")

# CSS:
# 1. ซ่อนปุ่ม +/- (Stepper)
# 2. จัดการ Input ให้เป็นช่องว่างๆ สะอาดๆ
st.markdown("""
<style>
    /* ซ่อนปุ่ม +/- ของ Streamlit */
    button[kind="secondary"] { display: none !important; }
    div[data-testid="stNumberInput"] > div > div > div:nth-child(2) { display: none !important; }
    
    /* ปรับ Input ให้ตัวใหญ่ อ่านง่าย */
    input[type="number"] { 
        font-size: 22px !important; 
        font-weight: 500; 
        color: #333;
        padding-left: 10px !important;
        -moz-appearance: textfield; /* Firefox remove arrows */
    }
    /* Chrome/Safari remove arrows */
    input::-webkit-outer-spin-button,
    input::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }

    /* จัด Layout ให้ Compact */
    .block-container { padding-top: 2rem; }
    div[data-testid="column"] { padding: 0 5px; }
    label { font-size: 16px !important; font-weight: bold; }
    
    /* กล่องผลลัพธ์ */
    .result-box {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        margin-top: 15px;
    }
    .result-val { font-size: 28px; font-weight: bold; color: #2E86C1; }
    .result-lbl { font-size: 14px; color: #666; }
</style>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📉 ถัวเฉลี่ยหุ้น", "🔄 คำนวณ % Auto"])

# ฟังก์ชันแปลง None เป็น 0.0 เพื่อใช้คำนวณ
def val(v):
    return v if v is not None else 0.0

# ==========================================
# TAB 1 : ถัวเฉลี่ย (จัดเรียงใหม่ตามสั่ง)
# ==========================================
with tab1:
    # --- ส่วนที่ 1: ของเดิม (วางคู่กัน) ---
    st.write("### 1. พอร์ตปัจจุบัน")
    c1, c2 = st.columns(2)
    with c1:
        # value=None ทำให้ช่องเริ่มต้นเป็นค่าว่าง
        old_shares = st.number_input("จำนวนหุ้นที่ถือ", value=None, placeholder="จำนวนหุ้น", step=1.0)
    with c2:
        old_price = st.number_input("ต้นทุนต่อหุ้น", value=None, placeholder="ราคาเดิม", step=0.01)

    st.write("---")

    # --- ส่วนที่ 2: ซื้อเพิ่ม (3 ช่อง เชื่อมกัน) ---
    st.write("### 2. ถ้าซื้อเพิ่ม")
    
    # Session State สำหรับการเชื่อม 3 ช่อง (เริ่มเป็น None เพื่อให้ว่าง)
    if 'buy_s' not in st.session_state: st.session_state.buy_s = None
    if 'buy_a' not in st.session_state: st.session_state.buy_a = None
    # ดึงราคาเดิมมาเป็นค่าตั้งต้นของราคาซื้อใหม่ (ถ้ามี) หรือปล่อยว่าง
    if 'buy_p' not in st.session_state: 
        st.session_state.buy_p = None 

    # Logic: ถ้าแก้ช่องหนึ่ง อีกช่องเปลี่ยน
    def on_share_change():
        s = val(st.session_state.buy_s)
        p = val(st.session_state.buy_p)
        if s > 0 and p > 0: st.session_state.buy_a = s * p
        elif s == 0: st.session_state.buy_a = None

    def on_amt_change():
        a = val(st.session_state.buy_a)
        p = val(st.session_state.buy_p)
        if p > 0: st.session_state.buy_s = a / p
    
    def on_price_change():
        s = val(st.session_state.buy_s)
        p = val(st.session_state.buy_p)
        if s > 0: st.session_state.buy_a = s * p

    b1, b2, b3 = st.columns(3)
    with b1:
        st.number_input("จำนวนหุ้น", key="buy_s", value=None, placeholder="หุ้น", step=1.0, on_change=on_share_change)
    with b2:
        st.number_input("จำนวนเงิน (USD)", key="buy_a", value=None, placeholder="เงินรวม", step=10.0, on_change=on_amt_change)
    with b3:
        st.number_input("ราคาที่ซื้อ", key="buy_p", value=None, placeholder="ราคา", step=0.01, on_change=on_price_change)

    # --- ส่วนแสดงผล ---
    # จะคำนวณก็ต่อเมื่อมีการกรอกข้อมูลอย่างน้อยบางส่วน
    total_shares = val(old_shares) + val(st.session_state.buy_s)
    total_cost = (val(old_shares) * val(old_price)) + val(st.session_state.buy_a)
    
    avg_price = 0.0
    if total_shares > 0:
        avg_price = total_cost / total_shares

    # แสดงผลเมื่อมีข้อมูล
    if total_shares > 0:
        st.markdown("### ✨ ต้นทุนจะกลายเป็น")
        r1, r2 = st.columns(2)
        with r1:
            st.markdown(f"<div class='result-box'><div class='result-val'>{total_shares:,.2f}</div><div class='result-lbl'>หุ้นรวม</div></div>", unsafe_allow_html=True)
        with r2:
            st.markdown(f"<div class='result-box'><div class='result-val'>{avg_price:,.2f}</div><div class='result-lbl'>ต้นทุนเฉลี่ย</div></div>", unsafe_allow_html=True)


# ==========================================
# TAB 2 : คำนวณ % Auto (เริ่มแบบว่างเปล่า)
# ==========================================
with tab2:
    st.write("### คำนวณราคา ↔ เปอร์เซ็นต์")

    # Init State เป็น None
    if 'base' not in st.session_state: st.session_state.base = None
    if 'pct' not in st.session_state: st.session_state.pct = None
    if 'diff' not in st.session_state: st.session_state.diff = None
    if 'final' not in st.session_state: st.session_state.final = None

    # Logic การคำนวณ (เช็ค None ก่อนคำนวณเสมอ)
    def calc_all(source):
        base = val(st.session_state.base)
        
        if source == 'base':
            # เปลี่ยนฐาน -> คำนวณใหม่โดยยึด % เดิม (ถ้ามี)
            pct = val(st.session_state.pct)
            st.session_state.diff = base * (pct / 100)
            st.session_state.final = base + st.session_state.diff
            
        elif source == 'pct':
            # เปลี่ยน % -> คำนวณเงิน
            pct = val(st.session_state.pct)
            st.session_state.diff = base * (pct / 100)
            st.session_state.final = base + st.session_state.diff
            
        elif source == 'diff':
            # เปลี่ยนเงิน -> คำนวณ %
            diff = val(st.session_state.diff)
            if base != 0: st.session_state.pct = (diff / base) * 100
            st.session_state.final = base + diff
            
        elif source == 'final':
            # เปลี่ยนราคาจบ -> คำนวณเงินและ %
            final = val(st.session_state.final)
            st.session_state.diff = final - base
            if base != 0: st.session_state.pct = (st.session_state.diff / base) * 100

    # UI
    st.number_input("ราคาปัจจุบัน (Base Price)", key="base", value=None, placeholder="ใส่ราคาตั้งต้น...", step=0.1, on_change=calc_all, args=('base',))
    
    st.write("") 
    
    col_pct, col_diff, col_final = st.columns(3)
    with col_pct:
        st.number_input("เปอร์เซ็นต์ %", key="pct", value=None, placeholder="%", step=1.0, on_change=calc_all, args=('pct',))
    with col_diff:
        st.number_input("ส่วนต่าง USD", key="diff", value=None, placeholder="USD", step=0.1, on_change=calc_all, args=('diff',))
    with col_final:
        st.number_input("ราคาจบ", key="final", value=None, placeholder="Price", step=0.1, on_change=calc_all, args=('final',))

