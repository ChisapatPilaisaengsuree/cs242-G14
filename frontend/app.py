import streamlit as st

# 1. ตั้งค่าหน้าจอ
st.set_page_config(page_title="RestroomAdmin - Login", layout="centered", initial_sidebar_state="collapsed")

# 2. คลีน CSS ใหม่ทั้งหมด (สวย คม ใช้ง่าย)
st.markdown("""
    <style>
    /* ซ่อน UI เดิมของ Streamlit */
    [data-testid="stSidebar"], [data-testid="stHeader"], [data-testid="stToolbar"] {
        display: none !important;
    }

    /* พื้นหลังหน้าจอ: สีเทาอ่อนเรียบๆ */
    .stApp {
        background-color: #f3f4f6 !important;
    }

    /* ล็อคหน้าจอไม่ให้เลื่อน */
    html, body, [data-testid="stAppViewContainer"] {
        overflow: hidden !important;
        height: 100vh !important;
    }

    /* --- จัดการกรอบ Login ให้สวยและเหลือกรอบเดียว --- */
    [data-testid="stColumn"]:nth-of-type(2) {
        background-color: white !important;
        border: 3px solid #111827 !important; /* กรอบดำหนากำลังดี */
        border-radius: 24px !important;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1) !important;
        padding: 60px 30px !important;
        margin-top: 0 ; /* ขยับลงมาให้กึ่งกลางจอ */
    }

    /* ลบกรอบซ้ำซ้อนภายในออก */
    [data-testid="stVerticalBlock"] {
        gap: 0rem !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: none !important;
    }

    /* ปรับแต่งช่องกรอกข้อมูลให้มินิมอล */
    .stTextInput input {
        border: 2px solid #e5e7eb !important;
        border-radius: 12px !important;
        padding: 12px !important;
        background-color: #f9fafb !important;
        transition: all 0.2s;
    }
    .stTextInput input:focus {
        border-color: #111827 !important;
        background-color: white !important;
    }
    .stTextInput label {
        color: #374151 !important;
        font-weight: 600 !important;
        margin-bottom: 8px !important;
    }

    /* จัดปุ่มไปทางขวาและทำให้ดูพรีเมียม */
    div.stButton {
        display: flex;
        justify-content: flex-end;
        margin-top: 25px;
    }
    div.stButton > button {
        background-color: #111827 !important;
        color: white !important;
        padding: 0 45px !important;
        border-radius: 12px !important;
        height: 50px !important;
        font-weight: bold !important;
        border: none !important;
        transition: transform 0.2s;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        background-color: #1f2937 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. ส่วนแสดงผล UI
# ใช้สัดส่วน 1:2:1 เพื่อให้กล่อง Login อยู่ตรงกลางพอดี
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # --- ไม่ต้องใส่ border=True ใน container แล้ว ---
    with st.container(): 
        # ส่วนหัว (Typography สวยๆ)
        st.markdown("<h2 style='text-align: center; margin-top: 10px; color: #111827; font-weight: 800; letter-spacing: -1px;'>RestroomAdmin</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #6b7280; font-size: 14px; margin-bottom: 40px;'>ระบบจัดการห้องน้ำส่วนกลางมหาวิทยาลัย</p>", unsafe_allow_html=True)
        
        # ฟอร์มกรอกข้อมูล
        email = st.text_input("อีเมล", placeholder="admin@uni.ac.th")
        password = st.text_input("รหัสผ่าน", type="password", placeholder="••••••••")
        
        # ปุ่มเข้าสู่ระบบ
        if st.button("เข้าสู่ระบบ"):
            if email == "admin@uni.ac.th" and password == "admin1234":
                st.success("กำลังพาคุณเข้าสู่ระบบ...")
                st.switch_page("pages/overview.py")
            else:
                st.error("ข้อมูลไม่ถูกต้อง กรุณาลองใหม่")
        
        # Footer เล็กๆ
        st.markdown("<div style='text-align: center; margin-top: 40px; color: #9ca3af; font-size: 12px;'>ทดสอบ: admin@uni.ac.th • รหัส admin1234</div>", unsafe_allow_html=True)