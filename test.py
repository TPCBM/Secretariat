import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 创建一个包含日期和时间段的DataFrame
def create_schedule(selected_month):
    # 获取所选月份的第一天和最后一天
    start_date = selected_month.replace(day=1)
    end_date = start_date + pd.offsets.MonthEnd(0)
    # 创建日期范围
    dates = pd.date_range(start=start_date, end=end_date)
    schedule = pd.DataFrame(index=dates, columns=['Morning', 'Afternoon'])
    return schedule

# 在日历上显示预订情况
def show_schedule(schedule):
    st.write(schedule)

# 提交预订信息
def submit_reservation(date, period, name, phone):
    global schedule
    schedule.loc[date, period] = f"{name} ({phone})"
    st.write("预订成功！")
    st.write(schedule)

def main():
    global schedule
    st.title("餐厅定位系统")

    # 月份选择
    selected_month = st.selectbox("月份选择", [f"{i} 月" for i in range(1, 13)])

    # 创建选定月份的日历
    selected_month_number = int(selected_month.split()[0])
    selected_date = datetime(datetime.now().year, selected_month_number, 1)
    schedule = create_schedule(selected_date)

    # 显示日历上的预订情况
    show_schedule(schedule)

    # 用户选择预订日期和时间段
    date = st.date_input("选择日期", min_value=schedule.index.min(), max_value=schedule.index.max())
    period = st.selectbox("选择时间段", ['Morning', 'Afternoon'])

    # 用户输入预订信息
    name = st.text_input("预订人姓名")
    phone = st.text_input("联系电话")

    # 提交预订信息
    if st.button("提交预订"):
        submit_reservation(date, period, name, phone)

if __name__ == "__main__":
    main()
