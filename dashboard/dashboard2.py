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
end = datetime.combine(today + timedelta(days=2), datetime.min.time()).isoformat() + 'Z'  # 調整為今天 + 2 天

# 獲取事件
calendar_id = 'sd2721idgjjildevu45dc6t4ek@group.calendar.google.com'  # 這裡可以替換為你的日曆 ID
events = get_calendar_events(calendar_id, start, end)

# 計算今天和明天的事件數量
events_by_day = pd.Series([event['start'].get('date', event['start'].get('dateTime')).split('T')[0] for event in events])
today_str = today.isoformat()  # 今天的日期字串
tomorrow_str = (today + timedelta(days=1)).isoformat()  # 明天的日期字串

# 計算今天和明天的事件數量
today_events_count = (events_by_day == today_str).sum()
tomorrow_events_count = (events_by_day == tomorrow_str).sum()

# 將今天和明天的事件數量組成 DataFrame
daily_events = pd.DataFrame({
    '日期': [today_str, tomorrow_str],
    '申請停放數量': [today_events_count, tomorrow_events_count]
})


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
        font-size: 50px;
        font-weight: bold;
        background: -webkit-linear-gradient(#ff7e5f, #feb47b); /* 漸變色 */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent; /* 文字填充透明 */
     }
    .section1 {
        background-color: #E0FFFF;  /* 淺灰色背景 */
        padding: 20px;
        border-radius: 10px;
        color: black;
        max-width: 100%;  /* 增加寬度 */
        text-align: center;  /* 文字置中 */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);  /* 添加陰影效果 */
    }
    .section1 h2 {
        font-size: 28px;  /* 調整字體大小 */
        text-align: center;  /* 文字置中 */
    }
    .col1-content {
        font-size: 20px;  /* 調整字體大小 */
    }    
    .section2 {
        background-color: #f0f0f0;  /* 淺灰色背景 */
        padding: 20px;
        border-radius: 10px;
        color: black;
        max-width: 100%;  /* 增加寬度 */
        text-align: center;  /* 文字置中 */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);  /* 添加陰影效果 */
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
        text-align: center;  /* 置中表格文字 */
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
# 第一個區塊內的樣式和表格顯示
with col1:
    st.markdown(f"""
        <div class="section1">
            <h2>240巷車位概況</h2>
            <div class="dataframe centered-table">
                {daily_events.to_html(classes='dataframe centered-table', index=False, border=0)}
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

#... 保留原有的代碼
# 新日历的本周每日事件显示区块
new_calendar_id = 'd0svld4vlapgnsl2sau7puqi30@group.calendar.google.com'

# 定义获取本周事件的函数
def get_week_events(new_calendar_id):
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    start_time = datetime.combine(start_of_week, datetime.min.time()).isoformat() + 'Z'
    end_time = datetime.combine(end_of_week, datetime.min.time()).isoformat() + 'Z'

    # 获取本周的事件
    week_events = get_calendar_events(new_calendar_id, start_time, end_time)
    
    # 打印事件以验证
    st.write("Week Events:", week_events)

    # 检查事件数量
    event_count = len(week_events)
    st.write("Number of Events:", event_count)

    return week_events, start_of_week, end_of_week

# 获取本周的事件
week_events, start_of_week, end_of_week = get_week_events(new_calendar_id)

# 安全地处理 week_events 并检查 'start' 是否存在
events_by_day = pd.Series([
    event['start'].get('date', event['start'].get('dateTime', '')).split('T')[0]
    for event in week_events if 'start' in event
])

# 打印 events_by_day 来确认其内容
st.write("Events by Day:", events_by_day)

# 设置本周的日期范围
week_days = pd.date_range(start=start_of_week, end=end_of_week).strftime('%Y-%m-%d')

# 计算每一天的事件数量
week_events_count = [events_by_day.str.contains(day).sum() for day in week_days]

# 将事件数量构造成 DataFrame
weekly_events_df = pd.DataFrame({
    '日期': week_days,
    '事件数量': week_events_count
})

# 显示本周事件数量
st.markdown("""
    <div class="section1">
        <h2>本周事件数量（新日历）</h2>
    </div>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div class="section2">
        <div class="dataframe centered-table">
            {weekly_events_df.to_html(classes='dataframe centered-table', index=False, border=0)}
        </div>
    </div>
""", unsafe_allow_html=True)
