# app.py

import streamlit as st
import pandas as pd
from calendar_display import main as display_calendar
from reservation_form import reservation_form

def main():
    st.title("勵進餐廳預定")

    # 创建一个全局变量用于保存预订信息
    reservation_data = pd.DataFrame(columns=['Date', 'Period', 'Name', 'Phone'])

    option = st.sidebar.selectbox(
        '頁面選單',
        ['空位查詢日曆', '填寫預定表單']
    )

    if option == '空位查詢日曆':
        # 将预订信息传递给日历显示页面
        display_calendar(reservation_data)
    elif option == '填寫預定表單':
        # 将 reservation_data 作为参数传递给填写表单页面
        reservation_form(reservation_data)

if __name__ == "__main__":
    main()
