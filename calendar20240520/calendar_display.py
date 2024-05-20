import streamlit as st
import pandas as pd
from datetime import datetime
import calendar

def create_schedule(year, month):
    # 获取当月第一天的星期和当月总天数
    first_day_of_month, num_days = calendar.monthrange(year, month)

    # 创建一个包含日期和时间段的DataFrame
    dates = pd.date_range(start=datetime(year, month, 1), periods=num_days)
    schedule = pd.DataFrame(index=dates, columns=['Morning', 'Afternoon'])
    return schedule

def show_schedule(year, month, reservation_data):
    st.write(f"### {year} 年 {month} 月預定情況")

    # 获取当月日历矩阵
    cal = calendar.monthcalendar(year, month)

    # 创建一个 DataFrame 来存储日历信息
    cal_df = pd.DataFrame(cal, columns=["一", "二", "三", "四", "五", "六", "日"])

    # 创建显示用的 DataFrame
    display_df = cal_df.applymap(lambda day: "" if day == 0 else "空閒")

    # 填充预订信息
    for index, row in reservation_data.iterrows():
        date = row['Date']
        if date.year == year and date.month == month:
            day = date.day

            for week in range(len(cal)):
                for weekday in range(7):
                    if cal[week][weekday] == day:
                        display_df.iat[week, weekday] = "已預訂"

    # 显示日历表格
    st.dataframe(display_df)

def main(reservation_data):
    selected_year = st.selectbox("選擇年份", [datetime.now().year + i for i in range(-1, 5)])
    selected_month = st.selectbox("訂位月份", [f"{i} 月" for i in range(1, 13)])
    selected_month_number = int(selected_month.split()[0])
    show_schedule(selected_year, selected_month_number, reservation_data)

if __name__ == "__main__":
    main()
