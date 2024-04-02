# reservation_form.py

import streamlit as st

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
            st.success("预订成功！")

if __name__ == "__main__":
    reservation_form()
