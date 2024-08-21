import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import gspread

# Google API 設定
SERVICE_ACCOUNT_FILE = 'dashboard/credentials.json'
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/spreadsheets.readonly']

# 認證並建立 API 服務
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=credentials)

# gspread 認證
gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)

# 取得日曆事件
def get_calendar_events(calendar_id, start_time, end_time):
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=start_time,
        timeMax=end_time,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    return events_result.get('items', [])

# 設置日期範圍
today = datetime.now().date()
start = datetime.combine(today, datetime.min.time()).isoformat() + 'Z'
end = datetime.combine(today + timedelta(days=1), datetime.min.time()).isoformat() + 'Z'

# 獲取事件
calendar_id = 'sd2721idgjjildevu45dc6t4ek@group.calendar.google.com'  # 這裡可以替換為你的日曆 ID
events = get_calendar_events(calendar_id, start, end)

# 計算每日事件數量
daily_events = pd.Series([event['start'].get('date', event['start'].get('dateTime')).split('T')[0] for event in events]).value_counts()

# 取得 Google Sheets 中的最新一筆資料
def get_latest_sheet_data(spreadsheet_id, sheet_name):
    sh = gc.open_by_key(spreadsheet_id)
    worksheet = sh.worksheet(sheet_name)
    data = worksheet.get_all_records()  # 取得所有數據
    df = pd.DataFrame(data)  # 將數據轉為 pandas DataFrame
    return df.tail(1)  # 取得最後一行資料

# 設置 Google Sheets 資訊
SPREADSHEET_ID = '1XiBEOWus9hnXzAMOX5dss-nheYKFEEIzeUzpcYXzmMM'  # 替換為你的 Google Sheets ID
SHEET_NAME = '表單回應 1'  # 替換為你的工作表名稱

# 顯示 Google Sheets 中的最新一筆資料
latest_data = get_latest_sheet_data(SPREADSHEET_ID, SHEET_NAME)

# 使用 Streamlit 顯示標題
st.markdown("""
    <style>
    .title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
    }
    .section1 {
        background: url('https://i.im.ge/2023/12/29/x3xWPF.2-0.png');
        background-size: contain;
        background-position: left top;
        background-repeat: no-repeat;
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
    .section1 h2 {
        font-size: 32px;  /* 調整字體大小 */
        text-align: center;  /* 文字置中 */
    }
    .section2 {
        background-color: #f0f0f0;  /* 淺灰色背景 */
        padding: 20px;
        border-radius: 10px;
        color: black;
        max-width: 100%;  /* 增加寬度 */
        text-align: center;  /* 文字置中 */
    }
    .dataframe {
        color: black;
        border-collapse: collapse;
        width: 100%;
    }
    .dataframe th, .dataframe td {
        padding: 10px;
        border: 1px solid black;
    }
    .hide-index {
        border-collapse: collapse;
        width: 100%;
    }
    .hide-index th, .hide-index td {
        padding: 10px;
        border: 1px solid black;
    }
    .hide-index td {
        padding-left: 0; /* 隱藏索引欄的內容 */
    }
    .col2-content {
        font-size: 14px;  /* 調整字體大小 */
    }
    .col1-content {
        font-size: 14px;  /* 調整字體大小 */
    }
    </style>
    <h1 class="title">大樓管理組 儀表板</h1>
    """, unsafe_allow_html=True)

# 更改 Series 的名稱
daily_events.name = '申請停放數量'

# 使用 columns 並排顯示兩個區塊，調整寬度比例
col1, col2 = st.columns([1, 1.5])  # col2 比 col1 寬

# 在第一列顯示「240巷車位概況」
with col1:
    st.markdown(f"""
        <div class="section1">
            <h2>240巷車位概況</h2>
            <div class="dataframe">
                {daily_events.to_frame().to_html(classes='dataframe', border=0)}
            </div>
        </div>
        """, unsafe_allow_html=True)

# 在第二列顯示「總處大小事(最新一筆)」
with col2:
    # 拆分 latest_data 的列
    columns_part1 = latest_data.iloc[:, :4]  # 取前4列
    columns_part2 = latest_data.iloc[:, 4:]  # 取第5列及後面的列

    # 生成 HTML 表格，隱藏索引
    columns_part1_html = columns_part1.to_html(classes='hide-index', border=0, index=False)
    columns_part2_html = columns_part2.to_html(classes='hide-index', border=0, index=False)

    # 顯示「總處大小事(最新一筆)」
    st.markdown(f"""
        <div class="section2 col2-content">
            <h4>總處大小事(最新一筆)</h4>
            <div class="dataframe">
                {columns_part1_html}
            </div>
            <div class="dataframe">
                {columns_part2_html}
            </div>
        </div>
        """, unsafe_allow_html=True)
