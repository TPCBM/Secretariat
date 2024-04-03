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

    # 填充预订信息
    for index, row in reservation_data.iterrows():
        date = row['Date']
        period = row['Period']
        name = row['Name']
        phone = row['Phone']
        if period == '中午(11:00-14:00)':
            calendar_df.loc[calendar_df.index == date, '中午(11:00-14:00)'] = f"{name} ({phone})"
        elif period == '晚上(17:00-20:00)':
            calendar_df.loc[calendar_df.index == date, '晚上(17:00-20:00)'] = f"{name} ({phone})"

    # 检查是否有日期和时间段已经被预订
    for index, row in calendar_df.iterrows():
        if row['中午(11:00-14:00)'] is not pd.NA:
            calendar_df.loc[index, '中午(11:00-14:00)'] = "已預訂"
        if row['晚上(17:00-20:00)'] is not pd.NA:
            calendar_df.loc[index, '晚上(17:00-20:00)'] = "已預訂"

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
