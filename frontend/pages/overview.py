import sys
import os

# บรรทัดนี้จะช่วยให้ Python หาโฟลเดอร์ components เจอ
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
import pandas as pd
from datetime import datetime

# นำเข้า Components ที่เราแยกไว้
from components.sidebar import render_sidebar
from components.card import inject_custom_css, render_metric_card

st.set_page_config(layout="wide", initial_sidebar_state="expanded")
inject_custom_css()

def get_current_thai_datetime():
    now = datetime.now()
    thai_days = ["จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"]
    thai_months = [
        "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
        "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
    ]
    
    # สร้างข้อความวันที่ เช่น "วันเสาร์ที่ 26 เมษายน 2569"
    date_str = f"วัน{thai_days[now.weekday()]}ที่ {now.day} {thai_months[now.month - 1]} {now.year + 543}"
    
    # สร้างข้อความเวลา เช่น "20:37:07"
    time_str = now.strftime("%H:%M:%S")
    
    return date_str, time_str

# เรียกใช้ฟังก์ชันเพื่อเก็บค่าวันที่และเวลา ณ ตอนที่โหลดหน้าเว็บ
current_date, current_time = get_current_thai_datetime()

st.set_page_config(page_title="ภาพรวม - RestroomAdmin", layout="wide", initial_sidebar_state="expanded")

# เรียกใช้งาน Sidebar และ CSS
render_sidebar()
inject_custom_css()

# --- ส่วนหัว ---
col_header1, col_header2, col_header3 = st.columns([2, 1, 1])
with col_header1:
    st.subheader("ภาพรวมระบบ")
    st.caption(f"{current_date}")
with col_header2:
    search_query = st.text_input(" ค้นหาห้องน้ำ...", placeholder="พิมพ์ชื่อห้องน้ำ", label_visibility="collapsed")
with col_header3:
    st.markdown(f"<div style='text-align: right; color: gray; margin-top: 5px;'>🟢 Live &nbsp; | &nbsp; {current_time} &nbsp; | &nbsp; <button class='logout-btn'>ออกจากระบบ</button></div>", unsafe_allow_html=True)


# --- การ์ดสรุปข้อมูล ---
col1, col2, col3, col4 = st.columns(4)
with col1: render_metric_card("ว่าง", "4", "ห้องน้ำ", "metric-val-green")
with col2: render_metric_card("ค่อนข้างเต็ม", "2", "ห้องน้ำ", "metric-val-orange")
with col3: render_metric_card("เต็ม / วิกฤต", "2", "ห้องน้ำ", "metric-val-red")
with col4: render_metric_card("เฉลี่ยการใช้งาน", "50%", "วันนี้", "metric-val-black")

st.write("---")

# --- ตารางข้อมูล (แบบไม่มีเส้น และปรับสีตามสถานะ) ---
st.markdown("<div style='font-size: 18px; font-weight: bold; margin-top: 15px; margin-bottom: 10px;'>รายการห้องน้ำ</div>", unsafe_allow_html=True)

data = {
    "ชื่อห้องน้ำ": ["ยิม7 - ชั้น1 - รวม", "SC2 - ชั้น1 - ชาย", "บร - ชั้น1 - ชาย", "ยิม7 - ชาย", "ยิม7 - หญิง", "บร - ชั้น2 - หญิง", "SC2 - ชั้น3 - หญิง", "SC3 - ชั้น2 - หญิง"],
    "เพศ": [" รวม", "🚹 ชาย", "🚹 ชาย", "🚹 ชาย", "🚺 หญิง", "🚺 หญิง", "🚺 หญิง", "🚺 หญิง"],
    "การใช้งาน": [100, 95, 72, 60, 39, 20, 10, 5],
    "ความจุ": ["4 ที่", "6 ที่", "6 ที่", "4 ที่", "4 ที่", "2 ที่", "6 ที่", "5 ที่"],
    "สถานะ": [" เต็ม", " เต็ม", " ค่อนข้างเต็ม", " ค่อนข้างเต็ม", " ว่าง", " ว่าง", " ว่าง", " ว่าง"],
    "อัปเดต": ["09:31", "09:45", "09:05", "09:18", "09:12", "08:52", "08:59", "08:55"]
}
df = pd.DataFrame(data)

# เริ่มสร้างตาราง HTML
html_table = "<div class='table-container'><table class='clean-table'><thead><tr><th>ชื่อห้องน้ำ</th><th>เพศ</th><th>การใช้งาน</th><th>ความจุ</th><th>สถานะ</th><th>อัปเดต</th></tr></thead><tbody>"

for i, row in df.iterrows():
    val = row['การใช้งาน']
    
    # กำหนดสีหลอด Progress Bar
    if val >= 90: bar_color = "#c62828" # แดง
    elif val >= 60: bar_color = "#ef6c00" # ส้ม
    else: bar_color = "#2e7d32" # เขียว
        
    # สร้างหลอด Progress Bar
    progress_html = f"<div style='display: flex; align-items: center; gap: 10px;'><div style='flex-grow: 1; background: #e0e0e0; border-radius: 4px; height: 6px;'><div style='width: {val}%; background: {bar_color}; height: 6px; border-radius: 4px;'></div></div><span style='font-size: 12px; color: #666; min-width: 35px;'>{val}%</span></div>"
    
    # จัดสีป้ายสถานะ
    # จัดสีป้ายสถานะ (แก้โดยเอา 'ค่อนข้างเต็ม' ขึ้นมาเช็กก่อน)
    if "ค่อนข้างเต็ม" in row['สถานะ']:
        status_bg, status_color = "#fff3e0", "#ef6c00" # ส้ม
    elif "เต็ม" in row['สถานะ']:
        status_bg, status_color = "#ffebee", "#c62828" # แดง
    else:
        status_bg, status_color = "#e8f5e9", "#2e7d32" # เขียว (ว่าง)
        
    status_badge = f"<span style='background: {status_bg}; color: {status_color}; padding: 4px 10px; border-radius: 12px; font-size: 12px;'>{row['สถานะ']}</span>"
    
    # ประกอบข้อมูลแต่ละแถวเข้าด้วยกัน
    html_table += f"<tr><td>{row['ชื่อห้องน้ำ']}</td><td style='color: #666;'>{row['เพศ']}</td><td style='width: 25%;'>{progress_html}</td><td style='color: #666;'>{row['ความจุ']}</td><td>{status_badge}</td><td style='color: #999;'>{row['อัปเดต']}</td></tr>"
    
html_table += "</tbody></table></div>"

# สั่งแสดงผลตารางออกหน้าจอ
st.markdown(html_table, unsafe_allow_html=True)

st.write("") # เว้นระยะห่างเล็กน้อย
col_bottom1, col_bottom2 = st.columns(2)

# --- ฝั่งซ้าย: การแจ้งเตือนล่าสุด ---
with col_bottom1:
    notif_data = [
        {"msg": "SC2 ชั้น1 ชาย — ใช้งาน 95% เกินเกณฑ์วิกฤต", "time": "09:45 น.", "color": "#c62828"},
        {"msg": "SC1 ชั้น1 รวม — เต็ม 100%", "time": "09:31 น.", "color": "#c62828"},
        {"msg": "ยิม7 ชาย — สูงต่อเนื่องกว่า 30 นาที", "time": "09:18 น.", "color": "#ef6c00"},
        {"msg": "SC3 ชั้น2 หญิง — กลับสู่สถานะปกติ", "time": "08:55 น.", "color": "#2e7d32"},
    ]
    
    notif_html = "<div class='info-box'><div class='info-header'>"
    notif_html += "<span style='font-weight: bold;'>การแจ้งเตือนล่าสุด</span>"
    notif_html += "<a href='#' style='color: #888; font-size: 13px; text-decoration: none;'>ดูทั้งหมด →</a></div>"
    
    for n in notif_data:
        notif_html += f"""
        <div class='notif-item'>
            <div class='dot' style='background-color: {n['color']};'></div>
            <div>
                <div style='font-size: 14px; font-weight: 500;'>{n['msg']}</div>
                <div style='font-size: 12px; color: #999;'>{n['time']}</div>
            </div>
        </div>"""
    notif_html += "</div>"
    st.markdown(notif_html, unsafe_allow_html=True)

# --- ฝั่งขวา: การใช้งานเฉลี่ยรายอาคาร ---
with col_bottom2:
    usage_data = [
        {"name": "SC1", "val": 100, "color": "#c62828"},
        {"name": "SC2", "val": 52, "color": "#ef6c00"},
        {"name": "SC3", "val": 5, "color": "#2e7d32"},
        {"name": "ยิม7", "val": 49, "color": "#ef6c00"},
        {"name": "บร", "val": 46, "color": "#2e7d32"},
    ]
    
    usage_html = "<div class='info-box'><div class='info-header'>"
    usage_html += "<span style='font-weight: bold;'>การใช้งานเฉลี่ยรายอาคาร</span></div>"
    
    for u in usage_data:
        usage_html += f"""
        <div class='usage-row'>
            <div class='usage-label'>{u['name']}</div>
            <div class='usage-bar-bg'>
                <div class='usage-bar-fill' style='width: {u['val']}%; background: {u['color']};'></div>
            </div>
            <div class='usage-percent'>{u['val']}%</div>
        </div>"""
    usage_html += "</div>"
    st.markdown(usage_html, unsafe_allow_html=True)