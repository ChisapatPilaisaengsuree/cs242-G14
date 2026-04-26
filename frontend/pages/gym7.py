import sys
from pathlib import Path
import streamlit as st
import pandas as pd

# --- แก้ปัญหา Path ---
root = str(Path(__file__).parent.parent)
if root not in sys.path:
    sys.path.append(root)

from components.card import inject_custom_css
from components.sidebar import render_sidebar

st.set_page_config(layout="wide", initial_sidebar_state="expanded")
inject_custom_css()
render_sidebar()

# --- แก้ไขจุดนี้: ใช้ Session State แทนการสร้างตัวแปร rooms ปกติ ---
if 'rooms_gym7' not in st.session_state:
    st.session_state.rooms_gym7 = [
        {
            "name": "ยิม7 - ชาย", 
            "gender": "♂ ชาย", 
            "usage": 60, 
            "cap": "8 ที่", 
            "status": "ค่อนข้างเต็ม", 
            "color": "#ef6c00", # สีส้ม
            "bg": "#fff3e0"
        },
        {
            "name": "ยิม7 - หญิง", 
            "gender": "♀ หญิง", 
            "usage": 39, 
            "cap": "6 ที่", 
            "status": "ว่าง", 
            "color": "#2e7d32", # สีเขียว
            "bg": "#e8f5e9"
        }
    ]

# --- ส่วนหัว (Header) ---
col_h1, col_h2 = st.columns([5, 4])
with col_h1:
    st.markdown("<div style='font-size: 24px; font-weight: bold; margin-top: 20px; margin-bottom: -5px;'>อาคาร GYM7</div>", unsafe_allow_html=True)
    st.caption("วันอาทิตย์ที่ 26 เมษายน 2569")

with col_h2:
    st.markdown(f"<div style='text-align: right; margin-top: -20px; font-size: 14px; color: gray;'></div>", unsafe_allow_html=True)

st.write("")

# --- ส่วนสรุป (Metric Cards) ---
m1, m2, m3, m4 = st.columns(4)
metrics = [
    {"label": "ว่าง", "val": "1", "unit": "ห้อง", "color": "#2e7d32"},
    {"label": "ค่อนข้างเต็ม", "val": "1", "unit": "ห้อง", "color": "#ef6c00"},
    {"label": "เต็ม", "val": "0", "unit": "ห้อง", "color": "#c62828"},
    {"label": "เฉลี่ยการใช้งาน", "val": "50%", "unit": "วันนี้", "color": "#111"},
]

for i, m in enumerate([m1, m2, m3, m4]):
    with m:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 14px; color: #666;">{metrics[i]['label']}</div>
            <div style="font-size: 28px; font-weight: bold; color: {metrics[i]['color']}; margin: 5px 0;">{metrics[i]['val']}</div>
            <div style="font-size: 12px; color: #999;">{metrics[i]['unit']}</div>
        </div>
        """, unsafe_allow_html=True)

st.write("")

# --- แถบเครื่องมือ: ค้นหา, ฟิลเตอร์ และปุ่มเพิ่มห้องน้ำ ---
col_tool1, col_tool2 = st.columns([1, 1])

with col_tool1:
    st.text_input("ค้นหาห้องน้ำ", placeholder="ค้นหาชื่อห้องน้ำ...", label_visibility="collapsed")

with col_tool2:
    c1, c2, c3, c_add = st.columns([1, 1, 1, 1.5])
    with c1: st.button("ทั้งหมด", use_container_width=True, type="primary")
    with c2: st.button("♂ ชาย", use_container_width=True)
    with c3: st.button("♀ หญิง", use_container_width=True)
    
    with c_add:
        # --- ฟีเจอร์เพิ่มห้องน้ำ (ใช้ Popover เพื่อความสวยงาม) ---
        with st.popover(" เพิ่มห้องน้ำ", use_container_width=True):
            st.markdown("**กรอกข้อมูลห้องน้ำใหม่**")
            new_name = st.text_input("ชื่อห้องน้ำ", placeholder="เช่น SC1 - ชั้น 2 - ชาย")
            new_floor = st.selectbox("ชั้น", ["ชั้น 1", "ชั้น 2", "ชั้น 3", "ชั้น 4"])
            new_gender = st.radio("เพศ", ["ชาย", "หญิง", "รวม"], horizontal=True)
            new_cap = st.number_input("ความจุ (ที่)", min_value=1, value=5)
            
            if st.button("ยืนยันการเพิ่มข้อมูล", use_container_width=True, type="primary"):
                icon = "🚻 " if new_gender == "รวม" else ("♂ " if new_gender == "ชาย" else "♀ ")
                
                # 2. สร้างข้อมูลก้อนใหม่
                new_room = {
                    "name": new_name,
                    "gender": f"{icon} {new_gender}",
                    "usage": 0,  # เพิ่มใหม่ให้เริ่มที่ 0%
                    "cap": f"{new_cap} ที่",
                    "status": "ว่าง",
                    "color": "#2e7d32",
                    "bg": "#e8f5e9"
                }
                
                # 3. เพิ่มลงใน Session State
                st.session_state.rooms_gym7.append(new_room)
                
                st.success(f"เพิ่ม {new_name} เรียบร้อยแล้ว!")
                # 4. สั่ง Rerun เพื่อให้หน้าจออัปเดตข้อมูลใหม่ทันที
                st.rerun()
            else:
                st.error("กรุณากรอกข้อมูลให้ครบถ้วนก่อนยืนยัน")
st.write("")

# --- ตารางแสดงรายการห้องน้ำ ---
# จำลองข้อมูล
rooms = [
    {"name": "ยิม7 - ชาย", "gender": "♂ ชาย", "usage": 60, "cap": "6 ที่", "status": "ค่อนข้างเต็ม", "color": "#ef6c00", "bg": "#fff3e0"},
    {"name": "ยิม7 - หญิง", "gender": "♀ หญิง", "usage": 39, "cap": "6 ที่", "status": "ว่าง", "color": "#2e7d32", "bg": "#e8f5e9"}
]

# ส่วนหัวตาราง
t_col = st.columns([3, 1.5, 3, 1.5, 1.5])
t_headers = ["ชื่อห้องน้ำ", "เพศ", "การใช้งาน", "ความจุ", "สถานะ"]
for i, head in enumerate(t_col):
    head.markdown(f"<div style='font-size: 13px; color: gray; font-weight: bold;'>{t_headers[i]}</div>", unsafe_allow_html=True)

st.divider()

# ข้อมูลในตาราง
for room in st.session_state.rooms_gym7:  # ใช้ข้อมูลจาก Session State
    r_col = st.columns([3, 1.5, 3, 1.5, 1.5])
    r_col[0].write(room['name'])
    r_col[1].markdown(f"<span style='background: #f3f4f6; padding: 2px 8px; border-radius: 5px; font-size: 13px;'>{room['gender']}</span>", unsafe_allow_html=True)
    
    # หลอด Progress ในตาราง
    with r_col[2]:
        st.markdown(f"""
        <div style="background: #eee; height: 8px; border-radius: 4px; margin-top: 10px;">
            <div style="width: {room['usage']}%; background: {room['color']}; height: 8px; border-radius: 4px;"></div>
        </div>
        """, unsafe_allow_html=True)
    
    r_col[3].write(room['cap'])
    r_col[4].markdown(f"<div style='background: {room['bg']}; color: {room['color']}; padding: 2px 10px; border-radius: 10px; text-align: center; font-weight: bold; font-size: 13px;'>{room['status']}</div>", unsafe_allow_html=True)