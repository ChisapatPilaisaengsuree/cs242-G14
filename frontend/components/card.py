import streamlit as st

def inject_custom_css():
    st.markdown("""
    <style>

        .block-container {
            padding-top: 1rem !important; 
            padding-bottom: 1rem !important;
        }
        header[data-testid="stHeader"] {
            display: none !important;
            height: 0px !important;
        }

        [data-testid="stSidebarCollapseButton"] {
            display: none !important;
        }
        button[title="Collapse sidebar"] {
            display: none !important;
        }
        [data-testid="stSidebarResizer"] {
            display: none !important;
        }

        [data-testid="stSidebarUserContent"] {
            padding-top: 0rem !important; 
        }

        [data-testid="stSidebarContent"] > div:first-child {
            padding-top: 0rem !important;
        }

        section[data-testid="stSidebar"] button[kind="header"] {
            display: none !important;
        }
        .metric-card {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 12px 16px;
            box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.05);
            margin-top: -15px;
        }
        .metric-title { font-size: 14px; color: #666; font-family: sans-serif;}
        .metric-val-green { font-size: 28px; font-weight: bold; color: #2e7d32; margin: 0px; line-height: 1.2;}
        .metric-val-orange { font-size: 28px; font-weight: bold; color: #ef6c00; margin: 0px; line-height: 1.2;}
        .metric-val-red { font-size: 28px; font-weight: bold; color: #c62828; margin: 0px; line-height: 1.2;}
        .metric-val-black { font-size: 28px; font-weight: bold; color: #212121; margin: 0px; line-height: 1.2;}
        .metric-sub { font-size: 11px; color: #999; margin-top: 5px;}

        /* --- ช่องค้นหา (Search Input) --- */
        div[data-baseweb="input"] {
            border-radius: 20px !important;
            border: 1px solid #d1d5db !important;
            background-color: #f9fafb !important;
            transition: all 0.3s ease;
            min-height: 34px !important;
        }
        div[data-baseweb="input"]:focus-within {
            border-color: #2e7d32 !important;
            box-shadow: 0 0 5px rgba(46, 125, 50, 0.2) !important;
            background-color: #ffffff !important;
        }
        div[data-baseweb="input"] input {
            padding: 6px 15px !important; 
            front-size: 14px !important;
        }

        /* --- ปุ่มออกจากระบบ (Logout Button) --- */
        .logout-btn {
            background-color: #ffffff;
            border: 1px solid #d1d5db;
            border-radius: 20px;
            padding: 6px 16px;
            font-size: 14px;
            color: #4b5563;
            cursor: pointer;
            transition: all 0.2s ease;
            font-family: inherit;
        }
        .logout-btn:hover {
            background-color: #f3f4f6;
            border-color: #9ca3af;
            color: #1f2937;
        }

        /* --- ซ่อนเมนูนำทางอัตโนมัติของ Streamlit (app, overview) --- */
        [data-testid="stSidebarNav"] {
            display: none !important;
        }

        /* --- ตารางแบบไม่มีเส้น (Clean Table) --- */
        .table-container {
            border-radius: 12px; 
            overflow: hidden; 
            border: 1px solid #e5e7eb; 
            box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.05); 
        }
        .clean-table {
            width: 100%;
            border-collapse: collapse; 
            font-size: 14px;
        }
        .clean-table th {
            color: #1f2937;
            font-weight: bold;
            background-color: #f3f4f6;
            padding: 12px 16px;
            text-align: left;
            border-bottom: 2px solid #e5e7ed; 
        }
        .clean-table td {
            padding: 16px 8px; 
            color: #333;
            border-bottom: 2px solid #f9fafb; 
        }
        
        /* เพิ่มเอฟเฟกต์ตอนเอาเมาส์ไปชี้แถว */
        .clean-table tbody tr:hover {
            background-color: #f9fafb;
            border-radius: 8px;
        }

        .info-box {
            background-color: white;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 20px;
            min-height: 320px;
        }
        .info-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        .notif-item {
            display: flex;
            align-items: flex-start;
            padding: 12px 0;
            border-bottom: 1px solid #f3f4f6;
        }
        .notif-item:last-child { border-bottom: none; }
        .dot {
            height: 10px;
            width: 10px;
            border-radius: 50%;
            margin-top: 5px;
            margin-right: 12px;
            flex-shrink: 0;
        }
        .usage-row {
            display: flex;
            align-items: center;
            margin-bottom: 22px;
        }
        .usage-label { width: 60px; font-size: 14px; color: #666; }
        .usage-bar-bg {
            flex-grow: 1;
            background: #eee;
            height: 8px;
            border-radius: 4px;
            margin: 0 15px;
        }
        .usage-bar-fill { height: 8px; border-radius: 4px; }
        .usage-percent { width: 40px; font-size: 13px; color: #444; text-align: right; }
        
        .info-box {
            background-color: white;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 20px;
            min-height: 335px;
            /* เพิ่มเงาให้นุ่มนวล */
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
            transition: transform 0.2s ease;
        }
        .info-box:hover {
            transform: translateY(-2px); /* เวลาชี้แล้วกล่องจะลอยขึ้นนิดนึง */
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08) !important;
        }
        .info-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        .notif-item {
            display: flex;
            align-items: flex-start;
            padding: 12px 0;
            border-bottom: 1px solid #f3f4f6;
        }
        .usage-row {
            display: flex;
            align-items: center;
            margin-bottom: 22px;
        }

        /* --- การ์ดห้องน้ำ (Restroom Grid Card) --- */
        .restroom-card {
            background: white;
            border-radius: 15px;
            padding: 20px;
            border: 1px solid #f0f0f0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 10px;
        }
        .gender-tag {
            padding: 2px 8px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 4px;
        }
        .tag-male { background: #e0f2fe; color: #0369a1; }
        .tag-female { background: #fdf2f8; color: #be185d; }
        .tag-total { background: #f3f4f6; color: #374151; }

        /* หลอด Progress ขนาดใหญ่ในการ์ด */
        .card-progress-bg {
            background: #eee;
            height: 12px;
            border-radius: 6px;
            margin: 15px 0;
            overflow: hidden;
        }
        .card-progress-fill { height: 100%; border-radius: 6px; }

        .card-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 13px;
            color: #666;
        }

        [data-testid="stSidebarNav"] {
            display: none !important;
        }

        /* --- ปรับสีปุ่ม Primary (ปุ่ม "ทั้งหมด") --- */
        button[kind="primary"] {
            background-color: #111827 !important; /* สีดำเข้ม */
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            transition: all 0.2s ease !important;
        }

        /* เอฟเฟกต์ตอนเอาเมาส์ไปชี้ (Hover) */
        button[kind="primary"]:hover {
            background-color: #374151 !important; /* สีเทาเข้มขึ้นนิดนึง */
            border-color: #374151 !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
        }
        
        /* ปรับสีปุ่มธรรมดา (ชาย / หญิง) ให้ดูคลีนเข้ากัน */
        button[kind="secondary"] {
            border: 1px solid #e5e7eb !important;
            border-radius: 8px !important;
            background-color: white !important;
            color: #374151 !important;
        }
    </style>
    """, unsafe_allow_html=True)

def render_metric_card(title, value, unit, color_class):
    """ฟังก์ชันสร้างการ์ด เพื่อลดความซ้ำซ้อนของโค้ด"""
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="{color_class}">{value}</div>
            <div class="metric-sub">{unit}</div>
        </div>
    """, unsafe_allow_html=True)