import streamlit as st
import pandas as pd
from datetime import datetime
import calendar

def create_schedule(selected_date):
    # 获取选择的年份和月份
    year = selected_date.year
    month = selected_date.month

    # 获取当月第一天的星期和当月总天数
    first_day_of_month, num_days = calendar.monthrange(year, month)

    # 创建一个包含日期和时间段的DataFrame
    dates = pd.date_range(start=selected_date.replace(day=1), periods=num_days)
    schedule = pd.DataFrame(index=dates, columns=['Morning', 'Afternoon'])
    return schedule

def show_schedule(schedule, reservation_data):
    st.write("### 預定情況")

    # 获取选择的年份和月份
    selected_date = schedule.index[0]
    year = selected_date.year
    month = selected_date.month

    # 获取当月第一天的星期和当月总天数
    first_day_of_month, num_days = calendar.monthrange(year, month)

    # 创建一个空的日历矩阵
    cal_matrix = [[""] * 7 for _ in range(6)]

    # 填充日期
    day_counter = 1
    for i in range(6):
        for j in range(7):
            if i == 0 and j < first_day_of_month:
                continue
            if day_counter > num_days:
                break
            cal_matrix[i][j] = day_counter
            day_counter += 1

    # 显示日历
    st.write("日\t一\t二\t三\t四\t五\t六")
    cols = st.columns(7)
    for week in cal_matrix:
        for i, day in enumerate(week):
            with cols[i]:
                if day != "":
                    date = datetime(year, month, day)
                    st.write(f"{day}")
                    reservations_on_date = reservation_data[reservation_data['Date'] == date]
                    if not reservations_on_date.empty:
                        for _, row in reservations_on_date.iterrows():
                            st.write(f"{row['Period']}: 已預訂")
                    else:
                        st.write("空閒")

def main(reservation_data):
    selected_month = st.selectbox("訂位月份", [f"{i} 月" for i in range(1, 13)])
    selected_month_number = int(selected_month.split()[0])
    selected_date = datetime(datetime.now().year, selected_month_number, 1)
    schedule = create_schedule(selected_date)
    show_schedule(schedule, reservation_data)

if __name__ == "__main__":
    main()
