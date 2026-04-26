import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.title(" RestroomAdmin")
        st.divider()
        
        st.markdown("**หลัก**")
        # ใช้ st.page_link เพื่อให้กดสลับหน้าใน Streamlit ได้ (ต้องมีไฟล์ในโฟลเดอร์ pages)
        st.page_link("pages/overview.py", label="ภาพรวม")
        st.button("ห้องน้ำทั้งหมด (8)", use_container_width=True)
        st.button("การแจ้งเตือน (3)", use_container_width=True)
        st.button("รายงาน", use_container_width=True)
        
        st.markdown("**อาคาร**")
        buildings = ["SC1", "SC2", "SC3", "ยิม7", "บร"]
        for b in buildings:
            st.button(f" {b}", use_container_width=True)
            
        st.markdown("**ตั้งค่า**")
        st.button("จัดการผู้ใช้", use_container_width=True)
        st.button("ระบบ", use_container_width=True)