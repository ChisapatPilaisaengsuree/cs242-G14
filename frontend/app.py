import streamlit as st
from components.login import render_login_form # เรียกจากโฟลเดอร์ components

# ตั้งค่าหน้าจอ
st.set_page_config(page_title="RestroomAdmin", layout="centered", initial_sidebar_state="collapsed")

# สร้างคอลัมน์กึ่งกลาง
col1, col2, col3 = st.columns([0.7, 2.6, 0.7])

with col2:
    email, password = render_login_form()
    
    if email and password:
        # ส่วนนี้ให้เพื่อนที่ทำ Backend มาเชื่อม Database ตรงนี้ได้เลย
        if email == "admin@uni.ac.th" and password == "admin1234":
            st.session_state.logged_in = True
            st.switch_page("pages/overview.py")
        else:
            st.error("อีเมลหรือรหัสผ่านไม่ถูกต้อง")