import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 创建一个包含日期和时间段的DataFrame
def create_schedule(start_date, end_date):
    dates = pd.date_range(start=start_date, end=end_date)
    schedule = pd.DataFrame(index=dates, columns=['Morning', 'Afternoon'])
    return schedule

# 在日历上显示预订情况
def show_schedule(schedule, selected_month):
    # 将 selected_month 转换为 pandas Timestamp 对象
    selected_month = pd.Timestamp(selected_month)

    # 过滤出所选月份的数据
    schedule_filtered = schedule[(schedule.index >= selected_month) & (schedule.index < (selected_month + pd.DateOffset(months=1)))]

    cols = st.columns(7)  # 创建7列的布局，代表一周的7天
    for date, row in schedule_filtered.iterrows():
        weekday = date.strftime('%a')
        col_idx = date.weekday()  # 获取当前日期的星期几对应的列索引
        with cols[col_idx]:
            st.write(f"**{date.strftime('%Y-%m-%d')} ({weekday})**")
            st.write(row['Morning'])
            st.write(row['Afternoon'])

# 提交预订信息
def submit_reservation(date, period, name, phone):
    global schedule
    schedule.loc[date, period] = f"{name} ({phone})"
    st.write("预订成功！")
    st.write(schedule)

def main():
    global schedule
    st.title("餐厅定位系统")

    # 获取当前日期
    today = datetime.today()
    current_month = today.replace(day=1)  # 获取当前月份的第一天
    current_year = today.year

    # 创建一个月份的日历
    selected_month = st.date_input("选择月份", current_month)
    start_date = selected_month
    end_date = selected_month + timedelta(days=30)
    schedule = create_schedule(start_date, end_date)

    # 显示日历上的预订情况
    show_schedule(schedule, selected_month)

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
