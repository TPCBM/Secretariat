import streamlit as st
import pandas as pd
from calendar_display import main as display_calendar
from reservation_form import reservation_form

def main():
    st.title("勵進餐廳預定")

    # 使用st.session_state来存储和共享变量
    if 'reservation_data' not in st.session_state:
        st.session_state.reservation_data = pd.DataFrame(columns=['Date', 'Period', 'Name', 'Phone'])

    option = st.sidebar.selectbox(
        '頁面選單',
        ['空位查詢日曆', '填寫預定表單']
    )

    if option == '空位查詢日曆':
        # 将预订信息传递给日历显示页面
        display_calendar(st.session_state.reservation_data)
    elif option == '填寫預定表單':
        # 调用 reservation_form 函数并将 reservation_data 作为参数传递给它
        st.session_state.reservation_data = reservation_form(st.session_state.reservation_data)

if __name__ == "__main__":
    main()
