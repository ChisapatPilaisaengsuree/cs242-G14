import streamlit as st
import requests
import sys
from pathlib import Path

# --- API Configuration ---
API_BASE_URL = "http://localhost:8000/api"

def show_edit_modal(restroom_id: int, restroom_data: dict):
    """
    แสดง Modal สำหรับแก้ไขข้อมูลห้องน้ำ
    
    Args:
        restroom_id: ID ของห้องน้ำ
        restroom_data: ข้อมูลห้องน้ำ dict ที่มี keys: building, floor, type, latitude, longitude, crowd_level
    """
    st.markdown("### แก้ไขข้อมูลห้องน้ำ")
    
    with st.form(f"edit_form_{restroom_id}", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            building = st.text_input(
                "อาคาร",
                value=restroom_data.get("building", ""),
                placeholder="เช่น SC1, SC2, บร5"
            )
            floor = st.number_input(
                "ชั้น",
                value=int(restroom_data.get("floor", 1)),
                min_value=1,
                max_value=10
            )
            crowd_level = st.selectbox(
                "ระดับความแออัด",
                ["low", "medium", "high"],
                index=["low", "medium", "high"].index(restroom_data.get("crowd_level", "low"))
            )
        
        with col2:
            restroom_type = st.selectbox(
                "ประเภท",
                ["male", "female", "disabled", "unisex"],
                index=["male", "female", "disabled", "unisex"].index(restroom_data.get("type", "male"))
            )
            latitude = st.number_input(
                "Latitude",
                value=float(restroom_data.get("latitude", 14.0)),
                format="%.6f"
            )
            longitude = st.number_input(
                "Longitude",
                value=float(restroom_data.get("longitude", 100.0)),
                format="%.6f"
            )
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            submit_btn = st.form_submit_button("💾 บันทึก", use_container_width=True, type="primary")
        with col_btn2:
            cancel_btn = st.form_submit_button("❌ ยกเลิก", use_container_width=True)
        
        if submit_btn:
            # เตรียมข้อมูลสำหรับ update
            update_data = {
                "building": building,
                "floor": floor,
                "type": restroom_type,
                "latitude": latitude,
                "longitude": longitude,
                "crowd_level": crowd_level
            }
            
            try:
                response = requests.put(
                    f"{API_BASE_URL}/restrooms/{restroom_id}",
                    json=update_data,
                    timeout=5
                )
                
                if response.status_code in [200, 201]:
                    st.success("✅ บันทึกข้อมูลสำเร็จ!")
                    st.session_state.edit_modal_open = False
                    st.session_state.need_refresh = True
                    st.rerun()
                else:
                    st.error(f"❌ เกิดข้อผิดพลาด: {response.status_code}")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ ไม่สามารถเชื่อมต่อ API: {str(e)}")
        
        if cancel_btn:
            st.session_state.edit_modal_open = False
            st.rerun()


def show_edit_button(restroom_id: int, restroom_data: dict):
    """
    แสดงปุ่มแก้ไข และจัดการ modal
    """
    if st.button("✏️ แก้ไข", key=f"edit_btn_{restroom_id}", use_container_width=True):
        st.session_state.edit_modal_open = True
        st.session_state.editing_id = restroom_id
        st.session_state.editing_data = restroom_data
        st.rerun()
    
    # แสดง modal ถ้า open
    if st.session_state.get("edit_modal_open") and st.session_state.get("editing_id") == restroom_id:
        show_edit_modal(restroom_id, restroom_data)
