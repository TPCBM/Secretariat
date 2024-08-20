import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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

# 使用 Streamlit 顯示
# st.title('大樓管理組 儀表板')

# 更改 Series 的名称
daily_events.name = '申請停放數量'

# 顯示事件數據
st.subheader('240巷車位概況')
st.write(daily_events)

# 顯示圖表
# st.subheader('事件數量圖表')
# fig, ax = plt.subplots()
# daily_events.sort_index().plot(kind='bar', ax=ax)
# ax.set_xlabel('日期')
# ax.set_ylabel('事件數量')
# ax.set_title('每日事件數量')
# st.pyplot(fig)
