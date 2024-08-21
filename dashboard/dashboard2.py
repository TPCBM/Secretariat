import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import gspread

# Google Calendar API 設定
SERVICE_ACCOUNT_FILE = 'dashboard/credentials.json'
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/spreadsheets.readonly']

# 認證並建立 API 服務
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=credentials)

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

# *取得 Google Sheets 中的最新一筆資料
def get_latest_sheet_data(spreadsheet_id, sheet_name):
    sh = gc.open_by_key(spreadsheet_id)
    worksheet = sh.worksheet(sheet_name)
    data = worksheet.get_all_records()  # 取得所有數據
    df = pd.DataFrame(data)  # 將數據轉為 pandas DataFrame
    return df.tail(1)  # 取得最後一行資料

# *設置 Google Sheets 資訊
SPREADSHEET_ID = 'your_google_sheet_id'  # 替換為你的 Google Sheets ID
SHEET_NAME = 'Sheet1'  # 替換為你的工作表名稱

# *顯示 Google Sheets 中的最新一筆資料
latest_data = get_latest_sheet_data(SPREADSHEET_ID, SHEET_NAME)

# 使用 Streamlit 顯示標題
st.markdown("""
    <style>
    .title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
    }
    </style>
    <h1 class="title">大樓管理組 儀表板</h1>
    """, unsafe_allow_html=True)

# 更改 Series 的名称
daily_events.name = '申請停放數量'

# 设置背景图片
background_image_url = 'https://i.im.ge/2023/12/29/x3xWPF.2-0.png'  # 确保图片在同一目录下

# 生成背景图的 CSS
background_css = f"""
<style>
.report-container {{
    background: url('{background_image_url}');
    background-size: contain;  /* 确保图片缩小显示 */
    background-position: left top;  /* 图片靠左上角对齐 */
    background-repeat: no-repeat;  /* 防止图片重复 */
    padding: 30px;
    border-radius: 10px;
    color: white;
    text-align: left;
}}
.dataframe {{
    color: black;
    margin-top: 30px;
}}
</style>
"""

# 显示背景图片和数据
st.markdown(background_css, unsafe_allow_html=True)
st.markdown(f"""
    <div class="report-container">
        <h2>240巷車位概況</h2>
        <div class="dataframe">
            {daily_events.to_frame().to_html(classes='dataframe', border=0)}
        </div>
    </div>
    """, unsafe_allow_html=True)

# 顯示 Google Sheets 最新一筆資料
st.subheader('Google Sheet 最新一筆資料')
st.write(latest_data)
