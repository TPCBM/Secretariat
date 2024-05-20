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

    # 调整矩阵顺序，确保以星期一为一周的第一天
    cal_adjusted = [[week[1], week[2], week[3], week[4], week[5], week[6], week[0]] for week in cal]

    # 创建一个 DataFrame 来存储日历信息
    cal_df = pd.DataFrame(cal_adjusted, columns=["一", "二", "三", "四", "五", "六", "日"])

    # 创建显示用的 DataFrame
    display_df = cal_df.applymap(lambda day: f"{day}" if day != 0 else "")

    # 填充预订信息
    for index, row in reservation_data.iterrows():
        date = row['Date']
        if date.year == year and date.month == month:
            period = row['Period']
            name = row['Name']
            phone = row['Phone']
            display_text = f"{name} ({phone})"
            day = date.day

            for week in range(len(cal)):
                for weekday in range(7):
                    if cal_adjusted[week][weekday] == day:
                        if period == '中午(11:00-14:00)':
                            display_df.iat[week, weekday] += f"\n{display_text} - 午"
                        elif period == '晚上(17:00-20:00)':
                            display_df.iat[week, weekday] += f"\n{display_text} - 晚"

    # 显示日历表格
    st.dataframe(display_df)

def main(reservation_data):
    selected_year = st.selectbox("選擇年份", [datetime.now().year + i for i in range(-1, 5)])
    selected_month = st.selectbox("訂位月份", [f"{i} 月" for i in range(1, 13)])
    selected_month_number = int(selected_month.split()[0])
    show_schedule(selected_year, selected_month_number, reservation_data)

if __name__ == "__main__":
    main()
