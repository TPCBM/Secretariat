# calendar_display.py

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def create_schedule(selected_month):
    # 创建一个包含日期和时间段的DataFrame
    start_date = selected_month.replace(day=1)
    end_date = start_date + pd.offsets.MonthEnd(0)
    dates = pd.date_range(start=start_date, end=end_date)
    schedule = pd.DataFrame(index=dates, columns=['Morning', 'Afternoon'])
    return schedule

def show_schedule(schedule, reservation_data):
    # 创建一个空的 DataFrame 来存储日历信息
    calendar_df = pd.DataFrame(index=schedule.index, columns=['預定日期', '中午(11:00-14:00)', '晚上(17:00-20:00)'])

    # 填充日期列
    calendar_df['預定日期'] = calendar_df.index.day

    # 检查每个日期和时间段是否在预订数据中
    for index, row in calendar_df.iterrows():
        date = row.name.date()
        morning_status = "空閒"
        afternoon_status = "空閒"
        if not reservation_data.empty:
            morning_reservations = reservation_data[(reservation_data['Date'] == date) & (reservation_data['Period'] == '中午(11:00-14:00)')]
            afternoon_reservations = reservation_data[(reservation_data['Date'] == date) & (reservation_data['Period'] == '晚上(17:00-20:00)')]
            if not morning_reservations.empty:
                morning_status = "已預訂"
            if not afternoon_reservations.empty:
                afternoon_status = "已預訂"
        calendar_df.loc[index, '中午(11:00-14:00)'] = morning_status
        calendar_df.loc[index, '晚上(17:00-20:00)'] = afternoon_status

    # 显示日历表格
    st.dataframe(calendar_df)

def main(reservation_data):
    selected_month = st.selectbox("訂位月份", [f"{i} 月" for i in range(1, 13)])
    selected_month_number = int(selected_month.split()[0])
    selected_date = datetime(datetime.now().year, selected_month_number, 1)
    schedule = create_schedule(selected_date)
    show_schedule(schedule, reservation_data)

if __name__ == "__main__":
    main()
