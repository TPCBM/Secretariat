# reservation_form.py

import streamlit as st
import pandas as pd
from datetime import datetime

# 用于保存预订信息的全局变量
reservation_data = pd.DataFrame(columns=['Date', 'Period', 'Name', 'Phone'])

def reservation_form():
    st.title("预订表单")

    date = st.date_input("选择日期")
    period = st.selectbox("选择时间段", ['Morning', 'Afternoon'])
    name = st.text_input("预订人姓名")
    phone = st.text_input("联系电话")

    if st.button("提交预订"):
        if name == '' or phone == '':
            st.error("姓名和电话为必填项！")
        else:
            # 将预订信息添加到全局变量中
            global reservation_data
            ＃reservation_data = reservation_data.append({'Date': date, 'Period': period, 'Name': name, 'Phone': phone}, ignore_index=True)
            # 创建一个新的 DataFrame 包含新的预订数据，并与之前的数据合并
            new_reservation = pd.DataFrame({'Date': [date], 'Period': [period], 'Name': [name], 'Phone': [phone]})
            reservation_data = pd.concat([reservation_data, new_reservation], ignore_index=True)

            st.success("预订成功！")

if __name__ == "__main__":
    reservation_form()
