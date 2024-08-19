import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

# Google Calendar API 設定
SERVICE_ACCOUNT_FILE = '/Users/bojuping/Desktop/VSCode/credentials.json'
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# 認證並建立 API 服務
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=credentials)

# 取得日曆事件
def get_calendar_events(calendar_id, start_time, end_time):
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=start_time.isoformat() + 'Z',
        timeMax=end_time.isoformat() + 'Z',
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    return events_result.get('items', [])

# 設置日期範圍
today = datetime.utcnow().date()
start = datetime(today.year, today.month, 1)
end = (start + timedelta(days=32)).replace(day=1)

# 獲取事件
calendar_id = 'sd2721idgjjildevu45dc6t4ek@group.calendar.google.com'  # 這裡可以替換為你的日曆 ID
events = get_calendar_events(calendar_id, start, end)

# 計算每日事件數量
daily_events = pd.Series([event['start'].get('date', event['start'].get('dateTime')).split('T')[0] for event in events]).value_counts()

# 使用 Streamlit 顯示
st.title('Google 日曆每日事件數量')

# 顯示事件數據
st.subheader('事件數量')
st.write(daily_events)

# 顯示圖表
# 使用 Altair 繪圖代替 matplotlib
st.subheader('事件數量圖表')
chart = alt.Chart(daily_events.reset_index()).mark_bar().encode(
    x='index:O',
    y='0:Q'
).properties(
    title='每日事件數量'
)
st.altair_chart(chart, use_container_width=True)
