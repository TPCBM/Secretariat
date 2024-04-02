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
    st.write("日\t一\t二\t三\t四\t五\t六")
    cols = st.columns(7)  # 创建7列的布局，代表一周的7天

    # 获取月份的第一天是星期几
    first_day_of_month = schedule.index[0]
    first_day_of_month_weekday = first_day_of_month.weekday()

    # 输出月份第一行之前的空白
    for i in range(first_day_of_month_weekday):
        with cols[i]:
            st.write(" ")

    # 输出日期和预订情况
    date_iter = schedule.index[0]
    while date_iter <= schedule.index[-1]:
        # 找到星期几对应的列
        col_idx = date_iter.weekday()
        with cols[col_idx]:
            # 如果不是当前月的日期，显示空白
            if date_iter.month != schedule.index[0].month:
                st.write(" ")
            else:
                # 显示日期和预订情况
                if pd.notna(schedule.loc[date_iter, 'Morning']) or pd.notna(schedule.loc[date_iter, 'Afternoon']):
                    st.write(f"{date_iter.day} 日：{schedule.loc[date_iter, 'Morning']} {schedule.loc[date_iter, 'Afternoon']}")
                else:
                    st.write(f"{date_iter.day} 日：")
            # 更新日期迭代器
            date_iter += timedelta(days=1)

# 提交预订信息
def submit_reservation(date, period, name, phone, schedule):
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
    # min_date = datetime.combine(schedule.index.min(), datetime.min.time()).date()
    # max_date = datetime.combine(schedule.index.max(), datetime.max.time()).date()
    # date = st.date_input("选择日期", min_value=min_date, max_value=max_date)
    date = st.date_input('选择日期', datetime.today()）
    period = st.selectbox("选择时间段", ['Morning', 'Afternoon'])

    
    # 用户填写预订信息
    name = st.text_input("预订人姓名")
    phone = st.text_input("联系电话")

    # 提交预订信息
    if st.button("提交预订"):
        if name == '' or phone == '':
            st.error("姓名和电话为必填项！")
        else:
            submit_reservation(date, period, name, phone, schedule)

if __name__ == "__main__":
    main()
