import streamlit as st
import pandas as pd
from datetime import datetime

def reservation_form(reservation_data):
    st.title("請填寫預定表單")

    date = st.date_input("訂位日期")
    period = st.selectbox("訂位時段", ['中午(11:00-14:00)', '晚上(17:00-20:00)'])
    name = st.text_input("訂位人姓名")
    phone = st.text_input("訂位人電話")

    if st.button("提交预订"):
        if name == '' or phone == '':
            st.error("姓名和電話為必填！")
        else:
            # 将预订信息添加到全局变量中
            new_reservation = pd.DataFrame({'Date': [date], 'Period': [period], 'Name': [name], 'Phone': [phone]})
            reservation_data = pd.concat([reservation_data, new_reservation], ignore_index=True)

            st.success("預定成功！")

            return reservation_data  # 返回更新后的 reservation_data

    # 如果没有提交预订，返回原始的 reservation_data
    return reservation_data
