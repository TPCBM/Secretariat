import streamlit as st
import pandas as pd
import base64
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

# Google Calendar API 設定
SERVICE_ACCOUNT_FILE = 'dashboard/credentials.json'
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

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

# 更改 Series 的名称
daily_events.name = '申請停放數量'

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

# 获取 Base64 编码的图片
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

background_image_base64 = get_base64_image('x3xWPF.2-0.png')  # 确保路径正确

# 生成背景图的 CSS
background_css = f"""
<style>
.report-container {{
    background: url(data:image/png;base64,{background_image_base64});
    background-size: cover;
    padding: 20px;
    border-radius: 10px;
    color: white;
    text-align: left;
}}
.dataframe {{
    color: black;
    margin-top: 20px;
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
