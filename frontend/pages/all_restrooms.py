import streamlit as st
import pandas as pd
import sys
import requests
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
    from components.edit_modal import show_edit_button
except ImportError:
    st.error("ยังหาโฟลเดอร์ components ไม่เจอ ตรวจสอบการวางไฟล์อีกครั้งนะครับ")

# --- API Configuration ---
API_BASE_URL = "http://localhost:8000/api"

# --- สร้างสถานะการเลือก Filter (ถ้ายังไม่มีให้เป็น 'ทั้งหมด') ---
if 'gender_filter' not in st.session_state:
    st.session_state.gender_filter = "ทั้งหมด"

if 'edit_modal_open' not in st.session_state:
    st.session_state.edit_modal_open = False

if 'editing_id' not in st.session_state:
    st.session_state.editing_id = None

if 'editing_data' not in st.session_state:
    st.session_state.editing_data = None

if 'need_refresh' not in st.session_state:
    st.session_state.need_refresh = False

# เรียกใช้งาน
st.set_page_config(layout="wide", initial_sidebar_state="expanded")
inject_custom_css()
render_sidebar()

# --- ฟังก์ชันสำหรับดึงข้อมูลห้องน้ำจาก API ---
@st.cache_data
def fetch_restrooms():
    """ดึงข้อมูลห้องน้ำทั้งหมดจาก API"""
    try:
        response = requests.get(f"{API_BASE_URL}/restrooms", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"❌ ไม่สามารถดึงข้อมูลห้องน้ำได้: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"❌ ไม่สามารถเชื่อมต่อ API: {str(e)}")
        return []

# แหล่งข้อมูลจาก API
api_data = fetch_restrooms()

# แปลงเป็น DataFrame พร้อม mapping ข้อมูล
def parse_api_data(api_data):
    """แปลงข้อมูลจาก API เป็น DataFrame ที่เหมาะสมสำหรับแสดงผล"""
    type_map = {"male": "ชาย", "female": "หญิง", "disabled": "พิการ", "unisex": "รวม"}
    crowd_map = {"low": 20, "medium": 55, "high": 85}
    status_map = {20: "ว่าง", 55: "ค่อนข้างเต็ม", 85: "เต็ม"}
    
    data = []
    for r in api_data:
        gender = type_map.get(r.get("type", "male"), r.get("type", "")).upper() if r.get("type") != "unisex" else "รวม"
        usage = crowd_map.get(r.get("crowd_level", "low"), 20)
        status = status_map.get(usage, "ไม่ทราบ")
        
        data.append({
            "id": r.get("id"),
            "name": f"{r.get('building')} ชั้น {r.get('floor')}",
            "loc": f"{r.get('building')} · ชั้น {r.get('floor')}",
            "gender": gender,
            "type": r.get("type"),
            "usage": usage,
            "status": status,
            "building": r.get("building"),
            "floor": r.get("floor"),
            "latitude": r.get("latitude"),
            "longitude": r.get("longitude"),
            "crowd_level": r.get("crowd_level"),
        })
    return pd.DataFrame(data) if data else pd.DataFrame()

df = parse_api_data(api_data)

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
        
        # เพิ่มปุ่มแก้ไข
        restroom_data = {
            "building": row["building"],
            "floor": row["floor"],
            "type": row["type"],
            "latitude": row["latitude"],
            "longitude": row["longitude"],
            "crowd_level": row["crowd_level"]
        }
        show_edit_button(row["id"], restroom_data)