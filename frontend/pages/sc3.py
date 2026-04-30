import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import requests

# --- แก้ปัญหา Path ---
root = str(Path(__file__).parent.parent)
if root not in sys.path:
    sys.path.append(root)

from components.card import inject_custom_css
from components.sidebar import render_sidebar

st.set_page_config(layout="wide", initial_sidebar_state="expanded")
inject_custom_css()
render_sidebar()

# --- ใช้ Session State สำหรับห้องน้ำที่เพิ่มใน local (เก่า) ---
if 'rooms_sc3' not in st.session_state:
    st.session_state.rooms_sc3 = []

# --- ตั้งค่า API URL ---
API_URL = "http://localhost:8000/api"

# --- ฟังก์ชันดึงข้อมูลห้องน้ำจาก API ---
@st.cache_data(ttl=5)
def get_restrooms_from_api():
    """ดึงข้อมูลห้องน้ำทั้งหมดจาก API"""
    try:
        res = requests.get(f"{API_URL}/restrooms", timeout=5)
        if res.status_code == 200:
            return res.json()
        else:
            st.error("❌ ไม่สามารถดึงข้อมูลจาก API")
            return []
    except Exception as e:
        st.error(f"❌ เชื่อมต่อ API ไม่ได้: {str(e)}")
        return []

# --- ฟังก์ชันสร้างห้องน้ำใหม่ผ่าน API ---
def create_restroom(building: str, floor: int, room_type: str, lat: float, lng: float, crowd: str):
    """สร้างห้องน้ำใหม่ผ่าน API"""
    try:
        payload = {
            "building": building,
            "floor": floor,
            "type": room_type,
            "latitude": lat,
            "longitude": lng,
            "crowd_level": crowd
        }
        res = requests.post(f"{API_URL}/restrooms", json=payload, timeout=5)
        if res.status_code == 200:
            return True, res.json()
        else:
            return False, res.json() if res.text else "Unknown error"
    except Exception as e:
        return False, str(e)

# --- ฟังก์ชันแปลงประเภทห้องน้ำ ---
def map_gender(room_type: str):
    mapping = {"male": "♂ ชาย", "female": "♀ หญิง", "disabled": "♿ คนพิการ"}
    return mapping.get(room_type, room_type)

def get_status_info(crowd_level: str):
    """ส่งคืน status, สี, และพื้นหลัง"""
    mapping = {
        "low": ("ว่าง", "#2e7d32", "#e8f5e9"),
        "medium": ("ค่อนข้างเต็ม", "#ef6c00", "#fff3e0"),
        "high": ("เต็ม", "#c62828", "#ffebee")
    }
    return mapping.get(crowd_level.lower(), ("ไม่ทราบ", "#888", "#f5f5f5"))

# --- ส่วนหัว (Header) ---
col_h1, col_h2 = st.columns([5, 4])
with col_h1:
    st.markdown("<div style='font-size: 24px; font-weight: bold; margin-top: 20px; margin-bottom: -5px;'>อาคาร SC3</div>", unsafe_allow_html=True)
    st.caption("วันอาทิตย์ที่ 26 เมษายน 2569")

with col_h2:
    st.markdown(f"<div style='text-align: right; margin-top: -20px; font-size: 14px; color: gray;'></div>", unsafe_allow_html=True)

st.write("")

# --- ดึงข้อมูลห้องน้ำจาก API ---
all_restrooms = get_restrooms_from_api()

# --- กรองเฉพาะห้องน้ำใน SC3 ---
sc3_restrooms = [r for r in all_restrooms if r.get("building") == "SC3"]

# --- คำนวณสถิติ ---
available_count = sum(1 for r in sc3_restrooms if r.get("crowd_level") == "low")
medium_count = sum(1 for r in sc3_restrooms if r.get("crowd_level") == "medium")
crowded_count = sum(1 for r in sc3_restrooms if r.get("crowd_level") == "high")
avg_usage = (crowded_count * 3 + medium_count * 1.5) / len(sc3_restrooms) * 100 if sc3_restrooms else 0

# --- ส่วนสรุป (Metric Cards) ---
m1, m2, m3, m4 = st.columns(4)
metrics = [
    {"label": "ว่าง", "val": str(available_count), "unit": "ห้อง", "color": "#2e7d32"},
    {"label": "ค่อนข้างเต็ม", "val": str(medium_count), "unit": "ห้อง", "color": "#ef6c00"},
    {"label": "เต็ม", "val": str(crowded_count), "unit": "ห้อง", "color": "#c62828"},
    {"label": "เฉลี่ยการใช้งาน", "val": f"{avg_usage:.0f}%", "unit": "วันนี้", "color": "#111"},
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
    search_query = st.text_input("ค้นหาห้องน้ำ", placeholder="ค้นหาชื่อห้องน้ำ...", label_visibility="collapsed")

with col_tool2:
    c1, c2, c3, c_add = st.columns([1, 1, 1, 1.5])
    with c1: st.button("ทั้งหมด", use_container_width=True, type="primary")
    with c2: st.button("♂ ชาย", use_container_width=True)
    with c3: st.button("♀ หญิง", use_container_width=True)
    
    with c_add:
        # --- ฟีเจอร์เพิ่มห้องน้ำ (ใช้ Popover) ---
        with st.popover("➕ เพิ่มห้องน้ำ", use_container_width=True):
            st.markdown("**กรอกข้อมูลห้องน้ำใหม่**")
            new_building = st.text_input("ชื่ออาคาร", value="SC3", placeholder="เช่น SC3")
            new_floor = st.number_input("ชั้น", min_value=1, value=1)
            new_gender = st.selectbox("เพศ", ["male", "female", "disabled"])
            new_lat = st.number_input("Latitude", value=14.0704, format="%.4f")
            new_lng = st.number_input("Longitude", value=100.6057, format="%.4f")
            new_crowd = st.selectbox("ความแออัด", ["low", "medium", "high"], index=0)
            
            if st.button("ยืนยันการเพิ่มข้อมูล", use_container_width=True, type="primary"):
                success, result = create_restroom(new_building, new_floor, new_gender, new_lat, new_lng, new_crowd)
                if success:
                    st.success(f"✅ เพิ่ม {new_building} - ชั้น {new_floor} เรียบร้อยแล้ว!")
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error(f"❌ เพิ่มไม่สำเร็จ: {result}")

st.write("")

# --- ตารางแสดงรายการห้องน้ำใน SC3 ---
if sc3_restrooms:
    # กรองตามคำค้นหา
    filtered_rooms = sc3_restrooms
    if search_query:
        filtered_rooms = [r for r in sc3_restrooms if search_query.lower() in r["building"].lower()]
    
    # ส่วนหัวตาราง
    t_col = st.columns([2.5, 1.5, 2.5, 1.5, 1.5])
    t_headers = ["ชื่อห้องน้ำ", "เพศ", "ความแออัด", "พิกัด", "สถานะ"]
    for i, head in enumerate(t_col):
        head.markdown(f"<div style='font-size: 13px; color: gray; font-weight: bold;'>{t_headers[i]}</div>", unsafe_allow_html=True)
    
    st.divider()
    
    # แสดงรายการจาก API
    for room in filtered_rooms:
        gender_display = map_gender(room.get("type", ""))
        crowd_level = room.get("crowd_level", "low")
        status_label, status_color, status_bg = get_status_info(crowd_level)
        
        r_col = st.columns([2.5, 1.5, 2.5, 1.5, 1.5])
        
        with r_col[0]:
            st.markdown(f"**{room['building']} - ชั้น {room['floor']}**")
        with r_col[1]:
            st.markdown(gender_display)
        with r_col[2]:
            st.markdown(crowd_level)
        with r_col[3]:
            st.markdown(f"({room['latitude']:.4f}, {room['longitude']:.4f})")
        with r_col[4]:
            st.markdown(f"<div style='background: {status_bg}; color: {status_color}; padding: 5px 10px; border-radius: 8px; text-align: center; font-weight: bold; font-size: 12px;'>{status_label}</div>", unsafe_allow_html=True)
else:
    st.info("📭 ยังไม่มีข้อมูลห้องน้ำใน SC3 จาก API")

# --- ส่วนเพิ่มเติม: ข้อมูลจาก Session State (เก่า) ---
if st.session_state.rooms_sc3:
    st.markdown("<div style='margin-top: 30px; font-size: 16px; font-weight: bold; color: #666;'>📌 ข้อมูลท้องถิ่น (Local Data)</div>", unsafe_allow_html=True)
    
    for room in st.session_state.rooms_sc3:
        r_col = st.columns([2.5, 1.5, 3, 1.5, 1.5])
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