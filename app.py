# app.py

import streamlit as st
from calendar_display import main as display_calendar
from reservation_form import reservation_form, reservation_data

def main():
    st.title("餐厅预订系统")

    option = st.sidebar.selectbox(
        '选择页面',
        ['显示日历', '填写预订表单']
    )

    if option == '显示日历':
        # 将预订信息传递给日历显示页面
        display_calendar(reservation_data)
    elif option == '填写预订表单':
        reservation_form()

if __name__ == "__main__":
    main()
