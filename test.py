import streamlit as st
import pandas as pd
from datetime import datetime

# 创建一个包含日期和时间段的DataFrame
def create_schedule(start_date, end_date):
    dates = pd.date_range(start=start_date, end=end_date)
    schedule = pd.DataFrame(dates, columns=['Date'])
    schedule['Morning'] = ''
    schedule['Afternoon'] = ''
    return schedule

# 在日历上显示预订情况
def show_schedule(schedule):
    st.write(schedule)

# 提交预订信息
def submit_reservation(date, period, name, phone):
    global schedule
    schedule.loc[schedule['Date'] == date, period] = f"{name} ({phone})"
    st.write("预订成功！")
    st.write(schedule)

def main():
    global schedule
    st.title("餐厅定位系统")

    # 获取当前日期
    today = datetime.today()
    current_month = today.month
    current_year = today.year

    # 创建一个月份的日历
    start_date = st.date_input("选择月份", datetime(current_year, current_month, 1))
    end_date = pd.to_datetime(start_date) + pd.DateOffset(days=30)
    schedule = create_schedule(start_date, end_date)

    # 显示日历上的预订情况
    show_schedule(schedule)

    # 用户选择预订日期和时间段
    date = st.date_input("选择日期")
    period = st.selectbox("选择时间段", ['Morning', 'Afternoon'])

    # 用户输入预订信息
    name = st.text_input("预订人姓名")
    phone = st.text_input("联系电话")

    # 提交预订信息
    if st.button("提交预订"):
        submit_reservation(date, period, name, phone)

if __name__ == "__main__":
    main()
