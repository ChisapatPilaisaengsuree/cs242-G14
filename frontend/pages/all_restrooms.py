import streamlit as st
import pandas as pd
import sys
from pathlib import Path
from datetime import datetime

# --- บรรทัดแก้ปัญหา Error: หาทางกลับไปที่โฟลเดอร์หลัก (frontend) ---
root = str(Path(__file__).parent.parent)
if root not in sys.path:
    sys.path.append(root)

# --- ทีนี้จะ Import ได้อย่างปลอดภัยแล้ว ---
try:
    from components.card import inject_custom_css
    from components.sidebar import render_sidebar
except ImportError:
    st.error("ยังหาโฟลเดอร์ components ไม่เจอ ตรวจสอบการวางไฟล์อีกครั้งนะครับ")

# --- สร้างสถานะการเลือก Filter (ถ้ายังไม่มีให้เป็น 'ทั้งหมด') ---
if 'gender_filter' not in st.session_state:
    st.session_state.gender_filter = "ทั้งหมด"

# เรียกใช้งาน
st.set_page_config(layout="wide", initial_sidebar_state="expanded")
inject_custom_css()
render_sidebar()

# --- ข้อมูลจำลอง ---
data = [
    {"name": "SC1 - ชั้น1 - รวม", "loc": "SC1 · ชั้น 1", "gender": "รวม", "usage": 100, "status": "เต็ม"},
    {"name": "SC2 - ชั้น1 - ชาย", "loc": "SC2 · ชั้น 1", "gender": "ชาย", "usage": 95, "status": "เต็ม"},
    {"name": "บร - ชั้น1 - ชาย", "loc": "บร · ชั้น 1", "gender": "ชาย", "usage": 72, "status": "ค่อนข้างเต็ม"},
    {"name": "ยิม7 - ชาย", "loc": "ยิม7 · ชั้น 1", "gender": "ชาย", "usage": 60, "status": "ค่อนข้างเต็ม"},
    {"name": "ยิม7 - หญิง", "loc": "ยิม7 · ชั้น 1", "gender": "หญิง", "usage": 39, "status": "ว่าง"},
    {"name": "บร - ชั้น2 - หญิง", "loc": "บร · ชั้น 2", "gender": "หญิง", "usage": 20, "status": "ว่าง"},
]
df = pd.DataFrame(data)

# --- ส่วนหัวและฟิลเตอร์ ---
col_t1, col_t2 = st.columns([5, 4]) 

with col_t1:
    # ใช้ค่าเดียวกัน (24px และ -25px) เพื่อให้ระนาบสายตาเท่ากันเป๊ะ
    st.markdown("<div style='font-size: 24px; font-weight: bold; margin-top: 20px; margin-bottom: -5px;'>ห้องน้ำทั้งหมด</div>", unsafe_allow_html=True)
    st.caption("วันอาทิตย์ที่ 26 เมษายน 2569")

with col_t2:
    st.markdown("<div style='margin-top: -5px;'></div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
    
    with c1: 
        st.text_input("ค้นหา", placeholder="ค้นหา...", label_visibility="collapsed")
    
    with c2: 
        # ถ้าเลือก 'ทั้งหมด' ให้ปุ่มเป็นสีเข้ม (primary)
        if st.button("ทั้งหมด", use_container_width=True, 
                     type="primary" if st.session_state.gender_filter == "ทั้งหมด" else "secondary"):
            st.session_state.gender_filter = "ทั้งหมด"
            st.rerun() # สั่งให้หน้าจอวาดใหม่ทันที
            
    with c3: 
        if st.button("♂ ชาย", use_container_width=True,
                     type="primary" if st.session_state.gender_filter == "ชาย" else "secondary"):
            st.session_state.gender_filter = "ชาย"
            st.rerun()
            
    with c4: 
        if st.button("♀ หญิง", use_container_width=True,
                     type="primary" if st.session_state.gender_filter == "หญิง" else "secondary"):
            st.session_state.gender_filter = "หญิง"
            st.rerun()

if st.session_state.gender_filter == "ทั้งหมด":
    display_df = df
else:
    # กรองเอาเฉพาะแถวที่เพศตรงกับที่เลือก
    display_df = df[df['gender'] == st.session_state.gender_filter]
st.write("---")

# ฟังก์ชันสำหรับเปลี่ยนค่า Filter
def set_filter(gender):
    st.session_state.gender_filter = gender

# --- แสดงผล Grid Cards (3 คอลัมน์) ---
cols = st.columns(3)
for i, (index, row) in enumerate(display_df.iterrows()): # ใช้ display_df
    with cols[i % 3]:
        # เลือกสีและไอคอนตามเพศ
        gender_class = "tag-male" if row['gender'] == "ชาย" else "tag-female" if row['gender'] == "หญิง" else "tag-total"
        gender_icon = "♂" if row['gender'] == "ชาย" else "♀" if row['gender'] == "หญิง" else "🚻"
        
        # เลือกสีหลอดและ Badge
        color = "#c62828" if row['usage'] >= 90 else "#ef6c00" if row['usage'] >= 60 else "#2e7d32"
        bg_status = "#ffebee" if row['usage'] >= 90 else "#fff3e0" if row['usage'] >= 60 else "#e8f5e9"

        card_html = f"""
        <div class="restroom-card">
            <div class="card-header">
                <div>
                    <div style="font-weight: bold; font-size: 16px;">{row['name']}</div>
                    <div style="display: flex; gap: 8px; margin-top: 5px; align-items: center;">
                        <span style="font-size: 12px; color: #888;">{row['loc']}</span>
                        <span class="gender-tag {gender_class}">{gender_icon} {row['gender']}</span>
                    </div>
                </div>
            </div>
            <div class="card-progress-bg">
                <div class="card-progress-fill" style="width: {row['usage']}%; background: {color};"></div>
            </div>
            <div class="card-footer">
                <span>{row['usage']}% ใช้งาน</span>
                <span style="background: {bg_status}; color: {color}; padding: 4px 12px; border-radius: 10px; font-weight: bold;">
                    {row['status']}
                </span>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)