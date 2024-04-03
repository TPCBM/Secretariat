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
    # 在日历上显示预订情况
    st.write("日\t一\t二\t三\t四\t五\t六")
    cols = st.columns(7)

    first_day_of_month = schedule.index[0]
    first_day_of_month_weekday = first_day_of_month.weekday()

    for i in range(first_day_of_month_weekday):
        with cols[i]:
            st.write(" ")

    date_iter = schedule.index[0]
    while date_iter <= schedule.index[-1]:
        col_idx = date_iter.weekday()
        with cols[col_idx]:
            if date_iter.month != schedule.index[0].month:
                st.write(" ")
            else:
                # 检查日期是否在预订数据中
                reservations_on_date = reservation_data[reservation_data['Date'] == date_iter]
                if not reservations_on_date.empty:
                    # 如果有预订信息，显示预订信息
                    for index, row in reservations_on_date.iterrows():
                        st.write(f"{date_iter.day} 日：{row['Name']} ({row['Phone']}) - {row['Period']}")
                else:
                    # 如果没有预订信息，显示空闲状态
                    st.write(f"{date_iter.day} 日：空閒")
        date_iter += timedelta(days=1)

def main(reservation_data):
    selected_month = st.selectbox("訂位月份", [f"{i} 月" for i in range(1, 13)])
    selected_month_number = int(selected_month.split()[0])
    selected_date = datetime(datetime.now().year, selected_month_number, 1)
    schedule = create_schedule(selected_date)
    show_schedule(schedule, reservation_data)

if __name__ == "__main__":
    main()
