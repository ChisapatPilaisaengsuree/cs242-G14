import streamlit as st

def render_sidebar():
    with st.sidebar:
        # ใช้ markdown แทน title เพื่อให้ปรับตำแหน่งให้ตรงกับหน้าหลักได้ง่ายขึ้น
        st.markdown("<h2 style='margin-top:0; padding-top:0;'>RestroomAdmin</h2>", unsafe_allow_html=True)
        st.divider()
        
        st.markdown("**หลัก**")
        # เปลี่ยนปุ่มทั้งหมดเป็น st.page_link
        st.page_link("pages/overview.py", label="ภาพรวม")
        
        # ใส่ชื่อไฟล์ให้ตรงกับที่คุณตั้งไว้ (เช่น pages/all_restrooms.py)
        st.page_link("pages/all_restrooms.py", label="ห้องน้ำทั้งหมด (8)")
        
        # หน้าอื่นๆ ถ้ายังไม่มีไฟล์จริง ให้ใส่ '#' ไว้ก่อน หรือคอมเมนต์ไว้ครับ
        st.page_link("pages/overview.py", label="การแจ้งเตือน (3)", disabled=True) 
        st.page_link("pages/overview.py", label="รายงาน", disabled=True)
        
        st.markdown("**อาคาร**")
        buildings = ["SC1", "SC2", "SC3", "ยิม7", "บร"]
        for b in buildings:
            # สมมติว่ามีหน้าแยกรายอาคาร
            st.page_link("pages/overview.py", label=f" {b}")
            
        st.markdown("**ตั้งค่า**")
        st.page_link("pages/overview.py", label="จัดการผู้ใช้")
        st.page_link("pages/overview.py", label="ระบบ")