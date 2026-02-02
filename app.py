import streamlit as st
import pandas as pd

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Stock Calculator", page_icon="📈")

st.title("📈 Stock Utility Tools")

# สร้าง Tabs เพื่อแยกฟังก์ชันการทำงาน
tab1, tab2 = st.tabs(["📊 คำนวณถัวเฉลี่ย (Avg Cost)", "🧮 คำนวณ % และราคา"])

# ==========================================
# TAB 1: คำนวณต้นทุนเฉลี่ย (Stock Average)
# ==========================================
with tab1:
    st.header("วางแผนซื้อถัวเฉลี่ย / เพิ่มทุน")

    # ส่วนที่ 1: ข้อมูลหุ้นที่มีอยู่เดิม (Portfolio ปัจจุบัน)
    st.subheader("1. พอร์ตปัจจุบัน")
    col1, col2 = st.columns(2)
    with col1:
        current_shares = st.number_input("จำนวนหุ้นที่มี (Shares)", min_value=0.0, value=2.18, step=0.01, format="%.4f")
    with col2:
        current_price = st.number_input("ราคาต้นทุนเดิม (Avg Price)", min_value=0.0, value=670.0, step=0.1)

    # คำนวณต้นทุนเดิม
    current_total_cost = current_shares * current_price
    st.info(f"💰 มูลค่ารวมปัจจุบัน: **{current_total_cost:,.2f} USD**")

    st.divider()

    # ส่วนที่ 2: ข้อมูลการซื้อเพิ่ม (New Buy)
    st.subheader("2. แผนการซื้อเพิ่ม")
    
    # ให้เลือกว่าจะกรอกเป็น "จำนวนหุ้น" หรือ "จำนวนเงิน"
    buy_mode = st.radio("ระบุการซื้อโดย:", ["ระบุจำนวนหุ้น (Shares)", "ระบุจำนวนเงิน (Amount)"], horizontal=True)
    
    col_buy1, col_buy2 = st.columns(2)
    with col_buy1:
        new_buy_price = st.number_input("ราคาที่จะซื้อใหม่ (New Price)", min_value=0.0, value=680.0, step=0.1)
    
    with col_buy2:
        if buy_mode == "ระบุจำนวนหุ้น (Shares)":
            add_shares = st.number_input("จำนวนหุ้นที่จะซื้อเพิ่ม", min_value=0.0, value=1.0, step=0.01)
            add_amount = add_shares * new_buy_price
        else:
            add_amount = st.number_input("จำนวนเงินที่จะซื้อเพิ่ม (USD)", min_value=0.0, value=60.0, step=10.0)
            # คำนวณกลับเป็นจำนวนหุ้น (ถ้าซื้อด้วยเงินก้อนนี้จะได้กี่หุ้น)
            if new_buy_price > 0:
                add_shares = add_amount / new_buy_price
            else:
                add_shares = 0

    if buy_mode == "ระบุจำนวนเงิน (Amount)":
        st.caption(f"💡 ด้วยเงิน {add_amount} USD ที่ราคา {new_buy_price} จะได้หุ้นประมาณ **{add_shares:,.4f} หุ้น**")

    # ส่วนที่ 3: สรุปผล (Calculation)
    st.divider()
    st.subheader("🏁 สรุปผลลัพธ์หลังซื้อเพิ่ม")

    if current_shares + add_shares > 0:
        total_new_shares = current_shares + add_shares
        total_new_cost = current_total_cost + add_amount
        new_average_price = total_new_cost / total_new_shares
        
        # แสดงผลแบบ Metrics เปรียบเทียบ
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric(label="จำนวนหุ้นรวม (Shares)", value=f"{total_new_shares:,.4f}", delta=f"{add_shares:,.4f}")
        with m2:
            st.metric(label="ต้นทุนรวม (Total Cost)", value=f"{total_new_cost:,.2f}", delta=f"{add_amount:,.2f}")
        with m3:
            # ใช้ delta_color="inverse" เพราะถ้าต้นทุนเฉลี่ยเพิ่มขึ้นจะเป็นสีแดง (แย่ลง) ถ้าลดลงเป็นสีเขียว (ดีขึ้น)
            diff = new_average_price - current_price
            st.metric(label="ราคาเฉลี่ยใหม่ (New Avg)", value=f"{new_average_price:,.2f}", delta=f"{diff:,.2f}", delta_color="inverse")

        # ตารางสรุปชัดๆ
        result_data = {
            "รายการ": ["ก่อนซื้อ", "ซื้อเพิ่ม", "หลังซื้อ"],
            "จำนวนหุ้น": [current_shares, add_shares, total_new_shares],
            "ราคา/หุ้น": [current_price, new_buy_price, new_average_price],
            "มูลค่ารวม": [current_total_cost, add_amount, total_new_cost]
        }
        st.table(pd.DataFrame(result_data))
    else:
        st.warning("กรุณากรอกจำนวนหุ้นหรือราคา")


# ==========================================
# TAB 2: คำนวณเปอร์เซ็นต์ (Percentage Calc)
# ==========================================
with tab2:
    st.header("เครื่องคิดเลข ราคา & เปอร์เซ็นต์")

    # ส่วน A: คำนวณราคาเป้าหมายจาก % (เช่น ถ้าราคาลง 2% จะเหลือเท่าไหร่)
    st.subheader("🅰️ หา 'ราคา' จากเปอร์เซ็นต์ (Change %)")
    with st.container(border=True):
        col_a1, col_a2 = st.columns(2)
        with col_a1:
            base_price_a = st.number_input("ราคาเริ่มต้น (Price)", value=20.0, key="base_a")
        with col_a2:
            percent_change = st.number_input("เปลี่ยนแปลงกี่ % (ใส่ลบคือลดลง)", value=-2.0, step=0.5, key="pct_a")
        
        # คำนวณ
        change_amount = base_price_a * (percent_change / 100)
        target_price = base_price_a + change_amount
        
        st.markdown(f"ถ้าราคา **{base_price_a}** เปลี่ยนแปลง **{percent_change}%**")
        st.markdown(f"👉 ราคาจะกลายเป็น: **:green[{target_price:,.2f}]** (เปลี่ยนแปลง {change_amount:,.2f})")

    st.write("") # เว้นวรรค

    # ส่วน B: คำนวณ % จากราคาที่เปลี่ยนไป (เช่น ลงไป 5 USD คิดเป็นกี่ %)
    st.subheader("🅱️ หา 'เปอร์เซ็นต์' จากส่วนต่างราคา (Diff Price)")
    with st.container(border=True):
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            base_price_b = st.number_input("ราคาเริ่มต้น (Price)", value=20.0, key="base_b")
        with col_b2:
            # ให้เลือกกรอกได้ 2 แบบ: ราคาสุดท้าย หรือ จำนวนที่ลดลง
            calc_method = st.radio("เลือกวิธีคำนวณ:", ["ระบุราคาปลายทาง (Target Price)", "ระบุส่วนต่าง (Amount Change)"])
            
        if calc_method == "ระบุราคาปลายทาง (Target Price)":
            target_price_b = st.number_input("ราคาปลายทางที่คาดหวัง", value=15.0, key="target_b")
            diff_amount = target_price_b - base_price_b
        else:
            diff_amount_input = st.number_input("ราคาลดลง/เพิ่มขึ้น กี่ USD (ใส่ลบคือลด)", value=-5.0, key="diff_b")
            diff_amount = diff_amount_input
            target_price_b = base_price_b + diff_amount

        # คำนวณ %
        if base_price_b != 0:
            percent_result = (diff_amount / base_price_b) * 100
        else:
            percent_result = 0

        st.markdown(f"จากราคา **{base_price_b}** ไปที่ **{target_price_b}** (ส่วนต่าง {diff_amount})")
        st.markdown(f"👉 คิดเป็น: **:blue[{percent_result:,.2f}%]**")

