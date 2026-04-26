import sys
from pathlib import Path
import streamlit as st
import pandas as pd

# --- แก้ปัญหา Path (ต้องอยู่บนสุด) ---
root = str(Path(__file__).parent.parent)
if root not in sys.path:
    sys.path.append(root)

# สังเกตชื่อไฟล์: ถ้าคุณเปลี่ยนชื่อไฟล์เป็น card.py ให้ใช้ components.card
from components.card import inject_custom_css 
from components.sidebar import render_sidebar

st.set_page_config(layout="wide", initial_sidebar_state="expanded")
inject_custom_css()
render_sidebar()

# --- ส่วนหัว (Header) ---
col_h1, col_h2 = st.columns([5, 4])
with col_h1:
    # margin-top: -25px เพื่อให้ระนาบเท่าหน้า Overview
    st.markdown("<div style='font-size: 24px; font-weight: bold; margin-top: 20px; margin-bottom: -5px;'>รายงาน</div>", unsafe_allow_html=True)
    st.caption("วันเสาร์ที่ 25 เมษายน 2568")

with col_h2:
    # ส่วน Live และ ออกจากระบบ
    st.markdown(f"<div style='text-align: right; margin-top: -20px; font-size: 14px; color: gray;'></div>", unsafe_allow_html=True)

st.write("---")

# --- เนื้อหา (Grid 2 คอลัมน์) ---
col1, col2 = st.columns(2)

with col1:
    usage_data = [
        {"name": "SC1", "val": 100}, {"name": "SC2", "val": 52},
        {"name": "ยิม7", "val": 49}, {"name": "บร", "val": 46},
        {"name": "SC3", "val": 5},
    ]
    
    usage_data = sorted(usage_data, key=lambda x: x['val'], reverse=True)
    html_left = "<div class='info-box' style='min-height: 400px;'><div style='font-weight: bold; margin-bottom: 25px;'>การใช้งานรายอาคาร (เฉลี่ย %)</div>"
    for item in usage_data:
        # --- กำหนดสีตามระดับการใช้งาน ---
        if item['val'] >= 90:
            bar_color = "#c62828"  # แดง (เต็ม/วิกฤต)
        elif item['val'] >= 50:
            bar_color = "#ef6c00"  # ส้ม (เริ่มเยอะ)
        else:
            bar_color = "#2e7d32"  # เขียว (ว่าง/ปกติ)

        html_left += f"""
        <div style='display: flex; align-items: center; margin-bottom: 20px;'>
            <div style='width: 50px; font-size: 14px; color: #666;'>{item['name']}</div>
            <div style='flex-grow: 1; background: #eee; height: 10px; border-radius: 5px; margin: 0 20px;'>
                <div style='width: {item['val']}%; background: {bar_color}; height: 10px; border-radius: 5px;'></div>
            </div>
            <div style='width: 40px; text-align: right; font-size: 13px;'>{item['val']}%</div>
        </div>"""
    html_left += "</div>"
    st.markdown(html_left, unsafe_allow_html=True)

with col2:
    summary_data = [
        ("ครั้งที่ใช้งานรวม", "42 ครั้ง"),
        ("ห้องที่ใช้บ่อยที่สุด", "SC3 หญิง"),
        ("ชั่วโมงพีค", "09:00 – 10:00"),
        ("เฉลี่ยการใช้งาน", "50%"),
        ("แจ้งเตือนทั้งหมด", "3 ครั้ง"),
    ]
    
    html_right = "<div class='info-box' style='min-height: 400px;'><div style='font-weight: bold; margin-bottom: 25px;'>สรุปรายวัน</div>"
    for label, value in summary_data:
        html_right += f"""
        <div style='display: flex; justify-content: space-between; padding: 15px 0; border-bottom: 1px solid #f0f0f0;'>
            <span style='color: #666; font-size: 14px;'>{label}</span>
            <span style='font-weight: bold; font-size: 14px;'>{value}</span>
        </div>"""
    html_right += "</div>"
    st.markdown(html_right, unsafe_allow_html=True)