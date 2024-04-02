import streamlit as st
from datetime import datetime

# 创建一个月份的日历
def create_calendar(month, year):
    import calendar
    cal = calendar.Calendar()
    days = cal.itermonthdays(year, month)
    return [day for day in days]

# 在日历上显示时间段的预订情况
def show_reservation(day):
    st.subheader(f"预订情况 - {day}")
    am_reserved = st.checkbox("上午已预订")
    pm_reserved = st.checkbox("下午已预订")
    return am_reserved, pm_reserved

# 提交预订信息
def submit_reservation(day, am_reserved, pm_reserved, name, phone):
    st.write(f"已成功提交预订：")
    st.write(f"日期：{day}")
    if am_reserved:
        st.write("上午已预订")
    if pm_reserved:
        st.write("下午已预订")
    st.write(f"预订人：{name}")
    st.write(f"联系电话：{phone}")

def main():
    st.title("餐厅定位系统")

    # 获取当前日期
    today = datetime.today()
    current_month = today.month
    current_year = today.year

    # 选择月份
    month = st.selectbox("选择月份", range(1, 13), index=current_month - 1)

    # 获取所选月份的日历
    calendar_days = create_calendar(month, current_year)

    for day in calendar_days:
        if day != 0:
            st.subheader(f"{current_year}-{month}-{day}")
            am_reserved, pm_reserved = show_reservation(f"{current_year}-{month}-{day}")
            if not (am_reserved or pm_reserved):
                name = st.text_input("预订人姓名")
                phone = st.text_input("联系电话")
                if st.button("提交预订"):
                    submit_reservation(f"{current_year}-{month}-{day}", am_reserved, pm_reserved, name, phone)

if __name__ == "__main__":
    main()
