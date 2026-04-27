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
            border: 2px solid #f1f5f9;
            border-radius: 16px;
            padding: 15px 19px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.03);
            margin-top: -15px;
            transition: transform 0.2s ease;
        }
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.05);
        }

        .metric-title { font-size: 13px; color: #64748b;font-weight: 500; font-family: sans-serif;}
        .metric-val-purple { font-size: 32px; font-weight: 800; color: #7e57c2; margin: 0; line-height: 1.1; }
        .metric-val-green { font-size: 32px; font-weight: 800; color: #10b981; margin: 0; line-height: 1.1; }
        .metric-val-orange { font-size: 32px; font-weight: 800; color: #f59e0b; margin: 0; line-height: 1.1; }
        .metric-val-red { font-size: 32px; font-weight: 800; color: #ef4444; margin: 0; line-height: 1.1; }
        .metric-sub { font-size: 11px; color: #94a3b8; margin-top: 8px; font-weight: 400; }
        .metric-val-black {
            font-size: 32px !important;      
            font-weight: 800 !important;     
            color: #000000 !important;     
            margin: 0 !important;      
            line-height: 1.1 !important;
        }

        /* --- ช่องค้นหา (Search Input) --- */
        div[data-baseweb="input"] {
            border-radius: 15px !important;
            border: 1px solid #e2e8f0 !important;
            background-color: #f8fafc !important;
            transition: all 0.3s ease;
            min-height: 40px !important;
        }
        div[data-baseweb="input"]:focus-within {
            border-color: #7e57c2 !important;
            box-shadow: 0 0 3px rgba(126, 87, 194, 0.1) !important;
            background-color: #ffffff !important;
        }
        div[data-baseweb="input"] input {
            padding: 6px 15px !important; 
            front-size: 14px !important;
        }

        /* --- ปุ่มออกจากระบบ (Logout Button) --- */
        .logout-btn {
            background-color: transparent;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 8px 16px;
            font-size: 14px;
            color: #64748b;
            cursor: pointer;
            transition: all 0.2s ease;
            font-family: inherit;
            text-align: center;
        }
        .logout-btn:hover {
            background-color: #fee2ee;
            border-color: #fecaca;
            color: #ef4444;
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
            background-color: #f8fafc;
            color: #475569;
            text-transform: uppercase;
            font-size: 11px;
            letter-spacing: 0.05em;
            border-bottom: 1px solid #e2e8f0;
        }
        .clean-table td {
            border-bottom: 1px solid #f1f5f9;
            padding: 16px 12px;
        }
        
        /* เพิ่มเอฟเฟกต์ตอนเอาเมาส์ไปชี้แถว */
        .clean-table tbody tr:hover {
            background-color: #f9fafb;
            border-radius: 8px;
        }

        .info-box, .restroom-card {
            background-color: white !important;
            border: 2px solid #f1f5f9 !important;
            border-radius: 20px !important;
            padding: 24px !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04) !important;
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
            background-color: #7e57c2 !important; /* สีม่วงหลัก */
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }

        /* เอฟเฟกต์ตอนเอาเมาส์ไปชี้ (Hover) */
        button[kind="primary"]:hover {
            background-color: #6a49a9 !important;
            box-shadow: 0 4px 12px rgba(126, 87, 194, 0.3) !important;
            transform: translateY(-1px);
        }
        
        /* ปรับสีปุ่มธรรมดา (ชาย / หญิง) ให้ดูคลีนเข้ากัน */
        button[kind="secondary"] {
            border: 1px solid #e2e8f0 !important;
            border-radius: 12px !important;
            color: #4b5563 !important;
        }
        button[kind="secondary"]:hover {
            border-color: #7e57c2 !important;
            color: #7e57c2 !important;
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