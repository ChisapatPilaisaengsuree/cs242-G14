import streamlit as st

def render_sidebar():
    with st.sidebar:
        # ใช้ markdown แทน title เพื่อให้ปรับตำแหน่งให้ตรงกับหน้าหลักได้ง่ายขึ้น
        st.markdown("<h2 style='margin-top:0; padding-top:0;'>🚻 ToiletFinder</h2>", unsafe_allow_html=True)
        st.divider()
        
        st.markdown("**หลัก**")
        st.page_link("pages/overview.py", label="ภาพรวม")
        st.page_link("pages/all_restrooms.py", label="ห้องน้ำทั้งหมด (8)")
        st.page_link("pages/reports.py", label="รายงาน")
        
        st.markdown("**อาคาร**")
        st.page_link("pages/sc1.py", label="SC1")
        st.page_link("pages/sc2.py", label="SC2")
        st.page_link("pages/sc3.py", label="SC3")
        st.page_link("pages/gym7.py", label="ยิม7")
        st.page_link("pages/boro.py", label="บร")
            
        st.markdown("**ตั้งค่า**")
        st.page_link("pages/overview.py", label="ระบบ")