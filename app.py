# app.py

import streamlit as st
import pandas as pd
from calendar_display import main as display_calendar
from reservation_form import reservation_form, reservation_data

def main():
    st.title("勵進餐廳預定")

    option = st.sidebar.selectbox(
        '頁面選單',
        ['空位查詢日曆', '填寫預定表單']
    )

    if option == '空位查詢日曆':
        # 将预订信息传递给日历显示页面
        display_calendar(reservation_data)
    elif option == '填寫預定表單':
        reservation_form()

if __name__ == "__main__":
    main()
